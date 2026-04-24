# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: DevOps & Infra)

### Release Discipline
- Infrastructure changes must be reviewable, reproducible, and auditable.
- Never bypass policy checks for convenience in CI/CD.
- Protect secret handling and artifact integrity at every stage.

### Merge/Release Gates
- Plan/apply (or equivalent) reviewed with no unknown drift.
- Pipeline security checks pass (SAST/dep/vuln scans as configured).
- Disaster recovery and rollback notes updated for impactful changes.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Earthly v0.8+ for containerized, reproducible CI/CD builds
- Earthfile syntax v0.8 with features like FUNCTION, IMPORT, and CACHE
- Earthly Satellites for cloud-based remote runners with persistent cache
- Docker and BuildKit as the underlying container runtime
- Multi-platform builds targeting linux/amd64 and linux/arm64
- Integration with GitHub Actions, GitLab CI, or Jenkins as the outer CI orchestrator
- Earthly Cloud for shared secrets and remote caching

## Project Structure

```
.
├── Earthfile
├── .earthly/
│   └── config.yml
├── services/
│   ├── api/
│   │   ├── Earthfile
│   │   ├── src/
│   │   └── Dockerfile
│   ├── worker/
│   │   ├── Earthfile
│   │   └── src/
│   └── web/
│       ├── Earthfile
│       └── src/
├── libs/
│   ├── common/
│   │   ├── Earthfile
│   │   └── src/
│   └── proto/
│       ├── Earthfile
│       └── protos/
├── deploy/
│   ├── Earthfile
│   ├── k8s/
│   └── terraform/
├── ci/
│   ├── Earthfile
│   ├── functions/
│   │   └── Earthfile
│   └── .github/
│       └── workflows/
│           └── ci.yml
└── .earthlyignore
```

## Architecture Rules

- The root Earthfile defines the top-level targets: all, test, lint, build, deploy
- Each service has its own Earthfile that is imported from the root using IMPORT ./services/api AS api
- Shared build logic must be in ci/functions/Earthfile using FUNCTION declarations
- Use CACHE for package manager caches (node_modules, .gradle, pip cache) to speed up builds
- All targets that produce artifacts must use SAVE ARTIFACT with explicit paths
- Container images must use SAVE IMAGE with tagged names; multi-platform builds use BUILD --platform
- Secrets must use Earthly secrets (--secret) or Earthly Cloud secrets; never pass secrets as build args
- Targets must be ordered: deps, build, test, lint, docker, deploy within each Earthfile

## Coding Conventions

- Target names use lowercase-with-dashes: build-api, test-integration, deploy-staging
- Function names use UPPER_SNAKE_CASE: INSTALL_DEPS, RUN_TESTS, BUILD_IMAGE
- Base images must be pinned to a digest, not just a tag: FROM python:3.12-slim@sha256:abc123...
- Use ARG for all configurable values with defaults; document each ARG with a comment
- COPY uses explicit source and destination paths; never COPY . . without an .earthlyignore
- All RUN commands that install packages must be cached: RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt
- Use IF/ELSE for conditional logic instead of shell conditionals for better readability

## Library Preferences

- Use earthly/lib for common utility functions (e.g., earthly/lib+INSTALL_DIND for Docker-in-Docker)
- Use SAVE IMAGE --push for pushing images directly from Earthly instead of separate docker push steps
- Use WITH DOCKER for integration tests that need running containers
- Use WAIT/END blocks for parallel target execution within a pipeline
- Use PIPELINE and TRIGGER for Earthly CI native pipelines when available

## File Naming

- Build definitions: Earthfile (capital E, no extension) in each directory
- Ignore file: .earthlyignore at repository root and in subdirectories
- Earthly config: .earthly/config.yml for local settings
- CI workflow files: ci.yml in the appropriate CI directory (.github/workflows/, .gitlab-ci/)
- Function libraries: Earthfile in ci/functions/ with FUNCTION declarations

## NEVER DO THIS

1. Never use RUN --privileged unless absolutely required for nested Docker; it disables security isolation
2. Never use LOCALLY targets in CI pipelines; they bypass containerization and break reproducibility
3. Never omit .earthlyignore; without it, COPY . . sends the entire directory including .git to BuildKit
4. Never hardcode image tags without digests in FROM statements; tags are mutable and break reproducibility
5. Never use --allow-privileged in CI without explicit security review; it allows arbitrary host access
6. Never pass secrets via ARG; use --secret flag or Earthly Cloud secrets to prevent leaking in build logs
7. Never skip the --ci flag when running Earthly in CI; it enables stricter mode and disables interactive features

## Testing

- Run earthly +test from the root to execute all test targets across all services
- Integration tests must use WITH DOCKER to spin up dependencies (databases, message queues)
- Validate Earthfile syntax with earthly ls to list all available targets before running
- CI must run earthly --ci +all which includes lint, test, build, and security scanning
- Test multi-platform builds locally with earthly --platform=linux/arm64 +build before pushing
- Cache effectiveness: compare build times with and without Earthly Satellites to quantify speedup
- Run earthly prune periodically in CI to prevent disk exhaustion from stale build cache

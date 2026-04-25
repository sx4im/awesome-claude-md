# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Tech Stack

- **Woodpecker**: CI/CD platform (v2.x)
- **Docker**: Pipeline execution environment
- **YAML**: Pipeline configuration
- **Gitea/GitHub/GitLab**: SCM integration
- **BoltDB/Postgres**: Database for build history
- **Minio/S3**: Log and artifact storage

## Project Structure

```
woodpecker-ci/
├── .woodpecker/                # Pipeline configs
│   ├── test.yml                # Test pipeline
│   ├── build.yml               # Build pipeline
│   └── release.yml             # Release pipeline
├── .woodpecker.yml             # Main pipeline (legacy)
├── Dockerfile                  # Build container
└── scripts/
    └── run-tests.sh
```

## Architecture Rules

- **Pipeline per concern.** Separate test, build, release. Triggered conditionally.
- **Matrix builds.** Test multiple versions. Python 3.9, 3.10, 3.11. Node 18, 20.
- **Service containers.** Define databases, caches as services. Link to main container.
- **Secret management.** Use Woodpecker secrets. Encrypted, injected as env vars.
- **Local execution.** Use `woodpecker-cli exec` for local testing.

## Coding Conventions

- **Pipeline syntax.** `steps: - name: test image: node:20 commands: - npm test`.
- **Conditional steps.** `when: branch: main` or `when: event: pull_request`.
- **Workspace.** Shared volume between steps. Pass artifacts between build and test.
- **Caching.** `cache: - path: node_modules` for dependency caching between builds.
- **Notifications.** `notify` section for Slack, email on build status.

## NEVER DO THIS

1. **Never commit secrets to .woodpecker.yml.** Use Woodpecker secrets UI. Encrypted storage.
2. **Never use :latest images.** Pin to specific versions. Reproducible builds need version pinning.
3. **Never skip when conditions.** Unconditional release steps deploy on every PR. Dangerous.
4. **Never ignore failures.** Steps fail fast. Use `failure: ignore` sparingly for optional checks.
5. **Never hardcode branches.** Use `CI_REPO_DEFAULT_BRANCH` instead of hardcoded `main` or `master`.
6. **Never forget about secrets rotation.** Rotate Woodpecker secrets periodically. Especially cloud keys.
7. **Never use privileged mode.** Breaks container security. Use DinD (Docker-in-Docker) for builds.

## Testing

- **Pipeline validation.** `woodpecker-cli lint` for syntax checking.
- **Local testing.** `woodpecker-cli exec` runs pipeline locally. Verify steps work.
- **Integration testing.** Push to test branch. Verify full pipeline executes correctly.
- **Matrix testing.** Verify all matrix combinations pass. No version-specific failures.
- **Notification testing.** Force failure. Verify notifications sent to correct channels.

## Claude Code Integration

- Use `@.woodpecker/` for pipeline configuration patterns
- Reference pipeline definitions for Docker-based CI/CD
- Apply lightweight CI/CD from architecture rules
- Validate against Woodpecker best practices in NEVER DO THIS

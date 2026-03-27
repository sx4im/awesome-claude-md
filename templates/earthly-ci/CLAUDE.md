# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

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

- Skaffold v2.10+ for continuous development and deployment to Kubernetes
- Docker or Buildpacks for container image building
- kubectl or Helm for Kubernetes manifest deployment
- kustomize for environment-specific configuration overlays
- kind or minikube for local Kubernetes cluster
- Google Cloud Build or kaniko for remote image building in CI
- Cloud Code IDE plugin for VS Code or JetBrains integration

## Project Structure

```
.
├── skaffold.yaml
├── services/
│   ├── api-gateway/
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── k8s/
│   │       ├── deployment.yaml
│   │       └── service.yaml
│   ├── user-service/
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── k8s/
│   │       ├── deployment.yaml
│   │       └── service.yaml
│   └── order-service/
│       ├── Dockerfile
│       ├── src/
│       └── k8s/
│           ├── deployment.yaml
│           └── service.yaml
├── k8s/
│   ├── base/
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   └── kustomization.yaml
│   ├── dev/
│   │   ├── kustomization.yaml
│   │   └── patches/
│   ├── staging/
│   │   └── kustomization.yaml
│   └── production/
│       └── kustomization.yaml
├── infra/
│   ├── postgres/
│   ├── redis/
│   └── skaffold-infra.yaml
└── integration-tests/
    └── skaffold-test.yaml
```

## Architecture Rules

- skaffold.yaml must define separate profiles for dev, staging, and production environments
- Dev profile must use skaffold dev with file sync enabled for hot reloading without image rebuilds
- Each microservice must have its own build artifact entry with a context pointing to its directory
- Use kustomize as the deploy method with profile-specific overlays; raw kubectl only for simple single-service projects
- Infrastructure dependencies (postgres, redis) must be in a separate Skaffold module (skaffold-infra.yaml) loaded via requires
- Port forwarding must be defined in skaffold.yaml under portForward, not via separate kubectl commands
- Image tagging: use sha256 strategy for CI and dateTime for local dev to enable quick identification
- Skaffold modules must use dependency ordering: infra deploys before app services

## Coding Conventions

- Profile names match environment names exactly: dev, staging, production
- Artifact names match the service directory name: api-gateway, user-service, order-service
- Dockerfiles must use multi-stage builds with a dev stage for hot reload (e.g., air for Go, nodemon for Node.js)
- Sync rules must map source file patterns to container paths: src/**/*.go -> /app/
- Custom build scripts go in scripts/build-{service}.sh and are referenced via custom builder
- All kubectl manifests must include resource requests and limits, even in dev profiles
- Health check probes must be defined in all deployments; readiness probe is mandatory

## Library Preferences

- Use ko for Go services instead of Docker for faster, distroless image builds
- Use Jib for Java/Kotlin services (via jib-maven-plugin or jib-gradle-plugin)
- Use Buildpacks for polyglot services that do not need custom Dockerfiles
- Use kustomize over Helm for manifest management unless the project already uses Helm charts
- Use Cloud Code plugin for IDE-integrated debugging with breakpoints in running containers
- Use skaffold verify for post-deployment verification tests

## File Naming

- Main config: skaffold.yaml at repository root
- Module configs: skaffold-{purpose}.yaml (skaffold-infra.yaml, skaffold-test.yaml)
- Dockerfiles: Dockerfile in each service directory; Dockerfile.dev for dev-specific builds
- Kubernetes manifests: lowercase-kebab-case matching resource type in k8s/ subdirectories
- Kustomize overlays: k8s/{environment}/kustomization.yaml
- Build scripts: scripts/build-{service}.sh for custom builders

## NEVER DO THIS

1. Never use latest as an image tag in skaffold.yaml; Skaffold manages tags automatically via its tagging strategy
2. Never run skaffold dev without --cleanup to prevent orphaned resources in the cluster
3. Never put secrets directly in Kubernetes manifests or skaffold.yaml; use secretGenerator in kustomize or External Secrets
4. Never use hostPath volumes in dev deployments; use skaffold file sync for source code synchronization instead
5. Never skip defining resource limits in dev; local clusters will OOM without them
6. Never hard-code the container registry in skaffold.yaml; use the defaultRepo configuration via skaffold config set default-repo

## Testing

- Run skaffold build --dry-run to validate all artifact configurations without actually building images
- Run skaffold render to preview the fully rendered Kubernetes manifests for each profile
- Use skaffold verify to run integration test containers after deployment completes
- Test file sync by modifying a source file during skaffold dev and verifying the container picks up the change within 2 seconds
- Validate all profiles with skaffold diagnose to catch configuration errors
- CI must run skaffold build followed by skaffold deploy --profile=staging with post-deploy verification
- Test skaffold debug to ensure debugger attachment works for each service language runtime
- Run skaffold delete after integration tests to clean up all deployed resources

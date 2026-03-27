# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Tilt v0.33+ for local Kubernetes development with live updates
- Tiltfile (Starlark) for declarative development environment configuration
- kind or k3d as the local Kubernetes cluster
- Docker for container image building with Tilt's optimized rebuild
- ctlptl for declarative local cluster management with built-in registry
- Helm or kustomize for Kubernetes manifest rendering
- Tilt Cloud for team-wide development environment visibility

## Project Structure

```
.
├── Tiltfile
├── tilt_modules/
│   ├── restart_process/
│   ├── helm_remote/
│   └── secret/
├── dev/
│   ├── ctlptl-cluster.yaml
│   ├── Dockerfile.dev
│   └── tilt-settings.yaml
├── services/
│   ├── frontend/
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── k8s/
│   │       └── deployment.yaml
│   ├── backend/
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── k8s/
│   │       └── deployment.yaml
│   └── worker/
│       ├── Dockerfile
│       ├── src/
│       └── k8s/
│           └── deployment.yaml
├── infra/
│   ├── postgres/
│   │   └── k8s/
│   ├── redis/
│   │   └── k8s/
│   └── kafka/
│       └── k8s/
├── charts/
│   └── my-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
└── scripts/
    ├── seed-db.sh
    └── setup-cluster.sh
```

## Architecture Rules

- The Tiltfile must define all services with explicit resource dependencies using k8s_resource with resource_deps
- Use live_update for all application services to avoid full image rebuilds on code changes
- Infrastructure services (postgres, redis, kafka) must be deployed first using resource_deps ordering
- Local development must use a registry managed by ctlptl; configure it in dev/ctlptl-cluster.yaml
- Use docker_build with live_update containing sync and run steps; only fall back to full rebuild for dependency changes
- Custom buttons in Tilt UI must be defined for common dev tasks: seed database, reset state, run migrations
- Tilt must auto-detect and display port forwards for all services with links in the UI
- Use config.define_string_list for optional service selection to allow developers to run a subset of services

## Coding Conventions

- Tiltfile functions use snake_case following Starlark conventions
- Resource names match the Kubernetes deployment name exactly for automatic association
- Use load() for importing Tilt extensions from tilt_modules/ or from the tilt-extensions repository
- Group related resources using labels: config.set_enabled_resources with label selectors
- Define all configurable values in dev/tilt-settings.yaml and read with read_yaml in the Tiltfile
- live_update steps must be ordered: sync first, then run commands, then restart_container if needed
- Port forwards must specify both local and container ports explicitly: port_forwards=['3000:3000', '9229:9229']

## Library Preferences

- Use ctlptl for local cluster lifecycle: ctlptl create cluster kind --registry=ctlptl-registry
- Use the tilt-extensions restart_process extension for compiled languages (Go, Rust, Java)
- Use helm_remote from tilt-extensions for third-party Helm charts (Bitnami PostgreSQL, Redis)
- Use the secret extension for injecting development secrets from local files
- Use custom_build for services that need non-Docker build tools (ko, Jib, Buildpacks)
- Use local_resource for non-Kubernetes tasks: codegen, proto compilation, dependency installation

## File Naming

- Main config: Tiltfile (capital T, no extension) at repository root
- Cluster config: dev/ctlptl-cluster.yaml for local cluster definition
- Developer settings: dev/tilt-settings.yaml for per-developer overrides (gitignored)
- Dev Dockerfiles: dev/Dockerfile.dev or Dockerfile.tilt for development-optimized images
- Extension modules: tilt_modules/{extension_name}/ following Tilt extension conventions
- Helper scripts: scripts/{action}.sh for setup and maintenance tasks

## NEVER DO THIS

1. Never use docker_build without live_update for application services; every code change will trigger a full rebuild taking 30+ seconds
2. Never use allow_k8s_contexts('*') in the Tiltfile; explicitly list allowed contexts to prevent accidental deployment to production clusters
3. Never put database credentials in the Tiltfile; use the secret extension to load them from local files outside version control
4. Never run Tilt against a shared development cluster without namespace isolation; use namespace-per-developer with the NAMESPACE environment variable
5. Never skip resource_deps for infrastructure; services will crash-loop waiting for databases that haven't started
6. Never use restart_container() in live_update for interpreted languages (Python, Node.js, Ruby); only sync files and let the runtime hot-reload

## Testing

- Run tilt ci to execute a headless build-and-test cycle that exits with a status code for CI integration
- Verify live_update works by changing a source file and confirming the update appears in the Tilt UI within 3 seconds
- Test resource_deps ordering by running tilt up with --stream and verifying infrastructure starts before application services
- Validate the Tiltfile syntax with tilt alpha lint before committing changes
- Run tilt down to verify all resources are cleaned up completely; check for orphaned PVCs and ConfigMaps
- Use tilt dump to export the full resource dependency graph and verify it matches the expected architecture
- Test developer onboarding by running the full setup from scratch: ctlptl apply, tilt up, verify all resources healthy
- Ensure tilt-settings.yaml defaults work without any local overrides for new team members

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Dagger v0.14+ for programmable CI/CD pipelines
- Dagger Go SDK as the primary pipeline language
- BuildKit as the execution engine with automatic caching
- Dagger Cloud for pipeline visualization and distributed caching
- Container-native pipeline execution with full Docker compatibility
- Integration with GitHub Actions, GitLab CI, or CircleCI as the outer runner
- Dagger modules for reusable pipeline components

## Project Structure

```
.
├── dagger/
│   ├── main.go
│   ├── go.mod
│   ├── go.sum
│   ├── build.go
│   ├── test.go
│   ├── deploy.go
│   └── dagger.json
├── modules/
│   ├── golang/
│   │   ├── main.go
│   │   └── dagger.json
│   ├── docker/
│   │   ├── main.go
│   │   └── dagger.json
│   └── k8s/
│       ├── main.go
│       └── dagger.json
├── src/
│   ├── cmd/
│   ├── internal/
│   └── pkg/
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
└── dagger.json
```

## Architecture Rules

- All CI/CD logic must be defined in Go code within the dagger/ directory; no shell scripts for build logic
- Pipelines must be structured as Dagger Functions that return a typed result (Container, Directory, File)
- Use Dagger modules for reusable components; each module has its own dagger.json and Go module
- Every pipeline function must accept a context.Context as the first parameter for cancellation
- Container operations must chain method calls to maximize BuildKit layer caching
- Secrets must be passed through dagger.Secret type using dag.SetSecret(); never as plain string arguments
- Pipeline outputs must be explicitly exported with Export() or published with Publish()
- Service dependencies (databases, caches) use Container.AsService() with health check bindings

## Coding Conventions

- Pipeline functions are exported methods on the main Dagger module struct
- Function names use PascalCase and describe the action: Build, Test, Lint, DeployToStaging
- Helper functions that are not pipeline entry points must be unexported (lowercase)
- Chain Container method calls in a single expression for readability and optimal caching
- Use dag.Container().From() for base images, not raw string references
- All file paths use dag.Host().Directory() with explicit include/exclude patterns
- Pipeline configuration values are function parameters with sensible defaults, not environment variables

## Library Preferences

- Use the official Dagger Go SDK (dagger.io/dagger) as the primary pipeline language
- Use dag.Container().From("golang:1.22-alpine") for Go builds with WithMountedCache for GOMODCACHE
- Use Dagger modules from the Daggerverse for common tasks: docker, helm, kubectl, terraform
- Prefer WithMountedCache over WithDirectory for dependency caches to enable layer reuse
- Use WithServiceBinding for database and service dependencies in integration tests
- Use Container.WithExec for running commands; never shell out to docker CLI from pipeline code

## File Naming

- Pipeline entry point: dagger/main.go containing the primary module struct and top-level functions
- Feature-specific pipelines: dagger/{concern}.go (build.go, test.go, deploy.go)
- Reusable modules: modules/{name}/main.go with dagger.json configuration
- Module metadata: dagger.json in each module root and the top-level project root
- CI integration: ci.yml or dagger.yml in the CI-specific workflow directory
- No Makefile wrappers; use dagger call directly in CI workflows

## NEVER DO THIS

1. Never use dag.Host().Directory(".") without include/exclude filters; it sends everything to BuildKit and breaks caching
2. Never store secrets in pipeline code or dagger.json; use dagger.Secret and environment-based secret injection
3. Never use Container.WithExec([]string{"sh", "-c", "..."}) for complex shell scripts; break them into multiple WithExec calls or use Go logic
4. Never ignore the error return from Export() or Publish(); failed exports must fail the pipeline
5. Never create unbounded parallel operations without concurrency limits; use errgroup with SetLimit()
6. Never skip the --focus=false flag in CI; it prevents Dagger from spinning up the TUI which hangs in headless mode

## Testing

- Run dagger call test to execute the full test pipeline locally before pushing
- Pipeline functions must be testable in isolation: pass mock containers and directories as inputs
- Integration tests use WithServiceBinding to start real databases in containers alongside the test container
- Validate module compatibility with dagger mod sync after dependency updates
- CI must run dagger call lint test build in sequence; deploy only on main branch after all checks pass
- Test caching efficiency by running the pipeline twice; second run should complete in under 10 seconds for cached targets
- Use Dagger Cloud traces to identify slow pipeline stages and optimize caching boundaries
- Run dagger call --help to verify all pipeline functions have proper documentation

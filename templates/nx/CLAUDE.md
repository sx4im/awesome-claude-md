# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Nx v18+ (smart monorepo build system)
- TypeScript/JavaScript
- React/Angular/Vue/Node support
- Distributed task execution
- Computation caching

## Project Structure

```
apps/
├── web-e2e/                    # E2E tests
├── web/                        # Web app
└── api/                        # API
libs/
├── shared-ui/                  # Shared library
└── utils/                      # Utilities
tools/
└── generators/                 # Custom generators
nx.json                         # Nx configuration
project.json                    # Per-project config
package.json
```

## Architecture Rules

- **Generators for consistency.** Use Nx generators to create apps and libraries.
- **Implicit dependencies.** Nx automatically detects project dependencies from imports.
- **Affected commands.** Run tasks only on changed projects: `nx affected:build`.
- **Computation caching.** Cache build outputs to avoid redundant work.

## Coding Conventions

- Generate app: `nx generate @nx/react:app web`.
- Generate lib: `nx generate @nx/react:lib shared-ui`.
- Run tasks: `nx build web`, `nx test shared-ui`.
- Affected: `nx affected:test --base=main`.
- Graph: `nx graph` to visualize dependencies.

## NEVER DO THIS

1. **Never manually create projects.** Always use Nx generators to maintain structure.
2. **Never ignore `project.json`/`package.json` project configuration.** Nx reads these.
3. **Never use Nx without understanding the project graph.** Run `nx graph` to visualize.
4. **Never skip the caching configuration.** Proper `outputs` and `inputs` for cache keys.
5. **Never forget about distributed CI.** `nx-cloud` or self-hosted agents for parallel execution.
6. **Never mix Nx and non-Nx tools carelessly.** Nx is opinionated. Follow its patterns.
7. **Never manually update imports across projects.** Use Nx's move/refactor generators.

## Testing

- Use `nx test` for unit tests.
- Use `nx e2e` for E2E tests.
- Verify affected detection works correctly.


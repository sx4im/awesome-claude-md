# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Turborepo v2 (monorepo build system)
- pnpm/npm/yarn workspaces
- Remote caching
- Pipeline configuration

## Project Structure

```
apps/
├── web/                        # Next.js app
├── docs/                       # Documentation site
└── api/                        # API server
packages/
├── ui/                         # Shared UI components
├── config/                     # Shared config (eslint, tsconfig)
└── utils/                      # Shared utilities
turbo.json                      # Turborepo configuration
pnpm-workspace.yaml             # pnpm workspace config
package.json                    # Root package.json
```

## Architecture Rules

- **Task pipeline.** Define task dependencies in `turbo.json`.
- **Remote caching.** Share build cache across team and CI.
- **Workspace-aware.** Leverages npm/pnpm/yarn workspaces.
- **Parallel execution.** Runs independent tasks in parallel.

## Coding Conventions

- turbo.json: `{"pipeline": {"build": {"dependsOn": ["^build"]}, "dev": {"cache": false}}}`.
- Run tasks: `turbo run build`, `turbo run dev`.
- Filter: `turbo run build --filter=web` for specific apps.
- Pipeline deps: `^build` means "build dependencies first".
- Cache config: `outputs: ['dist/**', '.next/**']` for build artifacts.

## NEVER DO THIS

1. **Never run tasks without `turbo`.** It skips the cache and pipeline optimization.
2. **Never forget `dependsOn` for dependent tasks.** Without it, tasks run out of order.
3. **Never ignore the cache configuration.** Proper `outputs` ensures correct caching.
4. **Never commit the local cache.** `.turbo/` should be gitignored.
5. **Never use Turborepo without workspaces.** It requires npm/pnpm/yarn workspaces.
6. **Never forget to configure remote caching.** `turbo login` + `turbo link` for team sharing.
7. **Never manually manage workspace dependencies.** Use `workspace:*` protocol in package.json.

## Testing

- Test pipeline with `turbo run test`.
- Verify remote cache hits in CI.
- Test task dependencies run in correct order.


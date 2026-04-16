# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- pnpm workspaces (monorepo package management)
- pnpm v8+
- Efficient node_modules
- Workspace protocol

## Project Structure

```
packages/
├── ui/                         # UI library
│   ├── package.json
│   └── src/
├── utils/                      # Utilities
│   ├── package.json
│   └── src/
└── core/                       # Core library
    ├── package.json
    └── src/
apps/
├── web/                        # Web app
└── api/                        # API
pnpm-workspace.yaml             # Workspace config
package.json                    # Root
```

## Architecture Rules

- **pnpm-workspace.yaml defines packages.** List glob patterns for workspace packages.
- **Workspace protocol for internal deps.** `"@scope/ui": "workspace:*"` links to local package.
- **Hoisting control.** pnpm's strictness prevents phantom dependencies.
- **Efficient disk usage.** Content-addressable store shares packages across projects.

## Coding Conventions

- pnpm-workspace.yaml: `packages: ['apps/*', 'packages/*']`.
- Install workspace dep: `pnpm add @scope/ui --filter @scope/web`.
- Run command: `pnpm --filter @scope/ui build`.
- Run in all: `pnpm -r build`.
- Add root dep: `pnpm add -D typescript -w`.

## NEVER DO THIS

1. **Never use npm/yarn in pnpm workspaces.** It breaks the workspace protocol.
2. **Never forget the `workspace:` protocol.** Without it, pnpm might fetch from registry.
3. **Never hoist unnecessarily.** pnpm's default strictness catches missing deps.
4. **Never ignore `.npmrc` for workspace config.** `link-workspace-packages=true`, etc.
5. **Never manually bump internal versions.** Use changesets or similar for versioning.
6. **Never commit `node_modules`.** Always gitignored, but especially with pnpm's structure.
7. **Never mix pnpm and npm lockfiles.** Delete `package-lock.json` when switching to pnpm.

## Testing

- Test with `pnpm -r test` for all packages.
- Verify workspace linking with `pnpm why @scope/ui`.
- Test filtering with `pnpm --filter` commands.


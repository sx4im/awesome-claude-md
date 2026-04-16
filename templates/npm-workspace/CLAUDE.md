# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- npm workspaces
- Node.js 20+
- Native npm monorepo support
- v7+ workspace protocol
- Shared dependencies

## Project Structure
```
packages/
├── ui/
│   └── package.json
├── utils/
│   └── package.json
└── core/
    └── package.json
apps/
├── web/
│   └── package.json
└── api/
    └── package.json
package.json                  // Root with workspaces
```

## Architecture Rules

- **Workspaces defined in root.** `workspaces: ['packages/*', 'apps/*']`.
- **Single node_modules.** At root, linked to packages.
- **Cross-reference with names.** `"@scope/ui": "^1.0.0"`.
- **Shared scripts.** Run from root with `--workspace` or `-w`.

## Coding Conventions

- Root package.json: `{ "workspaces": ["packages/*", "apps/*"] }`.
- Add to workspace: `npm init -w ./packages/new-package`.
- Install in workspace: `npm install lodash -w @scope/ui`.
- Run in workspace: `npm run build -w @scope/ui` or `npm run build --workspaces`.
- Add deps: `npm install @scope/ui --workspace @scope/web`.

## NEVER DO THIS

1. **Never use npm < 7 for workspaces.** Workspaces introduced in v7.
2. **Never install in package node_modules directly.** Use `-w` flag.
3. **Never forget to bump versions.** npm doesn't handle workspace versioning.
4. **Never commit package-lock in each workspace.** Only root lockfile.
5. **Never ignore the `nohoist` option.** For React Native packages.
6. **Never use without `preinstall` script.** Ensure correct npm version.
7. **Never forget to publish in order.** Dependencies must be published first.

## Testing

- Test workspace linking with `npm install`.
- Test scripts run from root.
- Test that changes in one package reflect in dependents.


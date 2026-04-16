# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Bun workspaces
- Bun 1.1+
- Ultra-fast package manager
- workspace: protocol
- Text lockfile

## Project Structure
```
packages/
├── ui/
│   └── package.json
└── utils/
    └── package.json
apps/
└── web/
    └── package.json
package.json                  // Root with workspaces
bun.lockb                     // Bun lockfile
```

## Architecture Rules

- **Workspaces auto-detected.** `workspace` field or workspaces in root.
- **workspace: protocol.** Link to local packages.
- **Text lockfile.** `bun.lockb` is a text file.
- **Fastest installs.** Bun's speed for monorepos.

## Coding Conventions

- Root: `{ "workspaces": ["packages/*", "apps/*"] }`.
- Link: `"@scope/ui": "workspace:*"` in dependent package.json.
- Install: `bun install` at root (fast).
- Run: `bun run --filter @scope/ui build` or `cd packages/ui && bun run build`.
- Add: `bun add lodash` in package directory.

## NEVER DO THIS

1. **Never use Bun workspaces for mixed projects.** Bun-only benefits.
2. **Never forget `workspace:*` protocol.** Links to local version.
3. **Never commit `bun.lockb` as binary.** It's actually text.
4. **Never mix bun and npm/pnpm carelessly.** Pick one package manager.
5. **Never skip `bun run` at root.** Can run scripts across workspaces.
6. **Never ignore Bun's node_modules structure.** Slightly different.
7. **Never use without testing Node.js compatibility.** Bun aims for compat.

## Testing

- Test workspace linking with `bun install`.
- Test `bun run` performance vs npm/yarn.
- Test that packages work when published (workspace: replaced).


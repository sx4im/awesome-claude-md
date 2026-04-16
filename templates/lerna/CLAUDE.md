# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Lerna (monorepo management)
- npm/yarn/pnpm workspaces
- Versioning and publishing
- Change detection
- Command running

## Project Structure
```
packages/
├── ui/
│   └── package.json
└── utils/
    └── package.json
lerna.json                    // Lerna configuration
package.json                  // Root
```

## Architecture Rules

- **Coordinates versions.** Bump all or changed packages.
- **Publishes to npm.** Handles registry publishing.
- **Runs commands.** Execute across packages.
- **Detects changes.** Only publish changed since last release.

## Coding Conventions

- Config: `{ "version": "independent", "npmClient": "pnpm", "packages": ["packages/*"] }`.
- Bootstrap: `lerna bootstrap` or use workspaces.
- Version: `lerna version` (interactive) or `lerna version patch`.
- Publish: `lerna publish from-git` or `lerna publish from-package`.
- Run: `lerna run build --scope @scope/ui` or `lerna run build --since`.
- Changed: `lerna changed` to see what's changed since last release.

## NEVER DO THIS

1. **Never use Lerna without workspaces.** Lerna 7+ requires npm/yarn/pnpm workspaces.
2. **Never forget to configure `version`.** `independent` vs `fixed`.
3. **Never skip `lerna version` before publish.** Version bumping is separate.
4. **Never ignore the `ignoreChanges` config.** For changelog-excluded files.
5. **Never use `lerna bootstrap` with modern workspaces.** `npm install` works.
6. **Never forget to configure `command.publish.directory`.** For dist publishing.
7. **Never skip verifying registry auth.** `npm whoami` before publish.

## Testing

- Test `lerna version` in dry-run mode.
- Test publishing to local registry first.
- Test changed detection is accurate.


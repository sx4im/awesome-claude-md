# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Yarn workspaces
- Yarn 4 (berry) or Yarn 1
- Plug'n'Play (PnP) optional
- Zero-installs support
- Constraints

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
.yarn/                        // Yarn specific
```

## Architecture Rules

- **Workspaces defined in root.** `workspaces: ['packages/*', 'apps/*']`.
- **PnP optional.** Traditional `node_modules` or Plug'n'Play.
- **Zero-installs.** Commit `.yarn/cache` for offline builds.
- **Constraints.** Enforce rules across workspace.

## Coding Conventions

- Root: `{ "workspaces": ["packages/*", "apps/*"], "packageManager": "yarn@4.0.0" }`.
- Install: `yarn install` at root.
- Add to workspace: `yarn workspace @scope/ui add lodash`.
- Run script: `yarn workspace @scope/ui build` or `yarn workspaces foreach run build`.
- Version: `yarn version check --interactive` then `yarn version apply`.

## NEVER DO THIS

1. **Never mix Yarn 1 and Yarn 4 without care.** Different architectures.
2. **Never forget `.yarnrc.yml`.** Required for Yarn 4 config.
3. **Never skip `yarn install` after cloning.** Zero-installs require cache.
4. **Never use `npm` commands in Yarn workspace.** Use `yarn` consistently.
5. **Never ignore constraints.** `constraints.pro` for enforcing rules.
6. **Never commit `.yarn/install-state.gz`.** Gitignore it.
7. **Never forget `yarn plugin` for release.** Version lifecycle management.

## Testing

- Test PnP compatibility with all tools.
- Test zero-install works after clone.
- Test constraints catch violations.


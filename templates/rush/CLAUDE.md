# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Rush (monorepo toolchain by Microsoft)
- PNPM as package manager
- Rig packages
- Build caching
- Change tracking

## Project Structure
```
common/
├── config/
│   └── rush/
│       └── rush.json           // Rush configuration
├── scripts/
└── temp/
libraries/
apps/
├── web/
└── api/
```

## Architecture Rules

- **Rush manages everything.** Commands, builds, publishing.
- **PNPM required.** Rush uses PNPM workspaces.
- **Rig packages.** Share configs across projects.
- **Build cache.** Skip unchanged projects.

## Coding Conventions

- Setup: `rush init` in repo root.
- Add project: Edit `rush.json`, add to `projects` array.
- Install: `rush update` (instead of `pnpm install`).
- Build: `rush rebuild` (clean) or `rush build` (incremental).
- Change: `rush change` (log changes) before PR.
- Publish: `rush publish -p` (apply and publish).
- Bulk commands: `rush my-bulk-command` defined in `command-line.json`.

## NEVER DO THIS

1. **Never use npm/yarn directly.** Always use Rush commands.
2. **Never forget `rush update` after `git pull`.** Syncs dependencies.
3. **Never skip `rush change` for publishable packages.** Required for changelog.
4. **Never ignore the `shouldPublish` flag.** In `rush.json` for private packages.
5. **Never commit `common/temp`.** Gitignored, generated.
6. **Never use without understanding "rig packages".** Share eslint, tsconfig.
7. **Never forget to configure `buildCacheEnabled`.** Speeds up CI.

## Testing

- Test `rush update` works correctly.
- Test incremental builds skip unchanged.
- Test publishing workflow with local registry.


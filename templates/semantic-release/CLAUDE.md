# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- semantic-release
- Conventional Commits
- Automatic versioning
- Changelog generation
- NPM/GitHub releases

## Project Structure
```
.release.json                   // or .releaserc.js
.github/
└── workflows/
    └── release.yml             // CI workflow
package.json
CHANGELOG.md                    // Generated
```

## Architecture Rules

- **Commit message driven.** Commits determine version bump.
- **Fully automated.** No manual version bumps.
- **Plugins for tasks.** Analyze, generate notes, publish.
- **CI only.** Runs in CI, not locally.

## Coding Conventions

- Config: `{ "branches": ["main"], "plugins": ["@semantic-release/commit-analyzer", "@semantic-release/release-notes-generator", "@semantic-release/changelog", "@semantic-release/npm", "@semantic-release/github"] }`.
- Commit: `fix: resolve button alignment` → patch bump.
- Commit: `feat: add dark mode` → minor bump.
- Commit: `BREAKING CHANGE: new API` → major bump.
- CI: `npx semantic-release` runs on push to main.

## NEVER DO THIS

1. **Never run semantic-release locally.** Designed for CI.
2. **Never commit version bumps manually.** semantic-release handles it.
3. **Never use without conventional commits.** Won't know how to bump.
4. **Never forget to configure CI tokens.** `GH_TOKEN`, `NPM_TOKEN`.
5. **Never skip the dry-run.** `semantic-release --dry-run` to test.
6. **Never use on non-main branch without config.** Specify branches.
7. **Never ignore failed releases.** Check logs, may need manual fix.

## Testing

- Test with `semantic-release --dry-run`.
- Test commit analyzer matches expected bumps.
- Test plugins execute in order.


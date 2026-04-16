# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- standard-version
- Conventional Commits
- Automatic versioning
- Changelog generation
- Git tagging

## Project Structure
```
package.json
CHANGELOG.md                    // Generated
.git/
└── tags
```

## Architecture Rules

- **Local versioning.** Run locally to bump version.
- **Conventional commits.** Parse commits for version.
- **Lifecycle scripts.** prebump, postbump, pretag, posttag.
- **Manual but standardized.** Consistent versioning process.

## Coding Conventions

- Run: `npx standard-version` (bumps, tags, commits).
- First release: `npx standard-version --first-release`.
- Dry run: `npx standard-version --dry-run`.
- Skip: `npx standard-version --skip.changelog --skip.tag`.
- Lifecycle: Add scripts to package.json: `"prebump": "npm test"`, `"postbump": "npm run build"`.

## NEVER DO THIS

1. **Never commit version bump manually first.** Let standard-version handle.
2. **Never forget to commit before running.** Needs clean state.
3. **Never use without conventional commits.** Won't know version.
4. **Never skip testing the dry-run first.** Verify what will happen.
5. **Never ignore the `skip` options.** Use when regenerating.
6. **Never use in CI blindly.** Designed for local use.
7. **Never forget to push after.** `git push --follow-tags origin main`.

## Testing

- Test dry-run output shows expected version.
- Test changelog generates correctly.
- Test lifecycle scripts run in order.
- Test first release flag.
- Test skip options work.

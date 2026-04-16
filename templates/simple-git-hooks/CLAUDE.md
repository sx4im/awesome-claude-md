# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- simple-git-hooks
- Zero dependency
- package.json configuration
- Fast
- Minimal

## Project Structure
```
package.json                    // Hooks defined here
src/
```

## Architecture Rules

- **Zero dependency.** Single package, no deps.
- **package.json config.** Define hooks in `simple-git-hooks` field.
- **Automatic setup.** Runs on postinstall.
- **Minimal.** Just runs commands, no fancy features.

## Coding Conventions

- Config: `{ "simple-git-hooks": { "pre-commit": "npx biome check --staged", "commit-msg": "npx commitlint --edit $1" } }`.
- Install: `npm install simple-git-hooks` (sets up hooks automatically).
- Postinstall: Runs automatically after npm install.
- No skip: No built-in skip mechanism—use `git commit --no-verify`.

## NEVER DO THIS

1. **Never forget to reinstall after deleting .git/hooks.** Hooks in .git, not node_modules.
2. **Never use for complex hook logic.** Just runs shell commands.
3. **Never expect parallel execution.** Runs sequentially.
4. **Never use without testing.** Make test commit to verify.
5. **Never ignore hook exit codes.** Non-zero fails the git operation.
6. **Never mix with husky/lefthook.** Use one git hooks manager.
7. **Never forget `$1` for commit-msg hook.** Passes commit message file.

## Testing

- Test hooks run on appropriate git actions.
- Test that failing commands block git operation.
- Test reinstall after `rm -rf .git/hooks`.


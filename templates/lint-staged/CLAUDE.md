# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- lint-staged
- Husky integration
- ESLint/Prettier/Biome
- Staged files only
- Fast linting

## Project Structure
```
.lintstagedrc.js                // or lint-staged.config.js
package.json                    // lint-staged config can be here
src/
```

## Architecture Rules

- **Staged files only.** Lint only what changed.
- **Fast feedback.** Don't lint entire codebase.
- **Auto-fix.** Fix automatically when possible.
- **Block bad commits.** Fail commit if lint fails.

## Coding Conventions

- Config: `module.exports = { '*.{js,jsx,ts,tsx}': ['eslint --fix', 'prettier --write'], '*.{json,css,md}': 'prettier --write' }`.
- Package.json: `{ "lint-staged": { "*.{ts,tsx}": "eslint --fix" } }`.
- With Husky: `echo "npx lint-staged" > .husky/pre-commit`.
- Glob patterns: Use micromatch syntax.

## NEVER DO THIS

1. **Never lint entire codebase in pre-commit.** Too slow—use lint-staged.
2. **Never skip the `--fix` flag.** Auto-fix what can be fixed.
3. **Never use slow commands in lint-staged.** Affects every commit.
4. **Never forget glob quotes in package.json.** `"*.{js,ts}": ...`.
5. **Never lint generated files.** Exclude `dist/`, `build/`.
6. **Never use lint-staged without git hooks.** Integrate with Husky.
7. **Never ignore exit codes.** Non-zero exit blocks commit.

## File Naming

- Config: `.lintstagedrc.js`, `lint-staged.config.js`, or `lint-staged` field in `package.json`
- Hooks: `.husky/pre-commit` contains `npx lint-staged`

## Testing

- Test with a staged file that has a lint error and verify commit is blocked.
- Test auto-fix applies correctly and stages the fixed file.
- Test commit is blocked when unfixable errors exist in staged files.
- Test with multiple staged files across different glob patterns.
- Test that unstaged files are not modified by lint-staged commands.


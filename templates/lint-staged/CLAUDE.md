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

## Testing

- Test with staged file that has lint error.
- Test auto-fix applies correctly.
- Test commit blocked when unfixable errors exist.
- Test with multiple staged files.


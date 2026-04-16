# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- commitlint
- Conventional Commits
- @commitlint/config-conventional
- Husky/simple-git-hooks integration
- Commit message linting

## Project Structure
```
.commitlintrc.js                // or commitlint.config.js
package.json
src/
```

## Architecture Rules

- **Conventional Commits.** `type(scope): subject` format.
- **Lint commit messages.** Enforce format on commit.
- **Generate changelogs.** From conventional commits.
- **Semantic versioning.** Determine version bumps from types.

## Coding Conventions

- Config: `module.exports = { extends: ['@commitlint/config-conventional'], rules: { 'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore']], 'subject-case': [2, 'never', ['sentence-case', 'start-case']], 'subject-full-stop': [2, 'never', '.'] } }`.
- Format: `feat(auth): add login functionality`.
- Types: `feat` (new feature), `fix` (bug fix), `docs` (documentation), `style` (formatting), `refactor` (code change), `test` (tests), `chore` (maintenance).
- Scope: Optional, describes affected area: `feat(api):`, `fix(ui):`.
- Breaking: `BREAKING CHANGE:` in footer or `feat(api)!:`.

## NEVER DO THIS

1. **Never write commit messages like sentences.** `add feature` not `Added feature`.
2. **Never skip the type.** Must start with `feat:`, `fix:`, etc.
3. **Never use past tense.** `add` not `added`.
4. **Never exceed 72 characters in subject.** Body for longer explanation.
5. **Never mix commitlint with non-conventional repos.** Enforce project-wide.
6. **Never forget the body for complex changes.** Explain what and why.
7. **Never use `chore` for everything.** Pick appropriate type.

## Testing

- Test with `echo "bad commit" | npx commitlint` (should fail).
- Test with valid conventional commit (should pass).
- Test in pre-commit hook.


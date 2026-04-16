# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- ESLint 8/9
- @typescript-eslint
- Strict rule configuration
- Prettier integration
- Pre-commit hooks

## Project Structure
```
.eslintignore
.eslintrc.js                   // or eslint.config.js (flat config)
.prettierrc
package.json
src/
└── ...                         // Code checked by ESLint
```

## Architecture Rules

- **Strict rule set.** Catch errors early.
- **Type-aware rules.** @typescript-eslint with type checking.
- **Consistent style.** Prettier for formatting.
- **Automated enforcement.** Husky + lint-staged.

## Coding Conventions

- Config: `module.exports = { parser: '@typescript-eslint/parser', parserOptions: { project: './tsconfig.json' }, extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended', 'plugin:@typescript-eslint/recommended-requiring-type-checking'], rules: { '@typescript-eslint/no-explicit-any': 'error', '@typescript-eslint/no-unused-vars': 'error', '@typescript-eslint/explicit-function-return-type': 'warn' } }`.
- Flat config (ESLint 9): `import tseslint from 'typescript-eslint'; export default tseslint.config(tseslint.configs.recommended, tseslint.configs.recommendedTypeChecked)`.
- Run: `eslint . --ext .ts,.tsx`.
- Fix: `eslint . --ext .ts,.tsx --fix`.

## NEVER DO THIS

1. **Never disable ESLint with comments carelessly.** Explain why when needed.
2. **Never mix prettier and ESLint formatting rules.** Prettier for format, ESLint for code quality.
3. **Never skip @typescript-eslint/recommended-requiring-type-checking.** Type-aware rules catch more bugs.
4. **Never ignore 'any' warnings.** Fix with proper types.
5. **Never use `console.log` without eslint exception.** `// eslint-disable-next-line no-console`.
6. **Never skip pre-commit hooks.** Catch issues before commit.
7. **Never ignore `no-floating-promises`.** Unhandled promises are bugs.

## Testing

- Test `eslint .` passes with no errors.
- Test `--fix` resolves auto-fixable issues.
- Test pre-commit hook catches errors.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Husky v9 (Git hooks)
- lint-staged
- Modern zero-config approach
- Git 2.9+
- Node.js 18+

## Project Structure
```
.husky/
├── pre-commit                  // Hook scripts
├── commit-msg
└── _/
    └── husky.sh                // Husky setup
package.json
```

## Architecture Rules

- **Zero configuration.** Auto-detects Git hooks directory.
- **Simple scripts.** Direct executable files in `.husky/`.
- **Fast initialization.** `husky init` sets up quickly.
- **Shebang required.** Scripts need proper shebang line.

## Coding Conventions

- Init: `npx husky init` or `echo "npx test" > .husky/pre-commit`.
- Add hook: `echo "npm run lint" >> .husky/pre-commit`.
- With lint-staged: `echo "npx lint-staged" > .husky/pre-commit`.
- Custom hooks: Create files in `.husky/` with appropriate names.

## NEVER DO THIS

1. **Never manually edit `.git/hooks`.** Husky manages these.
2. **Never skip the shebang in hook scripts.** `#!/bin/sh` or `#!/usr/bin/env sh`.
3. **Never use without `core.hooksPath` set.** Husky does this automatically.
4. **Never commit hook scripts without testing.** Can block all commits.
5. **Never use interactive commands in hooks.** Hooks run non-interactively.
6. **Never forget to make hooks executable.** `chmod +x .husky/pre-commit`.
7. **Never mix Husky v8 and v9 syntax.** Different initialization approaches.

## Testing

- Test with intentional lint error (should block commit).
- Test hook execution order.
- Test with `--no-verify` bypass.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Biome (linter, formatter)
- Rust-based speed
- ESLint + Prettier replacement
- TypeScript support
- One tool for all

## Project Structure
```
biome.json                      // Biome configuration
package.json
src/
└── ...                         // Code formatted and linted
```

## Architecture Rules

- **All-in-one.** Linter and formatter in one tool.
- **Fast.** Rust implementation, faster than ESLint + Prettier.
- **Compatible.** Similar rules to ESLint recommended.
- **Migration easy.** `biome migrate eslint --write`.

## Coding Conventions

- Config: `{ "organizeImports": { "enabled": true }, "linter": { "enabled": true, "rules": { "recommended": true, "suspicious": { "noConsoleLog": "error" } } }, "formatter": { "enabled": true, "indentStyle": "tab", "indentWidth": 2 } }`.
- Check: `biome check .` (lint + format + imports).
- Format: `biome format . --write`.
- Lint: `biome lint .`.
- CI: `biome ci .` (fails on errors).

## NEVER DO THIS

1. **Never mix Biome with ESLint/Prettier.** Pick one toolchain.
2. **Never skip `organizeImports`.** Automatic import sorting.
3. **Never ignore the `migrate` command.** Easy transition from ESLint.
4. **Never use Biome for Vue/Svelte files yet.** Limited support.
5. **Never forget `biome.json` in version control.** Share config.
6. **Never skip pre-commit integration.** `biome check --staged`.
7. **Never ignore rule overrides.** Configure per file if needed.

## Testing

- Test `biome check` passes.
- Test formatting is consistent.
- Test migration from ESLint works.


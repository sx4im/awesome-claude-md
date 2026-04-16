# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Knip (find unused code)
- TypeScript/JavaScript
- Monorepo support
- Fast analysis
- CI integration

## Project Structure
```
knip.config.ts                  // or knip.json
package.json                    // Can configure here too
src/
```

## Architecture Rules

- **Find unused exports.** Dead code detection.
- **Find unused dependencies.** Package.json bloat.
- **Find unused files.** Orphaned code.
- **Monorepo aware.** Cross-package references.

## Coding Conventions

- Config: `{ "entry": ["src/index.ts"], "project": ["src/**/*.ts"], "ignore": ["**/*.test.ts"], "rules": { "files": "error", "dependencies": "warn", "exports": "error" } }`.
- Run: `npx knip` (check), `npx knip --fix` (auto-fix where possible).
- CI: Add to CI pipeline, fail on errors.
- Ignore: `// @knipignore` comment or config file.

## NEVER DO THIS

1. **Never ignore all warnings blindly.** Review each finding.
2. **Never forget to configure `entry` points.** Without, can't determine used.
3. **Never use `--fix` without review.** May remove actually used code.
4. **Never skip the `ignore` config.** Test files, generated code.
5. **Never forget that dynamic imports may not be detected.** `import(path)`.
6. **Never ignore monorepo configuration.** `workspaces` in config.
7. **Never use without understanding false positives.** Some exports used dynamically.

## Testing

- Test with known unused code to verify detection.
- Test fix removes correct code.
- Test in CI blocks unused code.
- Test with monorepo setup.
- Test dynamic imports detection.


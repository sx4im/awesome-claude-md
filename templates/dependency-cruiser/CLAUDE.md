# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- dependency-cruiser
- Architecture validation
- Import graph visualization
- CI integration
- No circular dependencies

## Project Structure
```
.dependency-cruiser.cjs         // or .dependency-cruiser.js
package.json
src/
└── ...                         // Validated code
```

## Architecture Rules

- **Validate imports.** Enforce architecture rules.
- **Detect circular dependencies.** Break cycles.
- **Visualize architecture.** Generate dependency graphs.
- **Enforce boundaries.** Module separation.

## Coding Conventions

- Config: `module.exports = { forbidden: [{ name: 'no-circular', severity: 'error', from: {}, to: { circular: true } }, { name: 'no-cross-module', severity: 'error', from: { path: '^src/module-a' }, to: { path: '^src/module-b' } }] }`.
- Run: `npx depcruise src`.
- Graph: `npx depcruise --include-only '^src' --output-type dot src | dot -T svg > dependency-graph.svg`.
- Validate: `npx depcruise src --config .dependency-cruiser.cjs`.

## NEVER DO THIS

1. **Never ignore circular dependencies.** Break them immediately.
2. **Never forget to run in CI.** Prevent bad dependencies.
3. **Never use without understanding the config format.** Rules are powerful.
4. **Never skip the `options` configuration.** Module resolution, TypeScript.
5. **Never ignore severity levels.** `error` vs `warn` vs `info`.
6. **Never forget to update when refactoring.** Rules may need adjustment.
7. **Never use for large repos without caching.** Can be slow.

## Testing

- Test circular dependency detection works.
- Test architecture rules are enforced.
- Test graphs generate correctly.
- Test CI integration.
- Test with monorepo setup.


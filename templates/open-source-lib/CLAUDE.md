# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Platform & Framework Engineering)

### Release Discipline
- Preserve platform-specific lifecycle, build, and runtime constraints.
- Treat compatibility and upgrade paths as first-class requirements.
- Avoid hidden coupling that blocks portability or rollback.

### Merge/Release Gates
- Build/test matrix passes for supported targets.
- Critical startup/runtime flows validated under production-like config.
- Migration/rollback notes included for impactful framework changes.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- TypeScript 5.x (strict mode)
- Vitest for testing
- tsup for bundling
- Changesets for versioning and changelogs
- GitHub Actions for CI/CD
- npm for publishing

## Project Structure

```
.
├── src/
│   ├── index.ts           # Public API entry point: re-exports only
│   ├── core/              # Core logic modules
│   ├── utils/             # Internal utility functions
│   ├── errors.ts          # Custom error classes
│   └── types.ts           # Public type definitions
├── tests/
│   ├── unit/              # Unit tests mirroring src/ structure
│   └── integration/       # Integration tests
├── .changeset/            # Changeset files for versioning
├── tsup.config.ts         # Build configuration
├── vitest.config.ts       # Test configuration
├── tsconfig.json          # TypeScript configuration
├── tsconfig.build.json    # Build-specific TS config (excludes tests)
└── package.json
```

## Architecture Rules

- **`src/index.ts` is the public API.** It contains only re-exports: `export { createParser } from './core/parser'`. Nothing else. Users import from your package name, and this file defines exactly what they get.
- **Internal modules are not part of the public API.** Anything not exported from `src/index.ts` can be refactored or removed without a major version bump. Use a `@internal` JSDoc tag on internal helpers to make this explicit.
- **Errors are typed and descriptive.** Define custom error classes in `src/errors.ts`. Every error has a unique `code` property (e.g., `PARSE_FAILED`, `INVALID_CONFIG`). Never throw plain `Error('something went wrong')`.
- **Zero side effects at import time.** Importing your library must not execute any code, make network requests, or read environment variables. All behavior is triggered by function calls.
- **Dual ESM + CJS output.** Configure tsup to output both formats. Test both in CI.

## Public API Design Rules

- **Named exports only.** `export function createParser()`. never `export default`. Default exports cause naming conflicts and make auto-imports unreliable for consumers.
- **Every public function has JSDoc.** Include a description, `@param` for each parameter, `@returns`, `@throws` for possible errors, and `@example` with a runnable code snippet. No exceptions.
- **Semantic versioning is law.** Breaking change → major. New feature → minor. Bug fix → patch. Use Changesets to enforce this. every PR that changes behavior must include a changeset file.
- **Public type signatures never use `any`.** Use `unknown` for truly unknown types, generics for flexible types. `any` in a public API leaks into consumer codebases.
- **Function options use an options object, not positional arguments.** After 2 parameters, use `function createParser(input: string, options: ParserOptions)`. Not `function createParser(input: string, strict: boolean, maxDepth: number, encoding: string)`.

## Bundle Size Discipline

- **Check bundle size before adding any dependency.** Use `bundlephobia.com` or `pkg-size.dev`. If a dependency adds more than 5KB gzipped and you only use one function from it, copy that function instead.
- **Never bundle devDependencies.** `tsup` should mark all `dependencies` and `peerDependencies` as external. Only your source code ships.
- **Tree-shaking must work.** Set `"sideEffects": false` in `package.json`. Test tree-shaking by importing one function and checking the bundle size.
- **Audit the output.** After building, inspect `dist/` to ensure no test files, source maps (unless opt-in), or dev-only code leaked in.

## Coding Conventions

- One module per file. `parser.ts` exports the parser, `validator.ts` exports the validator. Co-locate related types at the top of the module.
- Internal helpers: prefix with `_` or keep in a `utils/` directory not exported from `index.ts`.
- Error handling: throw typed errors (your custom classes) and document them with `@throws`. Never silently swallow errors. Never return `null` to signal failure. throw or use a `Result` type.
- All functions are pure unless documented otherwise. If a function has side effects, name it accordingly: `writeConfig()`, `sendEvent()`.

## Library Preferences

- **Testing:** Vitest. not Jest (Vitest is faster, native ESM, same API). Not a hard migration if already on Jest, but new libraries should start with Vitest.
- **Bundling:** tsup. not Rollup directly (tsup has sensible defaults), not esbuild alone (tsup handles DTS generation). Not webpack (too heavy for libraries).
- **Versioning:** Changesets. not `standard-version` (Changesets handles monorepos and has better GitHub integration). Not manual `npm version`.
- **Linting:** ESLint flat config + `@typescript-eslint`. Not Biome yet (still maturing for library code quality rules).

## File Naming

- Source modules: `camelCase.ts` → `parser.ts`, `validator.ts`, `configLoader.ts`
- Test files: `camelCase.test.ts` → `parser.test.ts`, `validator.test.ts`
- Type files: `types.ts` for public types, `internal-types.ts` for internal types
- Error files: `errors.ts`. one file, all custom error classes
- Config files: standard names → `tsconfig.json`, `vitest.config.ts`, `tsup.config.ts`

## NEVER DO THIS

1. **Never add a peer dependency without documenting the minimum version.** If your library needs React >= 18, put it in `peerDependencies` AND in the README. Unresolved peer deps cause silent runtime failures for consumers.
2. **Never use `process.env` in library code.** Libraries don't own the environment. If you need configuration, accept it as a function argument or options object. Environment variables are the application's concern.
3. **Never bundle devDependencies.** Your test framework, linters, and build tools must never end up in the published npm package. Check with `npm pack --dry-run` before publishing.
4. **Never ship source maps to npm without opt-in.** Source maps are useful for debugging but inflate the install size. Default to no source maps, offer a `--sourcemap` build option.
5. **Never use `any` in public type signatures.** It infects the consumer's type safety. Use `unknown`, generics, or specific union types. If a type is hard to express, that's a design problem. simplify the API.
6. **Never break the public API without a major version bump.** Renaming a function, changing a parameter type, or removing an export all require a major release. Changesets enforce this if configured correctly.
7. **Never publish without running the full test suite.** CI must run lint, type-check, test, and build before publishing. No "I'll test it locally" shortcuts.

## JSDoc Standards

Every public export must have JSDoc following this pattern:

```typescript
/**
 * Parses a configuration string into a structured Config object.
 *
 * @param input - Raw configuration string in TOML format
 * @param options - Parser options
 * @returns Parsed and validated Config object
 * @throws {ParseError} If the input string is malformed
 * @throws {ValidationError} If required fields are missing
 *
 * @example
 * ```ts
 * import { parseConfig } from 'your-library';
 *
 * const config = parseConfig('[server]\nport = 3000');
 * console.log(config.server.port); // 3000
 * ```
 */
export function parseConfig(input: string, options?: ParseOptions): Config {
```

## Testing

- Use Vitest. Test files live in `tests/unit/` mirroring the `src/` structure.
- Every public function must have tests covering: normal input, edge cases, error cases.
- Test the public API from the consumer's perspective. import from `src/index.ts`, not internal modules.
- Integration tests verify the built output (`dist/`) works correctly in both ESM and CJS.
- Run `vitest --coverage` and enforce a minimum coverage threshold (aim for 90%+ on public API).

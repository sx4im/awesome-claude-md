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

## Production Delivery Playbook (Category: Release Engineering & Code Quality)

### Release Discipline
- Treat linting, typing, dependency policy, and changelog signals as release gates.
- Never bypass policy tooling to pass CI quickly.
- Keep rule changes minimal, explicit, and documented with rationale.

### Merge/Release Gates
- CI quality checks pass under project standard configuration.
- No false-positive suppression without scoped justification.
- Release metadata/versioning output validated for changed workflows.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

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
- Test CI integration passes.

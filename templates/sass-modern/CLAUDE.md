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

## Production Delivery Playbook (Category: Design System & CSS Tooling)

### Release Discipline
- Preserve token consistency, theming behavior, and cross-package style contracts.
- Avoid introducing runtime styling regressions that increase bundle or render cost.
- Keep accessibility and visual consistency as hard requirements.

### Merge/Release Gates
- Visual regression checks for core components/tokens pass.
- No critical CSS ordering/specificity regressions in production build.
- Design token and generated artifact integrity validated.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Sass/SCSS (modern features)
- @use and @forward modules
- CSS custom properties
- Vite/Webpack integration
- Stylelint for linting

## Project Structure
```
src/
├── styles/
│   ├── abstracts/
│   │   ├── _index.scss         // Forward all
│   │   ├── _variables.scss     // CSS vars
│   │   ├── _functions.scss
│   │   └── _mixins.scss
│   ├── components/
│   │   └── _button.scss
│   └── main.scss               // Entry point
```

## Architecture Rules

- **Module system.** Use `@use` and `@forward`, not `@import`.
- **Namespacing.** `variables.$primary` or `use ... as *` to unnamespace.
- **CSS variables for theming.** Sass vars for static values, CSS vars for dynamic.
- **Partials with underscore.** `_partial.scss` imported without underscore.

## Coding Conventions

- Module: `@use 'variables'; .btn { color: variables.$primary; }`.
- Forward: `@forward 'variables' hide $internal;` in `_index.scss`.
- With config: `@use 'variables' with ($primary: blue);`.
- Mixins: `@mixin flex-center { display: flex; align-items: center; }`.
- Include: `@include mixins.flex-center;`.
- CSS vars: `--primary: #{$sass-var};` to expose Sass to CSS.

## NEVER DO THIS

1. **Never use `@import`.** Deprecated in favor of `@use`/`@forward`.
2. **Never use global variables.** Everything should be namespaced.
3. **Never skip the `_index.scss` pattern.** Clean API for consumers.
4. **Never forget `meta.load-css`.** For dynamic imports.
5. **Never use Sass for everything.** CSS nesting now native—use it.
6. **Never ignore the module cache.** Each `@use` is cached per file.
7. **Never forget `!default`.** Allow configuration overrides.

## Testing

- Test Sass compiles without warnings.
- Test CSS custom properties output correctly.
- Test module resolution works across files.

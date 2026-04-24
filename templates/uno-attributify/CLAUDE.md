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

- UnoCSS with Attributify preset
- Vue/React/Svelte
- Semantic attributes for styling
- Clean component markup

## Project Structure
```
src/
├── components/
│   └── Button.vue              // Uses attributify attributes
├── uno.config.ts               // Attributify preset enabled
└── App.vue
```

## Architecture Rules

- **Attributes instead of classes.** `m-4` becomes `m="4"`.
- **Grouped utilities.** `flex="~ col gap-4"` groups flex-related classes.
- **Cleaner templates.** Separates styling from logic in markup.
- **Same power as classes.** All UnoCSS features available.

## Coding Conventions

- Enable: `presets: [presetAttributify(), presetWind()]`.
- Basic: `<div m="4" p="4" bg="blue-500" />`.
- Grouped: `<div flex="~ col gap-4 items-center" />`.
- Complex: `<div text="sm white dark:gray-400" font="bold" />`.
- Breakpoints: `<div md:p="8" sm:p="4" />`.

## NEVER DO THIS

1. **Never use without presetAttributify.** Won't work out of the box.
2. **Never mix class and attribute styles carelessly.** Pick one approach per component.
3. **Never forget quotes.** Attribute values with special chars need quotes.
4. **Never use for very dynamic values.** Classes better for computed styles.
5. **Never ignore the `type` declaration.** TS projects need attributify types.
6. **Never skip the `prefix` option.** Use `uno-` prefix to avoid conflicts.
7. **Never forget about CSS specificity.** Same specificity as classes.

## Testing

- Test all attributify patterns compile.
- Test responsive attributify works.
- Test TypeScript recognizes attributes.
- Test with Vue templates.
- Test with React components.

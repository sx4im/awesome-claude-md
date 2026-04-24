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

- Open Props (CSS custom properties)
- Vite/PostCSS integration
- Design token approach
- Subsettable imports

## Project Structure
```
src/
├── styles/
│   ├── props/
│   │   ├── index.css           // Import specific props
│   │   └── media.css           // Responsive props
│   └── globals.css             // Uses Open Props
└── main.ts
```

## Architecture Rules

- **CSS variables as tokens.** `--size-1`, `--color-blue-5`, etc.
- **Systematic scaling.** Predefined scales for size, color, shadow.
- **JIT-friendly.** Import only needed props.
- **No build step required.** Can use CDN version.

## Coding Conventions

- Import: `import 'open-props/style'` for all, or `import 'open-props/gray'` for specific.
- Usage: `font-size: var(--font-size-3); padding: var(--size-3);`.
- Gradients: `background: var(--gradient-1);`.
- Shadows: `box-shadow: var(--shadow-2);`.
- Animations: `animation: var(--animation-fade-in);`.
- Custom: Define your own on top: `--brand-color: var(--color-blue-5);`.

## NEVER DO THIS

1. **Never import all props without need.** Bundle size matters—subset.
2. **Never override Open Props directly.** Create semantic aliases.
3. **Never skip the normalize.** `open-props/normalize` provides base styles.
4. **Never use without understanding scales.** Learn the sizing/color scales.
5. **Never ignore the `oklch` colors.** Better perceptual uniformity.
6. **Never forget PostCSS plugin.** For JIT optimization if using build tools.
7. **Never mix with Tailwind blindly.** Different approaches—pick one.

## Testing

- Test CSS custom properties cascade correctly.
- Test animation performance.
- Test color contrast with OKLCH values.

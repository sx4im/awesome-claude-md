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

- Stencil (Web Components compiler)
- TypeScript
- JSX support
- Lazy loading
- Framework-agnostic output

## Project Structure
```
src/
├── components/
│   ├── my-button/
│   │   ├── my-button.tsx       // Stencil component
│   │   ├── my-button.css
│   │   └── my-button.e2e.ts    // E2E tests
│   └── my-card/
├── utils/
│   └── helpers.ts
└── index.html
```

## Architecture Rules

- **Compiler-based.** Generates optimized Web Components.
- **Decorators for metadata.** `@Component`, `@Prop`, `@State`, `@Event`.
- **JSX templating.** React-like JSX syntax.
- **Framework bindings.** Generates React, Vue, Angular wrappers.

## Coding Conventions

- Component: `@Component({ tag: 'my-button', styleUrl: 'my-button.css', shadow: true }) export class MyButton { @Prop() label: string; @State() count = 0; render() { return <button>{this.label}</button>; } }`.
- Props: `@Prop() label: string;` (immutable from outside).
- State: `@State() count = 0;` (internal mutable).
- Events: `@Event() myClick: EventEmitter; this.myClick.emit(data)`.

## NEVER DO THIS

1. **Never mutate @Prop directly.** Props are immutable.
2. **Never forget the @Component decorator.** Required metadata.
3. **Never use without understanding shadow vs scoped.** `shadow: true/false`.
4. **Never skip the `dist-custom-elements` output.** For tree-shaking.
5. **Never ignore the `hydrated` flag.** Check before DOM operations.
6. **Never mix mutable patterns with @State.** Mutate state object, trigger re-render.
7. **Never forget to build before testing in other frameworks.** Generates wrappers.

## Testing

- Test with Jest and Puppeteer.
- Test component methods directly.
- Test in consuming frameworks (React, Vue, Angular).

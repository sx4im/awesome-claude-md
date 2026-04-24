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

## Production Delivery Playbook (Category: Languages)

### Release Discipline
- Follow idiomatic language patterns and package ecosystem conventions.
- Prefer standard tooling for formatting, linting, and testing.
- Avoid introducing non-portable patterns without documented rationale.

### Merge/Release Gates
- Compiler/interpreter checks pass with strict settings where available.
- Core examples and sample usage remain executable.
- Dependency updates are pinned and reviewed for compatibility.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Goober (tiny CSS-in-JS)
- < 1KB runtime
- React/Preact/Vue/Svelte
- Critical CSS extraction
- Babel plugin for extraction

## Project Structure
```
src/
├── components/
│   └── Button.tsx              // Uses goober
├── styles/
│   └── global.ts               // Global styles
└── goober.config.js
```

## Architecture Rules

- **Smallest CSS-in-JS.** Under 1KB vs 10KB+ for alternatives.
- **CSS tagged template.** `` css`...` `` generates class names.
- **Styled components.** `styled('div')`...`` or `styled.div`...``.
- **Critical CSS.** `extractCss()` for SSR.

## Coding Conventions

- Setup: `import { css, styled } from 'goober'; setPragma(h);`.
- CSS: `const className = css`color: red; font-size: 16px;`;`.
- Styled: `const Button = styled('button')`background: blue; color: white;`;`.
- Dynamic: `const dynamic = css`color: ${props => props.color};`;` (runtime).
- Global: `css`@import url(...);`;` or `glob`body { margin: 0; }``.

## NEVER DO THIS

1. **Never forget `setPragma`.** Required for JSX integration.
2. **Never use without Babel plugin in production.** Critical CSS extraction.
3. **Never do heavy computations in template literals.** Runtime overhead.
4. **Never ignore the `target` option.** Set to `document.head` for shadow DOM.
5. **Never mix with other CSS-in-JS.** Pick one solution.
6. **Never forget keyframes.** `keyframes`...`` for animations.
7. **Never skip `extractCss()` in SSR.** Prevents flash of unstyled content.

## Testing

- Test bundle size is minimal.
- Test critical CSS extraction works.
- Test dynamic styles update correctly.

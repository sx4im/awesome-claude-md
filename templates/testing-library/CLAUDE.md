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

## Production Delivery Playbook (Category: Frontend)

### Release Discipline
- Enforce performance budgets (bundle size, LCP, CLS) before merge.
- Preserve accessibility baselines (semantic HTML, keyboard nav, ARIA correctness).
- Block hydration/runtime errors with production build verification.

### Merge/Release Gates
- Typecheck + lint + unit tests + production build pass.
- Critical route smoke tests for navigation, auth, and error boundaries.
- No new console errors/warnings in key user flows.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Testing Library (user-centric testing)
- React Testing Library (DOM)
- Jest/Vitest runner
- User Event v14
- jest-dom matchers

## Project Structure
```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx         # Co-located test
├── hooks/
│   └── useAuth.test.ts
└── test/
    └── test-utils.tsx          # Custom render
```

## Architecture Rules

- **Test behavior, not implementation.** Test what users see and do.
- **Queries prioritize accessibility.** `getByRole`, `getByLabelText` over `getByTestId`.
- **User Event for interactions.** Simulates realistic user events.
- **Avoid testing implementation details.** Don't test state, props, or internal methods.

## Coding Conventions

- Render: `render(<Component />)` from `@testing-library/react`.
- Query: `screen.getByRole('button', { name: /submit/i })`.
- User event: `const user = userEvent.setup(); await user.click(button)`.
- Async: `await screen.findByText('Loaded')` for async elements.
- Assert: `expect(button).toBeDisabled()` with `jest-dom`.
- Custom render: Create wrapper with providers (theme, router, etc.).

## NEVER DO THIS

1. **Never use `getByTestId` as first choice.** It's a last resort—prefer semantic queries.
2. **Never test implementation details.** Don't assert on `state` or check if function was called (unless it's the behavior).
3. **Never use `fireEvent` instead of `userEvent`.** `userEvent` is more realistic.
4. **Never forget `act` warnings.** Usually handled automatically, but understand when needed.
5. **Never test third-party libraries.** Test your code, not library internals.
6. **Never skip `screen` object.** It's the recommended way to query.
7. **Never use `container` queries.** They break easily—use role/label queries.

## Testing

- Test with `screen.debug()` to see rendered output.
- Test accessibility with `jest-axe`.
- Test with Testing Library Playground for query selection.

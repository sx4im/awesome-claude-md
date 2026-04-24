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

- Recoil (Facebook's state management)
- React 18+
- TypeScript 5.x
- React 18+ Concurrent Features (experimental integration)

## Project Structure

```
src/
├── atoms/
│   ├── index.ts                // Atom exports
│   ├── auth.ts                 // Auth atoms
│   └── ui.ts                   // UI atoms
├── selectors/
│   ├── index.ts                // Selector exports
│   └── derived.ts              // Computed values
├── hooks/
│   └── useRecoil.ts            // Custom Recoil hooks
└── lib/
    └── recoil-effects.ts       // Atom effects
```

## Architecture Rules

- **Atoms are units of state.** Create small, focused atoms: `textState`, `currentUserState`.
- **Selectors for derived state.** Pure functions that compute from atoms or other selectors.
- **Atom effects for side effects.** Persistence, logging, or synchronization using `effects_UNSTABLE`.
- **Family atoms for dynamic state.** `atomFamily` for parameterized state (per-item selection).

## Coding Conventions

- Create atom: `const textState = atom({ key: 'textState', default: '' })`.
- Create selector: `const charCountState = selector({ key: 'charCountState', get: ({get}) => get(textState).length })`.
- Use hooks: `const [text, setText] = useRecoilState(textState)`.
- Read-only: `const count = useRecoilValue(charCountState)`.
- Setter only: `const setText = useSetRecoilState(textState)`.

## Library Preferences

- **Recoil DevTools:** Use Recoilize or similar for debugging.
- **Persistence:** Atom effects for localStorage sync.
- **Async queries:** Use selectors or `useRecoilValueLoadable` with Suspense.
- **URL sync:** Custom effects for query parameter synchronization.

## File Naming

- Atom files: `[domain].ts` → `auth.ts`, `settings.ts`
- Selector files: `[purpose].ts` or co-located with atoms.
- Effects file: `effects.ts` or `recoil-effects.ts`.

## NEVER DO THIS

1. **Never duplicate atom keys.** Keys must be globally unique. Collisions cause silent failures.
2. **Never create atoms inside components.** Define at module level like hooks.
3. **Never ignore `key` prop requirements.** Every atom and selector needs a unique string key.
4. **Never use Recoil for server state.** Selectors can fetch, but TanStack Query is better for caching.
5. **Never forget to wrap with `RecoilRoot`.** All Recoil usage requires this provider at the root.
6. **Never ignore circular dependencies.** Selectors depending on each other in cycles cause infinite loops.
7. **Never use Recoil in production without considering alternatives.** Meta doesn't heavily invest in Recoil. Consider Jotai or Zustand for new projects.

## Testing

- Wrap tests with `RecoilRoot`. Provide `initializeState` for initial values.
- Test selectors by checking computed values with mock atoms.
- Test effects by verifying side effects (localStorage, etc.).
- Use `act()` for state updates in tests.

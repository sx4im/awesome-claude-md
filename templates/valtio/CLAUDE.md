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

- Valtio v1 (proxy-based state management)
- React 18+
- TypeScript 5.x
- React 18+ Concurrent Features

## Project Structure

```
src/
├── stores/
│   ├── index.ts                # Proxy exports
│   ├── auth.ts                 // Auth state proxy
│   └── ui.ts                   // UI state proxy
├── hooks/
│   └── useSnapshot.ts          // Custom snapshot hooks
└── lib/
    └── proxy-utils.ts          // Valtio utilities
```

## Architecture Rules

- **Proxies hold state.** Create state objects with `proxy({ count: 0, user: null })`.
- **Snapshots for React.** Use `useSnapshot()` in components to subscribe to proxy state.
- **Mutate directly.** Modify proxy state directly: `state.count++`. Valtio handles immutability under the hood.
- **Actions are optional.** Mutate from components or create action functions. Both work.

## Coding Conventions

- Create proxy: `const state = proxy({ count: 0 })` at module level.
- Use in components: `const snap = useSnapshot(state)` then use `snap.count`.
- Mutate state: `state.count++` or `state.user = newUser` from anywhere.
- Subscribe outside React: `subscribe(state, () => console.log(state.count))`.
- Derived state: `const derived = derive({ doubled: (get) => get(state).count * 2 })`.

## Library Preferences

- **derive:** `valtio/utils` for computed properties.
- **subscribe:** Built-in or from `valtio/vanilla` for non-React usage.
- **proxyMap/proxySet:** `valtio/utils` for Map and Set equivalents.
- **useSnapshot:** Always from `valtio` (React import).

## File Naming

- Proxy files: `[domain].ts` → `auth.ts`, `cart.ts`
- Barrel export: `stores/index.ts`

## NEVER DO THIS

1. **Never mutate snapshots.** `snap.count++` doesn't update state. Mutate the proxy: `state.count++`.
2. **Never use `useSnapshot` without reading from the snapshot.** `useSnapshot(state)` and then using `state.count` breaks reactivity.
3. **Never create proxies inside components.** Proxies are singletons. Define at module level.
4. **Never use Valtio for server state.** Use TanStack Query. Valtio is client state only.
5. **Never ignore the re-render scope.** `useSnapshot` re-renders the entire component. Split into smaller components for granular updates.
6. **Never mix Valtio with useState for the same data.** Pick one state management approach.
7. **Never forget to import from correct paths.** `useSnapshot` from `valtio`, `proxy` from `valtio/vanilla` or `valtio`.

## Testing

- Test proxy state changes directly. Proxies are plain objects with tracking.
- Test components by checking re-renders after proxy mutations.
- Mock proxies in tests by creating new proxy instances.
- Test subscriptions with the `subscribe` utility.

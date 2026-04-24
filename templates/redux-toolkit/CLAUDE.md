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

- Redux Toolkit (RTK) v2
- React Redux v9
- React 18+
- TypeScript 5.x
- Redux DevTools Extension

## Project Structure

```
src/
├── store/
│   ├── index.ts                # Store configuration
│   ├── root-reducer.ts         # Combined reducers
│   └── middleware.ts           // Custom middleware
├── features/
│   ├── auth/
│   │   ├── authSlice.ts        // Redux slice
│   │   ├── authSelectors.ts    // Memoized selectors
│   │   └── authThunks.ts       // Async thunks
│   └── posts/
│       ├── postsSlice.ts
│       └── postsThunks.ts
├── hooks/
│   └── redux.ts                // Typed useDispatch, useSelector
└── ...
```

## Architecture Rules

- **Feature-based slices.** Each domain (auth, posts, users) has its own slice with reducer, actions, and selectors.
- **RTK Query for API calls.** Use RTK Query for server state instead of manual thunks where applicable.
- **Selectors in slices.** Define selectors alongside slices using `createSelector` for memoization.
- **Thunks for async logic.** Use `createAsyncThunk` for API calls and side effects.

## Coding Conventions

- Create slice: `createSlice({ name: 'auth', initialState, reducers: { ... } })`.
- Export actions: `export const { login, logout } = authSlice.actions`.
- Export reducer: `export default authSlice.reducer`.
- Use selectors: `const user = useSelector(selectCurrentUser)` with memoized selectors.
- Dispatch: `const dispatch = useAppDispatch()` (typed version).
- Thunks: `createAsyncThunk('auth/login', async (credentials) => { ... })`.

## Library Preferences

- **RTK Query:** For API endpoints. Replaces manual fetch + caching logic.
- **Immer:** Built into RTK. Mutative updates in reducers are fine.
- **Reselect:** Built into RTK via `createSelector` for memoized selectors.
- **DevTools:** Redux DevTools Extension integration built-in.

## File Naming

- Slice files: `[feature]Slice.ts` → `authSlice.ts`
- Thunk files: `[feature]Thunks.ts` or co-located in slice.
- Selector files: `[feature]Selectors.ts` or in slice.

## NEVER DO THIS

1. **Never use plain Redux without Toolkit.** RTK eliminates boilerplate and prevents common mistakes. Always use RTK.
2. **Never define action types as strings manually.** RTK generates these. Don't use `const LOGIN = 'LOGIN'` pattern.
3. **Never mutate state in non-RTK reducers.** Outside `createSlice`, immutability rules apply. Spread operators only.
4. **Never ignore selector memoization.** Inline selectors like `state => state.auth.user` cause re-renders. Use `createSelector`.
5. **Never use `connect` HOC.** Use hooks: `useSelector`, `useDispatch`. `connect` is legacy API.
6. **Never store derived data in Redux.** Compute in selectors, not reducers.
7. **Never put non-serializable data in Redux.** No Dates (use timestamps), no functions, no class instances.

## Testing

- Test slices by calling reducers directly with actions.
- Test thunks by dispatching and checking state changes.
- Test selectors with mock state.
- Use `configureStore` in tests with preloaded state.

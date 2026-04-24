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

- TanStack Query (React Query) v5
- React 18+
- TypeScript 5.x
- Axios or native fetch
- React 18+ Concurrent Features

## Project Structure

```
src/
├── api/
│   ├── client.ts               # API client configuration
│   ├── queries/                # Query definitions
│   │   ├── users.ts
│   │   └── posts.ts
│   └── mutations/              # Mutation definitions
│       ├── users.ts
│       └── posts.ts
├── hooks/
│   └── useUsers.ts             # Custom query hooks
├── providers/
│   └── query-client.tsx        # QueryClientProvider setup
└── lib/
    └── query-keys.ts           # Centralized query keys
```

## Architecture Rules

- **Query keys are the source of truth.** Define query keys in `query-keys.ts` as objects with factory functions: `users.all()`, `users.detail(id)`.
- **Colocate queries with their domain.** User queries in `queries/users.ts`, not scattered in components.
- **Use custom hooks for common queries.** Don't repeat `useQuery({ queryKey, queryFn })` patterns. Create `useUsers()`, `useUser(id)` hooks.
- **Optimistic updates for UX.** Use `optimisticUpdate` pattern for mutations that should feel instant.

## Coding Conventions

- Query keys: `['users', 'list']`, `['users', 'detail', id]` for hierarchical invalidation.
- Query functions: Async functions that return data: `async () => { const res = await api.get('/users'); return res.data }`.
- Use `select` for data transformation: `select: (data) => data.map(transform)`.
- Use `enabled` for conditional fetching: `enabled: !!userId`.
- Destructure query results: `const { data, isLoading, error } = useUsers()`.

## Library Preferences

- **HTTP client:** Axios for interceptors, or native fetch with wrapper.
- **Dev tools:** `@tanstack/react-query-devtools` for debugging.
- **Persistence:** `@tanstack/query-sync-storage-persister` for offline support.
- **Server state:** TanStack Query handles all server state. Use Zustand/Jotai for client state only.

## File Naming

- Query files: `[domain].ts` → `users.ts`, `posts.ts`
- Query key utils: `query-keys.ts` or `queryKeys.ts`
- Custom hooks: `use[Domain].ts` → `useUsers.ts`

## NEVER DO THIS

1. **Never put query keys inline.** `queryKey: ['users']` in 10 places is unmaintainable. Use centralized keys.
2. **Never ignore error handling.** Queries can fail. Always handle `error` state or use Error Boundaries.
3. **Never mix server and client state.** Don't put API data in global state managers. TanStack Query is your server cache.
4. **Never forget to invalidate queries.** After a mutation, invalidate related queries: `queryClient.invalidateQueries({ queryKey: ['users'] })`.
5. **Never use `refetchInterval` for real-time data.** Use WebSockets or Server-Sent Events for real-time. Polling is wasteful.
6. **Never skip `staleTime` configuration.** Default `staleTime: 0` means constant refetching. Set appropriate values.
7. **Never ignore the `gcTime` (formerly cacheTime).** Inactive queries are garbage collected. Ensure `gcTime` > 0 for background data.

## Testing

- Mock queries with `QueryClientProvider` and `setQueryData` for initial states.
- Use MSW (Mock Service Worker) for API mocking in tests.
- Test loading, error, and success states.
- Test query invalidation after mutations.

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

- TanStack Router v1
- React 18+
- TypeScript 5.x
- File-based routing
- Type-safe navigation

## Project Structure
```
src/
├── routes/
│   ├── __root.tsx              // Root layout
│   ├── index.tsx               // Home route
│   ├── about.tsx
│   └── posts.
│       ├── index.tsx
│       └── $postId.tsx         // Dynamic route
├── components/
└── main.tsx
```

## Architecture Rules

- **100% type-safe.** Routes, params, search params all typed.
- **File-based routing.** `routes/` directory structure becomes URLs.
- **Code splitting automatic.** Each route is a separate chunk.
- **Search params validation.** Schema validation for query strings.

## Coding Conventions

- Config: `const routeTree = rootRoute.addChildren([indexRoute, aboutRoute]); const router = createRouter({ routeTree })`.
- Route: `export const Route = createFileRoute('/about')({ component: About })`.
- Params: `const { postId } = Route.useParams()` fully typed.
- Search: `const search = Route.useSearch()` with schema validation.
- Link: `<Link to="/about" search={{ page: 1 }}>About</Link>`.

## NEVER DO THIS

1. **Never use without the Router Devtools.** Essential for debugging.
2. **Never skip the search params schema.** `validateSearch: z.object({...})`.
3. **Never forget the `__root.tsx`.** Required for root layout.
4. **Never mix with React Router carelessly.** Migration possible but careful.
5. **Never ignore the `beforeLoad` hook.** For authentication, data loading.
6. **Never forget `loader` for data fetching.** Replaces route-level data loading.
7. **Never use `useSearch` without schema.** Type safety requires validation.

## Testing

- Test with `@tanstack/react-router` testing utilities.
- Test type safety with `tsc --noEmit`.
- Test navigation with router history.

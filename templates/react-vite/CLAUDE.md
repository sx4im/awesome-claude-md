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

- React 18 with TypeScript (strict mode)
- Vite 5.x as build tool and dev server
- TanStack Query v5 for server state
- Zustand for client state
- Tailwind CSS 3.x
- React Router v6 for routing

## Project Structure

```
src/
├── components/
│   ├── ui/               # Primitives: Button, Input, Modal, Tooltip
│   └── features/         # Domain components: UserCard, OrderSummary
├── hooks/                # Custom hooks (useAuth, useDebounce, useMediaQuery)
├── pages/                # Route-level components, one per route
├── stores/               # Zustand stores, one file per store
├── services/             # API call functions (never call fetch in components)
├── types/                # Shared TypeScript interfaces and types
├── utils/                # Pure utility functions (formatDate, cn, etc.)
└── main.tsx              # App entry point: router and providers
```

## Architecture Rules

- **One component per file.** A file named `UserCard.tsx` exports one component: `UserCard`. Co-locate its types at the top of the same file. don't create a separate types file per component.
- **State management decision tree:**
  - UI-only state (open/closed, form input) → `useState` or `useReducer`
  - Server state (data from APIs) → TanStack Query. never Zustand
  - Cross-component client state (theme, sidebar, auth) → Zustand
  - URL state (filters, pagination) → React Router search params
- **API calls go in `services/`.** Never call `fetch` directly in a component or hook. Each service file maps to a backend domain: `services/users.ts`, `services/orders.ts`. These functions return typed data, never raw `Response` objects.
- **Hooks always return objects.** `return { data, isLoading, error }`. not arrays. The only exception is a two-element tuple by design (like `useState`).

## Coding Conventions

- All function components use the `function` keyword: `export function UserCard()`. not `const UserCard = () => {}`. Arrow functions are for inline callbacks only.
- Explicit return types on **all** exported functions. Internal helpers can rely on inference.
- Import order (enforced by ESLint): React → external packages → `@/` aliased imports → relative imports → type-only imports.
- Use the `@/` path alias mapped to `src/`. Configured in `vite.config.ts` and `tsconfig.json`. Never use `../../../` chains.
- Boolean props: prefix with `is`, `has`, `should`, or `can`: `isDisabled`, `hasError`, `shouldAnimate`.
- Event handler props: prefix with `on`: `onClick`, `onSubmit`, `onFilterChange`.

## Library Preferences

- **State management:** Zustand. not Redux (too much boilerplate for client state) and not Jotai (atomic model is overkill for most SPAs). Zustand's `create` + selectors pattern is the right complexity.
- **Data fetching:** TanStack Query. not SWR (weaker mutation support, no devtools persistence). Use `queryKey` factories: `userKeys.detail(id)`, `userKeys.list(filters)`.
- **Styling:** Tailwind CSS with `clsx` + `tailwind-merge` wrapped in a `cn()` utility. Not CSS modules. co-locating styles in JSX is faster to iterate.
- **Forms:** `react-hook-form` with `zod` resolver. Not Formik. it re-renders the entire form tree.
- **Dates:** `date-fns`. not `moment` (deprecated, not tree-shakeable).
- **HTTP client:** `ky` or plain `fetch` with a typed wrapper. Not `axios`. ky is smaller and fetch-native.

## File Naming

- Components: `PascalCase.tsx` → `UserCard.tsx`, `OrderSummary.tsx`
- Hooks: `useCamelCase.ts` → `useAuth.ts`, `useDebounce.ts`
- Stores: `camelCase.store.ts` → `auth.store.ts`, `ui.store.ts`
- Services: `camelCase.ts` → `users.ts`, `orders.ts`
- Utils: `camelCase.ts` → `formatDate.ts`, `cn.ts`
- Types: `camelCase.ts` → `user.ts`, `order.ts`
- Test files: co-located as `ComponentName.test.tsx`

## NEVER DO THIS

1. **Never use Redux.** Zustand handles client state. TanStack Query handles server state. There is no use case for Redux in this project.
2. **Never use `useEffect` for derived state.** If a value can be computed from existing state or props, compute it during render: `const fullName = \`${firstName} ${lastName}\``. Not `useEffect(() => setFullName(...))`.
3. **Never mutate state directly.** Zustand's `set()` returns a new state reference. TanStack Query's cache is immutable. If you're using spread operators to update nested objects, consider `immer` middleware in Zustand.
4. **Never use `index` as `key` in dynamic lists.** If items can be added, removed, or reordered, use a stable unique ID. Index keys cause bugs with input focus, animations, and reconciliation.
5. **Never import from barrel files that re-export everything.** `import { Button } from '@/components'` breaks tree-shaking and creates circular dependency chains. Import directly: `import { Button } from '@/components/ui/Button'`.
6. **Never use `any`.** Use `unknown` + type guards for truly unknown data. Use generics for flexible types. `any` disables the type checker. it's always wrong.
7. **Never use class components.** Function components with hooks only. No `componentDidMount`, no `this.state`.

## Testing

- Use Vitest + React Testing Library. Tests live next to the component: `UserCard.test.tsx` alongside `UserCard.tsx`.
- Test behavior, not implementation: click buttons, check rendered text, verify API calls. never test `useState` internal values.
- Mock API calls at the service layer using `vi.mock('./services/users')`.
- Use `msw` (Mock Service Worker) for integration tests that need realistic request/response flows.

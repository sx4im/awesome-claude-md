# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

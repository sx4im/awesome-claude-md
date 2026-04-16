# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Zustand v4 (minimal state management)
- React 18+
- TypeScript 5.x
- Immer (optional, for immutable updates)
- Persist middleware (optional)

## Project Structure

```
src/
├── stores/
│   ├── index.ts                # Store exports
│   ├── auth-store.ts           # Authentication state
│   ├── ui-store.ts             # UI state (modals, theme)
│   └── cart-store.ts           # Domain-specific stores
├── hooks/
│   └── useStore.ts             # Store hydration helpers
└── types/
    └── store.ts                # Store type definitions
```

## Architecture Rules

- **One store per domain.** Auth store, UI store, Cart store. Not one giant global store.
- **Selectors for granular subscriptions.** Use selector functions to subscribe to only needed state slices.
- **Actions in the store.** Define state-modifying functions within the store, not external functions.
- **Immer for complex updates.** Use `immer` middleware for nested object updates without spreading.

## Coding Conventions

- Create store: `const useStore = create<StoreState>()((set, get) => ({ ... }))`.
- Use selectors: `const count = useStore((state) => state.count)` not `const { count } = useStore()`.
- Define actions: `increment: () => set((state) => ({ count: state.count + 1 }))`.
- For async: `fetchUser: async (id) => { const user = await api.getUser(id); set({ user }) }`.
- Type the store: `interface StoreState { count: number; increment: () => void }`.

## Library Preferences

- **Immer:** `import { immer } from 'zustand/middleware/immer'` for mutable-like updates.
- **Persistence:** `import { persist } from 'zustand/middleware'` for localStorage sync.
- **DevTools:** `import { devtools } from 'zustand/middleware'` for Redux DevTools integration.
- **Shallow:** `import { shallow } from 'zustand/shallow'` for comparing multiple state picks.

## File Naming

- Store files: `[domain]-store.ts` → `auth-store.ts`, `ui-store.ts`
- Index barrel: `stores/index.ts` exports all stores.

## NEVER DO THIS

1. **Never subscribe to entire store.** `const state = useStore()` re-renders on every state change. Always use selectors.
2. **Never mutate state without Immer.** `state.count++` doesn't work without Immer middleware. Use `set()` properly.
3. **Never create stores inside components.** Stores are singletons. Define them at module level.
4. **Never ignore TypeScript types.** Zustand works without types but you'll lose autocompletion and safety.
5. **Never mix Zustand with Context for the same state.** Pick one per domain.
6. **Never forget to handle hydration.** SSR with Zustand requires `useEffect` for client-only stores.
7. **Never use Zustand for server state.** Use TanStack Query for API data. Zustand is for client state only.

## Testing

- Test store logic independently of components. Stores are pure functions.
- Use `act()` from React Testing Library for state updates in tests.
- Mock stores by replacing the implementation in test setup.
- Test persistence middleware by mocking localStorage.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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


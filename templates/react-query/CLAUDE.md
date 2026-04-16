# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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


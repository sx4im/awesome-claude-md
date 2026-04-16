# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- SWR v2 (stale-while-revalidate data fetching)
- React 18+
- TypeScript 5.x
- Fetch API or Axios
- React 18+ Suspense support

## Project Structure

```
src/
├── hooks/
│   ├── useUsers.ts             // SWR custom hooks
│   ├── usePosts.ts
│   └── swr-config.ts           // Global SWR config
├── lib/
│   ├── api.ts                  // API client
│   └── fetcher.ts              // Default fetcher function
└── providers/
    └── swr-provider.tsx        // SWRConfig wrapper
```

## Architecture Rules

- **Fetcher function is reusable.** Define a global fetcher that handles auth, base URL, and error parsing.
- **Custom hooks for each endpoint.** `useUsers()`, `useUser(id)` wrap `useSWR` with proper keys and types.
- **Optimistic UI with mutate.** Use `mutate` for immediate updates before API confirmation.
- **Error retry with exponential backoff.** SWR handles this automatically with sensible defaults.

## Coding Conventions

- Global fetcher: `const fetcher = (url: string) => fetch(url).then(r => r.json())`.
- Use SWR: `const { data, error, isLoading } = useSWR('/api/users', fetcher)`.
- Custom hook: `export const useUsers = () => useSWR<User[]>('/api/users', fetcher)`.
- Mutations: `const { trigger } = useSWRMutation('/api/users', createUser)`.
- Revalidate: `mutate('/api/users')` after updates.

## Library Preferences

- **Infinite loading:** `useSWRInfinite` for paginated data.
- **Mutation:** `useSWRMutation` for POST/PUT/DELETE operations.
- **Immutable:** `useSWRImmutable` for data that never changes.
- **Suspense:** Enable `suspense: true` for React Suspense integration.

## File Naming

- Hook files: `use[Resource].ts` → `useUsers.ts`
- Config file: `swr-config.ts` or in providers.
- Fetcher file: `fetcher.ts`

## NEVER DO THIS

1. **Never use SWR keys that aren't unique.** The key determines caching. Collisions cause data mixing.
2. **Never forget to handle errors.** SWR errors don't throw. Check `error` in your UI.
3. **Never use `useSWR` for mutations.** Use `useSWRMutation` for write operations.
4. **Never ignore `isLoading` vs `isValidating`.** `isLoading` is no data yet. `isValidating` is revalidating in background.
5. **Never skip key serialization for complex keys.** Arrays/objects as keys: `useSWR(['/api/user', id])`.
6. **Never use SWR for client-only state.** SWR is for server state. Use Zustand/Jotai for UI state.
7. **Never forget `keepPreviousData` for pagination.** It prevents UI flickering when changing pages.

## Testing

- Mock fetcher in tests. SWR calls your fetcher—mock that function.
- Test loading states by delaying mock responses.
- Test error handling by rejecting the mock fetcher.
- Test mutations by verifying `mutate` is called with correct arguments.


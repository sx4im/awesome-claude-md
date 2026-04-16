# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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


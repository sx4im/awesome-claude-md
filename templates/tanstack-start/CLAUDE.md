# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- TanStack Start 1.x with React 19
- TanStack Router for type-safe file-based routing
- TanStack Query v5 for server state management
- Vinxi as the server runtime (Nitro-based)
- TypeScript 5.4+ in strict mode
- Tailwind CSS 4 with @tailwindcss/vite
- Drizzle ORM with PostgreSQL
- Zod 3 for runtime validation on both client and server
- Better Auth for authentication

## Project Structure

```
app/
  routes/
    __root.tsx          # Root layout with providers
    index.tsx           # Home page route
    _authed/            # Route group requiring authentication
      dashboard.tsx
      settings.tsx
    _public/            # Route group for public pages
    api/                # API routes (server functions)
  components/           # Shared React components
  hooks/                # Custom React hooks
  lib/
    server/             # Server-only utilities (db, auth)
    validators/         # Zod schemas shared client/server
    utils.ts            # Shared utility functions
  styles/
    app.css             # Tailwind CSS entry point
drizzle/
  migrations/           # Database migration files
  schema.ts             # Drizzle table definitions
public/                 # Static assets
```

## Architecture Rules

- Data fetching uses TanStack Router loaders with `createFileRoute`. Every route defines a `loader` that returns typed data via `routeContext` or server functions.
- Server functions created with `createServerFn` are the only way to execute server-side code. They validate inputs with Zod and return typed responses.
- Mutations go through server functions called from `useMutation` hooks (TanStack Query). After mutation, invalidate related query keys.
- Route-level code splitting is automatic via file-based routing. Lazy-load heavy components with `React.lazy()` inside route components only.
- Authentication guards are implemented as `beforeLoad` checks on route groups. Redirect unauthorized users to `/login`.
- All database queries go through Drizzle ORM. Raw SQL is forbidden except in migrations.
- Shared validation schemas in `lib/validators/` are used identically on client forms and server function inputs.

## Coding Conventions

- Route files export a `Route` constant created via `createFileRoute`. Routes define `component`, `loader`, `errorComponent`, and `pendingComponent`.
- Server functions use the naming pattern `$functionName` to visually distinguish them: `$getUser`, `$createPost`.
- Use `useLoaderData()` inside route components to access loader data. Never re-fetch data that the loader already provides.
- Components receive props as typed interfaces. Avoid `React.FC`. Use `function ComponentName(props: Props)` syntax.
- Error boundaries are defined per-route via `errorComponent` and at the root level for uncaught errors.
- Pending states use route-level `pendingComponent` for navigation and `useMutation().isPending` for form submissions.
- Environment variables accessed on the server use `process.env`. Client env vars use Vinxi's `import.meta.env` with `VITE_` prefix.

## Library Preferences

- Forms: @tanstack/react-form with Zod validation (never Formik or react-hook-form)
- State management: TanStack Query for server state, React context + useReducer for client-only UI state
- Tables: @tanstack/react-table v8 for sortable/filterable data grids
- Toasts: sonner for notifications
- Icons: lucide-react (never react-icons bundle)
- Date handling: date-fns (never moment.js)
- Email: React Email for transactional email templates

## File Naming

- Route files: match URL segment (`dashboard.tsx`, `users.$userId.tsx`)
- Components: `PascalCase.tsx`
- Hooks: `useCamelCase.ts`
- Server functions: `camelCase.server.ts`
- Validators: `camelCase.validator.ts`
- Types: `camelCase.types.ts`

## NEVER DO THIS

1. Never use `useEffect` for data fetching. Use TanStack Router loaders for initial data and TanStack Query for dynamic refetching.
2. Never import from `lib/server/` in client-side code. Server-only modules must only be accessed through server functions.
3. Never create API routes for operations that should be server functions. Use `createServerFn` for RPC-style calls.
4. Never store server state in React useState or useReducer. All server state belongs in TanStack Query cache.
5. Never skip Zod validation on server function inputs. Every server function must validate its arguments.
6. Never use string-based route paths for navigation. Use the generated `Route` objects for type-safe `Link` and `navigate` calls.

## Testing

- Unit tests: Vitest with @testing-library/react for component testing.
- Server function tests: Vitest calling server functions directly with mocked database context.
- Run tests with `npm run test` which executes `vitest run`.
- E2E tests: Playwright for critical user flows (auth, CRUD operations, navigation).
- Run e2e with `npm run test:e2e` which executes `playwright test`.
- All server functions must have validation error tests confirming Zod rejects bad input.
- Route loader tests verify correct data shape and authentication redirects.
- CI runs type checking with `tsc --noEmit` before test execution.

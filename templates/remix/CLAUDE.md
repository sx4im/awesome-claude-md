# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- Remix 2.x with React 18
- TypeScript (strict mode)
- Tailwind CSS 3.x
- Prisma + PostgreSQL (or your ORM)
- Deployed on Fly.io, Vercel, or Cloudflare

## Project Structure

```
app/
├── routes/
│   ├── _index.tsx           # Home page (/)
│   ├── _auth.tsx            # Layout route for auth pages
│   ├── _auth.login.tsx      # /login (nested under _auth layout)
│   ├── dashboard.tsx        # Layout route for /dashboard/*
│   ├── dashboard._index.tsx # /dashboard
│   ├── dashboard.settings.tsx
│   └── api.webhooks.stripe.ts  # API resource route (no UI)
├── components/
│   ├── ui/                  # Primitives (Button, Input, Card)
│   └── features/            # Domain (InvoiceRow, UserAvatar)
├── lib/
│   ├── db.server.ts         # Prisma client (server-only)
│   ├── auth.server.ts       # Session, cookie helpers
│   └── utils.ts             # Shared utilities
├── services/                # Domain logic (users.server.ts, billing.server.ts)
├── root.tsx                 # Root layout (html, head, body)
└── entry.server.tsx         # Server entry
```

## Architecture Rules

- **`loader` for reads, `action` for writes.** Every route has a `loader` (GET data) and/or `action` (handle POST/PUT/DELETE). This is Remix's core pattern — respect it. Never fetch data in `useEffect`.
- **Server code uses `.server.ts` suffix.** Files named `*.server.ts` are tree-shaken from the client bundle. Database access, secrets, and server logic must use this suffix. If you import a server file from client code, Remix throws a build error.
- **Progressive enhancement first.** Forms use `<Form>` (or native `<form>`) and work without JavaScript. The `action` handles the POST on the server. `useFetcher` adds client-side enhancements (optimistic UI, loading states) on top.
- **Nested routes = nested layouts.** `dashboard.tsx` is a layout that renders `<Outlet>`. `dashboard.settings.tsx` renders inside it. Use this for persistent sidebars, navs, and shared data loading. Flat routes with `_auth.login.tsx` use layout routes without URL nesting.
- **No client-side state management libraries.** Remix loaders are the state management. URL search params replace most Zustand/Redux patterns. `useFetcher` replaces TanStack Query. Only use Zustand for truly ephemeral client-side state (modals, tooltips).

## Coding Conventions

- Named exports for `loader`, `action`, and `meta`. Default export for the route component. This is Remix convention — don't fight it.
- Use `invariant(condition, message)` (from `tiny-invariant`) to assert preconditions in loaders and actions instead of long `if (!thing) throw` chains.
- Return typed responses from loaders using `json()` helper or direct Response objects. Use `typedjson` if you need Date serialization.
- Form validation: validate in the `action`, return errors with `json({ errors }, { status: 400 })`, display with `useActionData()`. Not client-side-only validation.
- Error boundaries: export `ErrorBoundary` from route files to catch errors per-route. The root `ErrorBoundary` in `root.tsx` catches everything else.

## Library Preferences

- **Forms:** Remix's built-in `<Form>` + `conform` or `remix-validated-form` for complex forms with Zod validation. Not `react-hook-form` — it fights Remix's server-first model.
- **Auth:** `remix-auth` strategies. Cookie-based sessions via `createCookieSessionStorage`. Not JWT in cookies — Remix's session API handles secure, httpOnly cookies natively.
- **Styling:** Tailwind CSS — works perfectly since Remix handles CSS imports. Not CSS-in-JS (it conflicts with Remix's streaming SSR).
- **ORM:** Prisma with `.server.ts` files — not Drizzle yet (Prisma has better Remix ecosystem support). Knex for raw SQL if needed.

## NEVER DO THIS

1. **Never fetch data in `useEffect`.** Use `loader` functions. They run on the server, avoid waterfalls, and send data with the initial HTML. Client-side fetching defeats Remix's entire architecture.
2. **Never import `.server.ts` files from client code.** It won't build. If you need shared types, put them in a plain `.ts` file. Business logic and database access stay in `.server.ts`.
3. **Never use `useState` for URL-derived state.** Filters, pagination, sort order — these are URL search params. Use `useSearchParams()`. URL state survives refresh, is shareable, and works with back/forward.
4. **Never return raw Prisma models from loaders.** Map to plain objects. Prisma models can contain `Date` objects and BigInt that don't serialize cleanly across the network boundary.
5. **Never skip error boundaries.** Every route that loads data should export an `ErrorBoundary`. Without it, a database error crashes the entire page instead of just the failing section.
6. **Never use `redirect()` inside a `try/catch` without re-throwing.** Remix's `redirect()` throws a Response — if you catch it, the redirect silently fails. Catch specific errors, not everything.
7. **Never put `<Scripts>` conditionally in `root.tsx`.** Remix needs the script tag to hydrate. Removing it breaks all client-side navigation. If you want a no-JS page, make it a separate resource route.

## Testing

- Use Vitest for unit tests. Test loader and action functions by calling them with mock Request objects.
- Use Playwright for E2E tests. Test the full server-rendered flow including form submissions.
- Test progressive enhancement: verify forms work with JavaScript disabled, then test enhanced UX with JS enabled.
- Mock Prisma in loader/action tests with `vitest-mock-extended`.

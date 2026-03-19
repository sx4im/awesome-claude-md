# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Next.js 14+ (App Router)
- TypeScript (strict mode)
- Supabase (Auth, Database, Storage, Realtime)
- Tailwind CSS 3.x
- Supabase client SDK + Server SDK
- Deployed on Vercel

## Project Structure

```
src/
├── app/
│   ├── (app)/               # Authenticated routes
│   ├── (marketing)/         # Public pages
│   ├── auth/
│   │   ├── callback/        # OAuth callback route
│   │   └── confirm/         # Email confirmation route
│   ├── api/                 # Webhooks only
│   └── layout.tsx
├── components/
│   ├── ui/
│   └── features/
├── lib/
│   ├── supabase/
│   │   ├── client.ts        # Browser Supabase client (createBrowserClient)
│   │   ├── server.ts        # Server Supabase client (createServerClient)
│   │   └── middleware.ts     # Auth session refresh in middleware
│   └── utils.ts
├── hooks/
│   └── useSupabase.ts       # Typed hooks for Supabase operations
├── types/
│   └── database.ts          # Generated types from `supabase gen types`
└── middleware.ts             # Session refresh + route protection
```

## Architecture Rules

- **Two Supabase clients, never mix them.** `createBrowserClient()` for client components. `createServerClient()` for server components, server actions, and route handlers. They handle auth cookies differently. using the wrong one leaks sessions or breaks auth.
- **Generate database types, don't write them.** Run `supabase gen types typescript --project-id <id> > types/database.ts` after every migration. Import `Database` type and pass it as generic: `createServerClient<Database>(...)`. Never manually define table types.
- **Middleware refreshes the session on every request.** Supabase Auth uses short-lived JWTs. The middleware in `middleware.ts` calls `supabase.auth.getUser()` to refresh the token. Without this, users get logged out arbitrarily.
- **Row Level Security (RLS) is mandatory.** Every table has RLS enabled. Policies define who can read, insert, update, delete. Never rely on application-level auth checks alone. RLS is the database-level safety net.
- **Server components for reads, server actions for writes.** Fetch data in server components using the server client. Mutations go through server actions that use the server client. Never mutate data from the browser client without RLS protecting the mutation.

## Coding Conventions

- Supabase queries are typed: `supabase.from('users').select('id, name, email')` returns typed data when `Database` generic is set. Never use `any` on query results.
- Error handling: always check `.error` on Supabase responses. `const { data, error } = await supabase.from('users').select()`. Never destructure only `data` and ignore `error`.
- Auth state: use `supabase.auth.getUser()` (server-side, contacts Supabase). not `supabase.auth.getSession()` (reads from cookie, can be stale). Use `getSession` only for fast UI checks where a stale session is acceptable.
- Realtime subscriptions go in client components with `useEffect`. Unsubscribe on cleanup: `return () => { channel.unsubscribe() }`. Never leave dangling subscriptions.
- Storage file paths: `{userId}/{filename}` pattern. RLS policies on storage buckets should match this pattern so users can only access their own files.

## Library Preferences

- **Auth:** Supabase Auth. built-in, handles OAuth, magic links, email/password. Not NextAuth (redundant when using Supabase).
- **Database:** Supabase PostgreSQL with generated types. not Prisma (Supabase's client SDK provides typed queries without a separate ORM, and RLS works at the database level).
- **Realtime:** Supabase Realtime channels. not Pusher or Socket.io (included in Supabase, no extra service).
- **File storage:** Supabase Storage with signed URLs for private files. not S3 directly (Supabase Storage wraps S3 with auth-aware policies).
- **Edge functions:** Supabase Edge Functions (Deno) for webhooks or background processing that doesn't fit in Next.js.

## NEVER DO THIS

1. **Never use `createBrowserClient` in server components.** It doesn't have access to cookies and will create an unauthenticated client. Use `createServerClient` on the server.
2. **Never skip RLS.** A table without RLS policies is accessible to anyone with the `anon` key. Even "admin-only" tables need explicit RLS policies.
3. **Never trust `getSession()` for security checks.** The session cookie can be tampered with. Use `getUser()` for any security-critical check. it contacts Supabase's auth server.
4. **Never hardcode the Supabase service role key in client code.** The `SUPABASE_SERVICE_ROLE_KEY` bypasses RLS. It must only exist in server-side code and environment variables.
5. **Never write database types manually.** Run `supabase gen types typescript` and import the generated types. Manual types drift from the real schema and cause runtime errors.
6. **Never skip the middleware session refresh.** Without it, Supabase's JWT expires and `getUser()` starts returning errors even for logged-in users. The middleware handles silent refresh.
7. **Never store user data without a foreign key to `auth.users`.** Every user-owned table references `auth.users(id)`. RLS policies use `auth.uid()` to scope access. Without the FK, you can't write RLS policies.

## Testing

- Use Vitest for unit tests. Mock the Supabase client with typed mocks.
- Use Supabase CLI's local development (`supabase start`) for integration tests against a real local PostgreSQL + Auth + Storage.
- Test RLS policies independently with SQL: set role, attempt query, assert result.
- E2E with Playwright. test auth flows (sign up, login, OAuth callback, logout).

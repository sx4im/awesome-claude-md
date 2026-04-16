# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Supabase Auth (GoTrue-based)
- Next.js/React/Any framework
- TypeScript 5.x
- PostgreSQL Row Level Security
- Magic links, OAuth, passwords

## Project Structure
```
src/
├── lib/
│   └── supabase.ts             # Supabase clients (server/browser)
├── app/
│   ├── auth/
│   │   └── callback/
│   │       └── route.ts        # OAuth callback
│   └── (auth)/
│       └── login/
│           └── page.tsx
├── components/
│   └── auth/
│       └── auth-form.tsx
└── middleware.ts               # Session refresh
```

## Architecture Rules

- **Two Supabase clients.** Server client (with service role) and browser client (with user session).
- **PKCE OAuth flow.** Secure OAuth with code challenge.
- **RLS for authorization.** Row Level Security policies in PostgreSQL.
- **Server Components get user via cookies.** Middleware refreshes session.

## Coding Conventions

- Server client: `createServerClient(cookies())` with `cookie-store` from `next/headers`.
- Browser client: `createBrowserClient(supabaseUrl, supabaseAnonKey)`.
- Sign in: `supabase.auth.signInWithPassword({ email, password })`.
- Sign up: `supabase.auth.signUp({ email, password, options: { emailRedirectTo: '...' } })`.
- OAuth: `supabase.auth.signInWithOAuth({ provider: 'github', options: { redirectTo: '...' } })`.
- Get user (server): `const { data: { user } } = await supabase.auth.getUser()`.
- RLS policy: `create policy "Users can read own data" on users for select using (auth.uid() = id)`.

## NEVER DO THIS

1. **Never expose service role key client-side.** `SUPABASE_SERVICE_ROLE` is server-only.
2. **Never disable RLS for convenience.** It's your authorization layer.
3. **Never forget to handle auth state changes.** Subscribe to `onAuthStateChange` on client.
4. **Never skip the callback route for OAuth.** Must exchange code for session.
5. **Never ignore email confirmation settings.** Configure in Supabase dashboard.
6. **Never use `supabase.auth.getSession()` for server-side auth.** Use `getUser()` instead.
7. **Never forget to refresh sessions in middleware.** Prevents expired session issues.

## Testing

- Test RLS policies with different user contexts.
- Test OAuth flows end-to-end.
- Test session refresh behavior.


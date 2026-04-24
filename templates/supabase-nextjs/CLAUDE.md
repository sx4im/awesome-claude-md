# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Full-Stack)

### Release Discipline
- Maintain contract consistency across UI, API, DB schema, and background jobs.
- Ship schema changes with backward-compatible rollout and rollback notes.
- Guard critical business flows with idempotency and retry safety.

### Merge/Release Gates
- API contract checks, migration checks, and e2e smoke tests pass.
- Auth and billing-critical paths validated explicitly.
- No breaking change without migration path and versioning note.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

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

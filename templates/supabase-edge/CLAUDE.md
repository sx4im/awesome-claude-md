# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Runtime: Deno (Supabase Edge Functions run on Deno Deploy infrastructure)
- Database: Supabase PostgreSQL accessed via PostgREST and supabase-js client
- Auth: Supabase Auth (GoTrue) with JWT verification
- Storage: Supabase Storage for file uploads
- Realtime: Supabase Realtime for WebSocket-based subscriptions
- CLI: Supabase CLI (`supabase`) for local dev and deployment
- Language: TypeScript (Deno-native, no build step)
- Testing: Deno built-in test runner

## Project Structure

```
supabase/
  functions/
    process-webhook/
      index.ts          # Webhook processing edge function
    send-email/
      index.ts          # Email sending edge function
    generate-report/
      index.ts          # Report generation edge function
    _shared/
      supabase.ts       # Supabase client factory (service role and anon)
      cors.ts           # CORS headers for browser requests
      auth.ts           # JWT extraction and user verification
      types.ts          # Shared type definitions
      validation.ts     # Zod schemas for request validation
  migrations/
    20240101000000_initial.sql
  seed.sql              # Seed data for local development
  config.toml           # Supabase local dev configuration
.env.local              # Local secrets (SUPABASE_SERVICE_ROLE_KEY, etc.)
```

## Architecture Rules

- Each edge function lives in its own directory under `supabase/functions/` with an `index.ts` entry point.
- Shared code goes in `supabase/functions/_shared/` -- the underscore prefix prevents it from being deployed as a function.
- Create two Supabase clients: one with `SUPABASE_SERVICE_ROLE_KEY` for admin operations, one with the user's JWT for RLS-respecting queries.
- Always verify the user's JWT from the `Authorization` header before processing requests. Use `supabase.auth.getUser(token)`.
- Database access prefers the supabase-js query builder over raw SQL. Use `supabase.from('table').select()`.
- Edge functions have a 150-second wall-clock limit and 50ms CPU time per request.
- Return proper CORS headers for every response when the function is called from a browser.

## Coding Conventions

- Edge function entry pattern: `Deno.serve(async (req) => { ... })` at the top of `index.ts`.
- Extract the bearer token: `const token = req.headers.get('Authorization')?.replace('Bearer ', '')`.
- Use the shared CORS helper for preflight: check `req.method === 'OPTIONS'` and return CORS headers immediately.
- Create the Supabase client per-request to pass the user's JWT: `createClient(url, anonKey, { global: { headers: { Authorization: req.headers.get('Authorization')! } } })`.
- Response format: `new Response(JSON.stringify({ data }), { status: 200, headers: { 'Content-Type': 'application/json', ...corsHeaders } })`.
- Use `Deno.env.get('SUPABASE_URL')` and `Deno.env.get('SUPABASE_ANON_KEY')` -- these are injected automatically.

## Library Preferences

- Database client: @supabase/supabase-js via esm.sh or npm: specifier
- Validation: Zod (lightweight, works well in Deno)
- Email: Resend API via fetch (no heavy SDK needed)
- Payments: Stripe API via fetch with typed request/response
- JWT decoding: djwt from deno.land/x for manual JWT inspection when needed
- No ORM: use supabase-js query builder which maps directly to PostgREST

## File Naming

- Function directories: kebab-case (`process-webhook/`, `send-email/`)
- Entry point: always `index.ts` inside each function directory
- Shared modules: camelCase in `_shared/` (`supabase.ts`, `cors.ts`)
- Migration files: timestamp prefix (`20240101000000_create_users.sql`)
- Test files: `*.test.ts` inside function directories

## NEVER DO THIS

1. Never import from `_shared/` using relative paths that go outside `supabase/functions/` -- Deno Deploy cannot resolve them.
2. Never use the service role key in client-side code or return it in responses -- it bypasses all Row Level Security.
3. Never skip CORS headers -- browser-based clients will fail silently without proper `Access-Control-Allow-Origin`.
4. Never use `supabase.auth.signUp()` or `supabase.auth.signIn()` inside edge functions -- those are client-side auth flows.
5. Never deploy with secrets in `config.toml` -- use `supabase secrets set KEY=VALUE` for production secrets.
6. Never bypass RLS by using the service role client for user-facing queries -- use the anon key with the user's JWT.

## Testing

- Use `deno test --allow-net --allow-env` for running tests locally.
- Test edge functions by importing the handler and passing constructed `Request` objects.
- Use `supabase start` to run a local Supabase stack (Postgres, Auth, Storage, PostgREST) via Docker.
- Local development: `supabase functions serve` watches for changes and restarts functions.
- Test PostgREST queries against the local Supabase instance at `http://localhost:54321`.
- Mock Supabase client responses for unit tests; use the local stack for integration tests.
- Verify RLS policies by testing queries with different user JWTs (admin vs regular user).
- Run `supabase db reset` to apply migrations and seed data before integration test runs.
- Test CORS by sending requests with `Origin` header and verifying `Access-Control-Allow-Origin` in response.

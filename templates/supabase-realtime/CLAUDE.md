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

- Supabase with PostgreSQL 15+ as the underlying database
- Supabase Realtime for WebSocket-based channels, presence tracking, and broadcast
- Supabase JS Client v2 (@supabase/supabase-js) for frontend integration
- React 18+ with @supabase/auth-helpers-react for authentication context
- Next.js 14 App Router for the web application framework
- Row Level Security (RLS) policies for all table access control
- Supabase Edge Functions (Deno) for server-side logic

## Project Structure

```
app/
  (auth)/
    login/page.tsx
    signup/page.tsx
  (dashboard)/
    layout.tsx              # Realtime provider wrapper
    chat/
      page.tsx              # Chat room with presence
      components/
        message-list.tsx    # Realtime message subscription
        presence-bar.tsx    # Online users indicator
        typing-indicator.tsx
    collaborate/
      page.tsx              # Collaborative document editing
      components/
        cursor-overlay.tsx  # Broadcast-based cursor sharing
lib/
  supabase/
    client.ts              # Browser Supabase client singleton
    server.ts              # Server-side Supabase client (cookies)
    middleware.ts           # Auth session refresh middleware
    realtime/
      channels.ts          # Channel name builders and subscriptions
      presence.ts          # Presence state management hooks
      broadcast.ts         # Broadcast event helpers
  hooks/
    use-realtime-query.ts  # Hook combining initial fetch + realtime sync
    use-presence.ts        # Presence tracking hook
    use-broadcast.ts       # Broadcast send/receive hook
    use-channel.ts         # Channel lifecycle management
supabase/
  migrations/
    20240101000000_create_messages.sql
    20240102000000_add_rls_policies.sql
    20240103000000_enable_realtime.sql
  functions/
    notify-users/
      index.ts             # Edge Function for push notifications
  config.toml              # Local dev configuration
  seed.sql
```

## Architecture Rules

- Enable Realtime on specific tables via `alter publication supabase_realtime add table messages`. Never enable Realtime on all tables; it creates unnecessary WAL processing overhead.
- Use Channels for application-level messaging (chat, notifications). Use Postgres Changes for database-driven updates (new records, updates). Use Broadcast for ephemeral data (cursor positions, typing indicators).
- Every table accessed by Realtime must have Row Level Security enabled with at least one policy. Realtime respects RLS policies; unauthorized users will not receive change events.
- Create a single Supabase client instance per environment (browser, server). Use `createBrowserClient()` for client components and `createServerClient()` for server components and middleware.
- Channel names follow the pattern `{resource}:{identifier}`, e.g., `room:abc123`, `document:doc456`. Never use user-specific data in channel names for shared channels.
- Presence state must be lightweight. Track only `user_id`, `display_name`, and `online_at`. Never put large objects in presence state; it is synced to every connected client.

## Coding Conventions

- Subscribe to Realtime channels in a `useEffect` cleanup pattern. Always call `supabase.removeChannel(channel)` in the cleanup function to prevent memory leaks.
- Use the `useRealtimeQuery` custom hook that combines an initial `supabase.from('table').select()` with a `.on('postgres_changes', ...)` subscription. The hook merges incoming events into local state.
- Handle Realtime connection states explicitly: `SUBSCRIBED`, `TIMED_OUT`, `CLOSED`, `CHANNEL_ERROR`. Show a reconnecting indicator to users on `TIMED_OUT`.
- Broadcast messages must include a `type` field for event discrimination: `{ type: 'cursor_move', payload: { x, y, userId } }`.
- Use `channel.track()` for presence and `channel.send()` for broadcast. These are distinct APIs; do not mix their use cases.
- Debounce high-frequency broadcasts (cursor movement, typing) to a maximum of 10 events per second per client using `lodash.throttle`.

## Library Preferences

- @supabase/supabase-js v2 over raw WebSocket connections to Realtime
- @supabase/auth-helpers-nextjs for Next.js App Router integration
- Zustand over Redux for client-side state management alongside Realtime
- Supabase Edge Functions over Next.js API routes for database triggers and webhooks
- PostgreSQL functions over Edge Functions for data validation logic that runs on insert/update
- Supabase CLI for local development, migrations, and type generation

## File Naming

- React components use PascalCase: `MessageList.tsx`, `PresenceBar.tsx`
- Hooks use camelCase with `use` prefix: `use-realtime-query.ts`, `use-presence.ts`
- Supabase lib files use kebab-case: `client.ts`, `channels.ts`
- Migration files use timestamp prefix: `20240101000000_description.sql`
- Edge Functions use kebab-case directory names: `notify-users/index.ts`

## NEVER DO THIS

1. Never subscribe to Postgres Changes without RLS policies on the table. Without RLS, any authenticated user receives all row changes regardless of authorization.
2. Never use Realtime Postgres Changes for high-throughput tables (more than 100 writes/second). Use Broadcast for high-frequency data and sync from the database on a polling interval.
3. Never store the Supabase service_role key in client-side code. The service_role key bypasses RLS. Use the anon key for browser clients and service_role only in Edge Functions.
4. Never create a new Supabase client on every render. Instantiate once in a module-level singleton or context provider, and reuse it across the application.
5. Never send sensitive data through Broadcast channels. Broadcast messages are distributed to all channel subscribers without server-side filtering; use Postgres Changes with RLS for access-controlled data.
6. Never use `supabase.realtime.setAuth()` with a hardcoded JWT. Use the session token from `supabase.auth.getSession()` which auto-refreshes.
7. Never forget to run `supabase gen types typescript` after migration changes. Stale types cause runtime errors when accessing new or renamed columns.

## Testing

- Test Realtime subscriptions using Supabase local development (`supabase start`) which includes a local Realtime server. Insert data via SQL and verify the client receives the change event.
- Test presence by connecting two clients to the same channel, tracking state on both, and asserting that each client sees the other in the presence state via `channel.presenceState()`.
- Test Broadcast by sending an event from one client and asserting the other client receives it within 1 second.
- Test RLS policies independently using `supabase.auth.signIn()` with different test users and verifying that Postgres Changes events are filtered correctly per user.
- Unit test custom hooks with React Testing Library and a mocked Supabase client that simulates channel events via `jest.fn()` callbacks.
- Test Edge Functions locally using `supabase functions serve` and sending HTTP requests with `curl` or a test client. Assert response codes and database side effects.

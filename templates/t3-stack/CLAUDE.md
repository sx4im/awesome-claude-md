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
- tRPC v11 for end-to-end type-safe API
- Prisma ORM + PostgreSQL
- NextAuth.js (Auth.js) for authentication
- Tailwind CSS 3.x
- TypeScript (strict mode)
- Deployed on Vercel

## Project Structure

```
src/
├── app/
│   ├── (app)/               # Authenticated routes
│   ├── (marketing)/         # Public pages
│   ├── api/
│   │   └── trpc/[trpc]/     # tRPC HTTP handler
│   └── layout.tsx
├── server/
│   ├── api/
│   │   ├── routers/         # tRPC routers (one per domain)
│   │   │   ├── user.ts
│   │   │   ├── post.ts
│   │   │   └── _app.ts      # Root router (merges all routers)
│   │   ├── trpc.ts          # tRPC instance, context, middleware
│   │   └── root.ts          # Export type: AppRouter
│   └── db.ts                # Prisma client singleton
├── lib/
│   ├── trpc/
│   │   ├── client.ts        # Client-side tRPC hooks
│   │   └── server.ts        # Server-side tRPC caller
│   └── auth.ts              # NextAuth config + helpers
├── components/
│   ├── ui/
│   └── features/
└── types/
```

## Architecture Rules

- **tRPC replaces REST API routes.** Every data operation goes through tRPC procedures. Never create `app/api/` route handlers for internal data. tRPC gives you type safety from database to component.
- **One router per domain.** `server/api/routers/user.ts` handles all user-related procedures. Routers are merged in `_app.ts`. Never put unrelated procedures in the same router.
- **Server-side tRPC calls in server components.** Use the server-side caller (`lib/trpc/server.ts`) in server components and server actions. Use tRPC hooks (`api.user.getById.useQuery()`) in client components.
- **Zod for all input validation.** Every tRPC procedure defines its input with a Zod schema: `.input(z.object({ id: z.string() }))`. Never accept unvalidated input.
- **Middleware for cross-cutting concerns.** Define `protectedProcedure` (requires auth), `adminProcedure` (requires admin role) as reusable middleware chains. Never check auth inside individual procedure handlers.

## Coding Conventions

- **tRPC procedure naming:** `router.{entity}.{action}` → `api.user.getById`, `api.post.create`, `api.post.list`. Verb matches the operation.
- **Prisma queries live in tRPC procedures.** Not in a separate service layer. tRPC procedures ARE the service layer in T3. Keep them focused: one procedure, one query.
- **Type inference, not manual types.** Use `RouterOutputs['user']['getById']` to infer return types. Never manually define types that duplicate what tRPC infers from Prisma.
- **Error handling:** throw `TRPCError` with specific codes: `NOT_FOUND`, `UNAUTHORIZED`, `BAD_REQUEST`, `FORBIDDEN`. Never return error objects in the success path.
- **React Query integration:** tRPC wraps TanStack Query. Use `useQuery` for reads, `useMutation` for writes, `utils.user.getById.invalidate()` after mutations.

## Library Preferences

- **API layer:** tRPC. not REST routes (tRPC gives end-to-end type safety), not GraphQL (overkill for most T3 apps).
- **Auth:** NextAuth.js (Auth.js). handles OAuth providers, sessions, and database adapters. Not Clerk (adds a third-party dependency). Not custom JWT (session-based is simpler).
- **Validation:** Zod. integrated into tRPC's input validation. Also used for env var validation in `env.mjs`.
- **Database:** Prisma. the T3 default. TypeSafe with tRPC inference. Not Drizzle (Prisma has deeper T3 ecosystem integration).
- **Environment validation:** `@t3-oss/env-nextjs` with Zod schemas. Type-safe env vars at build time.

## NEVER DO THIS

1. **Never create REST API routes for internal data.** That's what tRPC is for. `app/api/` routes are only for webhooks and third-party integrations that can't use tRPC.
2. **Never manually type tRPC outputs.** Use `RouterOutputs` inference. Manual types drift from the actual Prisma schema and break silently.
3. **Never skip input validation on tRPC procedures.** Every `mutation` and `query` that accepts arguments must have `.input(zodSchema)`. Unvalidated input is a security hole even with TypeScript.
4. **Never call tRPC hooks in server components.** Use the server-side caller. tRPC hooks (`useQuery`) require a React Query provider which only exists in client components.
5. **Never put auth checks inside individual procedures when middleware works.** Define `protectedProcedure` once and use it everywhere. Duplicating `if (!ctx.session) throw` in every procedure is fragile.
6. **Never import from `server/` in client code.** Server routers, database clients, and auth secrets must never reach the browser. tRPC's client hooks are the only bridge.
7. **Never use `any` in Zod schemas.** `z.any()` defeats the purpose of type-safe input validation. Define specific schemas for every field.

## Testing

- Test tRPC procedures by calling them directly with a mock context (providing session and database).
- Use Vitest for unit tests on procedures and utilities.
- E2E with Playwright. test the full stack from UI to database.
- Test protected procedures with both authenticated and unauthenticated contexts to verify middleware.

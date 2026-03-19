# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

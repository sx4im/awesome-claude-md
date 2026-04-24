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

## Production Delivery Playbook (Category: Backend)

### Release Discipline
- Fail closed on authz/authn checks and input validation.
- Use explicit timeouts/retries/circuit-breaking for external dependencies.
- Preserve API compatibility unless breaking change is approved and documented.

### Merge/Release Gates
- Unit + integration tests and contract tests pass.
- Static checks pass and critical endpoint latency regressions reviewed.
- Structured error handling verified for all modified endpoints.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- tRPC v11 (standalone server, not embedded in Next.js/T3)
- TypeScript (strict mode)
- Zod for input/output validation
- [EXPRESS/FASTIFY/NODE_HTTP] as the HTTP adapter
- [PRISMA/DRIZZLE] for database access
- SuperJSON for data serialization (dates, Maps, Sets)
- WebSocket adapter for subscriptions (if needed)

## Project Structure

```
src/
├── server.ts                  # HTTP server bootstrap, tRPC adapter mount
├── trpc/
│   ├── index.ts               # tRPC initialization: initTRPC, transformer
│   ├── context.ts             # Context factory: request -> { db, user, ... }
│   ├── middleware.ts          # Reusable middleware: isAuthed, hasRole, rateLimit
│   └── router.ts             # Root appRouter merging all sub-routers
├── routers/                   # Domain-specific routers
│   ├── user.router.ts         # user.list, user.byId, user.create, user.update
│   ├── post.router.ts         # post.list, post.create, post.publish
│   └── auth.router.ts         # auth.login, auth.register, auth.refresh
├── services/                  # Business logic (database queries, external APIs)
│   ├── user.service.ts
│   └── post.service.ts
├── schemas/                   # Shared Zod schemas used across routers
│   ├── user.schema.ts
│   └── pagination.schema.ts
├── types/                     # Exported types: AppRouter, Context
│   └── index.ts
└── utils/
    └── errors.ts              # Custom TRPCError factories
```

## Architecture Rules

- **Router-Service separation.** Routers define procedures (input validation, middleware chain, return type). Services contain business logic (DB queries, permission checks, external API calls). A router procedure calls a service function. Never put database queries inside a router procedure directly.
- **Context is built once per request.** `context.ts` exports a `createContext` function that receives the raw request and returns `{ db, user, requestId }`. Procedures access these via `ctx`. Never import the database client inside a router file.
- **Middleware is composable.** Define `isAuthed` middleware that throws `UNAUTHORIZED` if `ctx.user` is null. Define `hasRole('admin')` that checks `ctx.user.role`. Chain them: `protectedProcedure = t.procedure.use(isAuthed)`, `adminProcedure = protectedProcedure.use(hasRole('admin'))`.
- **Input and output schemas are explicit.** Every procedure has `.input(z.object({...}))`. Mutations and queries that return data also have `.output()` to enforce response shape. Never rely on implicit return types.
- **Export the AppRouter type, not the router instance.** The client imports `type AppRouter` for type inference. The actual router instance stays on the server. This is the entire point of tRPC's end-to-end type safety.

## Coding Conventions

- Router files export a single router: `export const userRouter = router({ ... })`. The root `router.ts` merges them: `appRouter = router({ user: userRouter, post: postRouter })`.
- Procedure naming follows REST-like semantics: `user.list`, `user.byId`, `user.create`, `user.update`, `user.delete`. Queries for reads, mutations for writes.
- Use `TRPCError` for all error responses. Always include a `code` (`NOT_FOUND`, `BAD_REQUEST`, `UNAUTHORIZED`, `FORBIDDEN`, `INTERNAL_SERVER_ERROR`) and a human-readable `message`.
- Enable SuperJSON as the transformer in `initTRPC.create({ transformer: superjson })`. This lets you return `Date`, `Map`, `Set`, `BigInt` and they serialize correctly. Without it, dates become strings and lose their type.
- Zod schemas shared across routers (pagination, sorting, ID params) live in `schemas/`. Router-specific schemas are co-located at the top of the router file.

## Library Preferences

- **Validation:** Zod exclusively. Not Yup (no TypeScript inference), not io-ts (verbose syntax). Zod schemas double as TypeScript types via `z.infer<typeof schema>`.
- **Serialization:** SuperJSON. Not custom transformers. SuperJSON handles edge cases (undefined in arrays, Infinity, RegExp) that JSON.stringify silently drops.
- **Database:** Prisma or Drizzle. The service layer abstracts this. Routers never import the ORM directly.
- **Auth:** JWT verified in context creation. Not in individual procedures. The context either has a `user` or it's `null`. Middleware guards handle the enforcement.
- **HTTP adapter:** `@trpc/server/adapters/standalone` for simple deployments, or `/adapters/express` if you need Express middleware (CORS, rate-limit, static files).
- **Client:** `@trpc/client` with `httpBatchLink` for batching multiple requests into one HTTP call. Not individual HTTP links per request.

## File Naming

- Routers: `kebab-case.router.ts` -> `user.router.ts`, `post.router.ts`
- Services: `kebab-case.service.ts` -> `user.service.ts`, `auth.service.ts`
- Schemas: `kebab-case.schema.ts` -> `user.schema.ts`, `pagination.schema.ts`
- Middleware: all in `trpc/middleware.ts` unless large enough to split by concern
- Types: `index.ts` in `types/` re-exports `AppRouter` and `Context`

## NEVER DO THIS

1. **Never import the router instance on the client.** Import `type AppRouter` only. If you import the actual router, you're bundling server code (database drivers, secrets) into the client.
2. **Never skip input validation.** A procedure without `.input()` accepts `undefined`. If it expects data, add a Zod schema. tRPC with no validation is just an untyped RPC with extra steps.
3. **Never use `any` in context or middleware types.** The entire value of tRPC is end-to-end type safety. One `any` in the middleware chain breaks inference for every downstream procedure.
4. **Never put business logic in routers.** Routers are the API boundary: validate input, call service, return output. If you're writing `if/else` chains or database queries in a router procedure, move it to a service.
5. **Never create deeply nested routers.** `appRouter.admin.users.management.list` is unreadable. Keep it to two levels max: `appRouter.user.list`, `appRouter.admin.listUsers`.
6. **Never forget error handling in services.** Services throw `TRPCError` with appropriate codes. Unhandled exceptions become `INTERNAL_SERVER_ERROR` with no useful message. Catch database errors (unique constraint, not found) and throw specific `TRPCError` instances.
7. **Never expose internal IDs or stack traces in error responses.** Production errors should have a user-facing message and a `code`. The full error context goes to server-side logging only.

## Testing

- Unit test services by mocking the database client. Pass a mock `db` and verify the service calls the right queries with the right parameters.
- Integration test routers using `createCaller`: `const caller = appRouter.createCaller({ db, user: mockUser })`. Call procedures directly and assert on return values and thrown errors.
- Test middleware by creating a minimal procedure with the middleware applied, calling it with various contexts, and verifying it allows or blocks as expected.
- Test input validation by calling procedures with malformed data and asserting `BAD_REQUEST` errors with Zod error details.
- End-to-end test with `@trpc/client` against a running server instance for critical paths (auth flow, data CRUD).

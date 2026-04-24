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

- Hono 4+ (lightweight edge-first web framework)
- TypeScript (strict mode)
- Zod + @hono/zod-openapi (validation + auto-generated OpenAPI docs)
- [Cloudflare Workers/Bun/Deno/Node.js] runtime
- Drizzle ORM + [D1/Turso/PostgreSQL] (or Prisma)
- Vitest for testing

## Project Structure

```
src/
├── index.ts                   # App entry point, route mounting
├── routes/
│   ├── [feature].ts           # Route definitions with OpenAPI schemas
│   └── index.ts               # Route aggregation
├── middleware/
│   ├── auth.ts                # JWT/API key verification
│   ├── logger.ts              # Request logging
│   └── error-handler.ts       # Global error middleware
├── schemas/
│   ├── [feature].ts           # Zod schemas for request/response
│   └── common.ts              # Shared schemas (pagination, errors)
├── services/
│   ├── [feature].ts           # Business logic
│   └── external/              # Third-party API clients
├── db/
│   ├── schema.ts              # Drizzle table definitions
│   ├── migrations/            # SQL migration files
│   └── index.ts               # Database client initialization
├── lib/
│   ├── types.ts               # App-wide TypeScript types
│   └── env.ts                 # Environment variable validation
└── workers/                   # Cloudflare Worker-specific (queues, crons, DO)
    ├── scheduled.ts
    └── queue.ts
wrangler.toml                  # Cloudflare Workers config (if applicable)
```

## Architecture Rules

- **Route files define OpenAPI specs inline.** Use `createRoute()` from `@hono/zod-openapi` to define path, method, request schema, and response schemas together. The route definition IS the documentation. Never maintain a separate OpenAPI spec file.
- **Middleware chain is explicit.** Register middleware via `app.use('path', middleware)` in the correct order. Auth middleware goes before route handlers. Error handler wraps everything. Never rely on implicit middleware ordering.
- **Services contain all business logic.** Route handlers extract validated input from `c.req.valid()`, call service functions, and return `c.json()`. Never put database queries or complex logic in route handlers.
- **Environment bindings are typed.** Define `Bindings` type for Cloudflare Workers env (KV, D1, R2, Queues) or validate env vars with Zod on startup. Access via `c.env` in handlers. Never use `process.env` directly in Workers.
- **Responses follow a consistent envelope.** Define standard response schemas: `{ data, meta }` for success, `{ error: { message, code } }` for errors. Never return bare objects or arrays.

## Coding Conventions

- **Use `createRoute` + `app.openapi()` pattern.** Define routes with full Zod validation for params, query, body, and all response codes. This generates OpenAPI docs and provides end-to-end type safety.
- **Zod schemas are the single source of truth.** Define request/response shapes as Zod schemas. Derive TypeScript types with `z.infer<>`. Never define separate interfaces that duplicate Zod schemas.
- **Context (`c`) is the only API surface.** Use `c.req` for request data, `c.json()` for responses, `c.env` for bindings, `c.var` for middleware-set variables. Never import global state or singletons.
- **Error handling with `HTTPException`.** Throw `new HTTPException(status, { message })` for expected errors. The error handler middleware catches these and formats the response. Never return error responses manually with `c.json({error}, 400)`.
- **Keep route files focused.** Each file handles one resource (e.g., `users.ts` handles `/users` and `/users/:id`). Export the sub-app and mount it in `index.ts` with `app.route('/users', usersApp)`.

## Library Preferences

- **Validation:** Zod + `@hono/zod-openapi`. Never use Joi, Yup, or manual validation.
- **ORM:** Drizzle (edge-native, lightweight) or Prisma with Accelerate for edge. Never use Knex or Sequelize.
- **Auth:** Hono's built-in `jwt()` middleware or `@hono/clerk-auth`. Never implement custom JWT parsing.
- **Rate limiting:** Cloudflare Rate Limiting or `@hono/rate-limiter`. Never implement custom in-memory rate limiting (it doesn't work across Workers).
- **Logging:** Hono's built-in logger middleware or structured JSON logging to `console.log` (captured by Workers runtime).
- **API docs:** Auto-generated from `@hono/zod-openapi` + Swagger UI via `@hono/swagger-ui`.

## File Naming

- Routes: `src/routes/[feature].ts` (plural: `users.ts`, `orders.ts`)
- Schemas: `src/schemas/[feature].ts` (matching route names)
- Services: `src/services/[feature].ts`
- Middleware: `src/middleware/[name].ts` (kebab-case)
- DB schema: `src/db/schema.ts` (single file or split by domain)

## NEVER DO THIS

1. **Never use `process.env` in Cloudflare Workers.** There is no `process` global. Use `c.env` for bindings and environment variables. This will throw a runtime error in production.
2. **Never use Node.js built-in modules without compatibility flags.** `fs`, `path`, `crypto` are not available in Workers by default. Use Web APIs (`crypto.subtle`, `fetch`) or enable the `nodejs_compat` flag in `wrangler.toml`.
3. **Never create global mutable state.** Workers are stateless and may run on different isolates per request. Global variables are not shared between requests reliably. Use KV, D1, or Durable Objects for state.
4. **Never skip Zod validation on inputs.** Hono doesn't validate by default. Without `@hono/zod-openapi` or manual `zValidator`, request bodies and params are untyped `any`. Every endpoint must validate.
5. **Never return large payloads from edge functions.** Workers have CPU time limits (10-50ms on free tier). Paginate responses, stream large data, and offload heavy computation to queues or Durable Objects.
6. **Never use `express`-style `req.body` parsing.** Hono uses `c.req.json()`, `c.req.text()`, `c.req.parseBody()` (for form data). There is no body-parser middleware. Express patterns will not work.
7. **Never duplicate Zod schemas as TypeScript interfaces.** Use `z.infer<typeof schema>` to derive types. Maintaining parallel type definitions leads to drift and defeats the purpose of schema-driven development.

## Testing

- **Route tests:** Use Hono's built-in `app.request()` test helper. Create the app, send requests, and assert on response status and JSON body. No HTTP server needed.
- **Service tests:** Import service functions and test with mock dependencies. Use dependency injection or module mocking with `vi.mock()` for database and external API calls.
- **Middleware tests:** Create a minimal Hono app with the middleware applied. Send requests through `app.request()` and assert on headers, status codes, and `c.var` values.
- **Integration tests:** Use `unstable_dev` from `wrangler` to spin up a local Workers environment. Test against real D1/KV bindings with `--local` flag.
- Run tests: `npx vitest` (unit), `npx wrangler dev --test-scheduled` (cron tests), `npx vitest --run` (CI).

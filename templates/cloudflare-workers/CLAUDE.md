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

## Production Delivery Playbook (Category: Cloud & Serverless)

### Release Discipline
- Design for cold starts, retries, and at-least-once execution semantics.
- Guard IAM permissions and network exposure with least privilege.
- Treat infrastructure config drift as deployment risk.

### Merge/Release Gates
- Deployment plan validated with environment-specific config checks.
- Critical alarms/observability are in place for changed services.
- Rollback path tested or documented before release.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Runtime: Cloudflare Workers (V8 isolates, not Node.js)
- Framework: Hono v4 for routing and middleware
- Database: Cloudflare D1 (SQLite-based, SQL migrations)
- Object Storage: Cloudflare R2 (S3-compatible)
- Key-Value: Cloudflare KV (eventually consistent)
- Queue: Cloudflare Queues for async processing
- CLI: Wrangler v3 for dev, deploy, and tail
- Language: TypeScript (strict mode)
- Package Manager: pnpm
- Testing: Vitest with miniflare for local simulation

## Project Structure

```
src/
  index.ts              # Hono app entry, route registration
  routes/
    api.ts              # REST API route handlers
    webhooks.ts         # Incoming webhook handlers
  middleware/
    auth.ts             # Bearer token / JWT validation
    cors.ts             # CORS configuration
    rateLimit.ts        # KV-based rate limiting
  services/
    db.ts               # D1 query helpers and typed queries
    storage.ts          # R2 upload/download helpers
    cache.ts            # KV get/set with TTL wrappers
  types/
    bindings.ts         # Env interface (D1, R2, KV, secrets)
    api.ts              # Request/response type definitions
  utils/
    response.ts         # Standardized JSON response builders
migrations/
  0001_initial.sql      # D1 migration files
wrangler.toml           # Worker configuration and bindings
vitest.config.ts        # Test config with miniflare pool
```

## Architecture Rules

- Define all bindings in `src/types/bindings.ts` as a single `Env` interface passed to `Hono<{ Bindings: Env }>`.
- Every route handler receives bindings via `c.env` -- never use global variables.
- Use D1 prepared statements with `.bind()` for all queries. Never interpolate SQL strings.
- Wrap R2 operations in try/catch and return proper HTTP status codes (404 for missing objects, 413 for size limits).
- KV reads are eventually consistent; use `cacheTtl` parameter for time-sensitive data.
- Keep each Worker under the 1MB compressed size limit. Use dynamic imports if needed.
- All middleware follows Hono's `MiddlewareHandler` signature and calls `await next()`.

## Coding Conventions

- Use `c.json()` for all JSON responses with explicit status codes: `c.json({ data }, 200)`.
- Name route files by resource (e.g., `users.ts`, `posts.ts`) and mount them with `app.route('/api/users', usersApp)`.
- Prefer `crypto.subtle` for hashing and HMAC -- the Web Crypto API is available, not Node crypto.
- Use `Date.now()` for timestamps. Store as Unix milliseconds in D1 integer columns.
- Error responses follow `{ error: string, code: string }` format.
- Environment secrets go in `.dev.vars` locally and are set via `wrangler secret put` in production.

## Library Preferences

- Routing and middleware: Hono (never express or itty-router)
- Validation: Zod with `@hono/zod-validator`
- JWT: `hono/jwt` middleware (not jsonwebtoken -- it requires Node)
- UUID generation: `crypto.randomUUID()` (built into Workers runtime)
- Date handling: native Date and Intl (no dayjs/moment -- keep bundle small)

## File Naming

- All source files: camelCase (`rateLimit.ts`, `authMiddleware.ts`)
- Migration files: sequential numbered prefix (`0001_create_users.sql`)
- Test files: colocated as `*.test.ts` next to source files
- Type files: grouped in `types/` directory, named by domain

## NEVER DO THIS

1. Never import Node.js built-in modules (fs, path, http) -- they do not exist in the Workers runtime.
2. Never use `console.log` for production logging -- use `wrangler tail` and structured logging with `c.env`.
3. Never store secrets in `wrangler.toml` -- use `.dev.vars` for local dev and `wrangler secret put` for production.
4. Never use blocking loops or heavy computation that exceeds the 30s CPU time limit (10ms on free plan).
5. Never rely on in-memory state between requests -- Workers are stateless, use KV or D1 for persistence.
6. Never use npm packages that depend on Node.js APIs (Buffer polyfills, stream, net) without checking Workers compatibility.
7. Never skip D1 migrations -- always use `wrangler d1 migrations apply` instead of manual schema changes.

## Testing

- Use Vitest with `@cloudflare/vitest-pool-workers` for integration tests against real D1/KV/R2 bindings.
- Define test bindings in `vitest.config.ts` under `miniflare` configuration.
- Test each route handler independently by creating a Hono app instance per test file.
- Mock external API calls with `undici.MockAgent` or intercept with Miniflare's fetch mock.
- Run `wrangler dev --local` for manual testing; run `vitest` for automated tests.
- Assert response status codes, headers (especially CORS), and JSON body structure.

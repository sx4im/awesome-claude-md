# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

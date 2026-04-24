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

- Runtime: Deno 2.x (V8-based, secure by default)
- Hosting: Deno Deploy (edge runtime, globally distributed)
- Storage: Deno KV (built-in distributed key-value store)
- Web Framework: Hono v4 (lightweight, works perfectly on Deno)
- Language: TypeScript (no tsconfig needed, Deno handles it natively)
- Dependency Management: Import maps via deno.json (no node_modules)
- Testing: Deno built-in test runner (`deno test`)
- Formatting: `deno fmt` (opinionated, no config needed)
- Linting: `deno lint` (built-in, strict defaults)
- Task Runner: deno.json `tasks` field

## Project Structure

```
main.ts                 # Hono app entry point, route registration
routes/
  api.ts                # REST API route handlers
  auth.ts               # Authentication routes (login, register)
  webhooks.ts           # Incoming webhook endpoints
middleware/
  cors.ts               # CORS headers middleware
  auth.ts               # JWT Bearer token validation
  rateLimit.ts          # KV-based rate limiting per IP
services/
  kv.ts                 # Deno KV helpers (get, set, list, atomic ops)
  auth.ts               # JWT sign/verify using Web Crypto API
  email.ts              # Outbound email via third-party API
types/
  api.ts                # Request/response type definitions
  kv.ts                 # KV key schema and value types
utils/
  response.ts           # Standard JSON response helpers
  crypto.ts             # Web Crypto utilities (hash, HMAC)
deno.json               # Import map, tasks, compiler options
deno.lock               # Lock file for dependency integrity
```

## Architecture Rules

- Use `Deno.openKv()` at module level to get a single KV instance; pass it to services, never open multiple connections.
- Design KV keys as typed tuples: `["users", userId]`, `["users_by_email", email]` for secondary indexes.
- Use `kv.atomic()` for multi-key writes that must be consistent (e.g., creating a user and their email index).
- Deno Deploy has a 50ms CPU time limit per request. Offload heavy computation to Deno Queues (`kv.enqueue()`).
- All dependencies come from `jsr:` (JSR registry) or `npm:` specifiers in the import map. Never use `https:` URLs.
- Deno Deploy does not support filesystem access (`Deno.readFile`, `Deno.writeFile`). Use KV or external storage.

## Coding Conventions

- Export the Hono app as default from `main.ts`: `export default app` (Deno Deploy convention).
- Use `Deno.serve()` for local development: `Deno.serve(app.fetch)`.
- Import all dependencies via the import map aliases in `deno.json`.
- Use Web Crypto API (`crypto.subtle`) for JWT signing, HMAC, and hashing -- not third-party crypto libs.
- KV values are automatically serialized via structured clone. Store plain objects, not stringified JSON.
- Error responses: `{ error: string, code: string }`. Success responses: `{ data: T }`.
- Use `Deno.env.get("VAR_NAME")` for environment variables.

## Library Preferences

- Web framework: Hono via `jsr:@hono/hono`
- Validation: Zod via `npm:zod` with `@hono/zod-validator`
- JWT: Manual implementation using Web Crypto API (SubtleCrypto HMAC)
- HTML rendering: Hono JSX middleware (if needed)
- Testing HTTP: Hono test client (`app.request('/path')`)
- Date handling: Temporal API or native Date (no third-party libs)

## File Naming

- All source files: camelCase (`rateLimit.ts`, `authService.ts`)
- Entry point: `main.ts` at project root (Deno Deploy convention)
- Test files: `*_test.ts` (Deno convention, underscore not dot)
- Type files: grouped in `types/` directory

## NEVER DO THIS

1. Never use `https://deno.land/` URL imports -- use `jsr:` or `npm:` specifiers in the import map instead.
2. Never use `node_modules` or `package.json` -- use `deno.json` for all configuration and dependency management.
3. Never use `Deno.readFile` or filesystem APIs in code deployed to Deno Deploy -- they are not available.
4. Never store large blobs (over 64KB) in Deno KV values -- use external object storage for large files.
5. Never use `eval()` or dynamic `import()` from user input -- Deno's permission system does not protect against this on Deploy.
6. Never skip `deno fmt` before committing -- it is the single source of truth for formatting, no Prettier needed.
7. Never create KV keys without a typed schema -- define all key patterns in `types/kv.ts` to prevent key collisions.

## Testing

- Use Deno's built-in test runner: `deno test --allow-net --allow-env`.
- Test Hono handlers using the built-in test client: `const res = await app.request('/api/items')`.
- For KV tests, use `Deno.openKv(":memory:")` to get an in-memory KV store.
- Structure tests with `Deno.test("description", async () => { ... })`.
- Use `assertEquals`, `assertThrows` from `jsr:@std/assert`.
- Mock external HTTP calls by injecting fetch wrappers into services.
- Run `deno task test` (defined in deno.json) as the standard test command.
- Run `deno lint` and `deno fmt --check` in CI alongside tests.

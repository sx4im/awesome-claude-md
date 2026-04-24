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

- Runtime: Google Cloud Run (fully managed, auto-scaling containers)
- Language: TypeScript 5.x on Node.js 20
- Framework: Express.js 4 (Cloud Run serves HTTP directly)
- Database: Cloud SQL for PostgreSQL 15 (via Unix socket or Cloud SQL Proxy)
- ORM: Drizzle ORM with drizzle-kit for migrations
- Messaging: Google Cloud Pub/Sub for async event processing
- Storage: Google Cloud Storage for file uploads
- Auth: Google Cloud IAM, Firebase Auth for end-user auth
- CLI: gcloud CLI, Docker for local builds
- Package Manager: pnpm
- Testing: Vitest

## Project Structure

```
src/
  index.ts              # Express app setup, port binding for Cloud Run
  routes/
    health.ts           # GET /health readiness and liveness checks
    api.ts              # REST API route definitions
  controllers/
    items.ts            # Request handling, calls services, returns responses
    events.ts           # Pub/Sub push endpoint handlers
  services/
    itemService.ts      # Business logic layer
    pubsub.ts           # Pub/Sub publish helpers
    storage.ts          # Cloud Storage upload/download helpers
  db/
    client.ts           # Drizzle client with Cloud SQL connection
    schema.ts           # Drizzle table definitions
  middleware/
    auth.ts             # Firebase ID token verification
    errorHandler.ts     # Express error handling middleware
    requestId.ts        # X-Request-Id propagation
  utils/
    config.ts           # Typed env var access with defaults
drizzle/
  migrations/           # SQL migration files from drizzle-kit
Dockerfile              # Multi-stage build for Cloud Run
cloudbuild.yaml         # Cloud Build CI/CD pipeline
```

## Architecture Rules

- Cloud Run requires the app to listen on the port specified by `process.env.PORT` (defaults to 8080).
- Always include a `GET /health` endpoint that returns 200 -- Cloud Run uses it for readiness checks.
- Connect to Cloud SQL using the Unix socket path `/cloudsql/PROJECT:REGION:INSTANCE` in production, localhost with Cloud SQL Proxy in dev.
- Pub/Sub push subscriptions send POST requests with base64-encoded messages. Decode with `Buffer.from(msg, 'base64').toString()`.
- Return 2xx from Pub/Sub handlers to acknowledge the message; return 4xx/5xx to trigger retry.
- Cloud Run instances may receive concurrent requests -- ensure handlers are stateless and thread-safe.
- Set `--min-instances=1` in production to avoid cold starts for latency-sensitive services.

## Coding Conventions

- Mount Express routers by domain: `app.use('/api/items', itemsRouter)`.
- Controllers parse request data and call service functions. Services contain business logic and call the DB.
- Use Drizzle's type-safe query builder: `db.select().from(items).where(eq(items.id, id))`.
- Pub/Sub event handlers live in `controllers/events.ts` and are mounted at `POST /events/<topic>`.
- Use `@google-cloud/logging-winston` or structured JSON to stdout for Cloud Logging integration.
- Set request timeouts via Cloud Run's `--timeout` flag (default 300s, max 3600s).

## Library Preferences

- Web framework: Express.js 4 (not Fastify or Koa for Cloud Run compatibility)
- Database: Drizzle ORM with pg driver (not Prisma -- faster cold starts)
- Pub/Sub: @google-cloud/pubsub
- Cloud Storage: @google-cloud/storage
- Auth: firebase-admin for ID token verification
- Validation: Zod with express middleware wrapper
- Logging: structured JSON via pino (Cloud Logging parses JSON from stdout)

## File Naming

- All source files: camelCase (`itemService.ts`, `errorHandler.ts`)
- Migration files: timestamp prefix generated by drizzle-kit (`0001_migration.sql`)
- Docker and CI files: standard names (`Dockerfile`, `cloudbuild.yaml`)
- Test files: `*.test.ts` colocated next to source files

## NEVER DO THIS

1. Never hardcode the port number -- always use `process.env.PORT || 8080` as Cloud Run injects the port.
2. Never use in-memory sessions or caching -- Cloud Run scales to zero and instances are ephemeral.
3. Never connect to Cloud SQL via public IP in production -- use Unix socket or Cloud SQL Auth Proxy.
4. Never return 5xx from a Pub/Sub push handler unless you want automatic retries with exponential backoff.
5. Never include secrets in `cloudbuild.yaml` or Dockerfile -- use Secret Manager and `--set-secrets` flag on deploy.
6. Never skip the health check endpoint -- Cloud Run will mark the revision as unhealthy without it.

## Testing

- Use Vitest for unit and integration tests.
- Unit test services by mocking the Drizzle db instance: `vi.mock('./db/client')`.
- Test Express routes using supertest: `request(app).get('/api/items').expect(200)`.
- Test Pub/Sub handlers by posting base64-encoded mock messages to the event endpoint.
- For integration tests, use a local PostgreSQL container and run Drizzle migrations before tests.
- Mock Google Cloud clients (@google-cloud/pubsub, @google-cloud/storage) in unit tests.
- Use `docker build . && docker run -p 8080:8080` for local end-to-end testing. CI runs in Cloud Build.

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

- Medusa.js 2.x e-commerce backend framework
- TypeScript throughout with strict compiler options
- PostgreSQL as the primary database via MikroORM
- Redis for event bus, caching, and background job processing
- Medusa's Module architecture for business domain separation
- Medusa Workflows for multi-step transactional operations

## Project Structure

```
src/
  modules/
    loyalty/
      index.ts
      service.ts
      models/
        loyalty-points.ts
      migrations/
        Migration20240101.ts
    custom-fulfillment/
      index.ts
      service.ts
  workflows/
    create-order-with-loyalty/
      index.ts
      steps/
        validate-loyalty-points.ts
        deduct-loyalty-points.ts
        create-order.ts
  subscribers/
    order-placed.ts
    payment-captured.ts
  api/
    store/custom/loyalty/
      route.ts
    admin/custom/analytics/
      route.ts
    middlewares.ts
  admin/
    widgets/
      loyalty-widget.tsx
    routes/analytics/
      page.tsx
  jobs/
    sync-inventory.ts
  links/
    loyalty-to-customer.ts
medusa-config.ts
tsconfig.json
```

## Architecture Rules

- Custom business logic encapsulated in Medusa Modules with their own models, services, migrations
- Multi-step operations that span modules use Workflows with compensating steps for rollback
- Subscribers react to domain events (order.placed, payment.captured) for side effects
- API routes in src/api/ follow Medusa's file-based routing: folder structure defines URL paths
- Module services extend MedusaService with typed model generics for CRUD operations
- Links connect entities across modules without tight coupling (defined in src/links/)

## Coding Conventions

- Module services export a class extending MedusaService<typeof ModelName>
- Workflow steps created with createStep() with input/output type parameters
- Workflows composed with createWorkflow() chaining steps with .next()
- Subscribers export default a config object with event name and handler function
- API route handlers receive MedusaRequest and MedusaResponse typed generics
- Use Medusa's container resolution (req.scope.resolve) for accessing services in routes
- Module models use MikroORM decorators: @Entity, @Property, @PrimaryKey

## Library Preferences

- ORM: MikroORM as required by Medusa 2.x — never use Prisma or TypeORM
- Payment: Medusa payment modules (Stripe via @medusajs/payment-stripe)
- Fulfillment: Custom fulfillment modules extending AbstractFulfillmentService
- Search: MeiliSearch via @medusajs/plugin-meilisearch for product search
- File storage: S3 module via @medusajs/file-s3 or local file module for dev
- Admin: Medusa Admin UI with React extensions using @medusajs/admin-sdk

## File Naming

- Module entry points: src/modules/module-name/index.ts exports module definition
- Module services: src/modules/module-name/service.ts (singular service file)
- Workflow step files: kebab-case descriptive names (validate-loyalty-points.ts)
- Subscriber files: kebab-case matching the event domain (order-placed.ts)
- API routes: route.ts inside folder structure matching the URL path
- Model files: kebab-case in models/ directory (loyalty-points.ts)

## NEVER DO THIS

1. Never access another module's database tables directly — use the module's service or a link
2. Never perform multi-module mutations outside of a Workflow — partial failures leave inconsistent state
3. Never import internal Medusa module code — use the container and dependency injection
4. Never skip compensating steps in Workflows — every mutating step needs a compensation
5. Never modify core Medusa modules — extend them or create custom modules instead
6. Never use setTimeout for background tasks — use Medusa's scheduled jobs system
7. Never hardcode prices or currencies — use Medusa's pricing module with currency-aware calculations

## Testing

- Use Jest with ts-jest for unit and integration testing
- Test modules in isolation by instantiating their service with a test database
- Test workflows using Medusa's workflow testing utilities with mocked step contexts
- Test API routes using supertest against a Medusa test instance
- Test subscribers by emitting events through the test event bus and asserting side effects
- Seed test data using module services in beforeAll hooks, clean up in afterAll
- Run tests with: npx jest --runInBand --forceExit

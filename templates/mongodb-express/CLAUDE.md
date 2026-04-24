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

## Production Delivery Playbook (Category: Database & Messaging)

### Release Discipline
- Protect data correctness with transactional boundaries and idempotent consumers.
- Preserve migration safety (forward + rollback) for schema/index changes.
- Handle poison messages and dead-letter routing explicitly.

### Merge/Release Gates
- Migration dry-run reviewed; no destructive change without backup plan.
- Consumer/producer contract tests pass.
- Data integrity checks and replay strategy documented.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Node.js 20 LTS with Express 4.x (not Express 5 beta)
- MongoDB 7.x with Mongoose 8.x ODM for schema validation and middleware
- MongoDB Atlas for hosted deployments; mongosh for local development
- Zod for request validation at the API layer (not Mongoose validation for input)
- Jest with mongodb-memory-server for testing
- ESLint with eslint-plugin-mongoose for schema linting
- pnpm for package management, tsx for development

## Project Structure

```
src/
  routes/
    users.routes.ts
    orders.routes.ts
    products.routes.ts
  controllers/
    users.controller.ts
    orders.controller.ts
  models/
    user.model.ts          # Mongoose schema + model export
    order.model.ts
    product.model.ts
    plugins/
      toJSON.plugin.ts     # Strip __v, rename _id to id
      paginate.plugin.ts   # Cursor-based pagination plugin
  middleware/
    auth.middleware.ts
    validate.middleware.ts  # Zod schema validation
    error.middleware.ts
  services/
    users.service.ts       # Business logic, calls model methods
    orders.service.ts
  aggregations/
    sales-report.pipeline.ts
    user-activity.pipeline.ts
  config/
    db.ts                  # Connection with retry logic
    index.ts               # Environment config
  utils/
    api-error.ts
    pick.ts
tests/
  integration/
  unit/
  fixtures/
```

## Architecture Rules

- Follow the Controller-Service-Model pattern strictly. Controllers parse requests and call services. Services contain business logic and call models. Models define schemas and static/instance methods.
- Never import a Model directly into a Controller. All data access flows through the Service layer.
- Use Mongoose lean queries (`.lean()`) for read-only operations to skip hydration overhead. Only use full documents when you need middleware or virtuals.
- Define all aggregation pipelines in dedicated files under `src/aggregations/`. Each pipeline is a function that accepts parameters and returns a pipeline array.
- Use Mongoose discriminators for polymorphic collections instead of separate collections with duplicated fields.
- Index every field used in query filters or sort operations. Define indexes in the schema file, never create them ad-hoc in production.

## Coding Conventions

- Export Mongoose models as named exports: `export const User = model<IUser>('User', userSchema)`.
- Define TypeScript interfaces for documents: `IUser` extends `Document`. Define a separate `IUserMethods` for instance methods.
- Use `Schema.pre('save')` hooks for denormalization updates. Use `Schema.post('save')` for side effects like sending emails.
- All API responses follow `{ success: boolean, data: T, message?: string }` shape.
- Use cursor-based pagination with `_id` comparison, never skip/offset pagination for large collections.
- Timestamps are always `createdAt` / `updatedAt` via Mongoose `timestamps: true`.

## Library Preferences

- Mongoose over the raw MongoDB Node.js driver for application code
- Zod over Joi or express-validator for request validation
- mongodb-memory-server over mocking Mongoose methods for tests
- helmet and cors as Express middleware, configured in app setup
- morgan for HTTP logging in development, pino in production

## File Naming

- All files use kebab-case with a dot-separated suffix: `user.model.ts`, `auth.middleware.ts`
- Aggregation pipelines: `descriptive-name.pipeline.ts`
- Test files sit in `tests/` with matching structure: `tests/unit/services/users.service.test.ts`

## NEVER DO THIS

1. Never use `mongoose.connect()` without setting `maxPoolSize`, `serverSelectionTimeoutMS`, and `retryWrites: true`.
2. Never store monetary values as floating-point numbers. Use Decimal128 or store cents as integers.
3. Never use `$where` operator or pass user input into aggregation `$expr` without sanitization. This enables NoSQL injection.
4. Never call `.populate()` more than two levels deep. Denormalize the data or use an aggregation `$lookup` instead.
5. Never define Mongoose schemas with `strict: false`. Every field must be explicitly declared in the schema.
6. Never use `Model.find()` without `.limit()`. Unbounded queries will exhaust server memory on large collections.

## Testing

- Use `mongodb-memory-server` to spin up an ephemeral MongoDB instance per test suite. Connect in `beforeAll`, drop the database in `afterEach`, disconnect in `afterAll`.
- Test aggregation pipelines with realistic fixture data (minimum 50 documents) to verify grouping and sorting.
- Integration tests hit the Express routes via supertest. Validate response status codes, body shape, and database state.
- Test Mongoose middleware by creating/saving documents and asserting side effects occurred.
- Seed test data using factory functions in `tests/fixtures/`, not raw JSON files.
- Verify index usage by running `.explain('executionStats')` in integration tests for critical queries.

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

- PocketBase 0.23+ as backend framework with embedded SQLite database
- Go 1.22+ for custom backend extensions and hooks
- Real-time subscriptions via SSE for live data updates
- PocketBase Admin UI for collection management and data browsing
- PocketBase JavaScript SDK for client integration
- S3-compatible storage for file uploads (configurable)

## Project Structure

```
pb_project/
  main.go
  hooks/
    users.go
    orders.go
    notifications.go
  services/
    email.go
    payment.go
  middleware/
    ratelimit.go
    logging.go
  migrations/
    1700000001_create_products.go
    1700000002_create_orders.go
  utils/
    validation.go
  types/
    models.go
  pb_data/
  pb_migrations/
  tests/
    users_test.go
    orders_test.go
  go.mod
  go.sum
  Dockerfile
```

## Architecture Rules

- Extend PocketBase by embedding pocketbase.PocketBase in main.go and adding hooks
- All collection schema changes done through Go migration files, never through Admin UI in production
- Business logic in hooks/ responds to record lifecycle events (OnBeforeCreate, OnAfterUpdate)
- Complex operations go in services/, hooks call services, services call the DAO layer
- Custom API endpoints registered via app.OnBeforeServe with e.Router group
- Real-time subscriptions scoped by collection-level and record-level rules

## Coding Conventions

- Use app.Dao() for database operations, never raw SQL on the SQLite file
- Access record fields through record.Get("field") and record.Set("field", value)
- API rules (collection permissions) defined in migration files, not hardcoded in hooks
- Custom endpoints return JSON via e.JSON(http.StatusOK, data) pattern
- Hook functions grouped by collection in separate files
- Error responses use apis.NewBadRequestError() and related helpers

## Library Preferences

- HTTP routing: PocketBase's embedded echo router via e.Router
- Validation: Go's built-in validation plus PocketBase's field-level validation rules
- Email: PocketBase's built-in mailer (app.NewMailClient()) with customizable templates
- Client SDK: PocketBase JavaScript SDK (pocketbase) for frontend integration
- Cron: app.OnBeforeServe with robfig/cron/v3 for scheduled tasks
- Logging: PocketBase's built-in structured logger via app.Logger()

## File Naming

- Go files use snake_case: user_hooks.go, email_service.go
- Migration files prefixed with Unix timestamp: 1700000001_description.go
- Test files use Go convention: filename_test.go colocated in same package
- Collection names are plural snake_case: users, order_items

## NEVER DO THIS

1. Never modify pb_data/data.db directly — always use the DAO or Admin API
2. Never define collection schemas in Admin UI for production — use migration files
3. Never skip API rules on collections — empty rules mean no access, "*" means public access
4. Never use app.Dao().DB() for writes without wrapping in app.Dao().RunInTransaction()
5. Never store secrets in collection records — use environment variables or app settings
6. Never rely on client-side filtering for security — enforce access control in API rules

## Testing

- Use Go's standard testing package with testify/assert for assertions
- Create test PocketBase instances with pocketbase.NewWithConfig pointing to temp directories
- Test hooks by creating records through the test app's DAO and verifying side effects
- Test custom endpoints using httptest.NewRecorder with the app's echo router
- Seed test data using app.Dao().SaveRecord() in test setup functions
- Use t.Parallel() for independent tests to speed up the test suite
- Run tests with: go test ./... -v -count=1

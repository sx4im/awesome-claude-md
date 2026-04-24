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

- Directus 11.x headless CMS and data platform
- PostgreSQL as the primary database
- TypeScript for all custom extensions
- Directus SDK (@directus/sdk) for programmatic API access
- Custom extensions: endpoints, hooks, operations, interfaces, displays
- Directus Flows for no-code/low-code automation with custom operations

## Project Structure

```
extensions/
  src/
    endpoints/
      custom-reports/
        index.ts
      import-export/
        index.ts
    hooks/
      audit-log/
        index.ts
      data-sync/
        index.ts
    operations/
      send-slack-notification/
        index.ts
        api.ts
        app.ts
    interfaces/
      map-picker/
        index.ts
        interface.vue
    displays/
      status-badge/
        index.ts
        display.vue
    modules/
      analytics-dashboard/
        index.ts
        module.vue
  migrations/
    20240101A-create-custom-tables.ts
snapshots/
  production-schema.yaml
docker-compose.yml
.env
```

## Architecture Rules

- All custom logic lives in Directus extensions, never in external middleware or proxy layers
- Endpoint extensions register Express-compatible routes under /custom/ namespace
- Hook extensions react to CRUD events (items.create, items.update) and system events
- Operation extensions integrate into Directus Flows for visual workflow automation
- Schema changes tracked via Directus schema snapshots (YAML) and applied with directus schema apply
- Database migrations for data changes that schema snapshots cannot capture

## Coding Conventions

- Endpoint extensions export a default function receiving router and context: (router, context) => {}
- Hook extensions export a default function receiving filter and action event registrars
- Use context.services.ItemsService for CRUD operations within extensions, not raw SQL
- Access the database via context.database (Knex) only when ItemsService is insufficient
- Respect Directus accountability by passing the user's accountability to service constructors
- Environment variables accessed via context.env, not process.env

## Library Preferences

- Database access: Directus ItemsService for CRUD, Knex (via context.database) for complex queries
- Auth: Directus built-in auth with configurable providers (OAuth2, LDAP, SAML)
- File storage: Directus built-in storage adapters (local, S3, GCS, Azure)
- Email: Directus built-in mailer via context.services.MailService
- Schema management: Directus CLI schema snapshot and apply commands
- Client SDK: @directus/sdk with composable client (rest, graphql, realtime, auth)
- Admin UI extensions: Vue 3 with Directus's design system components

## File Naming

- Extension directories named with kebab-case describing their purpose
- Each extension has an index.ts entry point
- Operation extensions split into api.ts (server-side) and app.ts (admin UI config)
- Interface and display extensions use a .vue file for the UI component
- Migration files prefixed with date and letter sequence: 20240101A-description.ts

## NEVER DO THIS

1. Never modify Directus system tables (directus_users, directus_roles) via raw SQL
2. Never bypass Directus's permission system by using admin accountability in user-facing endpoints
3. Never store schema changes only in the database — export to schema snapshots for version control
4. Never use process.env in extensions — use context.env to access environment variables
5. Never install extensions by copying files manually — use the Directus extension SDK build system
6. Never create REST endpoints that duplicate Directus's built-in CRUD API

## Testing

- Use Vitest for testing extension logic in isolation
- Test endpoint extensions by creating a mock router and context object
- Test hook extensions by invoking registered event handlers with mock event data
- Test operation extensions by calling the handler with mock operation context
- Use @directus/sdk in integration tests to verify extensions through the Directus API
- Run a test Directus instance via Docker Compose with a separate test database
- Seed test data using ItemsService in test setup, clean up via truncation
- Run tests with: npx vitest run

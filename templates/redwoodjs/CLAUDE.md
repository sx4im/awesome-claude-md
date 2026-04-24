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

- RedwoodJS 8+ (full-stack React framework)
- TypeScript (strict mode)
- GraphQL (with SDL-first schema)
- Prisma ORM + [PostgreSQL/SQLite]
- Storybook for component development
- Jest + @testing-library/react

## Project Structure

```
api/
├── src/
│   ├── graphql/             # SDL schema files (*.sdl.ts)
│   ├── services/            # Service functions (resolvers live here)
│   │   ├── users/
│   │   │   ├── users.ts
│   │   │   ├── users.test.ts
│   │   │   └── users.scenarios.ts
│   ├── directives/          # GraphQL directives (@requireAuth, @skipAuth)
│   ├── lib/
│   │   ├── auth.ts          # Auth decoder and getCurrentUser
│   │   ├── db.ts            # Prisma client singleton
│   │   └── logger.ts
│   └── functions/           # Serverless function handlers
├── db/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts
web/
├── src/
│   ├── components/          # Reusable UI components
│   ├── cells/               # Redwood Cells (auto-generated query components)
│   │   └── UsersCell/
│   │       ├── UsersCell.tsx
│   │       ├── UsersCell.test.tsx
│   │       └── UsersCell.mock.ts
│   ├── layouts/             # Layout components wrapping pages
│   ├── pages/               # Route-mapped page components
│   └── Routes.tsx           # All route definitions
```

## Architecture Rules

- **Cells are the data-fetching primitive.** Every component that fetches data MUST be a Cell. Cells export `QUERY`, `Loading`, `Empty`, `Failure`, and `Success` named exports. Never use raw `useQuery` or `fetch` in page components.
- **SDL defines the schema, services implement resolvers.** The SDL file declares types and queries/mutations. The corresponding service file contains the resolver functions. Never define resolver logic inline in SDL files.
- **Services are the only place for business logic.** Services call Prisma, enforce authorization, and contain domain rules. Cells and pages are presentation only.
- **Use `@requireAuth` and `@skipAuth` directives on every query/mutation.** RedwoodJS will throw a build error if a query or mutation lacks an auth directive. Never leave a resolver unprotected by accident.
- **Use Redwood's `validate` helper in services.** Import `validate` from `@redwoodjs/api` for input validation rather than writing manual checks or pulling in external validation libraries.

## Coding Conventions

- **File naming:** PascalCase for Cells (`UsersCell/UsersCell.tsx`), camelCase for services (`users.ts`), PascalCase for pages (`HomePage/HomePage.tsx`).
- **Cells must export all five states.** Always define `Loading`, `Empty`, `Failure`, `Success`, and `QUERY`. Omitting `Empty` or `Failure` causes silent rendering bugs.
- **Use Redwood's `navigate` and `routes` helpers.** Import from `@redwoodjs/router`. Never use `window.location` or raw anchor tags for internal navigation.
- **Prisma relations in services.** When resolving nested GraphQL types, add relation resolver functions in the service file (e.g., `User.posts = ...`). Never rely on Prisma `include` in the parent query to resolve nested fields.
- **Type safety with generated types.** Run `yarn rw generate types` after SDL changes. Import generated types from `types/graphql` in cells and services.

## Library Preferences

- **Auth:** Redwood's built-in auth (`@redwoodjs/auth`) with [dbAuth/Clerk/Supabase]. Never roll custom JWT logic.
- **Forms:** `@redwoodjs/forms` with `useForm`. Integrates with Cells and provides server-side error handling.
- **Styling:** [Tailwind CSS/CSS Modules]. Configured via `web/config/tailwind.config.js`.
- **Testing:** Jest + `@redwoodjs/testing/web` for Cells, `@redwoodjs/testing/api` for services.
- **Deployment:** [Vercel/Netlify/AWS Lambda] via `yarn rw deploy {target}`.

## File Naming

- Cells: `web/src/cells/[Name]Cell/[Name]Cell.tsx`
- Pages: `web/src/pages/[Name]Page/[Name]Page.tsx`
- Services: `api/src/services/[name]/[name].ts`
- SDL: `api/src/graphql/[name].sdl.ts`
- Scenarios: `api/src/services/[name]/[name].scenarios.ts`

## NEVER DO THIS

1. **Never use `useEffect` + `fetch` to load data.** Use a Cell. Cells handle loading, empty, and error states automatically and integrate with Redwood's GraphQL client.
2. **Never write raw SQL in services.** Use Prisma's query builder. Raw SQL bypasses type safety and breaks Redwood's conventions.
3. **Never put auth logic in components.** Use `@requireAuth` directive on the SDL, `requireAuth()` calls in services, and `<Private>` route wrappers. Auth checks in components are bypassable.
4. **Never import from `api/` in `web/` directly.** The API and web sides are separate build targets. Share types through generated GraphQL types or the `types/` directory.
5. **Never skip scenario files for service tests.** Scenarios provide test fixtures through Prisma seeding. Writing manual `prisma.create` calls in tests is fragile and skips Redwood's test lifecycle.
6. **Never define routes outside `Routes.tsx`.** All routes must be declared in the single Routes file using `<Route>` components. Dynamic route generation elsewhere will silently fail.
7. **Never call `db` (Prisma) from a Cell or component.** Database access happens exclusively on the API side through services and resolvers.

## Testing

- **Service tests:** Use scenarios (`*.scenarios.ts`) to define test data. Test functions are called with `scenario` helper that seeds the database before each test.
- **Cell tests:** Use `render` from `@redwoodjs/testing/web`. Mock GraphQL responses with `mockGraphQLQuery` and `mockGraphQLMutation`.
- **Page tests:** Wrap with `<MemoryRouter>` and mock auth context. Test that correct Cells are rendered, not the data inside them.
- Run full test suite with `yarn rw test` (watches by default) or `yarn rw test --no-watch` in CI.

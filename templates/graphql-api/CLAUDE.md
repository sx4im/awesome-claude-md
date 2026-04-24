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

- Node.js 20+ with TypeScript (strict mode)
- Apollo Server 4 or Yoga (GraphQL server)
- Pothos (code-first schema builder)
- Prisma + PostgreSQL
- DataLoader for N+1 prevention
- GraphQL Codegen for client types

## Project Structure

```
src/
├── schema/
│   ├── index.ts             # Schema builder instance and merged schema
│   ├── user.ts              # User type definitions + resolvers
│   ├── order.ts             # Order type definitions + resolvers
│   └── scalars.ts           # Custom scalars (DateTime, JSON, etc.)
├── services/                # Business logic (called by resolvers)
│   ├── user.service.ts
│   └── order.service.ts
├── loaders/                 # DataLoader factories per entity
│   ├── user.loader.ts
│   └── order.loader.ts
├── lib/
│   ├── prisma.ts            # Prisma client singleton
│   ├── context.ts           # Request context builder (auth, loaders)
│   └── auth.ts              # JWT verification, user extraction
├── types/
│   └── context.ts           # Context type definition
└── server.ts                # Server setup and startup
```

## Architecture Rules

- **Code-first schema with Pothos.** Define types, queries, and mutations in TypeScript using the Pothos builder. Never write `.graphql` schema files manually. the code IS the schema, and Pothos generates the SDL.
- **Resolvers are thin.** They extract arguments and context, call a service function, and return the result. Business logic lives in `services/`. Never do database queries in resolvers directly.
- **DataLoader for every relationship.** Every field that resolves related data uses a DataLoader. Without it, a query for 50 users with their orders makes 51 database queries. DataLoader batches them into 2.
- **Context is per-request.** The context is built fresh for every request in `lib/context.ts`. It contains: authenticated user, DataLoader instances, and the Prisma client. DataLoaders must be per-request. they cache results for the duration of one query.
- **One file per domain type.** `schema/user.ts` defines the User GraphQL type, its queries, mutations, and field resolvers. Don't scatter User-related definitions across multiple files.

## Coding Conventions

- GraphQL type naming: `User`, `Order`, `CreateUserInput`, `UpdateOrderInput`, `UserConnection` (for pagination). No suffixes on output types, `Input` suffix on input types, `Connection` suffix on paginated types.
- Mutations return the affected entity: `createUser` returns `User`, `deleteOrder` returns `Order`. Never return `Boolean`. the client needs the updated data.
- Cursor-based pagination for lists. Use Relay-style `Connection` types with `edges`, `nodes`, and `pageInfo`. Not offset-based. offset pagination breaks with concurrent inserts.
- Error handling: throw `GraphQLError` with specific `extensions.code` values: `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `VALIDATION_ERROR`. Never return errors in the data payload.
- Naming: queries are nouns (`user`, `users`, `order`). Mutations are verb + noun (`createUser`, `updateOrder`, `deleteUser`).

## Library Preferences

- **Schema:** Pothos. not TypeGraphQL (Pothos is more flexible with Prisma plugin), not Nexus (less maintained). Not schema-first with `.graphql` files (inferior DX for TypeScript projects).
- **Server:** Yoga (lighter, HTTP framework agnostic) or Apollo Server (more middleware, better observability). Pick based on infrastructure needs.
- **N+1 prevention:** DataLoader. non-negotiable. No alternatives. Every GraphQL API needs it.
- **Client codegen:** GraphQL Codegen for typed hooks (React) or SDK generation. Run after schema changes.
- **Auth:** JWT in Authorization header, verified in context builder. Not session cookies (GraphQL clients aren't browsers).

## NEVER DO THIS

1. **Never resolve relationships without DataLoader.** `user.orders` without DataLoader means one query per user in a list. 100 users = 101 queries. DataLoader batches to 2 queries regardless of list size.
2. **Never return `Boolean` from mutations.** The client needs the affected resource to update its cache. `deleteUser` returns the deleted `User` (with `id` at minimum).
3. **Never expose internal IDs or database implementation details in the schema.** Use opaque global IDs (`toGlobalId(type, dbId)`) if you need Relay compliance. Otherwise, keep IDs as strings.
4. **Never create DataLoader instances outside of per-request context.** DataLoaders cache results. A shared DataLoader across requests serves stale data to other users. Always create fresh loaders in the context builder.
5. **Never skip input validation.** Even though GraphQL validates types, it doesn't validate business rules. Check string lengths, email formats, and permission constraints in services.
6. **Never nest mutations.** Mutations at the root query level: `mutation { createUser(...) }`. Not `mutation { user { create(...) } }`. Nested mutations have unpredictable execution order.
7. **Never expose `__schema` and `__type` introspection in production without protection.** Disable introspection or protect it behind auth. It reveals your entire API surface to attackers.

## Testing

- Test resolvers by executing GraphQL operations against the schema with a test context.
- Test services with mocked Prisma client.
- Test DataLoaders with known batched IDs. assert they batch multiple calls into one query.
- Use `graphql` library's `execute()` function for unit tests. No HTTP server needed.

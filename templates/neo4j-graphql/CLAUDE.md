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

- Neo4j 5.x Community or Enterprise with APOC and GDS (Graph Data Science) plugins
- Node.js 20 with @neo4j/graphql 5.x for auto-generated GraphQL schema from type definitions
- Apollo Server 4 as the GraphQL server runtime
- neo4j-driver 5.x for direct Cypher execution outside of GraphQL resolvers
- TypeScript 5.x with strict mode enabled
- Cypher for all graph queries; never use OGM for complex traversals
- Jest with neo4j-testcontainers for integration testing

## Project Structure

```
src/
  schema/
    typeDefs/
      user.graphql
      product.graphql
      recommendation.graphql
    resolvers/
      user.resolver.ts
      recommendation.resolver.ts    # Custom resolvers using raw Cypher
    directives/
      auth.directive.ts
  cypher/
    queries/
      shortest-path.cypher
      community-detection.cypher
      collaborative-filtering.cypher
    mutations/
      merge-user.cypher
      create-relationship.cypher
  gds/
    projections.ts          # Named graph projections for GDS algorithms
    algorithms.ts           # PageRank, Louvain, Node2Vec wrappers
    pipelines.ts            # ML pipeline definitions
  middleware/
    neo4j-context.ts        # Driver and session injection
    auth.ts                 # JWT validation, user context
  config/
    database.ts             # Driver configuration, connection pool
    schema.ts               # @neo4j/graphql schema construction
  utils/
    cypher-builder.ts       # Parameterized query helpers
    result-mapper.ts        # Neo4j Record to plain object mapping
tests/
  integration/
  fixtures/
    seed.cypher             # Test graph seeding script
```

## Architecture Rules

- Use `@neo4j/graphql` type definitions to generate the base CRUD schema automatically. Only write custom resolvers for traversals deeper than 3 hops or GDS algorithm calls.
- Every Cypher query must use parameters (`$paramName`), never string concatenation. Store complex queries in `.cypher` files and load them at startup.
- Use `MERGE` instead of `CREATE` for nodes that have natural keys to prevent duplicates. Always set `ON CREATE SET` and `ON MATCH SET` clauses.
- Model relationships as first-class citizens with properties. Use relationship types in UPPER_SNAKE_CASE: `PURCHASED`, `FOLLOWS`, `REVIEWED`.
- Keep node labels singular and PascalCase: `User`, `Product`, `Category`. A node should rarely have more than 3 labels.
- Use Neo4j bookmarks for causal consistency across read replicas. Pass bookmarks through the GraphQL context.
- GDS graph projections must be named and created on startup, not per-request. Drop and recreate projections only during data refresh jobs.

## Coding Conventions

- Wrap all driver sessions in try/finally blocks that close the session. Use `session.executeRead()` and `session.executeWrite()` transaction functions, never `session.run()` directly.
- Map Neo4j Integer types to JavaScript numbers using `.toNumber()` immediately after query execution. Neo4j integers are 64-bit and not safe as JS numbers above 2^53.
- Use `@auth` and `@authorization` directives from `@neo4j/graphql` for field-level access control in type definitions.
- Return only the properties you need with explicit `RETURN` clauses. Never use `RETURN n` to return entire nodes in production queries.
- Log all Cypher queries at DEBUG level with their parameters (redact sensitive values) using pino.

## Library Preferences

- @neo4j/graphql over hand-written resolvers for standard CRUD
- Apollo Server 4 over express-graphql or Mercurius
- neo4j-driver over any ORM or query builder for complex graph operations
- @neo4j/graphql-ogm only for seeding scripts, not application code
- graphql-codegen for generating TypeScript types from the schema

## File Naming

- GraphQL type definitions use kebab-case with `.graphql` extension: `user-profile.graphql`
- Cypher files use kebab-case with `.cypher` extension: `shortest-path.cypher`
- TypeScript files use kebab-case: `user.resolver.ts`, `cypher-builder.ts`

## NEVER DO THIS

1. Never use unbounded variable-length path patterns like `(a)-[*]->(b)`. Always specify min/max bounds: `(a)-[*1..5]->(b)`.
2. Never create indexes inside application code. Define all indexes and constraints in migration Cypher scripts run by neo4j-migrations.
3. Never use `DETACH DELETE` on nodes without a `WHERE` clause. Always scope deletions to specific nodes by ID or property.
4. Never run GDS algorithms on the default database graph. Always project a named subgraph with only the needed labels and relationship types.
5. Never store large blobs or binary data as node properties. Store references (URLs, S3 keys) and keep binary data external.
6. Never ignore the `ResultSummary` counters. Check `counters.nodesCreated` and `counters.relationshipsCreated` to verify mutations behaved as expected.

## Testing

- Use `testcontainers` with the official Neo4j Docker image to spin up a disposable database per test suite.
- Seed test graphs using `.cypher` fixture files executed via the driver in `beforeAll`. Keep test graphs small (under 200 nodes) but representative.
- Test GDS algorithm wrappers by creating known graph structures (e.g., a triangle for community detection) and asserting expected scores.
- GraphQL integration tests use Apollo Server's `executeOperation` method, not HTTP requests.
- Verify Cypher query plans using `EXPLAIN` in integration tests for performance-critical queries. Assert that index lookups are used, not full scans.
- Test authorization by executing queries with different user contexts and verifying field-level access is enforced.

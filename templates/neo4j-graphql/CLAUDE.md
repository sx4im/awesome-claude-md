# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

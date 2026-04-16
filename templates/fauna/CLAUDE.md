# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fauna (distributed document-relational database)
- FQL v10 (Fauna Query Language)
- GraphQL support
- Multi-region by default
- ACID transactions

## Project Structure
```
src/
├── fauna/
│   ├── client.ts               # Client setup
│   ├── queries.ts              # FQL queries
│   └── schema.fsl              # Schema definition
├── lib/
│   └── fauna-utils.ts
└── types/
    └── fauna.types.ts
```

## Architecture Rules

- **Document-relational model.** Documents with relationships, not pure document or SQL.
- **FQL for complex queries.** Functional query language for data manipulation.
- **GraphQL for simple access.** Automatic GraphQL from schema.
- **Multi-region transactions.** Global ACID compliance.

## Coding Conventions

- Client: `const client = new Client({ secret: FAUNA_SECRET })`.
- FQL query: `client.query(fql`Collection("Users").all()`)`.
- Create document: `fql`Collection("Users").create({ name: "John" })`.
- Relations: Define in schema, query with dot notation: `user.account`.
- Functions: Create UDFs for complex business logic.
- Indexes: Define for query patterns, unique constraints.

## NEVER DO THIS

1. **Never treat Fauna like MongoDB.** It has strict schema and relations.
2. **Never skip schema definition.** Documents must match collection schema.
3. **Never ignore the cost model.** Understand compute and storage pricing.
4. **Never use N+1 queries.** Use FQL to fetch related data in single query.
5. **Never forget ABAC (Attribute-Based Access Control).** Define security rules in schema.
6. **Never ignore temporality.** Fauna keeps history; queries can be time-traveled.
7. **Never use without understanding FQL.** It's different from SQL or MongoDB queries.

## Testing

- Test FQL queries in Fauna dashboard.
- Test GraphQL queries with Playground.
- Test ABAC rules with different tokens.


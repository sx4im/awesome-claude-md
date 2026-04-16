# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fastify with Objection.js
- Objection 3.x
- Knex.js query builder
- Model-based ORM
- Relation mapping

## Project Structure
```
src/
├── models/
│   ├── User.ts                 // Objection models
│   └── Post.ts
├── migrations/
│   └── ...                     // Knex migrations
├── knexfile.ts                 // Knex configuration
└── app.ts
```

## Architecture Rules

- **Model classes.** Extend `Model` from objection.
- **Relation mappings.** `static relationMappings` for joins.
- **Knex underneath.** All Knex methods available.
- **Validation.** JSON Schema or `ajv` for validation.

## Coding Conventions

- Model: `class User extends Model { static tableName = 'users'; static relationMappings = { posts: { relation: Model.HasManyRelation, modelClass: Post, join: { from: 'users.id', to: 'posts.userId' } } } }`.
- Query: `const users = await User.query().withGraphFetched('posts').where('age', '>', 18)`.
- Insert: `const user = await User.query().insert({ name: 'John', email: 'john@example.com' })`.
- Transaction: `await User.transaction(async (trx) => { await User.query(trx).insert(...); await Post.query(trx).insert(...) })`.

## NEVER DO THIS

1. **Never use without Knex configuration.** Objection needs Knex instance.
2. **Never skip `tableName` definition.** Required for all models.
3. **Never forget `withGraphFetched` vs `withGraphJoined`.** Different join strategies.
4. **Never use raw queries without parameterization.** SQL injection risk.
5. **Never ignore the `modifiers`.** Reusable query fragments.
6. **Never skip migration running.** Database schema must match.
7. **Never use `insertGraph` without understanding.** Complex nested inserts.

## Testing

- Test with SQLite in-memory for unit tests.
- Test relation fetching.
- Test transactions rollback on error.


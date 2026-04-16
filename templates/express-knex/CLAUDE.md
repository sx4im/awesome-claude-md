# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Express with Knex.js
- Knex query builder
- Multiple database support
- Migrations and seeds
- Transaction support

## Project Structure
```
src/
├── db/
│   ├── knex.ts                 // Knex instance
│   └── migrations/
├── routes/
└── models/
```

## Architecture Rules

- **Query builder.** SQL construction without raw strings.
- **Migrations.** Schema version control.
- **Transactions.** ACID operations.
- **Raw queries.** Escape when needed.

## Coding Conventions

- Instance: `const knex = require('knex')({ client: 'pg', connection: process.env.DATABASE_URL })`.
- Query: `const users = await knex('users').where('age', '>', 18).select('id', 'name')`.
- Join: `knex('users').join('accounts', 'users.id', 'accounts.user_id').select('users.*', 'accounts.name as account_name')`.
- Raw: `knex.raw('select * from users where id = ?', [userId])`.
- Transaction: `await knex.transaction(async (trx) => { await trx('users').insert({ name: 'John' }); await trx('accounts').insert({ user_id: 1 }) })`.

## NEVER DO THIS

1. **Never use string concatenation in queries.** SQL injection risk.
2. **Never forget to `await` knex queries.** All queries return promises.
3. **Never skip migrations.** `knex migrate:latest` for schema changes.
4. **Never use `knex` as ORM.** It's a query builder—no models.
5. **Never ignore the `returning` clause.** For PostgreSQL `insert`/`update`.
6. **Never forget connection pooling.** Configure `pool` settings.
7. **Never use `knex.destroy()` in every request.** Manage lifecycle properly.

## Testing

- Test with SQLite in-memory for unit tests.
- Test migrations up/down.
- Test transactions rollback on error.


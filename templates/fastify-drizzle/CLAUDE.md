# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fastify with Drizzle ORM
- Drizzle Kit
- PostgreSQL/MySQL/SQLite
- Type-safe SQL
- Zod integration

## Project Structure
```
src/
├── db/
│   ├── schema.ts               // Drizzle schema
│   └── index.ts                // Database connection
├── migrations/
└── routes/
    └── users.ts
```

## Architecture Rules

- **Schema definition.** Define tables in TypeScript.
- **Type-safe queries.** SQL-like syntax with TypeScript inference.
- **Migrations with Kit.** `drizzle-kit` for schema migrations.
- **Relations.** Define foreign keys and relations in schema.

## Coding Conventions

- Schema: `export const users = pgTable('users', { id: serial('id').primaryKey(), name: varchar('name', { length: 255 }).notNull(), email: varchar('email').notNull().unique() })`.
- Relations: `export const usersRelations = relations(users, ({ many }) => ({ posts: many(posts) }))`.
- Query: `const allUsers = await db.select().from(users).where(eq(users.id, 1))`.
- Insert: `await db.insert(users).values({ name: 'John', email: 'john@example.com' })`.

## NEVER DO THIS

1. **Never use `drizzle-orm` without `drizzle-kit`.** Migrations essential.
2. **Never skip running migrations.** `npx drizzle-kit push:pg`.
3. **Never forget to generate types.** After schema changes.
4. **Never use `any` in schema definitions.** Loses type safety.
5. **Never ignore the SQL output.** Check generated queries.
6. **Never skip foreign key constraints.** Define in schema.
7. **Never use `*` selects in production.** Specify columns.

## Testing

- Test with Docker PostgreSQL or SQLite.
- Test migrations up/down.
- Test relations query performance.


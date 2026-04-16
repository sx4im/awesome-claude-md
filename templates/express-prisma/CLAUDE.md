# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Express with Prisma
- Prisma 5.x
- Prisma Client
- Schema-first
- Type-safe queries

## Project Structure
```
prisma/
├── schema.prisma               // Prisma schema
└── migrations/
src/
├── routes/
│   └── users.ts
├── controllers/
│   └── userController.ts
└── prisma.ts                   // Prisma client singleton
```

## Architecture Rules

- **Schema-first.** Define database in `schema.prisma`.
- **Prisma Client.** Auto-generated, type-safe database client.
- **Singleton pattern.** Single PrismaClient instance.
- **Migrations.** Version control your database schema.

## Coding Conventions

- Schema: `model User { id Int @id @default(autoincrement()) email String @unique name String? createdAt DateTime @default(now()) }`.
- Client: `import { PrismaClient } from '@prisma/client'; const prisma = new PrismaClient()`.
- Query: `const users = await prisma.user.findMany({ where: { email: { contains: 'test' } }, include: { posts: true } })`.
- Create: `const user = await prisma.user.create({ data: { email: 'test@test.com', name: 'Test' } })`.

## NEVER DO THIS

1. **Never create multiple PrismaClient instances.** Use singleton.
2. **Never forget to run migrations.** `prisma migrate dev` or `deploy`.
3. **Never edit the generated client.** Changes lost on regeneration.
4. **Never skip connection management.** `$connect()` and `$disconnect()`.
5. **Never use raw queries without escaping.** Risk of SQL injection.
6. **Never ignore the `select` option.** Fetch only needed fields.
7. **Never forget to regenerate after schema changes.** `prisma generate`.

## Testing

- Test with test database.
- Test with Prisma's `jest` integration.
- Mock PrismaClient for unit tests.


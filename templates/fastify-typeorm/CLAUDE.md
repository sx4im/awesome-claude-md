# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fastify with TypeORM
- TypeORM 0.3+
- PostgreSQL/MySQL/SQLite
- Decorator-based entities
- Repository pattern

## Project Structure
```
src/
├── entity/
│   └── User.ts                 // TypeORM entities
├── migration/
├── routes/
│   └── users.ts
├── data-source.ts              // TypeORM connection
└── app.ts
```

## Architecture Rules

- **DataSource configuration.** Single source of truth for connection.
- **Entity decorators.** `@Entity`, `@Column`, `@PrimaryGeneratedColumn`.
- **Repository pattern.** `Repository<T>` for database operations.
- **Decorators with TypeScript.** `emitDecoratorMetadata` required.

## Coding Conventions

- Entity: `@Entity() export class User { @PrimaryGeneratedColumn() id: number; @Column() name: string; }`.
- DataSource: `export const AppDataSource = new DataSource({ type: 'postgres', host: 'localhost', entities: [User], synchronize: true })`.
- Repository: `const userRepository = AppDataSource.getRepository(User); await userRepository.find()`.
- Initialize: `await AppDataSource.initialize(); app.addHook('onClose', async () => { await AppDataSource.destroy() })`.

## NEVER DO THIS

1. **Never use `synchronize: true` in production.** Use migrations.
2. **Never forget `await dataSource.initialize()`.** Must connect before queries.
3. **Never skip entity registration.** Add all entities to DataSource.
4. **Never use `.save()` for updates without checking.** Can create duplicates.
5. **Never ignore lazy loading implications.** `relations: ['profile']` vs lazy.
6. **Never forget to handle `QueryFailedError`.** Database errors need handling.
7. **Never use `getRepository` in every request.** Cache or inject.

## Testing

- Test with test database.
- Test migrations up/down.
- Test repository methods.


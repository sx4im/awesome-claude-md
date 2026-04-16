# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Express with MikroORM
- MikroORM 6.x
- Data Mapper pattern
- Unit of Work
- TypeScript decorators

## Project Structure
```
src/
├── entities/
│   └── User.ts                 // MikroORM entities
├── migrations/
├── mikro-orm.config.ts         // Configuration
└── server.ts
```

## Architecture Rules

- **Identity Map pattern.** Entities tracked in EntityManager.
- **Unit of Work.** Changes flushed at end of transaction.
- **Lazy loading.** References loaded on demand.
- **Data Mapper.** Separate entities from database logic.

## Coding Conventions

- Entity: `@Entity() export class User { @PrimaryKey() id: number; @Property() name: string; @ManyToOne(() => Team) team: Team }`.
- Init: `const orm = await MikroORM.init(mikroOrmConfig)`.
- Query: `const em = orm.em.fork(); const users = await em.find(User, { age: { $gt: 18 } }, { populate: ['team'] })`.
- Persist: `const user = new User('John'); await em.persistAndFlush(user)`.

## NEVER DO THIS

1. **Never use global EntityManager.** Always fork: `orm.em.fork()`.
2. **Never forget `await em.flush()`.** Changes not persisted until flush.
3. **Never mutate entities after flush.** Detach or refetch.
4. **Never ignore the Identity Map.** Same ID returns same instance.
5. **Never skip migrations.** `npx mikro-orm migration:create`.
6. **Never forget to populate relations.** `populate: ['relation']`.
7. **Never use `em.clear()` unnecessarily.** Loses all tracked entities.

## Testing

- Test with `@mikro-orm/sqlite` in-memory.
- Test Unit of Work behavior.
- Test lazy loading with references.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Express with TypeORM
- TypeORM 0.3+
- Class decorators
- Repository pattern
- TypeScript

## Project Structure
```
src/
├── entity/
│   └── User.ts                 // TypeORM entities
├── controller/
│   └── UserController.ts       // Route controllers
├── repository/
└── data-source.ts              // TypeORM connection
```

## Architecture Rules

- **Active Record or Data Mapper.** Choose pattern per entity.
- **Repository injection.** Inject repositories into controllers.
- **Decorators.** `@Entity`, `@Column`, `@PrimaryGeneratedColumn`.
- **Async/await.** All TypeORM operations return promises.

## Coding Conventions

- Entity: `@Entity() export class User extends BaseEntity { @PrimaryGeneratedColumn() id: number; @Column() name: string; }`.
- Active Record: `const users = await User.find(); await User.save({ name: 'John' })`.
- Data Mapper: `const userRepo = AppDataSource.getRepository(User); const user = await userRepo.findOne({ where: { id: 1 } })`.
- Controller: `export class UserController { private userRepo = AppDataSource.getRepository(User); async getAll(req: Request, res: Response) { const users = await this.userRepo.find(); res.json(users) } }`.

## NEVER DO THIS

1. **Never use `synchronize: true` in production.** Always use migrations.
2. **Never forget to await TypeORM calls.** All operations are async.
3. **Never skip entity decorator metadata.** `emitDecoratorMetadata: true` in tsconfig.
4. **Never use `createQueryBuilder` for simple queries.** Repository methods are cleaner.
5. **Never ignore lazy loading behavior.** Understand when relations load.
6. **Never skip connection error handling.** `initialize().catch()`.
7. **Never forget to close connections.** `destroy()` on app shutdown.

## Testing

- Test with SQLite in-memory database.
- Test migrations separately.
- Test repository methods with mock data.


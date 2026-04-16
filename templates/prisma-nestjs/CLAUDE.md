# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Prisma with NestJS
- @nestjs/prisma
- Prisma Client
- Prisma Service pattern
- TypeScript

## Project Structure
```
src/
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── src/
│   ├── prisma/
│   │   ├── prisma.module.ts
│   │   └── prisma.service.ts   // PrismaClient wrapper
│   ├── users/
│   │   └── users.service.ts
│   └── app.module.ts
```

## Architecture Rules

- **Prisma Service.** Wrapper around PrismaClient for NestJS DI.
- **Module pattern.** `PrismaModule` exports `PrismaService`.
- **Service injection.** Use `PrismaService` in other services.
- **Lifecycle hooks.** Connect/disconnect with `onModuleInit`/`onModuleDestroy`.

## Coding Conventions

- Service: `@Injectable() export class PrismaService extends PrismaClient implements OnModuleInit { async onModuleInit() { await this.$connect(); } async enableShutdownHooks(app: INestApplication) { this.$on('beforeExit', async () => { await app.close(); }); } }`.
- Module: `@Module({ providers: [PrismaService], exports: [PrismaService] }) export class PrismaModule {}`.
- Usage: `@Injectable() export class UsersService { constructor(private prisma: PrismaService) {} async findAll() { return this.prisma.user.findMany(); } }`.

## NEVER DO THIS

1. **Never instantiate PrismaClient directly.** Always use PrismaService.
2. **Never skip `onModuleInit`.** Connection should be explicit.
3. **Never forget `enableShutdownHooks`.** Graceful shutdown.
4. **Never create multiple PrismaClient instances.** Use singleton pattern.
5. **Never ignore transaction handling.** Use `$transaction` for atomic ops.
6. **Never skip migration running.** Database must match schema.
7. **Never use raw queries without escaping.** Risk of SQL injection.

## Testing

- Test with test database or `prisma.$transaction` rollback.
- Test PrismaService lifecycle.
- Mock PrismaService for unit tests.


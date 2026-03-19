# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- NestJS 10+ (Node.js framework)
- TypeScript (strict mode)
- Prisma (or TypeORM/MikroORM) + PostgreSQL
- Jest for testing
- Class Validator & Class Transformer
- Passport for Authentication

## Project Structure

```
src/
├── app.module.ts              # Root module
├── main.ts                    # Application entry point
├── common/                    # Shared code across modules
│   ├── filters/               # Global exception filters
│   ├── interceptors/          # Request/response interceptors
│   ├── guards/                # Auth and role guards
│   ├── decorators/            # Custom decorators (e.g., @CurrentUser)
│   └── dto/                   # Shared DTOs (e.g., PaginationQueryDto)
└── modules/                   # Feature modules
    ├── users/
    │   ├── users.module.ts
    │   ├── users.controller.ts
    │   ├── users.service.ts
    │   ├── dto/
    │   │   ├── create-user.dto.ts
    │   │   └── update-user.dto.ts
    │   └── entities/          # Business logic entities or wrappers
    └── auth/
        ├── auth.module.ts
        ├── auth.controller.ts
        ├── auth.service.ts
        └── strategies/        # Passport strategies (jwt, local)
```

## Architecture Rules

- **Modular Architecture.** Nest uses Angular-like modules. Every feature (Users, Orders, Auth) gets its own module. Modules encapsulate controllers, services, and exports. Never put everything in `app.module.ts`.
- **Dependency Injection (DI).** Use constructor injection for all services and providers. Never instantiate services manually with `new Service()`. This is core to NestJS testability.
- **Controller ↔ Service Separation.** Controllers handle HTTP routes, extract parameters, and validate requests. They delegate business logic to Services. Services handle business logic and database access. Never put database queries in a controller.
- **Data Transfer Objects (DTOs).** Define strict class-based DTOs for request bodies. Use `class-validator` annotations (`@IsString()`, `@IsEmail()`). Enable Nest's `ValidationPipe` globally and set `whitelist: true` to automatically strip unvalidated properties.
- **Guards for Authorization.** Check roles and permissions using custom Guards (`@UseGuards(JwtAuthGuard, RolesGuard)`). Never perform auth checks inside controller logic or services unless they are highly dynamic business rules.

## Coding Conventions

- **Naming Conventions.** Files use kebab-case (`users.controller.ts`). Classes use PascalCase (`UsersController`). DTOs suffix with `Dto` (`CreateUserDto`).
- **Interfaces vs Classes for DTOs.** Always use `class` for DTOs. not TypeScript `interface`. TypeScript interfaces disappear at runtime, which breaks NestJS's runtime validation using decorators.
- **Return explicit types.** Always define return types on controller endpoints and service methods. Use generic wrapper types like `Promise<User>` or a custom `ResponseDto`.
- **Global Pipes and Filters.** Configure `ValidationPipe` globally in `main.ts`. Create an `AllExceptionsFilter` to catch and format unhandled errors consistently across the API.
- **Environment config.** Use `@nestjs/config` for environment variables. Create a typed configuration schema or validation using Joi/Zod to fail fast on startup if variables are missing.

## Library Preferences

- **ORM:** Prisma. not TypeORM (unless legacy). Prisma gives superior type inference and schema management.
- **Validation:** `class-validator` and `class-transformer`. built right into NestJS's ValidationPipe.
- **Authentication:** `@nestjs/passport`. wraps Passport.js cleanly into NestJS modules.
- **Logging:** `@nestjs/common` `Logger` or `nestjs-pino` for structured JSON logging.
- **API Documentation:** `@nestjs/swagger`. generates OpenAPI specs automatically from decorators on controllers and DTOs.

## NEVER DO THIS

1. **Never skip DTO validation.** An endpoint without a validated DTO is an injection vector. Always use `ValidationPipe` with `whitelist: true`.
2. **Never leak database errors to the client.** Catch Prisma/SQL exceptions in a global Exception Filter and map them to appropriate HTTP errors (`ConflictException`, `NotFoundException`).
3. **Never resolve cyclic dependencies with `forwardRef` if you can avoid it.** Circular module dependencies mean your domain boundaries are wrong. Refactor the shared logic into a common/third module instead.
4. **Never make an API call or DB query in a controller.** Controllers only handle the HTTP layer. All heavy lifting goes in `@Injectable()` services.
5. **Never use `req` or `res` objects directly unless necessary.** Use NestJS parameter decorators (`@Body()`, `@Query()`, `@Param()`). Accessing raw Express `res` forces you to handle the response lifecycle manually and breaks compatibility with Fastify.
6. **Never leave generic exceptions.** Throw specific HttpException classes provided by Nest: `throw new NotFoundException('User not found')` instead of `throw new Error()`.
7. **Never mutate data in a `GET` request.** Controllers should strictly map semantic HTTP methods (GET, POST, PATCH, PUT, DELETE) to the correct CRUD operations.

## Testing

- **Unit tests:** Use Jest (NestJS default). Mock dependencies in `Test.createTestingModule()`. Test services in isolation by mocking repositories/Prisma.
- **e2e tests:** Found in the `test/` directory. Boot the full application context with a test database using `INestApplication` and `supertest` to run integration tests against actual endpoints.
- Test endpoint validation logic to ensure DTOs reject bad data properly.

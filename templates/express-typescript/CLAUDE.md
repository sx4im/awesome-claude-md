# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Node.js 20+ with TypeScript 5.x (strict mode)
- Express 4.x (migrate to 5.x when stable)
- Prisma ORM + PostgreSQL
- Zod for request validation
- JWT authentication (access + refresh tokens)
- Vitest for testing

## Project Structure

```
src/
├── routes/
│   ├── users.routes.ts      # Route definitions only
│   ├── orders.routes.ts
│   └── index.ts             # Collects and exports all routers
├── controllers/
│   ├── users.controller.ts  # Request handling, calls services
│   └── orders.controller.ts
├── services/
│   ├── users.service.ts     # Business logic, calls Prisma
│   └── orders.service.ts
├── middleware/
│   ├── auth.ts              # JWT verification
│   ├── validate.ts          # Zod schema validation middleware
│   ├── error-handler.ts     # Global error handler
│   └── rate-limit.ts        # Rate limiting
├── schemas/
│   ├── user.schema.ts       # Zod schemas for request bodies
│   └── order.schema.ts
├── lib/
│   ├── prisma.ts            # Prisma client singleton
│   ├── logger.ts            # Pino logger setup
│   └── config.ts            # Environment validation with Zod
├── types/
│   └── express.d.ts         # Extended Express Request types
└── server.ts                # App factory + server startup
```

## Architecture Rules

- **Three-layer split: routes → controllers → services.** Routes define endpoints and attach middleware. Controllers extract request data and call services. Services contain business logic and database queries. Nothing else.
- **Routes never contain logic.** A route file is a list of `router.get()` / `router.post()` calls that wire paths to controllers with middleware in between.
- **Controllers never call Prisma directly.** They call service functions and return the result. Controller functions handle `req` and `res`. services never see Express types.
- **Every request body is validated with Zod.** Use the `validate` middleware with a Zod schema before the controller runs. Controllers can trust that `req.body` matches the schema.
- **App factory pattern.** `server.ts` exports a `createApp()` function that builds the Express app. This makes testing possible without starting a real HTTP server.

## Coding Conventions

- **Named exports everywhere.** `export function createUser()`. never `export default`. This applies to controllers, services, middleware, and schemas.
- **Async error handling:** wrap all async route handlers with a `catchAsync` wrapper that forwards errors to the global error handler. Never use try/catch in every controller.
- **Environment variables:** validate with Zod in `lib/config.ts` at startup. Import `config` throughout the app. never use `process.env` directly after the config module.
- **HTTP status codes:** use named constants from a status code enum or object. `return res.status(HTTP_STATUS.CREATED).json(data)`. not magic numbers.
- **Response envelope:** all API responses follow `{ success: boolean, data?: T, error?: { message: string, code: string } }`. Never return raw data or inconsistent shapes.

## Library Preferences

- **ORM:** Prisma. not TypeORM (decorator-based, less type-safe) and not Knex (too low-level for most CRUD apps). Prisma's generated client gives you exact types per query.
- **Validation:** Zod. not Joi (no TypeScript inference) and not express-validator (chainable API is harder to compose). Zod schemas double as TypeScript types with `.infer<>`.
- **Logging:** Pino. not Winston (Pino is faster, JSON-native, and has better structured logging). Use `pino-http` middleware for automatic request logging.
- **Auth:** JWT with `jose` library. not `jsonwebtoken` (jose is maintained, supports ESM, handles JWK sets). Use short-lived access tokens (15min) + long-lived refresh tokens (7d).
- **Rate limiting:** `express-rate-limit` for basic limits. For production, use Redis-backed rate limiting with `rate-limit-redis`.

## File Naming

- Routes: `{domain}.routes.ts` → `users.routes.ts`, `orders.routes.ts`
- Controllers: `{domain}.controller.ts` → `users.controller.ts`
- Services: `{domain}.service.ts` → `users.service.ts`
- Schemas: `{domain}.schema.ts` → `user.schema.ts`
- Middleware: `{name}.ts` → `auth.ts`, `validate.ts`, `error-handler.ts`
- Tests: co-located as `{name}.test.ts` → `users.service.test.ts`

## NEVER DO THIS

1. **Never put business logic in route handlers.** Routes wire URLs to controllers. If you're writing an `if` statement in a route file, you're in the wrong layer.
2. **Never use `any` for request types.** Extend Express's `Request` type in `types/express.d.ts` to add `user`, `session`, or other custom properties. Never cast `req as any`.
3. **Never use `console.log` for logging.** Use Pino. It's JSON-structured, has log levels, and doesn't silently disappear in production the way `console.log` outputs do.
4. **Never return stack traces in production error responses.** The global error handler should return a user-friendly message with an error code. Full stack traces go to logs only.
5. **Never store JWT secrets in code.** They come from environment variables, validated at startup. Rotate them without redeploying by using JWK sets.
6. **Never skip input validation.** Every `POST`, `PUT`, and `PATCH` endpoint must have a Zod schema. Unvalidated input is a security vulnerability, not a shortcut.
7. **Never use synchronous file operations.** `fs.readFileSync` blocks the event loop. Use `fs.promises` or `fs/promises` for all file I/O.

## Testing

- Use Vitest with `supertest` for HTTP-level tests against the app factory (no real server needed).
- Unit test services by mocking Prisma with `vitest-mock-extended`.
- Test middleware independently: create mock `req`/`res`/`next` and assert behavior.
- Integration tests use a test database with Prisma migrations, truncated between tests.

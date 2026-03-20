# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fastify 4+ (high-performance Node.js web framework)
- TypeScript (strict mode)
- JSON Schema (request/response validation via Fastify's built-in AJV)
- Prisma ORM + [PostgreSQL/MySQL]
- Pino (structured logging, built into Fastify)
- Vitest + @fastify/inject

## Project Structure

```
src/
├── app.ts                     # Fastify instance creation + plugin registration
├── server.ts                  # Server start (listen) entry point
├── plugins/
│   ├── auth.ts                # Authentication plugin (decorates request)
│   ├── prisma.ts              # Prisma client plugin (decorates fastify)
│   ├── sensible.ts            # @fastify/sensible for error helpers
│   └── swagger.ts             # @fastify/swagger + @fastify/swagger-ui
├── modules/
│   ├── [feature]/
│   │   ├── index.ts           # Route plugin (registers routes)
│   │   ├── schema.ts          # JSON Schemas for request/response
│   │   ├── handler.ts         # Route handler functions
│   │   ├── service.ts         # Business logic
│   │   └── types.ts           # TypeScript types derived from schemas
├── schemas/
│   └── common.ts              # Shared schemas (pagination, error responses)
├── lib/
│   ├── errors.ts              # Custom error classes
│   └── env.ts                 # Environment validation with @fastify/env
└── prisma/
    ├── schema.prisma
    └── migrations/
```

## Architecture Rules

- **Everything is a plugin.** Fastify's architecture is plugin-based. Database connections, auth, feature routes—all are encapsulated as plugins registered with `fastify.register()`. Never attach functionality to the Fastify instance outside a plugin.
- **Encapsulation is enforced by default.** Plugins registered with `fastify.register()` create an encapsulated context. Decorators and hooks inside a plugin are invisible to sibling plugins. Use `fastify-plugin` (fp wrapper) only when you intentionally need to break encapsulation (e.g., shared decorators).
- **JSON Schema validates everything.** Define request body, querystring, params, headers, and response schemas. Fastify compiles them with AJV for near-zero-cost validation. Never validate manually in handlers.
- **Handler functions are thin.** Handlers extract validated data from `request.body`, `request.params`, `request.query`, call service functions, and return the result. Fastify serializes the return value automatically. Never call `reply.send()` unless you need streaming.
- **Services own business logic and data access.** Services call Prisma, enforce authorization rules, and implement domain logic. Handlers never import Prisma directly.

## Coding Conventions

- **Use `Type Provider` for schema-to-type inference.** Install `@fastify/type-provider-json-schema-to-ts` or `@fastify/type-provider-typebox`. This derives TypeScript types from JSON Schemas at compile time. Never manually define types that mirror your schemas.
- **Return values, don't `reply.send()`.** Fastify handlers can simply `return { data }` and Fastify handles serialization. Using `reply.send()` bypasses response serialization schemas. Only use `reply.send()` for streams or manual control.
- **Register routes with `prefix` option.** When registering a module plugin, use `{ prefix: '/api/v1/users' }`. Never hardcode full paths in route definitions.
- **Use `fastify.log` everywhere.** Fastify wraps Pino. Use `request.log` in handlers (includes request ID) and `fastify.log` in plugins. Never use `console.log`—it's unstructured and loses request context.
- **Decorators for shared state.** Use `fastify.decorate('prisma', prismaClient)` and `fastify.decorateRequest('user', null)` for request-scoped data. Never use global variables or module-level singletons.

## Library Preferences

- **Validation:** JSON Schema with AJV (built-in). Use `@fastify/type-provider-typebox` for TypeBox or `json-schema-to-ts` for type inference. Never use Zod or Joi in Fastify—they bypass the optimized AJV pipeline.
- **Serialization:** Fastify's `response` schema with `fast-json-stringify` (automatic). Never use `JSON.stringify` manually.
- **Auth:** `@fastify/jwt` for JWT or `@fastify/passport` for strategy-based auth. Decorate requests with user data in a preHandler hook.
- **API docs:** `@fastify/swagger` + `@fastify/swagger-ui`. Auto-generated from JSON Schemas on routes.
- **Rate limiting:** `@fastify/rate-limit`. Configured as a global plugin. Never implement custom rate limiting.
- **Logging:** Pino (built-in). Configure log level in Fastify options. Use `pino-pretty` in development only.

## File Naming

- Route plugins: `src/modules/[feature]/index.ts`
- Schemas: `src/modules/[feature]/schema.ts`
- Handlers: `src/modules/[feature]/handler.ts`
- Services: `src/modules/[feature]/service.ts`
- Plugins: `src/plugins/[name].ts` (kebab-case)
- Shared schemas: `src/schemas/common.ts`

## NEVER DO THIS

1. **Never use Express middleware in Fastify.** Express middleware (e.g., `cors()`, `helmet()`) uses a different `(req, res, next)` signature. Use Fastify equivalents (`@fastify/cors`, `@fastify/helmet`). Express middleware will silently break or cause memory leaks.
2. **Never use `console.log` for logging.** Fastify integrates Pino deeply. Using `console.log` loses request IDs, structured formatting, and log level filtering. Always use `fastify.log` or `request.log`.
3. **Never skip response schemas.** Without a response schema, Fastify uses `JSON.stringify` (slow) and you risk leaking internal fields (passwords, tokens). Response schemas enable `fast-json-stringify` and act as an allow-list for output fields.
4. **Never wrap all plugins with `fastify-plugin` (fp).** The `fp` wrapper breaks encapsulation intentionally. Only use it for plugins that MUST decorate the parent context (auth, database). Feature route plugins should NEVER use `fp`.
5. **Never use `async` without returning or awaiting.** Fastify detects if a handler is async and expects a return value or a thrown error. Forgetting to return causes the request to hang indefinitely with no error.
6. **Never validate inside handlers when schemas exist.** Duplicating validation in handler code (e.g., `if (!body.email)`) is redundant when JSON Schema already validates. It adds overhead and creates inconsistencies.
7. **Never register the same plugin twice without `fastify-plugin` scoping.** Duplicate plugin registration throws `FST_ERR_PLUGIN_ALREADY_REGISTERED`. Use encapsulation or the `name` option to differentiate instances.

## Testing

- **Use `fastify.inject()` for route testing.** It simulates HTTP requests without starting a server. Returns a response object with `statusCode`, `json()`, and `headers`. No need for `supertest`.
- **Build the app fresh per test.** Import `buildApp()` (your app factory) in each test. This ensures clean plugin state and prevents test pollution. Never share a Fastify instance between test suites.
- **Test validation rejections.** Send invalid payloads and assert `400` responses with AJV error format. Validation is a critical part of Fastify's contract. Test that bad data is rejected, not just that good data works.
- **Service tests with mocked Prisma.** Use `vi.mock` to mock the Prisma client. Test service functions in isolation without a database. For integration tests, use a test database with Prisma migrations.
- Run tests: `npx vitest` (unit), `npx vitest --run` (CI), `npx vitest --coverage` (coverage report).

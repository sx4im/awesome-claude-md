# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Deno 2.x runtime with TypeScript (no build step, no node_modules)
- Oak 16+ middleware framework for HTTP routing
- Deno KV for persistent key-value storage (built into Deno runtime)
- Zod for request validation and schema definition
- djwt (deno.land/x/djwt) for JSON Web Token handling
- std library (jsr:@std/) for path, dotenv, datetime, and crypto utilities

## Project Structure

```
src/
  main.ts
  router.ts
  routes/
    auth.routes.ts
    user.routes.ts
  controllers/
    auth.controller.ts
    user.controller.ts
  services/
    auth.service.ts
    user.service.ts
  repositories/
    user.repository.ts
  middleware/
    auth.middleware.ts
    error.middleware.ts
  schemas/
    user.schema.ts
    auth.schema.ts
  kv/
    connection.ts
    indexes.ts
  types/
    mod.ts
deno.json
deno.lock
```

## Architecture Rules

- All imports use JSR packages (jsr:@std/) or deno.land/x/ URLs — never npm: for Oak ecosystem
- Repository pattern for all Deno KV access: controllers never touch KV directly
- Routes files define Oak Router instances, controllers handle request/response, services hold logic
- Deno KV keys follow hierarchical naming: ["users", id], ["users_by_email", email]
- Secondary indexes in KV are maintained manually in repository layer
- All KV mutations that affect multiple keys use atomic transactions (kv.atomic())

## Coding Conventions

- Use Deno's native TypeScript — no tsconfig.json needed, configure in deno.json
- Validate all incoming request bodies with Zod schemas before processing
- Oak context helpers: ctx.response.body for responses, ctx.state for request-scoped data
- Use Deno.env.get() for environment variables, loaded from .env via std/dotenv
- Prefer web standard APIs: crypto.subtle for hashing, fetch for HTTP calls

## Library Preferences

- HTTP framework: Oak (not Hono, Fresh, or Aleph)
- Validation: Zod — define schemas in dedicated .schema.ts files
- Database: Deno KV for primary storage; use npm:postgres if relational DB is needed
- Testing: Deno's built-in test runner with std/assert
- Task running: deno task defined in deno.json, not Makefiles or scripts
- Linting and formatting: deno lint and deno fmt with default rules

## File Naming

- All source files use kebab-case with dot-separated purpose: user.controller.ts
- Re-export files named mod.ts (Deno convention), not index.ts
- Schema files: singular-noun.schema.ts (user.schema.ts)
- Test files colocated as filename_test.ts (Deno convention, underscore not dot)

## NEVER DO THIS

1. Never use node_modules or package.json — this is a Deno project using deno.json
2. Never import without explicit file extensions — Deno requires .ts extensions in local imports
3. Never use KV .get() without handling the null/versionstamp case
4. Never mutate multiple KV keys without kv.atomic() — partial writes cause inconsistency
5. Never use Oak's ctx.request.body() without specifying the type option
6. Never skip --allow-net, --allow-read, --allow-env flags — declare them in deno.json tasks
7. Never use CommonJS require() or module.exports — Deno is ESM only

## Testing

- Use Deno.test() with the built-in test runner
- Create a test KV instance with Deno.openKv(":memory:") for isolated tests
- Use std/assert for assertions: assertEquals, assertRejects, assertThrows
- Test Oak routes using superoak for HTTP-level integration tests
- Mock services by passing dependency objects to controllers
- Run with: deno test --allow-net --allow-read --allow-env --coverage=coverage/

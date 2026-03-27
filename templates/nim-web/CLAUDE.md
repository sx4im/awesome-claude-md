# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: Nim 2.x with ARC/ORC memory management
- Backend Framework: Jester 0.6 HTTP framework (built on httpbeast for async I/O)
- Frontend Framework: Karax for single-page applications compiled to JavaScript
- Build Tool: nimble for project management, nim compiler with --mm:orc flag
- Database: norm ORM for SQLite/PostgreSQL, or db_connector for raw queries
- Templating: Source code filters with nimja or htmlgen for server-rendered HTML
- Package Manager: nimble with .nimble file dependency declarations

## Project Structure

```
src/
  app.nim                   # Jester server entry, route definitions, middleware
  config.nim                # Configuration loading from environment and JSON
  routes/
    user_routes.nim          # /users endpoint handlers
    auth_routes.nim          # /auth login/register/logout handlers
    api_routes.nim           # REST API route group
  models/
    user.nim                 # User object type with norm annotations
    session.nim              # Session token type and validation procs
  services/
    user_service.nim         # User business logic, validation, hashing
    auth_service.nim         # JWT creation with nim-jwt, bcrypt password handling
  db/
    connection.nim           # Database pool setup, transaction helpers
    migrations.nim           # Schema migration runner
  middleware/
    auth_middleware.nim       # JWT verification, request context injection
    logging_middleware.nim    # Structured request/response logging
  frontend/
    app.nim                  # Karax main entry, buildHtml DSL
    components/
      navbar.nim             # Navigation component with routing
      user_list.nim          # User listing with virtual DOM diffing
    api_client.nim           # Ajax calls via Karax's kxi module
  utils/
    response.nim             # JSON response builders, error formatters
    validation.nim           # Input validation proc chains
app.nimble                   # Package manifest with dependencies and tasks
config.json                  # Default runtime configuration
```

## Architecture Rules

- Route handlers are thin: parse request parameters, call service procs, return JSON responses.
- Service procs contain all business logic and return Result types or raise specific exceptions via `CatchableError` subtypes.
- All database access goes through procs in `db/` and `models/` modules. Route handlers never import db_connector directly.
- Karax frontend follows the single-state model: one `State` object rendered by a top-level `createDom` proc.
- Use Nim's effect system: annotate procs with `{.raises: [].}` or `{.raises: [DbError, IoError].}` to document and enforce error handling.
- Separate compile targets: backend compiles to C with `nim c`, frontend compiles to JS with `nim js`.

## Coding Conventions

- Proc names: camelCase. Type names: PascalCase. Module names: snake_case. Constants: camelCase.
- Use `object` types with explicit fields; avoid tuples for domain data.
- Prefer `Option[T]` from std/options over nil checks. Use `result` type from std/results for error handling.
- Pragmas on public API procs: `{.gcsafe.}` for async code, `{.raises: [SpecificError].}` for documented failures.
- Use `func` instead of `proc` for procs with no side effects to enable compiler optimizations.
- String formatting: use `std/strformat` with `fmt` macro, e.g., `fmt"{user.name} ({user.email})"`.

## Library Preferences

- HTTP server: Jester on httpbeast for production async performance
- JSON: std/json for serialization, jsony for high-performance parsing
- Database ORM: norm for typed database access with SQLite and PostgreSQL
- JWT: nim-jwt for token creation and verification
- Password hashing: nimcrypto for bcrypt, or bcrypt nimble package
- Logging: chronicles for structured logging with topics and severity levels
- Testing: std/unittest with suite/test blocks, testament for advanced test runner
- WebSocket: ws nimble package for real-time communication

## File Naming

- Source files: snake_case matching module content: `user_service.nim`, `auth_routes.nim`.
- One module per file. Modules group related types and procs.
- Frontend components: one file per component in `src/frontend/components/`.
- Test files: `tests/test_<module>.nim` with `t` prefix for test directory convention.

## NEVER DO THIS

1. Never use raw `ptr` or `pointer` types for application data; use `ref object` for heap allocation with ARC/ORC tracking.
2. Never use `{.gcsafe.}` cast to silence thread safety warnings without verifying there is no shared mutable state.
3. Never use `cast` between unrelated types; use explicit conversion procs with validation.
4. Never import `db_connector` or `norm` in route handler files; all DB access goes through service or db module procs.
5. Never use global `var` for request-scoped state; pass context through proc parameters or Jester's request object.
6. Never compile the frontend with `nim c`; always use `nim js` for Karax code targeting the browser.
7. Never use `os.sleep` in async code; use `sleepAsync` from std/asyncdispatch.

## Testing

- Run tests: `nimble test` which discovers and runs all `tests/test_*.nim` files.
- Use `std/unittest` with `suite` and `test` blocks: `check(result == expected)`, `expect(ExceptionType)`.
- Test Jester handlers by importing route procs directly and constructing mock Request objects.
- Database tests use an in-memory SQLite database initialized fresh per test suite.
- Frontend tests: compile Karax components with `nim js` and test with a headless browser or Node.js runtime.
- Run static analysis: `nim check src/app.nim` for type checking without compilation.
- CI pipeline: `nimble install --depsOnly && nimble test && nim c -d:release src/app.nim`.

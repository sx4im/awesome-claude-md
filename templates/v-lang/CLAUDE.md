# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: V 0.4.x with compile-time memory management and C interop
- Web Framework: vweb for HTTP routing with built-in template engine
- Build Tool: V compiler (v run, v build) with v.mod package manifest
- Database: Built-in ORM with PostgreSQL, SQLite, or MySQL backends
- Serialization: Built-in json module with attribute-based field mapping
- Frontend: vweb template files (.html) with V template syntax
- Package Manager: vpm (V Package Manager) or vpkg for dependencies

## Project Structure

```
src/
  main.v                    # vweb.run entry point, server configuration
  app.v                     # App struct definition with DB pool and shared state
  config.v                  # Configuration loading from environment and TOML
  routes/
    user_routes.v            # User endpoint handlers as App methods
    auth_routes.v            # Login/register/logout handlers
    api_routes.v             # JSON API endpoints with versioning
    static_routes.v          # Static file serving configuration
  models/
    user.v                   # User struct with ORM table mapping attributes
    session.v                # Session struct, token generation
  services/
    user_service.v           # User business logic, validation functions
    auth_service.v           # Password hashing, JWT token handling
  middleware/
    auth.v                   # Before_request handler for authentication
    cors.v                   # CORS header injection
    logging.v                # Request logging with timestamps
  templates/
    index.html               # vweb template with @{variable} interpolation
    users/
      list.html              # User listing template
      detail.html            # User detail template
    partials/
      header.html            # Shared header partial
      footer.html            # Shared footer partial
  db/
    connection.v             # Database connection setup and pooling
    migrations.v             # Schema migration runner
  utils/
    response.v               # JSON response builders, error formatters
    validation.v             # Input validation with error accumulation
static/
  css/
    style.css                # Application stylesheet
  js/
    app.js                   # Client-side JavaScript
tests/
  user_test.v                # Unit tests for user services
  api_test.v                 # HTTP integration tests
v.mod                        # Package manifest with version and dependencies
```

## Architecture Rules

- Route handlers are methods on the `App` struct. Keep them thin: parse input, call service, return response.
- The `App` struct holds shared state: database connection, configuration, caches. Passed implicitly to all handlers.
- Service functions are free functions (not methods) that accept explicit parameters, making them testable without the App context.
- Use V's built-in ORM for simple CRUD: `sql db { select from User where id == user_id }`. Drop to raw SQL for complex joins.
- Templates use vweb's built-in template engine with `@{expr}` for interpolation and `@if`/`@for` for logic.
- Before_request method on App handles middleware-like concerns: auth checks, logging, CORS headers.

## Coding Conventions

- Function names: snake_case. Struct names: PascalCase. Module names: snake_case. Constants: snake_case.
- All public functions need doc comments starting with `//`.
- Use `?` operator for propagating errors from `!` (result) return types: `result := do_thing() or { return err(err) }`.
- Prefer `or` blocks for error handling: `value := risky_fn() or { default_value }`.
- Use `struct` update syntax for immutable updates: `User{...existing_user, name: new_name}`.
- Prefer `arrays.map`, `arrays.filter`, `arrays.reduce` over manual for loops for data transformations.

## Library Preferences

- HTTP framework: vweb (standard library) for full-stack web applications
- JSON: Built-in `json.encode()` and `json.decode()` with struct attributes
- Database: Built-in `db.sqlite` or `db.pg` with ORM syntax
- Crypto: Built-in `crypto.bcrypt` for password hashing, `crypto.hmac` for signatures
- Logging: Built-in `log` module with levels: info, warn, error, debug
- Testing: Built-in `assert` in test functions, `v test .` runner
- HTTP client: Built-in `net.http` for outgoing requests
- TOML: Built-in `toml` module for configuration file parsing
- Regex: Built-in `regex` module for pattern matching and validation

## File Naming

- Source files: snake_case matching content domain: `user_routes.v`, `auth_service.v`.
- Group routes by resource in `routes/` directory, one file per resource.
- Template files: snake_case .html in `templates/` mirroring route structure.
- Test files: `<module>_test.v` suffix, in `tests/` directory.

## NEVER DO THIS

1. Never use `unsafe` blocks for pointer arithmetic unless wrapping a C library; V's memory model handles allocation safely.
2. Never use global mutable variables; store shared state in the App struct passed to handlers.
3. Never ignore `or` results from functions returning optionals; always handle the error case explicitly.
4. Never use `#include` C interop headers in application logic; isolate C bindings in dedicated wrapper modules.
5. Never use string concatenation in loops; use `strings.Builder` for efficient string assembly.
6. Never put business logic in vweb route handlers; extract into service functions for testability.
7. Never use `[manualfree]` attribute unless profiling proves the GC pause is a bottleneck.

## Testing

- Run tests: `v test tests/` which discovers all `*_test.v` files in the directory.
- Test functions are named `test_<description>` and use `assert` for assertions.
- HTTP integration tests: create test App instance with in-memory SQLite, call handlers directly.
- Test ORM operations against a test database initialized in test setup, cleaned in teardown.
- Use `$if test {` compile-time conditional for test-only code paths and mock configurations.
- Run with `v -stats test tests/` for timing information on each test.
- CI pipeline: `v fmt -verify . && v test tests/ && v -prod build src/main.v` to verify formatting, tests, and release build.

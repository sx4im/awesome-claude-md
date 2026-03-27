# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: Crystal 1.12+ with static typing and compile-time type inference
- Web Framework: Kemal 1.4 for HTTP routing with Crystal's Fiber-based concurrency
- Build Tool: Crystal compiler with shards for dependency management
- Database: crystal-db with crystal-pg (PostgreSQL) or crystal-sqlite3
- ORM: Granite ORM for Active Record pattern or Jennifer for more complex queries
- Serialization: JSON::Serializable module for automatic JSON mapping
- Templating: ECR (Embedded Crystal) for server-rendered views

## Project Structure

```
src/
  app.cr                    # Entry point, Kemal.run configuration
  config.cr                 # Environment-based config using ENV with defaults
  routes/
    user_routes.cr           # GET/POST/PUT/DELETE /users handlers
    auth_routes.cr           # POST /login, /register, /logout
    api_routes.cr            # API versioned routes /api/v1/*
  models/
    user.cr                  # User model with Granite columns and validations
    session.cr               # Session model, token generation
  services/
    user_service.cr          # User business logic, returns Result types
    auth_service.cr          # JWT via crystal-jwt, Crypto::Bcrypt for passwords
  middleware/
    auth_handler.cr          # Kemal::Handler subclass for JWT verification
    cors_handler.cr          # CORS headers handler for API routes
    request_logger.cr        # Structured JSON request logging
  views/
    layouts/
      application.ecr        # Base HTML layout with yield
    users/
      index.ecr              # User listing page
      show.ecr               # User detail page
  helpers/
    view_helpers.cr          # HTML escaping, date formatting helpers
    response_helpers.cr      # JSON response builders, error formatters
  db/
    migrations/
      001_create_users.cr    # Micrate migration: create_table :users
    seed.cr                  # Database seed data for development
spec/
  spec_helper.cr             # Test setup, database cleaner, factory methods
  routes/
    user_routes_spec.cr      # HTTP integration tests with test client
  models/
    user_spec.cr             # Model validation and persistence tests
  services/
    user_service_spec.cr     # Service layer unit tests
shard.yml                    # Dependency declarations
shard.lock                   # Locked dependency versions
```

## Architecture Rules

- Route handlers are thin: parse params, call services, render response. Maximum 15 lines per handler block.
- Service classes encapsulate business logic and return union types for success/failure: `User | ServiceError`.
- Models define schema, validations, and associations only. No HTTP or business logic in models.
- Custom Kemal::Handler subclasses for middleware. Register with `add_handler` in priority order.
- Use Crystal's union types and case/when for error handling instead of raising exceptions in service layers.
- ECR templates in `views/` for HTML responses; JSON::Serializable for API responses. Never mix concerns.

## Coding Conventions

- Class names: PascalCase. Method names: snake_case. Constants: SCREAMING_SNAKE_CASE. Files: snake_case.
- Use `record` for immutable value objects, `class` for entities with identity and behavior.
- Methods return explicit types: `def find_user(id : Int64) : User?` using nilable types for optional results.
- Use `getter` and `property` macros instead of manually writing getters/setters.
- Prefer `String::Builder` for string concatenation in loops over repeated `+` operations.
- Use `ensure` blocks for resource cleanup; prefer `File.open(path) do |f| ... end` block syntax.

## Library Preferences

- HTTP framework: Kemal for routing, HTTP::Server for custom low-level servers
- JSON: Built-in JSON::Serializable with annotations for field mapping
- Database: crystal-pg with Granite ORM; use raw crystal-db for complex queries
- Migrations: Micrate for SQL schema migrations with up/down methods
- JWT: crystal-jwt for token operations
- Password: Crypto::Bcrypt::Password from the standard library
- WebSocket: Kemal built-in WebSocket support via `ws "/path"` blocks
- Testing: Built-in Spec framework with describe/it/expect syntax
- HTTP client: HTTP::Client from stdlib for outgoing requests

## File Naming

- Source files: snake_case matching class or module name: `user_service.cr`, `auth_handler.cr`.
- One class or module per file. Nested types stay in the parent file if small.
- Route files group endpoints by resource: `user_routes.cr` for all `/users/*` routes.
- Spec files mirror source path: `spec/services/user_service_spec.cr`.

## NEVER DO THIS

1. Never use `as` casting without first checking with `is_a?`; it raises at runtime on type mismatch.
2. Never use `not_nil!` in production code; handle nil cases explicitly with `if obj = maybe_nil` pattern.
3. Never store database connections in class variables; use connection pooling via DB.open with a connection string.
4. Never use `spawn` without error handling; uncaught exceptions in fibers crash silently. Use `spawn(same_thread: true)` for debugging.
5. Never modify shard.lock manually; use `shards install` and `shards update` to manage dependencies.
6. Never use `pp` or `puts` for production logging; use the Log module with severity levels and backends.
7. Never define methods on `Object` or `Value`; Crystal's type hierarchy makes monkey-patching dangerous.

## Testing

- Run tests: `crystal spec` which runs all `spec/**/*_spec.cr` files.
- Use built-in Spec framework: `describe`, `it`, `expect(value).to eq(expected)`.
- HTTP integration tests: use `HTTP::Client` against a test server or Kemal's built-in test helpers.
- Database tests: wrap each test in a transaction and rollback via `DB.transaction do |tx| ... tx.rollback end`.
- Use factory methods in `spec_helper.cr` for creating test data: `def create_user(name = "Test") ... end`.
- Run with `crystal spec --order random` to detect test interdependencies.
- CI: `shards install && crystal spec && crystal tool format --check src/ spec/`.

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Rust (latest stable, 2024 edition)
- Actix-web 4 framework
- SQLx with compile-time checked queries
- PostgreSQL 15+ via `sqlx::PgPool`
- Tokio async runtime (Actix-web uses Tokio internally)
- serde / serde_json for serialization
- actix-web middleware for auth, logging, CORS

## Project Structure

```
src/
├── main.rs                  # Entry point: HttpServer::new, App::new, config
├── lib.rs                   # App factory fn for integration tests
├── config.rs                # Env-based config with envy or dotenvy
├── routes/
│   ├── mod.rs               # web::scope and web::resource composition
│   ├── users.rs             # /api/users endpoints
│   └── health.rs            # /health liveness + readiness
├── handlers/                # Thin handlers: extract → service → respond
│   ├── user_handler.rs
│   └── auth_handler.rs
├── services/                # Business logic, no Actix types allowed
│   ├── user_service.rs
│   └── auth_service.rs
├── models/
│   ├── user.rs              # Domain + DB row types with Serialize/Deserialize
│   ├── error.rs             # AppError implementing ResponseError
│   └── dto.rs               # Request/response DTOs separate from DB models
├── middleware/
│   ├── auth.rs              # JWT validation middleware
│   └── request_id.rs        # X-Request-Id propagation
├── extractors/
│   └── auth.rs              # FromRequest impl for AuthenticatedUser
└── db/
    ├── mod.rs               # PgPool creation
    └── queries/             # .sql files for sqlx::query_file!
```

## Architecture Rules

- **Handlers are thin.** Extract with `web::Json<T>`, `web::Path<T>`, `web::Data<AppState>`. Call a service. Return `Result<HttpResponse, AppError>`. Zero business logic in handlers.
- **Services never import `actix_web`.** Services take typed arguments and `&PgPool`. They return `Result<T, AppError>`. This makes them testable without spinning up an HTTP server.
- **`AppError` implements `actix_web::ResponseError`.** Map each variant to a status code and JSON body in `error_response()`. Handlers never manually build error responses.
- **State via `web::Data<AppState>`.** AppState holds PgPool, config, and shared clients. Register with `app.app_data(web::Data::new(state))`. Never use `lazy_static` for shared state.
- **Route composition in `routes/mod.rs`.** Each domain module exposes a `pub fn config(cfg: &mut web::ServiceConfig)`. The top-level configures: `cfg.service(web::scope("/api/users").configure(users::config))`.

## Coding Conventions

- **Error handling:** `thiserror` for AppError variants. Implement `From<sqlx::Error>`, `From<jsonwebtoken::errors::Error>`, etc. Never `.unwrap()` in handler or service code.
- **Serialization:** `#[derive(Serialize, Deserialize)]` with `#[serde(rename_all = "camelCase")]` on all DTOs. JSON responses are always camelCase regardless of Rust's snake_case fields.
- **Validation:** Use the `validator` crate with `#[derive(Validate)]` on request DTOs. Validate in the handler before passing to the service. Return 422 with per-field errors.
- **Logging:** `tracing` + `tracing-actix-web` for request spans. Add `#[tracing::instrument(skip(pool))]` to service functions. Use structured fields: `tracing::info!(user_id = %id, "created user")`.
- **Async:** All I/O is async. CPU-heavy work goes on `web::block()` or `tokio::task::spawn_blocking`. Never call `std::thread::sleep` or blocking I/O on the async runtime.

## Library Preferences

- **Web framework:** Actix-web 4. Not Axum for this project (Actix has mature middleware ecosystem, built-in WebSocket actors, and battle-tested performance). Not Rocket (less production usage, slower ecosystem adoption).
- **Database:** SQLx with compile-time checked queries. Not Diesel (SQLx lets you write real SQL). Not SeaORM (unnecessary abstraction over SQLx).
- **Auth:** `jsonwebtoken` for JWT. `argon2` for password hashing. Never bcrypt (argon2 is the modern standard, resistant to GPU attacks).
- **Serialization:** serde. Non-negotiable.
- **Error types:** `thiserror` for enums. `anyhow` only in main.rs or one-off scripts.

## File Naming

- All source files: `snake_case.rs` → `user_handler.rs`, `auth_service.rs`
- Modules with children: directory + `mod.rs` → `routes/mod.rs`, `routes/users.rs`
- SQL query files: `snake_case.sql` → `find_user_by_email.sql`
- Tests: inline `#[cfg(test)] mod tests` for unit tests; `tests/` directory for integration tests

## NEVER DO THIS

1. **Never use `.unwrap()` or `.expect()` in handlers or services.** Actix-web catches panics per-worker, but a panic still kills that worker's in-flight requests. Return `Result` and let `ResponseError` handle it.
2. **Never use `web::block` for async operations.** `web::block` moves work to a blocking threadpool. It is for CPU-bound or synchronous code only. Wrapping an async database call in `web::block` deadlocks when the threadpool is exhausted.
3. **Never share `PgPool` via `Clone` into closures.** Use `web::Data<AppState>` for all shared state. Cloning PgPool into `move` closures bypasses Actix's dependency injection and makes testing impossible.
4. **Never implement `FromRequest` with synchronous blocking I/O.** `FromRequest::from_request` runs on the async runtime. Database lookups in extractors must be async. Blocking here starves the event loop.
5. **Never return `HttpResponse::Ok().finish()` for errors.** Define `AppError` variants, implement `ResponseError`, and return `Err(AppError::NotFound)`. Manual status code juggling leads to inconsistent error shapes.
6. **Never put business logic in middleware.** Middleware handles cross-cutting concerns: auth token validation, request logging, CORS. Domain rules like "users can only edit their own profiles" belong in services.
7. **Never skip `cargo clippy -- -D warnings` in CI.** Clippy catches unused Results, redundant clones, and subtle logic bugs that compile fine but are wrong.

## Testing

- Unit tests: `#[cfg(test)] mod tests` in each service module. Test with a real test database via `sqlx::test`.
- Integration tests: `tests/` directory. Use `actix_web::test::init_service(app)` and `actix_web::test::call_service` to send real HTTP requests to the app without a network socket.
- Use `actix_web::test::TestRequest::post().uri("/api/users").set_json(&body).to_request()` for request construction.
- Run `cargo test`, `cargo clippy -- -D warnings`, and `cargo fmt --check` in CI. All three must pass.
- Mock external services (email, payment) with trait objects. Never mock the database—use `sqlx::test` with a real PostgreSQL instance.

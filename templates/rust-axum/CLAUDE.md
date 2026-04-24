# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Backend)

### Release Discipline
- Fail closed on authz/authn checks and input validation.
- Use explicit timeouts/retries/circuit-breaking for external dependencies.
- Preserve API compatibility unless breaking change is approved and documented.

### Merge/Release Gates
- Unit + integration tests and contract tests pass.
- Static checks pass and critical endpoint latency regressions reviewed.
- Structured error handling verified for all modified endpoints.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Rust (latest stable, 2024 edition)
- Axum 0.7+ web framework
- SQLx for compile-time checked SQL queries
- PostgreSQL 15+
- Tokio async runtime
- Tower middleware ecosystem

## Project Structure

```
src/
├── main.rs                  # Entry point: config loading, server startup
├── lib.rs                   # App builder, public API for integration tests
├── config.rs                # Configuration parsing from env vars
├── routes/
│   ├── mod.rs               # Router composition (merges all routers)
│   ├── users.rs             # /api/users handlers
│   └── health.rs            # /health endpoint
├── handlers/                # Request handlers (thin: extract, call service, respond)
├── services/                # Business logic (pure functions + database calls)
│   ├── user_service.rs
│   └── auth_service.rs
├── models/                  # Data types (domain models, DB row types)
│   ├── user.rs
│   └── error.rs             # AppError enum implementing IntoResponse
├── middleware/               # Tower middleware (auth, logging, rate limiting)
│   └── auth.rs
├── extractors/              # Custom Axum extractors
│   └── auth.rs              # AuthUser extractor from JWT
└── db/
    ├── mod.rs               # Pool creation
    └── queries/             # SQL files (if using sqlx::query_file!)
```

## Architecture Rules

- **Handlers are thin.** They extract data from the request (path params, query, body, extensions), call a service function, and return a response. No business logic in handlers.
- **Services own business logic.** They take typed arguments and a `PgPool` reference, perform validation and database operations, and return `Result<T, AppError>`. Services never see Axum types.
- **`AppError` implements `IntoResponse`.** Define an error enum in `models/error.rs` that maps to HTTP status codes. Handlers return `Result<Json<T>, AppError>`. Axum converts errors to responses automatically.
- **State is shared via Axum's `State` extractor.** Create an `AppState` struct containing `PgPool`, config, and shared clients. Pass it when building the router. Never use `lazy_static` or global mutable state.
- **Compile-time SQL verification.** Use `sqlx::query!` or `sqlx::query_as!` macros. They verify SQL against the database at compile time. Never use runtime string-built queries.

## Coding Conventions

- **Error handling:** use `thiserror` for error type definitions. `#[derive(thiserror::Error)]` on `AppError`. Map external errors with `impl From<sqlx::Error> for AppError`. Never use `.unwrap()` in handler or service code.
- **Serialization:** `serde` with `#[derive(Serialize, Deserialize)]`. Use `#[serde(rename_all = "camelCase")]` for JSON API responses. Field names in JSON are always camelCase even though Rust uses snake_case.
- **Request validation:** use `axum::extract::Json<T>` where `T: Deserialize` with `validator` crate for field-level validation. Return 422 with specific field errors, not 400 with a generic message.
- **Logging:** use `tracing` with `tracing-subscriber`. Add `#[tracing::instrument]` to every handler and service function. Use structured fields: `tracing::info!(user_id = %id, "user created")`.
- **Naming:** types are `PascalCase`, functions and variables are `snake_case`, constants are `SCREAMING_SNAKE_CASE`. Modules mirror the domain: `users`, `orders`, `auth`.

## Library Preferences

- **Web framework:** Axum. not Actix-web (Axum is Tower-native, better composability). Not Rocket (Axum has more momentum and Tower ecosystem access).
- **Database:** SQLx. not Diesel (SQLx uses compile-time checked raw SQL, Diesel's DSL is another language to learn). Not SeaORM (adds abstraction overhead without enough benefit over SQLx).
- **Serialization:** Serde. this isn't optional. Everything uses Serde.
- **Error types:** `thiserror` for library-style enum errors. `anyhow` only in `main.rs` or scripts where you don't need typed errors. Never use `anyhow` in library or service code.
- **Logging:** `tracing`. not `log` (tracing has spans, structured data, and async support).

## File Naming

- All files: `snake_case.rs` → `user_service.rs`, `auth.rs`
- Modules with multiple files: directory with `mod.rs` → `routes/mod.rs`, `routes/users.rs`
- SQL files (if separate): `snake_case.sql` → `get_user_by_id.sql`
- Tests: inline `#[cfg(test)] mod tests` for unit tests, `tests/` directory for integration tests

## NEVER DO THIS

1. **Never use `.unwrap()` in handler or service code.** It panics and kills the request (or the entire server in single-threaded contexts). Return `Result<T, AppError>` and let the error middleware handle it. `.unwrap()` is acceptable only in tests and `main()`.
2. **Never use `lazy_static` or global mutable state for app dependencies.** Use Axum's `State` extractor with an `AppState` struct. Global state is untestable and creates hidden coupling.
3. **Never build SQL strings at runtime.** Use `sqlx::query!` for compile-time verified queries. String concatenation is an SQL injection vulnerability. Parameterize everything.
4. **Never block the Tokio runtime.** CPU-heavy work goes on `tokio::task::spawn_blocking()`. Synchronous file I/O uses `tokio::fs`. Never call `std::thread::sleep()`. use `tokio::time::sleep()`.
5. **Never ignore the borrow checker by cloning everything.** If you're adding `.clone()` to make the compiler happy, you're papering over a design issue. Restructure ownership or use `Arc` deliberately with a comment explaining why.
6. **Never return raw database column types in API responses.** Map database row types to response types with explicit field selection. Internal IDs, timestamps, and audit fields should not leak to the API consumer.
7. **Never skip `cargo clippy`.** Run `cargo clippy -- -D warnings` in CI. Clippy catches real bugs: unused Results, redundant clones, and logic errors that compile but are wrong.

## Testing

- Unit tests: `#[cfg(test)] mod tests` in each module. Test service functions with a test database pool.
- Integration tests: `tests/` directory. Build the Axum app with `lib::create_app()`, use `axum::test::TestClient` or `reqwest` against a spawned server.
- Use `sqlx::test` macro for database tests. it creates a test database per test and rolls back transactions.
- Run `cargo test`, `cargo clippy`, and `cargo fmt --check` in CI. All three must pass.

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Rust 1.75+ (2021 edition) with rusqlite 0.31.x as the SQLite binding
- SQLite 3.45+ compiled with the bundled feature flag for reproducible builds
- r2d2-sqlite for connection pooling in multi-threaded server applications
- serde 1.x with serde_json for serializing query results
- tokio 1.x for async runtime when wrapping blocking rusqlite calls via `spawn_blocking`
- cargo-nextest for test execution, cargo-llvm-cov for coverage

## Project Structure

```
src/
  db/
    mod.rs                 # Pool initialization and configuration
    connection.rs          # Connection setup, PRAGMA configuration
    migrations.rs          # Schema migration runner (embedded SQL)
    pool.rs                # r2d2 pool configuration and helpers
  models/
    mod.rs
    user.rs                # User struct with FromRow implementation
    document.rs
    session.rs
  repositories/
    mod.rs
    user_repo.rs           # CRUD operations for users
    document_repo.rs
    traits.rs              # Repository trait definitions
  queries/
    user_queries.sql       # Raw SQL queries loaded at compile time
    document_queries.sql
  error.rs                 # Custom error type wrapping rusqlite::Error
  lib.rs
  main.rs
migrations/
  001_initial_schema.sql
  002_add_sessions.sql
  003_add_fts_index.sql
tests/
  common/
    mod.rs                 # Test database setup helpers
  integration/
    user_tests.rs
    document_tests.rs
```

## Architecture Rules

- Enable WAL (Write-Ahead Logging) mode on every connection open. Execute `PRAGMA journal_mode=WAL` immediately after opening. WAL allows concurrent readers with a single writer.
- Set `PRAGMA foreign_keys=ON` on every new connection. SQLite disables foreign key enforcement by default, and r2d2 creates fresh connections.
- Use a single r2d2 connection pool with `max_size` set to the number of CPU cores. SQLite's single-writer model means more connections only help for concurrent reads.
- Run all write operations through a dedicated function that acquires a connection, begins an `IMMEDIATE` transaction, and commits. This prevents `SQLITE_BUSY` errors by acquiring the write lock at transaction start.
- Embed migration SQL files using `include_str!()` and run them sequentially at application startup. Track applied migrations in a `_migrations` table.
- Use `STRICT` tables (SQLite 3.37+) for all new tables to enforce column type checking at the database level.

## Coding Conventions

- Implement `FromRow` manually for all model structs by extracting columns by name with `row.get::<_, Type>("column_name")`. Never use positional indexing.
- Use `rusqlite::params![]` macro for binding query parameters. Never format values into SQL strings.
- Wrap `rusqlite::Error` in a custom `DbError` enum using `thiserror`. Map specific error codes: `ErrorCode::ConstraintViolation` to a domain-specific `DuplicateEntry` variant.
- Return `Result<T, DbError>` from all repository methods. Never unwrap in library code.
- Use `conn.execute_batch()` for multi-statement DDL operations. Use `conn.prepare_cached()` for frequently executed queries to leverage the prepared statement cache.
- Define all SQL queries as constants in the repository module or load them with `include_str!()` from `.sql` files.

## Library Preferences

- rusqlite with `bundled` feature over linking to system SQLite (reproducible builds)
- r2d2-sqlite over creating connections manually for multi-threaded access
- thiserror over anyhow for library error types (anyhow is acceptable in binaries)
- serde for model serialization, not custom Display implementations
- refinery or rust-embed for migrations if the project outgrows `include_str!()`
- tokio::task::spawn_blocking for integrating rusqlite with async code

## File Naming

- All Rust files use snake_case: `user_repo.rs`, `connection.rs`
- SQL migration files use numbered prefixes: `001_initial_schema.sql`
- SQL query files use snake_case: `user_queries.sql`
- Test files go in `tests/integration/` with `_tests` suffix: `user_tests.rs`

## NEVER DO THIS

1. Never open SQLite in WAL mode without also setting `PRAGMA synchronous=NORMAL`. The default `FULL` synchronous in WAL mode adds unnecessary fsync calls with no safety benefit.
2. Never use `conn.execute()` for `SELECT` queries. Use `conn.prepare()` and `stmt.query_map()` to iterate over results.
3. Never hold a database connection across an await point. Acquire, use, and return the connection to the pool within a single `spawn_blocking` closure.
4. Never use `VACUUM` on a production database during runtime. It locks the entire database and rewrites the file. Schedule it during maintenance windows.
5. Never store large blobs (over 1MB) directly in SQLite. Store them as files and keep the file path in the database. SQLite performance degrades with large blobs.
6. Never disable the `PRAGMA busy_timeout`. Set it to at least 5000ms to handle write contention gracefully instead of immediately returning `SQLITE_BUSY`.
7. Never use `BEGIN DEFERRED` (the default) for write transactions. Use `BEGIN IMMEDIATE` to acquire the write lock upfront and avoid deadlocks.

## Testing

- Create an in-memory database (`:memory:`) for each unit test. Run migrations against it before each test to ensure schema consistency.
- Use `rusqlite::Connection::open_in_memory()` directly in tests; no need for the connection pool in unit tests.
- Test migration ordering by applying migrations one at a time and querying `sqlite_master` to verify table existence and column types.
- Integration tests use a temporary file-based database (via `tempfile::NamedTempFile`) to test WAL mode behavior, which requires a real file.
- Test concurrent read/write behavior by spawning multiple threads that read and one thread that writes, asserting no `SQLITE_BUSY` errors with proper `busy_timeout`.
- Test `FromRow` implementations by inserting known data and verifying the deserialized struct matches the expected values.

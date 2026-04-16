# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Axum (Tokio-based Rust web framework)
- Rust 1.75+
- Tower ecosystem
- Type-safe extractors
- Modular middleware

## Project Structure
```
src/
├── main.rs                     // Entry point
├── routes/
│   └── users.rs                // Route handlers
├── handlers/
│   └── user.rs                 // Request handlers
├── state.rs                    // App state
└── error.rs                    // Error types
```

## Architecture Rules

- **Tower-based.** Uses `tower` for middleware and services.
- **Extractors.** `Path`, `Query`, `Json` for request parsing.
- **IntoResponse.** Implement for custom responses.
- **State via extensions.** `Extension<State>` or `State<S>`.

## Coding Conventions

- Handler: `async fn get_user(Path(id): Path<u64>, State(pool): State<PgPool>) -> Result<Json<User>, AppError> { ... }`.
- Router: `Router::new().route("/users/:id", get(get_user))`.
- State: `Router::new().with_state(pool)`.
- Layers: `Router::new().layer(TraceLayer::new_for_http())`.
- IntoResponse: `impl IntoResponse for AppError { fn into_response(self) -> Response { ... } }`.

## NEVER DO THIS

1. **Never ignore the `State` extractor.** Type-safe state extraction.
2. **Never block the async runtime.** Use `spawn_blocking` for CPU-intensive work.
3. **Never forget to implement `IntoResponse` for errors.** Consistent error handling.
4. **Never use `unwrap` in handlers.** Propagate errors with `?`.
5. **Never ignore the `tower` ecosystem.** Rich middleware available.
6. **Never skip `tracing` setup.** Essential for production logging.
7. **Never use `Arc<State>` unnecessarily.** State is already shared.

## Testing

- Test with `axum::serve` and test requests.
- Test extractors with `Request::builder()`.
- Test layers/middleware separately.


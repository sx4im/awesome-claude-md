# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Actix Web (Rust web framework)
- Rust 1.75+
- Actor-based (optional)
- High performance
- Type-safe extractors

## Project Structure
```
src/
├── main.rs                     // Entry point
├── handlers/
│   └── users.rs                // Route handlers
├── models/
│   └── user.rs                 // Data models
├── middleware/
│   └── auth.rs                 // Middleware
└── routes.rs                   // Route configuration
```

## Architecture Rules

- **Actor system optional.** Can use without actors.
- **Extractors.** Type-safe request data extraction.
- **Middleware as transforms.** `wrap` and `wrap_fn`.
- **State management.** Application state shared across handlers.

## Coding Conventions

- Handler: `async fn get_user(info: web::Path<(u64,)>, db: web::Data<DbPool>) -> Result<HttpResponse, Error> { let user = sqlx::query_as::<_, User>(...).fetch_one(db.get_ref()).await?; Ok(HttpResponse::Ok().json(user)) }`.
- Route: `App::new().route("/users/{id}", web::get().to(get_user))`.
- State: `App::new().app_data(web::Data::new(pool))`.
- Middleware: `App::new().wrap(middleware::Logger::default())`.

## NEVER DO THIS

1. **Never block the thread.** Use `async` for all IO.
2. **Never ignore the `Data<T>` extractor.** For application state.
3. **Never forget error handling.** `Result` propagates errors.
4. **Never use `thread::spawn` directly.** Use `actix_rt::spawn`.
5. **Never ignore the `HttpServer::new` closure.** Called for each worker.
6. **Never skip `actix_web::main`.** Required runtime.
7. **Never use `unsafe` without need.** Actix is safe Rust—keep it that way.

## Testing

- Test with `actix_web::test`.
- Test extractors with `TestRequest`.
- Test middleware ordering.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Rocket (Rust web framework)
- Rust 1.75+
- Type-safe routing
- Async/await
- Built-in testing

## Project Structure
```
src/
├── main.rs                     // Entry point
├── routes/
│   ├── mod.rs                  // Route modules
│   └── users.rs
├── models/
│   └── user.rs                 // Data models
├── fairings/
│   └── auth.rs                 // Middleware
└── Rocket.toml                 // Configuration
```

## Architecture Rules

- **Declarative routing.** Attributes define routes: `#[get("/users")]`.
- **Type safety.** Route params, query strings, forms are typed.
- **Fairings.** Rocket's middleware system.
- **Built-in templating.** Handlebars integration.

## Coding Conventions

- Route: `#[get("/users/<id>")] fn get_user(id: u64) -> Json<User> { ... }`.
- Launch: `#[launch] fn rocket() -> _ { rocket::build().mount("/", routes![get_user]) }`.
- Fairing: `impl Fairing for MyFairing { ... }` then `rocket.attach(MyFairing)`.
- State: `#[get("/")] fn index(state: &State<MyState>) -> ...`.

## NEVER DO THIS

1. **Never ignore the `launch` attribute.** Required entry point.
2. **Never forget route mounting.** `mount("/", routes![...])`.
3. **Never skip type checking route params.** Rocket validates at compile time.
4. **Never use blocking operations.** Rocket is async—use `async`/`await`.
5. **Never ignore the `Responder` trait.** Implement for custom responses.
6. **Never forget to configure `Rocket.toml`.** Environment-specific settings.
7. **Never skip the `catchers!` macro.** For error handling.

## Testing

- Test with `rocket::local::blocking::Client`.
- Test routes with typed requests.
- Test fairing attachment.


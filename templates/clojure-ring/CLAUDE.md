# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: Clojure 1.12 on JVM 21 with virtual threads
- Web Framework: Ring 1.12 HTTP abstraction with Compojure routing
- Build Tool: Leiningen 2.x with profiles for dev/test/prod
- Database: next.jdbc 1.3 with HikariCP connection pooling and HoneySQL for query building
- Serialization: Cheshire for JSON, Transit for Clojure-to-Clojure communication
- Frontend: Hiccup for server-rendered HTML, or ClojureScript with Reagent if SPA
- REPL: nREPL with CIDER middleware for interactive development

## Project Structure

```
src/
  app/
    core.clj                # -main entry, system startup via Integrant or Mount
    config.clj              # Configuration loading from EDN files and env vars
    server.clj              # Jetty/http-kit server lifecycle
    routes.clj              # Compojure route definitions, defroutes macro
    middleware.clj           # Ring middleware stack: wrap-json, wrap-cors, wrap-auth
    handler/
      user.clj              # User endpoint handlers, ring request->response
      auth.clj              # Login/logout/token handlers
    db/
      core.clj              # DataSource setup, transaction helper macros
      user.clj              # User queries via HoneySQL, returns maps
      migrations.clj         # Migratus migration runner
    domain/
      user.clj              # User validation, business rules as pure functions
      auth.clj              # Token generation, password hashing with buddy-hashers
    util/
      response.clj          # Response builders: ok, created, bad-request, not-found
      validation.clj         # Spec-based or Malli validation helpers
resources/
  config.edn                # Default configuration map
  migrations/               # SQL migration files: 001-create-users.up.sql
dev/
  user.clj                  # Dev namespace with REPL helpers, system reset
project.clj                 # Leiningen project definition
```

## Architecture Rules

- Handlers are thin: destructure the Ring request map, call domain functions, return a response map.
- Domain functions are pure: they take data and return data. No side effects, no database calls.
- Database functions live in `db/` namespace and return plain Clojure maps. No ORM objects.
- Use Integrant or Mount for stateful component lifecycle (DB pool, server, caches). Never use global def for stateful resources.
- Middleware is composed in a specific order in `middleware.clj`. Authentication wraps inside routing.
- All configuration reads from `config.edn` merged with environment variables. No hardcoded values.

## Coding Conventions

- Namespace names match directory path: `app.handler.user` for `src/app/handler/user.clj`.
- Use `defn-` for private functions. Prefer small, composable functions over large multi-arity ones.
- Destructure maps in function arguments: `(defn create-user [{:keys [email name password]}] ...)`.
- Use threading macros `->` for object-like transforms and `->>` for sequence operations.
- Keywords for map keys, never strings. Use namespaced keywords for domain entities: `:user/email`, `:user/name`.
- Prefer `when` over `(if x y nil)`. Use `cond` with `:else` for multi-branch logic.

## Library Preferences

- HTTP server: http-kit for async/WebSocket or ring-jetty-adapter for simplicity
- Routing: Compojure with defroutes, or Reitit for data-driven routing
- JSON: Cheshire for parse/generate, ring-json middleware for automatic body handling
- Database: next.jdbc with HoneySQL; avoid raw SQL strings in handler code
- Validation: Malli for data-driven schemas, clojure.spec.alpha for function contracts
- Auth: Buddy for JWT tokens and password hashing (buddy-sign, buddy-hashers)
- Logging: tools.logging with Logback backend, structured via clojure.tools.logging

## File Naming

- snake_case for filenames: `user_handler.clj`, but kebab-case for namespaces: `user-handler`.
- One namespace per file. Namespace matches directory structure exactly.
- Test files: `test/app/handler/user_test.clj` mirroring source with `_test` suffix.

## NEVER DO THIS

1. Never use `def` inside a function body for stateful bindings; use `let` or atoms explicitly.
2. Never use `swap!` on a global atom for request-scoped state; pass state through function arguments or use dynamic vars with `binding`.
3. Never call `System/exit` in library code; only in `-main`. Use exceptions or error maps for failures.
4. Never use `eval` or `resolve` for dynamic dispatch in production code; use multimethods or protocols.
5. Never put database calls inside domain functions; keep domain logic pure and testable.
6. Never use `future` without error handling; unhandled exceptions in futures are silently swallowed.

## Testing

- Run tests: `lein test` or `lein test :only app.handler.user-test` for focused runs.
- Use clojure.test: `deftest` with `testing` blocks and `is` assertions.
- Test handlers by calling them directly with mock Ring request maps: `(handler {:request-method :get :uri "/users"})`.
- Database tests use a test profile with a separate database; wrap each test in a rolled-back transaction via `next.jdbc/with-transaction`.
- Use `with-redefs` sparingly for mocking external services; prefer dependency injection via component arguments.
- REPL workflow: evaluate forms in CIDER, use `(reset)` in dev namespace to reload changed code.
- Run `lein check` and `lein kibit` for static analysis before committing.

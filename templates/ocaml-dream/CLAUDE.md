# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: OCaml 5.x with effect handlers and multicore support
- Web Framework: Dream 1.0 (Lwt-based HTTP with WebSocket support)
- Build System: Dune 3.x with dune-project and per-directory dune files
- Package Manager: opam 2.x with .opam file pinning
- Database: Caqti for connection pooling with type-safe SQL via Petrol or Rapper
- Serialization: Yojson for JSON, ppx_yojson_conv for derived serializers
- HTML: Tyxml for type-safe HTML generation, Dream.html for raw responses

## Project Structure

```
bin/
  main.ml                  # Server startup, Dream.run configuration
  dune                     # Executable target linking app library
lib/
  app.ml                   # Dream router, middleware stack
  handler/
    user_handler.ml         # Request handlers for /users endpoints
    auth_handler.ml         # Login/logout/session handlers
  model/
    user.ml                 # User type with yojson derivation
    session.ml              # Session token types and validation
  service/
    user_service.ml         # Business logic, orchestrates DB and validation
    auth_service.ml         # Password hashing with Bcrypt, JWT with Jose
  repo/
    user_repo.ml            # Caqti queries for user CRUD
    db.ml                   # Connection pool setup, migration runner
  middleware/
    auth_middleware.ml       # Dream.middleware for session verification
    logging.ml               # Request/response structured logging
  dune                      # Library target with ppx and dependencies
test/
  test_user_service.ml      # Alcotest unit tests for service layer
  test_handlers.ml          # Integration tests using Dream.test
  dune                      # Test runner configuration
dune-project                # Project metadata, opam generation
app.opam                    # Generated opam file with dependencies

```

## Architecture Rules

- All handlers are thin: parse request, call service, format response. No business logic in handlers.
- Service functions return `(result, error) Lwt.t` and never raise exceptions. Wrap all external calls with `Lwt.catch`.
- Database queries go through the `repo/` layer. Handlers and services never construct SQL directly.
- Domain types in `model/` are pure OCaml records with `[@@deriving yojson]`. No framework dependencies in model files.
- Use Dream.middleware for cross-cutting concerns. Each middleware is a standalone module with a `wrap` function.
- All async operations use Lwt. Never use `Lwt_main.run` inside library code; only in `bin/main.ml`.

## Coding Conventions

- Module names: PascalCase matching file name. Function names: snake_case. Type names: snake_case.
- Use labeled arguments (`~name`) for functions with more than two parameters of the same type.
- Pattern match with explicit variants; avoid catch-all `| _ ->` on variant types.
- Prefer `Result.bind` and `let*` / `let+` ppx syntax over nested match expressions.
- Use `Option.value ~default:` instead of match on `Some/None` for simple defaults.
- Module signatures (.mli files) required for all public-facing modules in `lib/`.

## Library Preferences

- HTTP client: Cohttp_lwt_unix for outgoing HTTP requests
- JSON: Yojson.Safe.t as interchange format, ppx_yojson_conv for derivation
- Password hashing: Bcrypt via bcrypt opam package
- JWT: Jose library for token creation and verification
- Logging: Logs library with Dream.logger middleware for request logs
- Testing: Alcotest for unit tests, Dream.test for handler integration tests
- Validation: Custom validation module returning `(value, string list) result`

## File Naming

- One module per file, snake_case: `user_handler.ml`, `auth_service.ml`.
- Interface files: `user_handler.mli` alongside every public `.ml` file.
- Test files: `test_<module>.ml` prefix convention in `test/` directory.
- Dune files: one per directory, declaring library or executable targets.

## NEVER DO THIS

1. Never use `Obj.magic` or `Obj.repr` to bypass the type system; refactor types instead.
2. Never call `Lwt.async` without an error handler; use `Lwt.on_failure` or `Lwt.dont_wait`.
3. Never store database connection handles in global mutable state; pass the Caqti pool through Dream's app context.
4. Never use `open!` at the top level for large modules like `Lwt`; use local opens `let open Lwt.Syntax in`.
5. Never write raw SQL strings in handler code; all queries must be Caqti typed requests in `repo/` modules.
6. Never use `Unix.sleep` in async code; use `Lwt_unix.sleep` instead.
7. Never catch all exceptions with `try ... with _ ->`; match specific exception types.

## Testing

- Run tests: `dune runtest` which discovers all test executables.
- Unit tests use Alcotest: `Alcotest.(check string) "label" expected actual`.
- Handler tests use `Dream.test` to create mock requests: `Dream.test handler @@ Dream.request ~method_:`GET "/path"`.
- Database tests use a dedicated test database; `repo/db.ml` reads `DATABASE_URL` from environment.
- Use `Lwt_main.run` in test setup to run async test cases.
- CI runs `opam install . --deps-only --with-test && dune runtest` in a locked opam switch.

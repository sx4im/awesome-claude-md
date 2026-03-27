# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: Gleam 1.x targeting Erlang/BEAM runtime
- Frontend Framework: Lustre 4.x for type-safe SPAs with TEA (The Elm Architecture)
- Backend: Wisp HTTP framework on top of Mist server
- Build Tool: gleam build / gleam run / gleam test
- Package Manager: Hex packages via gleam add
- Database: Sqlight for SQLite or Gleam PGO for PostgreSQL
- Serialization: gleam/json and gleam/dynamic for JSON encode/decode

## Project Structure

```
src/
  app.gleam               # Application entry, starts Wisp server
  router.gleam             # HTTP route definitions, pattern matching on path segments
  web/
    middleware.gleam        # Request logging, auth, CORS middleware
    responses.gleam         # Shared response builders, error formatters
  client/
    app.gleam               # Lustre client entry, init/update/view
    model.gleam             # Application Model type and init function
    msg.gleam               # Msg union type for all user actions
    components/
      nav.gleam             # Navigation bar component with sub-messages
      form.gleam            # Reusable form component with validation
    effects.gleam           # Side effects: HTTP calls, localStorage, timers
  db/
    queries.gleam           # SQL query functions returning Result types
    schema.gleam            # Row decoder functions using dynamic.decode
  shared/
    types.gleam             # Types shared between client and server
    validation.gleam        # Validation logic reused on both targets
test/
  app_test.gleam            # Router integration tests
  client/
    model_test.gleam        # Update function unit tests
```

## Architecture Rules

- Follow The Elm Architecture strictly: Model holds all state, Msg describes every possible event, update is pure.
- Every Lustre component that manages sub-state must define its own Model and Msg types and a dedicated update function.
- Server routes return `wisp.Response` and never panic; all errors flow through Result types.
- Use `gleam/dynamic` decoders for all external data (JSON, DB rows, form input). Never use unsafe casts.
- Shared types in `src/shared/` must compile to both Erlang and JavaScript targets. No target-specific imports there.
- Effects in Lustre must go through `lustre/effect.from` and never perform side effects in `update`.

## Coding Conventions

- Function names: snake_case. Types: PascalCase. Module names: snake_case matching file name.
- All public functions require doc comments starting with `///`.
- Use `use` expressions for monadic chaining with Result and Option instead of nested case expressions.
- Pattern match exhaustively; never use a wildcard `_` catch-all on custom types to ensure new variants cause compile errors.
- Pipe operator `|>` for data transformation chains; keep each step on its own line when chaining more than two.

## Library Preferences

- HTTP client: gleam_httpc on server, lustre_http on client
- JSON: gleam_json for encoding, gleam/dynamic decoders for decoding
- UUID: gleam_uuid for unique identifiers
- Time: birl for datetime handling across targets
- Crypto: gleam_crypto for hashing and token generation
- HTML: lustre/element/html for type-safe HTML, nakai for server-side rendering

## File Naming

- One module per file, file name matches module name in snake_case.
- Components live in `src/client/components/` with one file per component.
- Test files mirror source structure under `test/` with `_test.gleam` suffix.

## NEVER DO THIS

1. Never use `let assert` in production code paths; it crashes the process. Reserve it only for tests.
2. Never import Erlang FFI modules in code that must also compile to JavaScript.
3. Never put side effects inside the `update` function; use `lustre/effect` for all side effects.
4. Never use `dynamic.unsafe_coerce`; always decode with proper dynamic decoders.
5. Never store server secrets in shared modules; keep credentials in environment variables read via `gleam/erlang/os.get_env`.
6. Never mutate state outside the Model; Lustre components must be purely functional.

## Testing

- Run tests: `gleam test` which executes all `_test.gleam` files.
- Use `gleeunit` for test organization with `gleeunit.main()` as runner.
- Test Lustre update functions by calling `update(model, msg)` directly and asserting on the returned Model.
- Use `wisp/testing` module to create test requests and assert on responses for router tests.
- Test dynamic decoders with known-good and known-bad JSON strings to verify error messages.
- Run both targets: `gleam test --target erlang` and `gleam test --target javascript` for shared modules.

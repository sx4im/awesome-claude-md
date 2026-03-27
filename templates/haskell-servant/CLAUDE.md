# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: Haskell (GHC 9.6+) with GHC2021 language standard
- Web Framework: Servant 0.20 for type-level HTTP API definitions
- Build Tool: Cabal 3.10 (preferred) or Stack 2.x with resolver lts-22
- Database: Persistent with Esqueleto for type-safe SQL queries, PostgreSQL backend
- Serialization: Aeson for JSON with Generic deriving and custom ToJSON/FromJSON instances
- Authentication: Servant-auth with JWT tokens
- Logging: Katip structured logging with JSON output

## Project Structure

```
app/
  Main.hs                  # Entry point, reads config, starts Warp server
src/
  Api.hs                   # Top-level Servant API type combining all sub-APIs
  Api/
    User.hs                # UserAPI type definition with Capture, ReqBody, etc.
    Auth.hs                # AuthAPI type with login/register endpoints
  Server.hs                # Top-level server implementation, natural transformation
  Server/
    User.hs                # UserAPI handler implementations in AppM monad
    Auth.hs                # AuthAPI handlers, JWT issuance
  Domain/
    User.hs                # User domain type, Persistent model via quasiquoter
    Types.hs               # Newtypes: UserId, Email, HashedPassword
  Effect/
    Database.hs            # MonadDatabase class, Persistent pool operations
    Auth.hs                # MonadAuth class, JWT verification/signing
  Config.hs                # AppConfig record, environment variable parsing via Env
  AppM.hs                  # Application monad: ReaderT AppConfig (LoggingT IO)
test/
  Spec.hs                  # Hspec discovery main module
  Api/
    UserSpec.hs             # Servant client-based integration tests
    AuthSpec.hs             # Auth flow integration tests
  Domain/
    UserSpec.hs             # Property tests with QuickCheck for domain logic
package.yaml               # hpack configuration (generates .cabal)
cabal.project              # Multi-package project config with constraints
```

## Architecture Rules

- The Servant API type is the single source of truth. Handlers, clients, and docs are all derived from it.
- Business logic lives in `Domain/` and `Effect/` modules. Servant handlers only parse input, call domain functions, and format output.
- Use the `AppM` monad (ReaderT over IO) for all handlers. Access config and DB pool via `asks`.
- Define MTL-style typeclasses in `Effect/` for database and external service access to enable test mocking.
- All domain types must have Aeson instances. Use `deriveJSON defaultOptions{fieldLabelModifier = camelTo2 '_'}` for consistency.
- Error handling: return `ServerError` from handlers via `throwError`. Never use `error` or `undefined`.

## Coding Conventions

- Enable `OverloadedStrings`, `DeriveGeneric`, `TypeOperators`, `DataKinds` in default-extensions.
- Use explicit import lists or qualified imports. Never use unqualified `Prelude` alternatives.
- Newtypes for all domain identifiers: `newtype UserId = UserId Int64 deriving (Eq, Show, FromHttpApiData, ToJSON)`.
- Record syntax for all data types with more than two fields. Use `HasField` or lens for access.
- Type signatures on all top-level bindings. Use `-Wall -Werror` in CI.
- Prefer `Text` over `String` everywhere. Use `Data.Text` and `Data.Text.Encoding` for conversions.

## Library Preferences

- HTTP server: Warp as the underlying server for Servant
- JSON: Aeson with Generic deriving, custom instances only when field names differ
- Database: Persistent for schema/migrations, Esqueleto for complex queries
- Validation: Validation applicative from `validation` package for accumulating errors
- Config: Envparse (System.Envy) for reading typed config from environment variables
- Logging: Katip for structured JSON logs with context, co-log as alternative
- Testing: Hspec for structure, QuickCheck for properties, servant-client for API tests

## File Naming

- One module per file, PascalCase matching module path: `src/Api/User.hs` for `Api.User`.
- Test files: `test/Api/UserSpec.hs` with `Spec` suffix, discovered by hspec-discover.
- Keep module hierarchy shallow: maximum three levels deep.

## NEVER DO THIS

1. Never use `String` for data that crosses module boundaries; use `Text` or `ByteString`.
2. Never use partial functions (`head`, `tail`, `fromJust`, `read`) in production code; use safe alternatives from `safe` or pattern match.
3. Never use `unsafePerformIO` or `unsafeCoerce` outside of clearly marked, reviewed FFI wrappers.
4. Never derive `Read` for types used in parsing; use Aeson or custom parsers with proper error handling.
5. Never use `IO` directly in domain logic; abstract through MTL-style typeclasses for testability.
6. Never leave orphan instances; define them in the module where the type or class is defined.
7. Never use Template Haskell splices that generate code at module scope without a clear comment explaining the generated API.

## Testing

- Run tests: `cabal test` or `stack test` which runs hspec-discover.
- Unit tests for pure domain logic using Hspec `describe/it` blocks with `shouldBe`, `shouldSatisfy`.
- Property tests with QuickCheck: derive `Arbitrary` for domain types, test roundtrip JSON encoding.
- Integration tests: spin up Warp on a random port, use `servant-client` to call endpoints programmatically.
- Database tests: use `persistent-test` with an in-memory SQLite backend for fast isolation.
- CI: `cabal build all && cabal test all --test-show-details=streaming`.

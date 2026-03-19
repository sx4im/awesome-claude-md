# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Go 1.22+
- Chi router (or standard library `net/http` with Go 1.22+ routing)
- PostgreSQL with `pgx` driver
- `sqlc` for type-safe SQL
- `slog` for structured logging
- Docker for deployment

## Project Structure

```
.
├── cmd/
│   └── server/
│       └── main.go          # Entry point: config, DI, server start
├── internal/
│   ├── api/
│   │   ├── handler/         # HTTP handlers (one file per domain)
│   │   ├── middleware/       # Auth, logging, recovery, CORS
│   │   └── router.go        # Route registration
│   ├── domain/              # Business logic and domain types
│   │   ├── user.go          # User type + UserService interface
│   │   └── order.go
│   ├── repository/          # Database access (implements domain interfaces)
│   │   ├── user_repo.go
│   │   └── queries/         # sqlc generated code
│   ├── service/             # Service implementations
│   │   ├── user_service.go
│   │   └── order_service.go
│   └── config/
│       └── config.go        # Environment parsing with envconfig
├── migrations/              # SQL migration files
├── sqlc.yaml                # sqlc configuration
├── Dockerfile
├── docker-compose.yml
└── go.mod
```

## Architecture Rules

- **Everything domain-specific lives in `internal/`.** The `internal` directory is Go's built-in access control. nothing outside this module can import it. Use it.
- **`cmd/` is for entry points only.** `main.go` parses config, creates dependencies, wires them together, and starts the server. No business logic. No route definitions.
- **Domain types define interfaces, implementations live elsewhere.** `domain/user.go` defines `type UserService interface` and `type UserRepository interface`. `service/user_service.go` implements `UserService`. `repository/user_repo.go` implements `UserRepository`.
- **Dependency injection via constructor functions.** `NewUserService(repo UserRepository, logger *slog.Logger) *userService`. No global variables. No `init()` functions with side effects.
- **Handlers are methods on a struct that holds dependencies.** `type UserHandler struct { svc domain.UserService }`. This makes testing trivial. inject a mock service.

## Coding Conventions

- **Error handling:** always check errors. Never use `_` to discard an error. Wrap errors with context: `fmt.Errorf("getting user %s: %w", id, err)`. Use custom error types for domain errors (`ErrNotFound`, `ErrConflict`).
- **Naming:** Go conventions. short variable names in small scopes (`u` for user in a 5-line function), descriptive names in larger scopes. Interfaces end with `-er` when single-method: `Reader`, `Writer`, `Validator`.
- **Context propagation:** every function that does I/O takes `ctx context.Context` as its first parameter. Handlers extract it from `r.Context()` and pass it down.
- **Struct tags:** use `json:"snake_case"` for JSON serialization. Use `db:"column_name"` for database mapping. Never expose Go PascalCase field names in JSON responses.
- **No frameworks for business logic.** Chi is fine for routing. stdlib is fine for HTTP. But business logic uses plain Go. no ORMs, no magic.

## Library Preferences

- **Router:** Chi. not Gin (Chi is stdlib-compatible, Gin uses a custom context), not Fiber (non-stdlib, opaque request handling). With Go 1.22+, stdlib routing is also viable for simple APIs.
- **Database:** `pgx` + `sqlc`. not GORM (hides SQL behind magic, generates unpredictable queries), not `sqlx` (sqlc generates type-safe code from SQL you write). Write SQL, get Go code.
- **Logging:** `slog` (stdlib). not `zap` (slog is now stdlib and good enough for most apps), not `logrus` (deprecated in favor of structured logging).
- **Config:** `envconfig` or `env`. not Viper (too heavy for most Go services, pulls in YAML/TOML/JSON parsers you don't need).
- **Migrations:** `goose` or `golang-migrate`. not running DDL in application code.

## File Naming

- All files: `snake_case.go` → `user_handler.go`, `order_service.go`
- Test files: `_test.go` suffix → `user_handler_test.go`
- Packages: single lowercase word → `handler`, `service`, `repository`, `middleware`
- One primary type per file. `user.go` defines `User` and its methods. Don't put `Order` in the same file.

## NEVER DO THIS

1. **Never ignore errors.** `result, _ := doSomething()` is a bug waiting to happen. If you genuinely don't need the error, document why with a comment. Better yet, handle it.
2. **Never use global mutable state.** No package-level `var db *sql.DB`. Pass dependencies through constructors. Global state makes testing impossible and concurrency dangerous.
3. **Never use `init()` for anything besides simple registration (like SQL drivers).** Complex initialization in `init()` runs before `main()`, can't be tested, and creates import-order dependencies.
4. **Never use GORM for new projects.** It generates unpredictable SQL, makes N+1 queries easy to miss, and its API changes between major versions. Use `sqlc`. write the SQL you want, get type-safe Go code.
5. **Never use `panic` for recoverable errors.** Return errors. `panic` is for genuinely unrecoverable situations (programmer bugs, impossible states). HTTP handlers should never panic.
6. **Never embed a mutex by value.** `sync.Mutex` must be a pointer or embedded. never passed by value. Copying a mutex copies its lock state and creates races.
7. **Never use `interface{}` (or `any`) when you know the type.** Define concrete types. If you're using `any` because the type varies, use generics.

## Testing

- Use stdlib `testing` package. No test frameworks. `go test` and table-driven tests handle everything.
- Table-driven tests for handlers: define `[]struct{ name, method, path, body, wantStatus }` and loop.
- Mock interfaces with hand-written mocks or `gomock`. Keep mocks minimal. only mock external boundaries (database, HTTP clients).
- Integration tests use `testcontainers-go` to spin up a real PostgreSQL instance. Tag them with `//go:build integration`.
- Run `go vet` and `staticcheck` in CI. They catch real bugs that unit tests miss.

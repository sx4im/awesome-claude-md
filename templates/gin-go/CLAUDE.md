# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Go 1.22+
- Gin web framework
- GORM v2 ORM with PostgreSQL driver
- Swagger via swag CLI + gin-swagger
- zerolog for structured JSON logging
- golang-migrate for database migrations
- Docker + docker-compose for local dev

## Project Structure

```
.
├── cmd/
│   └── api/
│       └── main.go              # Entry point: config, DI, server start
├── internal/
│   ├── handler/                 # Gin handlers (one file per domain)
│   │   ├── user_handler.go      # @Summary, @Router annotations for swag
│   │   └── auth_handler.go
│   ├── middleware/               # Gin middleware: auth, logging, recovery, CORS
│   │   ├── auth.go
│   │   ├── logger.go            # zerolog request logging middleware
│   │   └── recovery.go          # Custom recovery with structured error logging
│   ├── model/                   # GORM models + domain types
│   │   ├── user.go              # gorm.Model embedded, json tags, validation tags
│   │   └── response.go          # Standard API response envelope
│   ├── repository/              # Database access layer
│   │   └── user_repo.go         # GORM queries, scopes, preloads
│   ├── service/                 # Business logic layer
│   │   └── user_service.go      # Orchestrates repos, enforces rules
│   ├── dto/                     # Request/response DTOs (separate from GORM models)
│   │   └── user_dto.go          # CreateUserRequest, UserResponse
│   └── config/
│       └── config.go            # Env parsing with envconfig
├── docs/                        # swag-generated Swagger JSON/YAML (auto-generated)
├── migrations/                  # SQL migration files (up/down pairs)
├── Makefile                     # swagger, migrate, run, test targets
└── go.mod

```

## Architecture Rules

- **Handlers bind and validate, services decide, repositories persist.** Handler: bind JSON → validate → call service → write response. Service: apply business rules → call repo(s) → return result. Repository: GORM queries only.
- **Handlers never call GORM directly.** All database access goes through the repository layer. This lets you swap GORM for raw SQL or sqlc without touching handlers.
- **DTOs are not GORM models.** `CreateUserRequest` is a DTO with `binding:"required"` tags. `User` is a GORM model with `gorm:"column:..."` tags. Map between them explicitly in the service layer. Never expose GORM models in API responses.
- **Dependency injection via constructor functions.** `NewUserHandler(svc UserService)` and `NewUserService(repo UserRepository)`. Wire everything in `main.go`. No global variables, no `init()` side effects.
- **Standard response envelope.** All responses use `{"data": ..., "error": null}` or `{"data": null, "error": {"code": "...", "message": "..."}}`. Define in `model/response.go`. Never return bare JSON objects.

## Coding Conventions

- **Swagger annotations on every handler.** Use `// @Summary`, `// @Tags`, `// @Accept json`, `// @Produce json`, `// @Param`, `// @Success`, `// @Failure`, `// @Router` comments. Run `swag init -g cmd/api/main.go` to regenerate.
- **Error handling:** Return errors, never panic. Wrap with context: `fmt.Errorf("user_repo.FindByID: %w", err)`. Map to HTTP codes in handlers: `ErrNotFound` → 404, `ErrConflict` → 409, default → 500.
- **Logging:** zerolog with `log.With().Str("request_id", id).Logger()`. Use the logger middleware to attach a request-scoped logger to `c.Set("logger", logger)`. Retrieve in handlers with `c.MustGet("logger").(zerolog.Logger)`.
- **Validation:** Use Gin's built-in binding with `binding:"required,email"` struct tags. Register custom validators for domain rules. Return 422 with field-level errors, not generic 400.
- **Context propagation:** Extract `c.Request.Context()` and pass it to services and repositories. GORM calls use `.WithContext(ctx)`. Never ignore context cancellation.

## Library Preferences

- **Router:** Gin. Not Chi (project already uses Gin conventions and middleware). Not stdlib (Gin's binding/validation and middleware chain save boilerplate).
- **ORM:** GORM v2. Use Scopes for reusable query fragments. Use `.Session(&gorm.Session{})` for clean session management. Use `.Preload()` deliberately—never lazy-load.
- **Logging:** zerolog. Not slog (zerolog has zero-allocation JSON output, better performance for high-traffic APIs). Not zap (zerolog's API is simpler).
- **Docs:** swag + gin-swagger. Not hand-written OpenAPI (swag generates from code annotations, stays in sync automatically).
- **Migrations:** golang-migrate. Not GORM AutoMigrate (AutoMigrate cannot drop columns, rename fields, or handle data migrations. It's fine for prototyping, dangerous in production).

## File Naming

- All files: `snake_case.go` → `user_handler.go`, `user_service.go`
- Test files: `_test.go` suffix → `user_handler_test.go`
- Packages: single lowercase word → `handler`, `service`, `repository`, `middleware`
- Migration files: `{timestamp}_{description}.up.sql` / `.down.sql` → `20240115120000_create_users.up.sql`

## NEVER DO THIS

1. **Never use GORM's `AutoMigrate` in production.** It cannot handle column drops, renames, or data migrations. Use `golang-migrate` with explicit up/down SQL files. AutoMigrate silently does nothing when it can't figure out the diff.
2. **Never return GORM models directly in API responses.** GORM models contain `CreatedAt`, `UpdatedAt`, `DeletedAt`, and internal fields. Map to response DTOs. `c.JSON(200, user)` where `user` is a GORM model leaks database schema to API consumers.
3. **Never use `c.Bind()` without checking the error.** `c.ShouldBindJSON(&req)` returns an error. Check it, return 422 with validation details. Skipping this lets malformed requests reach your service layer.
4. **Never call `c.Abort()` without returning.** `c.Abort()` stops middleware chain execution but does NOT stop the current handler function. Always `c.AbortWithStatusJSON(...)` followed by `return`.
5. **Never use `db.Raw()` for queries that GORM can express.** Use GORM's query builder with Scopes. Raw SQL bypasses GORM's safety features and makes SQL injection possible if you interpolate strings.
6. **Never log with `fmt.Println` or `log.Println`.** Use zerolog everywhere. Unstructured logs are unsearchable, unfiltered, and useless in production log aggregators.
7. **Never use Gin's default recovery middleware in production.** It logs stack traces to stdout. Replace with a custom recovery middleware that logs to zerolog and returns your standard error envelope.

## Testing

- Use stdlib `testing` package with table-driven tests. No test frameworks.
- Handler tests: use `httptest.NewRecorder()` and `gin.CreateTestContext(w)`. Mock the service interface. Assert status codes and response body shapes.
- Service tests: inject mock repositories. Test business rules in isolation from HTTP and database concerns.
- Repository tests: use `testcontainers-go` to spin up a real PostgreSQL instance. Run migrations. Test against real SQL. Tag with `//go:build integration`.
- Run `go vet`, `staticcheck`, and `golangci-lint` in CI. Swagger regeneration check: `swag init && git diff --exit-code docs/`.

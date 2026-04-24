# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Backend)

### Release Discipline
- Fail closed on authz/authn checks and input validation.
- Use explicit timeouts/retries/circuit-breaking for external dependencies.
- Preserve API compatibility unless breaking change is approved and documented.

### Merge/Release Gates
- Unit + integration tests and contract tests pass.
- Static checks pass and critical endpoint latency regressions reviewed.
- Structured error handling verified for all modified endpoints.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Go 1.22+
- Fiber v2 (fasthttp-based web framework)
- GORM v2 or sqlc for database access
- PostgreSQL 15+
- JWT via `golang-jwt/jwt/v5`
- Fiber rate limiter middleware
- Air for hot reload in development

## Project Structure

```
.
├── cmd/
│   └── server/
│       └── main.go              # Entry point: config, fiber.New(), routes, Listen()
├── internal/
│   ├── handler/                 # Fiber handlers (one file per domain)
│   │   ├── user_handler.go
│   │   └── auth_handler.go
│   ├── middleware/
│   │   ├── auth.go              # JWT validation via fiber.Handler
│   │   ├── rate_limiter.go      # Per-route rate limiting config
│   │   └── request_id.go        # X-Request-Id generation
│   ├── model/                   # Domain types and DB models
│   │   ├── user.go
│   │   └── error.go             # AppError with Fiber-compatible error responses
│   ├── repository/              # Database access layer
│   │   └── user_repo.go
│   ├── service/                 # Business logic (no Fiber imports)
│   │   └── user_service.go
│   ├── dto/                     # Request/response DTOs with validate tags
│   │   └── user_dto.go
│   ├── validator/               # Custom validation setup
│   │   └── validator.go         # go-playground/validator integration
│   └── config/
│       └── config.go            # Env parsing
├── migrations/
├── Makefile
└── go.mod
```

## Architecture Rules

- **Fiber handlers are thin.** Parse body with `c.BodyParser(&dto)`, validate, call service, return `c.JSON()`. No business logic in handlers. No database calls.
- **Services never import `gofiber/fiber`.** Services take typed Go arguments and return `(T, error)`. They are testable without any HTTP context. If you need `fiber.Ctx` in a service, your architecture is wrong.
- **Fiber is NOT net/http compatible.** Fiber uses `fasthttp`, not `net/http`. Standard Go middleware (Chi, stdlib) will not work. Only use Fiber-native middleware or write custom `fiber.Handler` functions.
- **Repository interface pattern.** Define `type UserRepository interface` in the service package. Implement it in `repository/`. Inject via constructor. Never use package-level `var DB *gorm.DB`.
- **Rate limiting is per-route, not global.** Apply `limiter.New()` to specific route groups. Auth endpoints get stricter limits (5/min). CRUD endpoints get standard limits (100/min). Health endpoints are unlimited.

## Coding Conventions

- **Error handling:** Define `AppError` struct with `Code int`, `Message string`, `Details any`. Implement `error` interface. Use a custom Fiber `ErrorHandler` in `fiber.Config` that converts `AppError` to consistent JSON. Never use `c.Status(500).SendString("error")`.
- **Validation:** Use `go-playground/validator/v10`. Create a package-level validator in `internal/validator/`. Call `validate.Struct(&dto)` in handlers. Return 422 with per-field error messages, not a raw validator dump.
- **JSON responses:** Always `c.Status(code).JSON(response)`. Use a response helper: `Success(c, data)` → 200 with `{"data": ...}`. `Created(c, data)` → 201. `Error(c, appErr)` → maps error code.
- **Fiber context values:** Use `c.Locals("user", claims)` to pass auth data from middleware to handlers. Type-assert safely: `claims, ok := c.Locals("user").(*Claims)`.
- **Naming:** Go conventions. Interfaces in the consumer package. Concrete types in the provider package. Short receivers: `(h *UserHandler)`, `(s *UserService)`, `(r *UserRepo)`.

## Library Preferences

- **Framework:** Fiber v2. Not Gin (Fiber's API is closer to Express.js, faster with fasthttp). Not Echo (Fiber has better middleware ecosystem and documentation).
- **Database:** GORM v2 for rapid development, or sqlc for performance-critical paths. Use GORM Scopes for reusable query logic. Use sqlc when you need full control over generated SQL.
- **Auth:** `golang-jwt/jwt/v5` for JWT. Not `dgrijalva/jwt-go` (unmaintained, security issues). Store refresh tokens in the database, not in JWTs.
- **Validation:** `go-playground/validator/v10`. Not hand-rolled validation (the tag system handles 90% of cases, custom validators handle the rest).
- **Rate limiting:** Fiber's built-in `limiter` middleware with a Redis store for multi-instance deployments. In-memory store for single-instance or development.

## File Naming

- All files: `snake_case.go` → `user_handler.go`, `auth_service.go`
- Test files: `_test.go` suffix → `user_handler_test.go`
- Packages: single lowercase word → `handler`, `service`, `repository`, `middleware`
- Migration files: `{version}_{description}.up.sql` / `.down.sql`

## NEVER DO THIS

1. **Never assume Fiber is net/http compatible.** `fiber.Ctx` is NOT `http.Request`. `c.Body()` returns `[]byte` from fasthttp, not an `io.Reader`. Standard Go HTTP middleware will not work. Never wrap `http.Handler` and expect it to function correctly.
2. **Never store `fiber.Ctx` or pass it to goroutines.** Fiber reuses `fasthttp.RequestCtx` across requests. If you pass `c` to a goroutine, it will contain garbage data from the next request. Copy any needed values out first: `userID := c.Locals("userID")`.
3. **Never use `c.SendString` for API responses.** Always use `c.JSON()` with a typed response struct. `SendString` produces inconsistent content types and makes API documentation impossible.
4. **Never put JWT secrets in code or config files.** Load from environment variables only. Use `os.Getenv("JWT_SECRET")` in config parsing. Never commit `.env` files with real secrets.
5. **Never skip rate limiting on auth endpoints.** Login and registration endpoints are brute-force targets. Apply strict rate limits: 5 requests per minute per IP on `/auth/login`, 3 per minute on `/auth/register`.
6. **Never use `gorm.Model` without understanding what it adds.** It embeds `ID`, `CreatedAt`, `UpdatedAt`, `DeletedAt`. The soft-delete `DeletedAt` adds a WHERE clause to every query. If you don't want soft deletes, embed only the fields you need.
7. **Never return GORM errors directly to the client.** GORM errors contain internal details like table names and column types. Map them to `AppError` in the repository layer. `gorm.ErrRecordNotFound` → `AppError{Code: 404}`.

## Testing

- Handler tests: use Fiber's built-in `app.Test(req)` method. Build requests with `http.NewRequest`. Assert on `resp.StatusCode` and parsed JSON body.
- Service tests: inject mock repositories via interfaces. Test business logic without HTTP or database.
- Repository tests: use `testcontainers-go` with PostgreSQL. Run real migrations. Test against actual SQL. Tag with `//go:build integration`.
- JWT middleware tests: create valid/expired/malformed tokens. Assert 401 responses with correct error messages.
- Run `go vet`, `staticcheck`, and `golangci-lint run` in CI. Fail on any warning.

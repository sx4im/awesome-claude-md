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

- Kotlin 2.0+ with coroutines
- Ktor 3.x server framework (CIO or Netty engine)
- Exposed ORM for SQL access
- Koin for dependency injection
- kotlinx.serialization for JSON (not Jackson, not Gson)
- PostgreSQL 15+ via HikariCP connection pool
- Gradle Kotlin DSL (build.gradle.kts)

## Project Structure

```
src/
├── main/
│   └── kotlin/
│       └── {package}/
│           ├── Application.kt          # embeddedServer or EngineMain, install plugins
│           ├── plugins/
│           │   ├── Serialization.kt     # ContentNegotiation + kotlinx.serialization
│           │   ├── Routing.kt           # Top-level route composition
│           │   ├── StatusPages.kt       # Exception-to-HTTP-response mapping
│           │   └── DependencyInjection.kt # Koin module installation
│           ├── routes/
│           │   ├── UserRoutes.kt        # Route("/api/users") extension function
│           │   └── AuthRoutes.kt
│           ├── service/
│           │   ├── UserService.kt       # Business logic, suspend functions
│           │   └── AuthService.kt
│           ├── repository/
│           │   ├── UserRepository.kt    # Exposed DSL queries, newSuspendedTransaction
│           │   └── Tables.kt           # Exposed Table object definitions
│           ├── model/
│           │   ├── User.kt             # Domain model (plain data class)
│           │   ├── Error.kt            # AppException sealed class hierarchy
│           │   └── dto/                # @Serializable request/response DTOs
│           └── config/
│               └── AppConfig.kt        # Typesafe config or env-based configuration
├── test/
│   └── kotlin/
│       └── {package}/
│           ├── routes/
│           │   └── UserRoutesTest.kt    # testApplication { } based tests
│           └── service/
│               └── UserServiceTest.kt
└── resources/
    ├── application.conf               # HOCON config (Ktor default)
    └── db/
        └── migration/                 # Flyway SQL migrations
```

## Architecture Rules

- **Plugins configure, routes handle, services decide, repositories persist.** Each layer only talks to the one below it. Routes never call repositories. Services never see `ApplicationCall`.
- **Routes are extension functions on `Route`.** Define `fun Route.userRoutes(userService: UserService)` and call it from `plugins/Routing.kt`. Never define routes inside `Application.module()` directly—it becomes unreadable past 5 endpoints.
- **All I/O functions are `suspend`.** Repository functions use `newSuspendedTransaction { }` from Exposed. Service functions that call repos are `suspend`. Ktor's routing handlers are already in a coroutine context. Never block a coroutine with `runBlocking` or `Thread.sleep`.
- **Koin modules match the package structure.** Define `val serviceModule = module { single { UserService(get()) } }`. Install in `Application.kt` with `install(Koin) { modules(serviceModule, repoModule) }`. Inject in routes with `val userService by inject<UserService>()`.
- **StatusPages maps exceptions to responses.** Define a sealed class `AppException` with subclasses `NotFoundException`, `ValidationException`, `ConflictException`. Install `StatusPages` and map each to the correct HTTP status code and JSON body.

## Coding Conventions

- **Serialization:** All DTOs use `@Serializable` from kotlinx.serialization. Never use Jackson (`@JsonProperty`) or Gson. kotlinx.serialization is compile-time, no reflection, and works with Kotlin's type system natively.
- **Null safety:** Leverage Kotlin's null safety everywhere. API responses use non-nullable types. Optional query params use `call.request.queryParameters["page"]?.toIntOrNull() ?: 1`. Never use `!!` outside of tests.
- **Data classes for DTOs:** `@Serializable data class CreateUserRequest(val email: String, val name: String)`. Validate in the service layer, not with annotation processors. Use `require()` or `check()` for preconditions that throw `IllegalArgumentException`, caught by StatusPages.
- **Exposed DSL, not DAO.** Use Exposed's DSL API (`Users.select { Users.id eq userId }`) instead of the DAO API. The DSL is explicit about what SQL runs. The DAO pattern hides queries behind property access and causes N+1 problems.
- **Coroutine context:** Never use `GlobalScope.launch`. Use `CoroutineScope` tied to the application lifecycle. For background tasks, create a supervised scope: `val appScope = CoroutineScope(SupervisorJob() + Dispatchers.Default)`.

## Library Preferences

- **Serialization:** kotlinx.serialization. Not Jackson (reflection-based, doesn't understand Kotlin data classes properly without extra modules, `null` handling is broken). Not Gson (same reflection issues, no Kotlin support).
- **DI:** Koin. Not Dagger/Hilt (overkill for server-side Kotlin, annotation processing slows builds). Not manual DI (fine for tiny projects, unmanageable past 10 services).
- **ORM:** Exposed DSL. Not Exposed DAO (hides queries, causes N+1). Not Hibernate (reflection-heavy, impedance mismatch with Kotlin).
- **Database pool:** HikariCP. Configure `maximumPoolSize` based on available connections, not a random large number.
- **Migrations:** Flyway. Not Liquibase (Flyway's SQL-first approach is simpler).

## File Naming

- All files: `PascalCase.kt` → `UserService.kt`, `UserRoutes.kt`, `Tables.kt`
- Test files: `PascalCaseTest.kt` → `UserRoutesTest.kt`, `UserServiceTest.kt`
- One primary class per file. `UserService.kt` contains `class UserService`. Config: `application.conf` (HOCON), `build.gradle.kts`.

## NEVER DO THIS

1. **Never use Jackson with Ktor.** Ktor's native serialization plugin works with kotlinx.serialization. Jackson requires a separate module (`ktor-serialization-jackson`), handles Kotlin nullability incorrectly, and silently produces wrong JSON for data classes with default parameters.
2. **Never use `runBlocking` inside a route handler.** Ktor handlers are already suspended. `runBlocking` blocks the thread and defeats the purpose of coroutines. Just call `suspend` functions directly.
3. **Never use Exposed DAO's lazy-loading in API handlers.** `User.findById(id)` with related entities triggers N+1 queries. Use the DSL with explicit joins: `(Users innerJoin Orders).select { Users.id eq id }`.
4. **Never use `GlobalScope` for background work.** It creates orphan coroutines that survive request cancellation and leak memory. Use a structured `CoroutineScope` tied to the application lifecycle.
5. **Never use `!!` (non-null assertion) in production code.** It throws `NullPointerException` with no context. Use `?: throw NotFoundException("User $id not found")` or `requireNotNull(value) { "descriptive message" }`.
6. **Never define all routes in `Application.module()`.** Split into extension functions per domain. `Application.module()` installs plugins and calls `routing { userRoutes(); authRoutes() }`.
7. **Never hardcode database credentials.** Use `application.conf` with env var substitution: `url = ${?DATABASE_URL}`. Never commit credentials.

## Testing

- Use Ktor's `testApplication { }` DSL for route testing. It starts an in-memory server with no network socket.
- Create test Koin modules that override production modules with fakes or mocks.
- Test services with `kotlinx-coroutines-test` and `runTest { }`. Never use `runBlocking` in tests—use `runTest` for proper coroutine test support.
- Repository tests: use Testcontainers with PostgreSQL. Run Flyway migrations. Test against real SQL.
- Run `./gradlew detekt` for static analysis and `./gradlew ktlintCheck` for formatting in CI.

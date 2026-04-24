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

## Production Delivery Playbook (Category: Mobile)

### Release Discipline
- Protect offline/poor-network behavior and state recovery paths.
- Avoid platform-specific regressions by validating iOS/Android parity.
- Respect battery/performance constraints in background tasks.

### Merge/Release Gates
- Build and runtime smoke tests pass on target platforms.
- Crash-prone paths (auth, navigation, persistence) validated.
- No release with unresolved permission/security handling gaps.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Language: Kotlin 2.0+ with K2 compiler across all targets
- Shared UI: Compose Multiplatform (Android, iOS, Desktop)
- Shared Logic: Kotlin Multiplatform (KMP) with expect/actual declarations
- Networking: Ktor 3 with KotlinX Serialization
- Database: SQLDelight 2 with platform-specific drivers
- DI: Koin Multiplatform
- Async: Kotlin Coroutines with Flow (common module)
- Navigation: Decompose with Compose extensions
- Build: Gradle with convention plugins, version catalogs

## Project Structure

```
composeApp/
  src/
    commonMain/kotlin/
      di/                     # Koin module definitions (commonModule, platformModule expect)
      data/
        remote/               # Ktor API client, request/response DTOs
        local/                # SQLDelight queries (.sq files in sqldelight/ dir)
        repository/           # Repository implementations using Ktor + SQLDelight
      domain/
        model/                # Shared domain models (data classes, value classes)
        repository/           # Repository interfaces
        usecase/              # Business logic use cases
      ui/
        theme/                # MaterialTheme setup, Color, Typography for Compose MP
        components/           # Shared composables (buttons, lists, loading states)
        navigation/           # Decompose RootComponent, child stack configuration
        screens/              # Feature screens with Component + Composable pairs
      util/                   # Multiplatform utilities (expect/actual for platform specifics)
    androidMain/kotlin/       # Android-specific actuals (Context-based services, SQLite driver)
    iosMain/kotlin/           # iOS-specific actuals (NSUserDefaults, Darwin SQLite driver)
    desktopMain/kotlin/       # Desktop-specific actuals (JVM SQLite driver, file paths)
  sqldelight/                 # .sq files for SQLDelight schema and queries
iosApp/                       # Xcode project with Swift entry point calling Compose
  iosApp/
    ContentView.swift         # ComposeUIViewController wrapper
    iOSApp.swift              # @main App entry point
gradle/
  libs.versions.toml          # Version catalog for all dependencies
build-logic/                  # Convention plugins for shared build configuration
```

## Architecture Rules

- All business logic lives in `commonMain`; platform modules contain only expect/actual implementations
- Decompose components hold business logic and state; composables are pure UI renderers
- Every feature has a Component interface, a DefaultComponent implementation, and a Composable function
- Repositories return `Flow<T>` for observable data and `suspend` functions for one-shot operations
- Koin modules are split: `commonModule` for shared bindings, `platformModule()` for platform-specific factories
- SQLDelight `.sq` files define the schema; never write raw SQL strings in Kotlin code

## Coding Conventions

- Use `expect`/`actual` sparingly; prefer interfaces with platform-specific implementations injected via Koin
- Ktor client is configured in commonMain with `HttpClient { install(ContentNegotiation) { json() } }`
- Use `Value<State>` from Decompose for component state; convert to Compose state with `subscribeAsState()`
- All DTOs use `@Serializable` from KotlinX Serialization; map DTOs to domain models at the repository boundary
- Prefer `kotlinx.datetime` over `java.time` for date handling in shared code
- Use `kotlinx.io` for multiplatform file and stream operations
- Name Koin modules as `val featureModule = module { ... }` and install them in the root Koin application

## Library Preferences

- HTTP: Ktor 3 Client (not Retrofit, which is JVM-only)
- JSON: KotlinX Serialization (not Gson or Moshi)
- Database: SQLDelight 2 (not Room, which is Android-only in production)
- Image loading: Coil 3 Multiplatform with Compose integration
- Date/time: kotlinx-datetime
- Logging: Kermit by Touchlab for multiplatform logging
- Key-value storage: multiplatform-settings by russhwolf

## File Naming

- Components: `FeatureComponent.kt` (interface) and `DefaultFeatureComponent.kt` (implementation)
- Composables: `FeatureScreen.kt` (contains the `@Composable` function)
- SQLDelight: `EntityName.sq` for schema and queries
- Expect/actual: keep in same package path across source sets; file name matches the declaration
- Koin modules: `FeatureModule.kt` in the di package

## NEVER DO THIS

1. Never use `java.*` or `android.*` imports in `commonMain`; these break iOS and Desktop compilation
2. Never use `GlobalScope` or `Dispatchers.Main` directly; use the coroutine scope provided by Decompose components
3. Never put UI composables in platform-specific source sets unless they wrap a truly native widget
4. Never use hardcoded strings for SQLDelight table or column names; use generated type-safe accessors
5. Never skip the DTO-to-domain-model mapping; network/database shapes must not leak into the UI layer
6. Never add platform-specific dependencies to `commonMain` build.gradle.kts; use expect/actual or Koin injection

## Testing

- Common tests go in `commonTest` and run on all targets via `./gradlew allTests`
- Use `kotlin.test` assertions (`assertEquals`, `assertTrue`) in common test code, not JUnit-specific APIs
- Test Ktor client code with `MockEngine` that returns predefined responses
- Test SQLDelight queries with an in-memory driver (`JdbcSqliteDriver(IN_MEMORY)` for JVM tests)
- Decompose component tests create the component directly and assert state transitions
- Use Turbine for testing Flow emissions from repositories in common code
- Run platform-specific tests with `./gradlew :composeApp:iosSimulatorArm64Test` for iOS verification

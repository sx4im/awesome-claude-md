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

- Kotlin 1.9+
- Jetpack Compose (Material 3)
- Hilt for dependency injection
- Retrofit + OkHttp for networking
- Room for local database
- Kotlin Coroutines + Flow
- Minimum SDK: 26 (Android 8.0)

## Project Structure

```
app/src/main/java/com/company/project/
├── di/                      # Hilt modules (NetworkModule, DatabaseModule)
├── data/
│   ├── remote/              # Retrofit API interfaces, DTOs
│   │   ├── UserApi.kt
│   │   └── dto/
│   ├── local/               # Room DAOs, entities
│   │   ├── UserDao.kt
│   │   └── entity/
│   └── repository/          # Repository implementations
│       └── UserRepositoryImpl.kt
├── domain/
│   ├── model/               # Domain models (clean, no annotations)
│   │   └── User.kt
│   ├── repository/          # Repository interfaces
│   │   └── UserRepository.kt
│   └── usecase/             # Use case classes
│       ├── GetUserUseCase.kt
│       └── LoginUseCase.kt
├── ui/
│   ├── theme/               # Material 3 theme (Color, Type, Theme)
│   ├── navigation/          # NavHost, routes, NavGraph
│   ├── screens/
│   │   ├── home/
│   │   │   ├── HomeScreen.kt
│   │   │   └── HomeViewModel.kt
│   │   └── profile/
│   └── components/          # Reusable composables
└── util/                    # Extensions, constants, formatters
```

## Architecture Rules

- **Clean Architecture: UI → Domain → Data.** UI layer calls use cases. Domain defines models and repository interfaces. Data implements repositories with Retrofit and Room. Domain never depends on Data or UI.
- **One ViewModel per screen.** `HomeViewModel` handles `HomeScreen`'s state. ViewModels expose state via `StateFlow` and handle events via functions. Never share ViewModels across screens.
- **Use cases are optional but recommended for complex logic.** If a ViewModel just calls one repository method, you can skip the use case. If it orchestrates multiple repositories or has business rules, use a use case class.
- **Hilt provides all dependencies.** Every ViewModel, repository, and API client is injected. Define modules in `di/`. Never use `object` singletons for dependencies. Hilt handles scoping.
- **Compose Navigation handles all navigation.** Define routes as sealed classes or strings in `navigation/`. Never use Fragment transactions or manual Activity starts.

## Coding Conventions

- **UI state in a sealed interface.** `sealed interface HomeUiState { data object Loading : HomeUiState; data class Success(val users: List<User>) : HomeUiState; data class Error(val message: String) : HomeUiState }`. ViewModels expose `StateFlow<HomeUiState>`.
- **Composables:** `@Composable` functions start with uppercase: `HomeScreen()`, `UserCard()`. Stateless composables take all data as parameters. Stateful wrappers inject the ViewModel.
- **Kotlin data classes for all models.** Domain models, DTOs, and Room entities are all `data class`. DTOs have `@SerializedName` annotations. Domain models are clean.
- **Coroutines:** use `viewModelScope` in ViewModels. Use `Dispatchers.IO` for I/O operations. Never use `GlobalScope`.
- **Repository pattern:** repositories return `Flow<T>` for observable data and `suspend fun` for one-shot operations.

## Library Preferences

- **DI:** Hilt. not Koin (Hilt has compile-time verification, Koin resolves at runtime and crashes on missing deps). Not manual DI (too much boilerplate).
- **Networking:** Retrofit + OkHttp + Kotlin Serialization. not Ktor client (Retrofit has better Android ecosystem support). Kotlin Serialization over Gson (faster, no reflection).
- **Local DB:** Room. not SQLDelight (Room has better Compose integration and wider adoption on Android). Not raw SQLite.
- **Images:** Coil. not Glide (Coil is Kotlin-first, lighter, Compose-native). Use `AsyncImage` composable.
- **Navigation:** Compose Navigation with type-safe routes (Kotlin Serialization integration in recent versions).

## NEVER DO THIS

1. **Never do UI work off the main thread.** Compose composables are main-thread only. Use `LaunchedEffect` or ViewModel coroutines for async work, then update state which Compose observes.
2. **Never use `GlobalScope.launch`.** It leaks coroutines that outlive the screen. Use `viewModelScope` in ViewModels, `rememberCoroutineScope()` in composables, and `lifecycleScope` in Activities.
3. **Never mutate `MutableStateFlow` directly from composables.** Expose functions on the ViewModel: `viewModel.onSearchQueryChanged(query)`. State mutation is the ViewModel's responsibility.
4. **Never use `remember` for heavy objects.** `remember` survives recomposition but not configuration changes. Use ViewModel for state that must survive rotation. `remember` is for derived UI values only.
5. **Never hardcode strings in composables.** Use `stringResource(R.string.key)` for all user-facing text. Hardcoded strings can't be translated and don't appear in Android string resources analysis.
6. **Never use `@Inject` on constructor parameters without `@HiltViewModel`.** ViewModels need `@HiltViewModel` annotation. Without it, Hilt can't provide the ViewModel through `hiltViewModel()`.
7. **Never use `LiveData` in new code.** Use `StateFlow` and `collectAsStateWithLifecycle()`. LiveData is the old pattern. Flow integrates better with Compose and Kotlin coroutines.

## Testing

- **Unit tests:** JUnit 5 + Turbine (for Flow testing) + MockK. Test ViewModels by collecting StateFlow emissions.
- **UI tests:** Compose Testing (`createComposeRule()`) with semantic matchers. Test user interactions, not composable internals.
- **Integration tests:** Hilt testing with `@HiltAndroidTest`. Mock API responses with MockWebServer.
- Run `./gradlew detekt` for static analysis. Treat warnings as errors in CI.

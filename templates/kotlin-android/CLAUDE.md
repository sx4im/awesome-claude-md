# [PROJECT NAME] — [ONE LINE DESCRIPTION]

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
- **Hilt provides all dependencies.** Every ViewModel, repository, and API client is injected. Define modules in `di/`. Never use `object` singletons for dependencies — Hilt handles scoping.
- **Compose Navigation handles all navigation.** Define routes as sealed classes or strings in `navigation/`. Never use Fragment transactions or manual Activity starts.

## Coding Conventions

- **UI state in a sealed interface.** `sealed interface HomeUiState { data object Loading : HomeUiState; data class Success(val users: List<User>) : HomeUiState; data class Error(val message: String) : HomeUiState }`. ViewModels expose `StateFlow<HomeUiState>`.
- **Composables:** `@Composable` functions start with uppercase: `HomeScreen()`, `UserCard()`. Stateless composables take all data as parameters. Stateful wrappers inject the ViewModel.
- **Kotlin data classes for all models.** Domain models, DTOs, and Room entities are all `data class`. DTOs have `@SerializedName` annotations. Domain models are clean.
- **Coroutines:** use `viewModelScope` in ViewModels. Use `Dispatchers.IO` for I/O operations. Never use `GlobalScope`.
- **Repository pattern:** repositories return `Flow<T>` for observable data and `suspend fun` for one-shot operations.

## Library Preferences

- **DI:** Hilt — not Koin (Hilt has compile-time verification, Koin resolves at runtime and crashes on missing deps). Not manual DI (too much boilerplate).
- **Networking:** Retrofit + OkHttp + Kotlin Serialization — not Ktor client (Retrofit has better Android ecosystem support). Kotlin Serialization over Gson (faster, no reflection).
- **Local DB:** Room — not SQLDelight (Room has better Compose integration and wider adoption on Android). Not raw SQLite.
- **Images:** Coil — not Glide (Coil is Kotlin-first, lighter, Compose-native). Use `AsyncImage` composable.
- **Navigation:** Compose Navigation with type-safe routes (Kotlin Serialization integration in recent versions).

## NEVER DO THIS

1. **Never do UI work off the main thread.** Compose composables are main-thread only. Use `LaunchedEffect` or ViewModel coroutines for async work, then update state which Compose observes.
2. **Never use `GlobalScope.launch`.** It leaks coroutines that outlive the screen. Use `viewModelScope` in ViewModels, `rememberCoroutineScope()` in composables, and `lifecycleScope` in Activities.
3. **Never mutate `MutableStateFlow` directly from composables.** Expose functions on the ViewModel: `viewModel.onSearchQueryChanged(query)`. State mutation is the ViewModel's responsibility.
4. **Never use `remember` for heavy objects.** `remember` survives recomposition but not configuration changes. Use ViewModel for state that must survive rotation. `remember` is for derived UI values only.
5. **Never hardcode strings in composables.** Use `stringResource(R.string.key)` for all user-facing text. Hardcoded strings can't be translated and don't appear in Android string resources analysis.
6. **Never use `@Inject` on constructor parameters without `@HiltViewModel`.** ViewModels need `@HiltViewModel` annotation. Without it, Hilt can't provide the ViewModel through `hiltViewModel()`.
7. **Never use `LiveData` in new code.** Use `StateFlow` and `collectAsStateWithLifecycle()`. LiveData is the old pattern — Flow integrates better with Compose and Kotlin coroutines.

## Testing

- **Unit tests:** JUnit 5 + Turbine (for Flow testing) + MockK. Test ViewModels by collecting StateFlow emissions.
- **UI tests:** Compose Testing (`createComposeRule()`) with semantic matchers. Test user interactions, not composable internals.
- **Integration tests:** Hilt testing with `@HiltAndroidTest`. Mock API responses with MockWebServer.
- Run `./gradlew detekt` for static analysis. Treat warnings as errors in CI.

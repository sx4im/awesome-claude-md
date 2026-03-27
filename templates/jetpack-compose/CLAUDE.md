# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: Kotlin 2.0+ with K2 compiler
- UI: Jetpack Compose with Material 3 (Material You)
- DI: Hilt (Dagger under the hood)
- Async: Kotlin Coroutines + Flow
- Networking: Retrofit 2 + OkHttp + Kotlinx Serialization
- Database: Room with KSP annotation processing
- Navigation: Compose Navigation with type-safe routes
- Image Loading: Coil 3 (Compose integration)
- Build: Gradle with Kotlin DSL and version catalogs

## Project Structure

```
app/
  src/main/kotlin/com/example/app/
    di/                  # Hilt modules (NetworkModule, DatabaseModule, RepositoryModule)
    data/
      local/             # Room DAOs, entities, database class
      remote/            # Retrofit API interfaces, DTOs
      repository/        # Repository implementations
    domain/
      model/             # Domain models (plain Kotlin data classes)
      repository/        # Repository interfaces
      usecase/           # Use cases (single-responsibility, operator invoke)
    ui/
      theme/             # Theme.kt, Color.kt, Type.kt, Shape.kt
      components/        # Reusable composables (buttons, cards, dialogs)
      navigation/        # NavHost setup, Screen sealed class, NavGraph
      screens/
        home/            # HomeScreen.kt, HomeViewModel.kt, HomeUiState.kt
        detail/          # DetailScreen.kt, DetailViewModel.kt
    util/                # Extension functions, constants
    App.kt               # @HiltAndroidApp Application class
    MainActivity.kt      # Single activity, setContent with theme
```

## Architecture Rules

- Follow unidirectional data flow: ViewModel exposes StateFlow of UiState, UI collects it
- Every screen gets a sealed interface UiState with Loading, Success, and Error substates
- ViewModels never hold references to Context or lifecycle-aware components
- Use cases wrap single business operations and call repository interfaces from the domain layer
- Repositories in data layer implement domain interfaces; domain layer has zero Android dependencies
- UI events flow through a sealed interface UiEvent from Composable to ViewModel via a single onEvent function

## Coding Conventions

- Use `collectAsStateWithLifecycle()` instead of `collectAsState()` for all Flow collection in composables
- Stateless composables receive data and lambdas as parameters; stateful wrappers call the ViewModel
- Hilt ViewModels use `@HiltViewModel` and inject dependencies via constructor
- Name composable functions as nouns (ProfileCard, SettingsPanel), not verbs
- Prefer `rememberSaveable` over `remember` for any state that should survive configuration changes
- Use `LaunchedEffect` for one-shot events; `snapshotFlow` when converting Compose state to Flow
- Apply `Modifier` as the first optional parameter in every composable; never hardcode sizes in child composables

## Library Preferences

- HTTP client: Retrofit with KotlinX Serialization converter (not Gson or Moshi)
- Image loading: Coil with `AsyncImage` composable (not Glide)
- Logging: Timber for debug logs, strip in release via ProGuard
- Testing: JUnit 5 + Turbine for Flow testing + MockK for mocking
- Compose testing: `createComposeRule` with semantics-based assertions

## File Naming

- Screens: `FeatureScreen.kt` containing the composable, co-located with `FeatureViewModel.kt` and `FeatureUiState.kt`
- Data classes / DTOs: `EntityNameDto.kt` for network, `EntityNameEntity.kt` for Room
- DI modules: `FeatureModule.kt` annotated with `@Module @InstallIn`
- Use cases: `VerbNounUseCase.kt` (e.g., `GetUserProfileUseCase.kt`)

## NEVER DO THIS

1. Never use `GlobalScope.launch` -- always use `viewModelScope` in ViewModels or a supervised scope in repositories
2. Never pass `ViewModel` instances directly to composables; pass state and event lambdas instead
3. Never use `mutableStateOf` inside a ViewModel for UI state; use `MutableStateFlow` with `StateFlow` exposure
4. Never call `suspend` functions from composables without `LaunchedEffect` or `rememberCoroutineScope`
5. Never store API keys or secrets in BuildConfig fields; use the Secrets Gradle plugin or local.properties excluded from VCS
6. Never use `LiveData` in new code; the project is fully migrated to Kotlin Flow and Compose state
7. Never create God ViewModels with more than 300 lines; split by feature or delegate to use cases

## Testing

- Unit test every use case and repository with fakes or MockK mocks
- Use Turbine (`app.cash.turbine`) to test StateFlow and SharedFlow emissions in ViewModels
- Compose UI tests use `ComposeTestRule` with `onNodeWithText`, `onNodeWithContentDescription`, and semantic matchers
- Integration tests for Room use `Room.inMemoryDatabaseBuilder` with `runTest` coroutine scope
- Run `./gradlew testDebugUnitTest` for unit tests; `./gradlew connectedDebugAndroidTest` for instrumented tests
- Aim for test coverage on all use cases and ViewModels; UI tests cover critical user flows only

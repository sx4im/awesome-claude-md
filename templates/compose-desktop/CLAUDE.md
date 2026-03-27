# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: Kotlin 2.0+ with JVM target 17
- UI: Compose for Desktop (JetBrains Compose Multiplatform, desktop target)
- Navigation: Decompose 3 with Compose extensions for type-safe child stacks
- DI: Koin 4 with constructor injection
- Async: Kotlin Coroutines + Flow for reactive data streams
- Database: Exposed ORM with H2 or SQLite JDBC for local persistence
- Networking: Ktor 3 Client with CIO engine
- Serialization: KotlinX Serialization for JSON
- Build: Gradle with Kotlin DSL, Compose Gradle plugin, jpackage for distribution

## Project Structure

```
src/
  main/kotlin/com/example/app/
    Main.kt                    # application {} entry point, Window composable, Koin init
    di/
      AppModule.kt             # Koin module definitions for services, repositories, components
    navigation/
      RootComponent.kt         # Decompose root with childStack for top-level destinations
      RootContent.kt           # Composable mapping component instances to UI
      ScreenConfig.kt          # Sealed class for navigation destinations with serialization
    ui/
      theme/
        AppTheme.kt            # MaterialTheme with custom ColorScheme, Typography, Shapes
        Colors.kt              # Light and dark color palettes
      components/
        AppScaffold.kt         # Main window layout with sidebar and content area
        SidebarNav.kt          # Persistent sidebar with navigation items
        DialogHost.kt          # Centralized dialog management composable
      screens/
        home/
          HomeComponent.kt     # Decompose component interface and implementation
          HomeScreen.kt        # Composable UI for home
        settings/
          SettingsComponent.kt
          SettingsScreen.kt
    data/
      local/
        AppDatabase.kt         # Exposed database connection and table definitions
        entities/              # Exposed Table objects (Users, Projects, etc.)
        dao/                   # Data access objects using Exposed DSL
      remote/
        ApiClient.kt           # Ktor HttpClient with ContentNegotiation, Logging
        dto/                   # Data transfer objects with @Serializable
      repository/
        ItemRepository.kt      # Repository implementation combining local and remote
    domain/
      model/                   # Domain data classes
      usecase/                 # Single-purpose use case classes
    util/
      CoroutineDispatchers.kt  # Injectable dispatcher provider for testing
      FileUtils.kt             # Platform file path resolution
  main/resources/
    fonts/                     # Bundled font files
    icons/                     # SVG or PNG icons for tray and window
    sqldelight/ or schema/     # Database migration scripts if applicable
```

## Architecture Rules

- Decompose components own all business logic and expose `Value<State>` for UI consumption
- Composables are stateless renderers; they read component state via `subscribeAsState()` and call component methods
- The Root component manages the child stack; child components never navigate directly, they emit events upward
- Koin provides all dependencies; never use `object` singletons for services or repositories
- Database transactions run on `Dispatchers.IO` via the injected dispatcher provider
- Domain models are separate from Exposed entities and DTOs; mapping happens at repository boundaries

## Coding Conventions

- Use `application { }` DSL as the entry point; configure `Window(onCloseRequest = ::exitApplication)`
- Handle window state (size, position) with `rememberWindowState()` and persist it between launches
- System tray integration uses `Tray(icon, menu = { ... })` inside the `application` block
- Keyboard shortcuts use `Modifier.onKeyEvent` or `MenuItem(shortcut = KeyShortcut(Key.S, ctrl = true))`
- Use `Modifier.pointerHoverIcon(PointerIcon.Hand)` for clickable elements to match desktop UX expectations
- File dialogs use `javax.swing.JFileChooser` wrapped in a coroutine on `Dispatchers.IO`; do not block the UI thread
- Prefer `LazyColumn` with `key` for large lists; use `SelectionContainer` for text that users may want to copy

## Library Preferences

- Database: Exposed ORM (JetBrains) with H2 embedded or SQLite via JDBC driver
- HTTP client: Ktor 3 with CIO engine (no OkHttp dependency needed on desktop)
- Logging: SLF4J with Logback for file-based logging in production
- File watching: Java NIO WatchService wrapped in a Kotlin Flow
- Packaging: Compose Gradle plugin `jpackage` task for .dmg, .msi, .deb installers
- Markdown rendering: JetBrains Jewel library or custom Compose-based renderer
- Testing: JUnit 5 + Kotlin Coroutines Test + Compose Desktop test framework

## File Naming

- Decompose components: `FeatureComponent.kt` (contains interface + DefaultFeatureComponent class)
- Composable screens: `FeatureScreen.kt` (pure composable rendering)
- Exposed tables: `EntityNameTable.kt` (e.g., `ProjectsTable.kt`)
- DAOs: `EntityNameDao.kt`
- Repositories: `FeatureRepository.kt`
- Koin modules: `FeatureModule.kt`

## NEVER DO THIS

1. Never use `Thread.sleep()` or blocking calls on the main thread; use `delay()` or `withContext(Dispatchers.IO)`
2. Never access Swing components from coroutines without switching to `Dispatchers.Main` (Swing EDT)
3. Never hardcode file paths; use `System.getProperty("user.home")` and resolve app-specific directories
4. Never create multiple `HttpClient` instances; configure one in Koin as a singleton with proper `close()` on shutdown
5. Never skip `onCloseRequest` cleanup; dispose coroutine scopes, close database connections, and flush logs
6. Never use `mutableStateOf` in Decompose components; use `MutableValue` from Decompose for lifecycle-safe state

## Testing

- Unit test Decompose components by instantiating them directly with mock dependencies
- Use `kotlinx-coroutines-test` with `runTest` and `TestDispatcher` for coroutine-based logic
- Database tests use an in-memory H2 instance created fresh per test with `Database.connect("jdbc:h2:mem:test")`
- Ktor client tests use `MockEngine` with predefined response queues
- Compose UI tests use `createComposeRule()` from the desktop testing library with `onNodeWithText` assertions
- Run all tests with `./gradlew test`; generate coverage reports with Kover plugin
- Integration tests verify full component stacks with real database and mock network

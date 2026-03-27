# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Language: Swift 5.10+ with strict concurrency checking enabled
- UI: SwiftUI with AppKit interop for advanced macOS controls
- Data Persistence: SwiftData with CloudKit sync
- Reactive: Combine for publisher chains; async/await with structured concurrency for new code
- Networking: URLSession with async/await (no third-party HTTP libraries)
- Architecture: MVVM with Observable macro (Swift 5.9+)
- Build: Xcode 16+, Swift Package Manager for dependencies
- Minimum target: macOS 14 Sonoma

## Project Structure

```
Sources/
  App/
    AppMain.swift            # @main entry point, WindowGroup and Settings scenes
    AppDelegate.swift        # NSApplicationDelegate for AppKit lifecycle hooks
  Features/
    Sidebar/
      SidebarView.swift
      SidebarViewModel.swift
    Editor/
      EditorView.swift
      EditorViewModel.swift
    Settings/
      SettingsView.swift       # Settings scene with TabView
  Models/
    Document.swift             # @Model SwiftData entity
    Tag.swift                  # @Model with relationships
  Services/
    PersistenceService.swift   # ModelContainer setup, migration logic
    NetworkService.swift       # URLSession wrapper, endpoint definitions
    FileSystemService.swift    # Sandboxed file access, security-scoped bookmarks
  Views/
    Components/                # Reusable SwiftUI views (toolbar items, custom controls)
    Modifiers/                 # Custom ViewModifiers (e.g., conditional modifiers)
  Utilities/
    Logger+Extensions.swift    # os.Logger category setup
    KeyboardShortcuts.swift    # KeyEquivalent definitions
  Resources/
    Assets.xcassets
    Localizable.xcstrings
```

## Architecture Rules

- Use the `@Observable` macro on all view models; do not use `ObservableObject` or `@Published`
- Views are pure functions of state; they read from the view model and dispatch actions
- Services are injected via SwiftUI Environment using custom `EnvironmentKey` definitions
- Never import AppKit in SwiftUI views; create `NSViewRepresentable` wrappers in the Components folder
- SwiftData models live in the Models folder and never contain business logic
- Prefer `@Query` in views for simple data reads; use the view model for complex filtered or sorted queries

## Coding Conventions

- Use Swift structured concurrency (async/await, TaskGroup, AsyncStream) for all new asynchronous code
- Actor isolation: mark services as `actor` when they manage mutable shared state
- Use `os.Logger` with subsystem and category for all logging; never use `print` in production code
- Apply `@MainActor` to view models since they drive UI state
- Prefer `NavigationSplitView` over deprecated `NavigationView` for macOS multi-column layouts
- Use `.focusedSceneValue` for menu bar command integration and cross-window communication
- Keyboard shortcuts must use `keyboardShortcut(_:modifiers:)` and follow macOS HIG conventions

## Library Preferences

- Markdown rendering: swift-markdown by Apple for AST parsing
- Syntax highlighting: TreeSitter via SwiftTreeSitter bindings
- Keychain: use the Security framework directly; no third-party keychain wrappers
- Networking: URLSession only (no Alamofire); define Endpoint structs with URLRequest builders
- Testing: Swift Testing framework (`@Test`, `#expect`) for new tests; XCTest for UI tests

## File Naming

- Views: `FeatureView.swift` (SwiftUI view)
- View models: `FeatureViewModel.swift` (annotated with `@Observable`)
- SwiftData models: singular noun `Document.swift`, `Project.swift`
- Services: `PurposeService.swift` (e.g., `PersistenceService.swift`)
- AppKit wrappers: `NSFeatureViewRepresentable.swift`

## NEVER DO THIS

1. Never use `@ObservedObject` or `@StateObject` in new code; use `@Observable` macro and `@State` for ownership
2. Never force-unwrap optionals outside of test code; use `guard let` or `if let` with meaningful error handling
3. Never block the main thread with synchronous file I/O or network calls
4. Never hardcode strings in views; use `String(localized:)` and Localizable.xcstrings for all user-facing text
5. Never use `UserDefaults` for sensitive data; use Keychain Services via the Security framework
6. Never bypass the App Sandbox entitlements; request only the minimum file access needed via NSOpenPanel and security-scoped bookmarks

## Testing

- Use Swift Testing (`import Testing`) with `@Test` and `@Suite` for all new unit tests
- Test view models by asserting state changes after method calls with `#expect`
- SwiftData tests use an in-memory `ModelConfiguration` for isolation
- Network tests use a custom `URLProtocol` subclass to stub HTTP responses; no third-party mocking
- UI tests use XCUITest with accessibility identifiers set via `.accessibilityIdentifier("sidebar.item.\(id)")`
- Run tests with Cmd+U in Xcode or `swift test` from the command line for SPM packages

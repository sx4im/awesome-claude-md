# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- Swift 5.9+ / Xcode 15+
- SwiftUI for all UI
- Swift Concurrency (async/await, actors)
- SwiftData or Core Data for persistence
- Swift Package Manager for dependencies
- Minimum deployment target: iOS 17+

## Project Structure

```
App/
├── App.swift                # @main entry point, app-level config
├── Features/
│   ├── Auth/
│   │   ├── Views/           # LoginView, RegisterView
│   │   ├── ViewModels/      # AuthViewModel (@Observable)
│   │   └── Models/          # User, AuthState
│   ├── Home/
│   │   ├── Views/
│   │   ├── ViewModels/
│   │   └── Models/
│   └── Settings/
├── Core/
│   ├── Network/             # APIClient, endpoint definitions, interceptors
│   ├── Storage/             # SwiftData models, persistence manager
│   ├── Auth/                # Keychain wrapper, token management
│   └── Extensions/          # Swift/SwiftUI extensions
├── Components/              # Reusable views (PrimaryButton, AvatarView)
├── Resources/               # Assets, Localizable.strings, Info.plist
└── Utilities/               # Constants, Formatters, Logger
```

## Architecture Rules

- **MVVM with `@Observable`.** Every feature has Views (SwiftUI), ViewModels (`@Observable` classes), and Models (plain structs). Views observe ViewModels. ViewModels call services. Never put network calls or business logic in Views.
- **Feature-first organization.** Group by feature, not by type. `Features/Auth/` contains its own Views, ViewModels, and Models. Shared components go in `Components/` and `Core/`.
- **SwiftUI is the only UI framework.** No UIKit unless wrapping a component that SwiftUI doesn't support yet (via `UIViewRepresentable`). Never use Storyboards or XIBs.
- **Swift Concurrency everywhere.** Use `async/await` for all async operations. Use `@MainActor` on ViewModels. Use `actors` for thread-safe shared state. Never use completion handlers or `DispatchQueue` for new code.
- **Dependency injection via environment.** Pass services through SwiftUI's `@Environment` and custom `EnvironmentKey`s. Never use singletons with `shared` instances for anything that needs to be tested.

## Coding Conventions

- **ViewModels use `@Observable` (iOS 17+).** Not `ObservableObject` + `@Published` — `@Observable` is more performant (fine-grained tracking) and less boilerplate.
- **Views are small.** A View that exceeds 100 lines should be split into subviews. Extract reusable pieces into `Components/`. Use `ViewModifier` for shared styling.
- **Error handling:** throw typed errors, never return optionals to indicate failure. Define error enums: `enum NetworkError: LocalizedError { case unauthorized, serverError(Int) }`.
- **Naming:** Views end with `View` (`ProfileView`), ViewModels end with `ViewModel` (`ProfileViewModel`). Models are plain nouns (`User`, `Order`).
- **Access control:** Mark everything `private` or `fileprivate` by default. Only expose what other modules need. Never leave internal access on properties that should be private.

## Library Preferences

- **Networking:** `URLSession` with async/await and a thin typed wrapper. Not Alamofire (URLSession is sufficient with Swift Concurrency). Define endpoints as static configs, not string URLs.
- **Persistence:** SwiftData for new projects (iOS 17+). Core Data only if supporting iOS 16. Not Realm (vendor lock-in).
- **Keychain:** `KeychainAccess` — not raw Security framework calls (the API is C-based and error-prone).
- **Images:** AsyncImage (built-in) for simple use. Kingfisher or Nuke for caching and transformations.
- **Dependency injection:** SwiftUI Environment + custom keys. Not Swinject or Resolver (SwiftUI's DI is sufficient for most apps).

## NEVER DO THIS

1. **Never put business logic in SwiftUI Views.** Views describe UI. Navigation decisions, data transformations, and API calls belong in ViewModels or services.
2. **Never use `@ObservedObject` when `@State` or `@Observable` works.** `@ObservedObject` doesn't own the object — if the parent view re-renders, the object gets recreated. Use `@State` for View-owned state.
3. **Never force-unwrap optionals in production code.** `value!` is a crash waiting to happen. Use `guard let`, `if let`, or nil coalescing (`??`). Force-unwrap is only acceptable in tests and previews.
4. **Never block the main thread with synchronous I/O.** File reads, network calls, and database queries must be `async`. Use `Task { }` to bridge from synchronous SwiftUI lifecycle methods.
5. **Never use stringly-typed identifiers.** No `UserDefaults.standard.string(forKey: "token")` with raw strings. Define keys as constants or use a typed wrapper.
6. **Never use `DispatchQueue.main.async` in new code.** Use `@MainActor` and `MainActor.run { }`. GCD is legacy — Swift Concurrency is the replacement.
7. **Never ignore Xcode warnings.** Treat warnings as errors in CI. Deprecation warnings and unused variable warnings indicate real problems.

## Testing

- Use XCTest. Test ViewModels by injecting mock services and asserting state changes.
- Use `@MainActor` on test classes that test ViewModels (they're main-actor-isolated).
- SwiftUI Previews serve as visual tests — keep them up to date with realistic mock data.
- Snapshot tests with `swift-snapshot-testing` for critical UI components.

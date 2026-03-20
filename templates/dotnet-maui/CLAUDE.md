# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- .NET 8+ with .NET MAUI
- C# 12 (nullable reference types enabled)
- MVVM pattern with CommunityToolkit.Mvvm
- CommunityToolkit.Maui for converters, behaviors, and popups
- SQLite-net for local storage
- [Refit / HttpClient] for REST API consumption

## Project Structure

```
[SOLUTION_NAME].sln
├── src/
│   ├── [PROJECT_NAME]/                     # Main MAUI project
│   │   ├── App.xaml(.cs)                   # App shell, DI bootstrap
│   │   ├── AppShell.xaml(.cs)              # Navigation structure
│   │   ├── MauiProgram.cs                  # Host builder and service registration
│   │   ├── Views/
│   │   │   ├── MainPage.xaml(.cs)
│   │   │   └── SettingsPage.xaml(.cs)
│   │   ├── ViewModels/
│   │   │   ├── MainViewModel.cs
│   │   │   └── SettingsViewModel.cs
│   │   ├── Models/
│   │   │   └── [DomainObject].cs
│   │   ├── Services/
│   │   │   ├── INavigationService.cs
│   │   │   ├── IApiService.cs
│   │   │   └── DatabaseService.cs
│   │   ├── Converters/
│   │   │   └── BoolToColorConverter.cs
│   │   ├── Resources/
│   │   │   ├── Styles/
│   │   │   ├── Fonts/
│   │   │   └── Images/
│   │   └── Platforms/                      # Platform-specific code
│   │       ├── Android/
│   │       ├── iOS/
│   │       ├── MacCatalyst/
│   │       └── Windows/
│   └── [PROJECT_NAME].Core/               # Shared logic (optional class library)
├── tests/
│   ├── [PROJECT_NAME].UnitTests/
│   └── [PROJECT_NAME].UITests/            # Appium-based UI tests
```

## Architecture Rules

- **Strict MVVM separation.** Views know about ViewModels (via `BindingContext`). ViewModels never reference Views, Pages, or UI types. ViewModels expose `ObservableProperty` attributes and `RelayCommand` attributes. Code-behind files (`.xaml.cs`) contain only navigation wiring and platform-specific visual logic.
- **Dependency injection for everything.** Register all ViewModels, Services, and Pages in `MauiProgram.cs` using `builder.Services`. Never `new` up a ViewModel or Service manually. Use constructor injection exclusively.
- **Shell-based navigation.** Define routes in `AppShell.xaml` and navigate via `Shell.Current.GoToAsync("//route")`. Register detail routes with `Routing.RegisterRoute()`. Never use `Navigation.PushAsync(new SomePage())` — it bypasses DI and creates untestable tight coupling.
- **Platform code in Platforms/ only.** Use `#if ANDROID` / `#if IOS` sparingly and only inside `Platforms/` directories or partial classes. Never scatter `#if` blocks through ViewModels. Abstract platform differences behind interfaces resolved by DI.
- **Async all the way.** Every I/O operation (API calls, database reads, file access) is async. Use `[RelayCommand]` which generates async command wrappers. Never call `.Result` or `.Wait()` — it deadlocks the MAUI UI thread.

## Coding Conventions

- **CommunityToolkit.Mvvm source generators.** Use `[ObservableProperty]` instead of manual `INotifyPropertyChanged`. Use `[RelayCommand]` instead of manual `ICommand` implementations. This eliminates boilerplate and reduces ViewModel sizes by 60%.
- **Naming:** ViewModels are `FeatureViewModel.cs`, Views are `FeaturePage.xaml`. The ViewModel for `SettingsPage` is `SettingsViewModel`. Never suffix ViewModels with `Page` or Views with `ViewModel`.
- **Data binding syntax.** Use `{Binding PropertyName}` in XAML. Use `x:DataType` for compiled bindings on every page: `<ContentPage x:DataType="vm:MainViewModel">`. Compiled bindings catch typos at build time instead of silently failing at runtime.
- **Converters are reusable.** Create converters in `Converters/` and register them in `App.xaml` as `Application.Resources`. Never create a converter used by only one binding — use `DataTrigger` or a computed property on the ViewModel instead.
- **Semantic properties for accessibility.** Set `SemanticProperties.Description` and `SemanticProperties.Hint` on all interactive elements. MAUI's accessibility support works cross-platform but only if you use it.

## Library Preferences

- **MVVM framework:** CommunityToolkit.Mvvm (source-generated, no reflection, AOT-compatible). Not Prism.MAUI (heavy, complex setup). Not ReactiveUI unless the team already uses Rx extensively.
- **HTTP:** Refit for typed API interfaces, or HttpClientFactory for manual control. Not raw `new HttpClient()` (socket exhaustion, no DI lifecycle management).
- **Local database:** sqlite-net-pcl with async API. Not LiteDB (less MAUI community support). Not Entity Framework Core (too heavy for mobile local storage).
- **UI components:** CommunityToolkit.Maui for popups, animations, and converters. Syncfusion/Telerik for data grids and charts if budget allows.
- **Images:** SVG via `MauiImage` build action with automatic platform-specific rasterization. Not manually creating 1x/2x/3x PNGs.

## File Naming

- Views: `FeaturePage.xaml` + `FeaturePage.xaml.cs`
- ViewModels: `FeatureViewModel.cs`
- Services: `IFeatureService.cs` (interface) + `FeatureService.cs` (implementation)
- Models: `PascalCase.cs` matching the domain object name
- Converters: `DescriptiveNameConverter.cs` (e.g., `InverseBoolConverter.cs`)

## NEVER DO THIS

1. **Never put business logic in code-behind.** `MainPage.xaml.cs` handles only page-level visual events that have no ViewModel equivalent (lifecycle, platform-specific rendering). If you find yourself writing `if/else` in code-behind, it belongs in the ViewModel.
2. **Never use `MainThread.BeginInvokeOnMainThread` in ViewModels.** CommunityToolkit's `ObservableProperty` and command infrastructure already marshal to the UI thread. If you need to manually dispatch, your architecture has a threading bug.
3. **Never hardcode colors or font sizes in XAML.** Use `StaticResource` or `DynamicResource` referencing styles in `Resources/Styles/`. Hardcoded `TextColor="#FF0000"` makes dark mode support impossible and creates visual inconsistency.
4. **Never use `Task.Run()` to wrap synchronous code and call it "async."** `Task.Run(() => SyncMethod())` just moves the blocking call to a thread pool thread. It doesn't make the operation async. Use genuinely async APIs or acknowledge the method is synchronous.
5. **Never ignore platform-specific sizing.** Use `OnPlatform` and `OnIdiom` for values that differ across platforms. A button that looks correct on Android will be too small on iOS and oversized on Windows. Test on every target platform.
6. **Never forget to dispose subscriptions.** If a ViewModel subscribes to `MessagingCenter` or `WeakReferenceMessenger`, unsubscribe when the page disappears. Leaked subscriptions cause duplicate event handling and memory leaks.
7. **Never deploy without testing on physical devices.** The MAUI hot reload and emulators hide performance issues, gesture problems, and platform-specific rendering bugs that only appear on real hardware.

## Testing

- Unit test ViewModels by instantiating them with mocked services. Assert that commands update `ObservableProperty` values and call service methods correctly. No UI framework needed.
- Use `xUnit` with `Moq` or `NSubstitute` for service mocking. Verify navigation calls: `mockNavService.Verify(n => n.GoToAsync("//details"), Times.Once)`.
- Use Appium with the MAUI driver for end-to-end UI tests on emulators. Set `AutomationId` on all testable elements in XAML.
- Test on at least Android and iOS physical devices before release. Windows and MacCatalyst can use emulators for CI but verify layouts on real hardware for production releases.

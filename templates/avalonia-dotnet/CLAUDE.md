# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Framework: Avalonia UI 11+ for cross-platform desktop (Windows, macOS, Linux)
- Language: C# 12 with .NET 9
- Architecture: MVVM with CommunityToolkit.Mvvm source generators
- Data Binding: Avalonia compiled bindings with x:DataType
- Navigation: Custom INavigationService with view model-first approach
- Database: Entity Framework Core 9 with SQLite provider
- HTTP: HttpClient with IHttpClientFactory from Microsoft.Extensions.Http
- DI: Microsoft.Extensions.DependencyInjection
- Styling: Avalonia Fluent theme with custom resource dictionaries

## Project Structure

```
src/
  App/
    App.axaml                  # Application root, styles, resources
    App.axaml.cs               # OnFrameworkInitializationCompleted, DI setup
    Program.cs                 # Entry point with AppBuilder configuration
    ViewLocator.cs             # Convention-based View-ViewModel resolution
  ViewModels/
    MainWindowViewModel.cs     # Shell window VM with navigation state
    HomeViewModel.cs           # Feature VMs inheriting ObservableObject
    SettingsViewModel.cs
    Dialogs/
      ConfirmDialogViewModel.cs
  Views/
    MainWindow.axaml           # Shell window with NavigationView or SplitView
    MainWindow.axaml.cs
    HomePage.axaml             # UserControl pages
    SettingsPage.axaml
    Dialogs/
      ConfirmDialog.axaml      # Custom dialog windows
  Models/
    Item.cs                    # Domain entities (POCO classes)
    AppSettings.cs             # Settings model serialized to JSON
  Services/
    INavigationService.cs      # Navigation interface
    NavigationService.cs       # Implementation managing content control binding
    IDialogService.cs          # Dialog abstraction for testability
    DialogService.cs
    IDatabaseService.cs
    DatabaseService.cs         # EF Core DbContext wrapper
  Data/
    AppDbContext.cs             # EF Core DbContext with DbSet properties
    Migrations/                # EF Core migrations (auto-generated)
    Configurations/
      ItemConfiguration.cs     # IEntityTypeConfiguration for fluent model config
  Converters/
    BoolToVisibilityConverter.cs
    EnumToStringConverter.cs
  Assets/
    Fonts/
    Icons/
    Styles/
      CustomStyles.axaml       # Shared style resources
```

## Architecture Rules

- Follow MVVM strictly: views never reference services directly; all logic goes through view models
- Use CommunityToolkit.Mvvm source generators: `[ObservableProperty]`, `[RelayCommand]`, `partial` classes
- Views discover their view model via `ViewLocator` convention: `HomeView` resolves to `HomeViewModel`
- All services are registered in DI container and injected via constructor into view models
- Navigation is view model-first: navigate by creating/activating a view model; ViewLocator finds the view
- Database access goes through a service layer, not directly from view models

## Coding Conventions

- Use compiled bindings everywhere: `<TextBlock Text="{Binding Name}" x:DataType="vm:HomeViewModel" />`
- Declare observable properties with `[ObservableProperty] private string _name;` (source-generated property: `Name`)
- Commands use `[RelayCommand]` attribute on methods: `[RelayCommand] private async Task SaveAsync()`
- Async relay commands automatically manage `IsRunning` for loading state
- Use `IAsyncRelayCommand` for commands that need cancellation support
- AXAML styles use `<Style Selector="Button.primary">` with Avalonia CSS-like selectors
- Handle platform differences with `RuntimeInformation.IsOSPlatform()` in services, never in views

## Library Preferences

- MVVM: CommunityToolkit.Mvvm 8+ (source generators, not reflection)
- Database: EF Core 9 with SQLite (Microsoft.EntityFrameworkCore.Sqlite)
- Serialization: System.Text.Json with source-generated serializer contexts
- HTTP: IHttpClientFactory with typed clients from Microsoft.Extensions.Http
- Logging: Microsoft.Extensions.Logging with Serilog sink for file output
- Settings storage: JSON file in Environment.SpecialFolder.ApplicationData
- Icons: Avalonia.Svg.Skia for SVG icon rendering or FluentAvalonia icon pack
- Theming: FluentAvaloniaUI for Windows 11 Fluent design on all platforms

## File Naming

- Views: `FeaturePage.axaml` with `FeaturePage.axaml.cs` code-behind
- ViewModels: `FeatureViewModel.cs` inheriting `ObservableObject`
- Services: `IFeatureService.cs` (interface) and `FeatureService.cs` (implementation)
- Models: singular `Item.cs`, `User.cs`
- Converters: `PurposeConverter.cs` (e.g., `BoolToVisibilityConverter.cs`)
- EF Configurations: `EntityNameConfiguration.cs`

## NEVER DO THIS

1. Never use code-behind for business logic; `.axaml.cs` files should only contain view-specific initialization or event-to-command bridging
2. Never use reflection-based bindings in release builds; always set `x:DataType` for compiled bindings
3. Never reference view types from view models; view models must be UI-framework-agnostic for testability
4. Never use `MessageBox.Show()` directly; use `IDialogService` so dialogs can be mocked in tests
5. Never block the UI thread with `.Result` or `.Wait()` on async calls; use `async/await` throughout
6. Never hardcode file paths with backslashes; use `Path.Combine()` and `Environment.SpecialFolder` for cross-platform compatibility
7. Never install platform-specific NuGet packages in the shared project; use conditional compilation or platform-specific projects

## Testing

- Unit test view models with xUnit and Moq/NSubstitute for service mocking
- Test `[RelayCommand]` methods by calling the underlying method and asserting property changes
- Verify `[ObservableProperty]` notifications using `PropertyChanged` event subscriptions in tests
- EF Core tests use `InMemoryDatabase` provider or a test SQLite database
- Test converters independently by calling `Convert()` and `ConvertBack()` with known inputs
- Integration tests spin up the DI container with test registrations
- Run tests with `dotnet test` from the solution root
- No UI automation tests by default; use Avalonia's headless testing platform for rendering verification

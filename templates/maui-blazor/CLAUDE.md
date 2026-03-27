# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Framework: .NET 9 MAUI Blazor Hybrid
- Language: C# 12 with nullable reference types enabled
- UI: Blazor Razor components rendered in BlazorWebView on native platforms
- Styling: Bootstrap 5 via Blazor + custom SCSS compiled to CSS
- State Management: Fluxor (Flux/Redux pattern for Blazor) with dependency injection
- Data: Entity Framework Core 9 with SQLite for local storage
- HTTP: HttpClient with Refit for typed API interfaces
- DI: Microsoft.Extensions.DependencyInjection (built into MAUI)
- Platforms: Android, iOS, Windows, macOS (Mac Catalyst)

## Project Structure

```
Platforms/
  Android/
    MainApplication.cs         # Android application class
    AndroidManifest.xml
  iOS/
    AppDelegate.cs
    Info.plist
  Windows/
    App.xaml                   # WinUI application entry
  MacCatalyst/
    AppDelegate.cs
MauiProgram.cs                 # CreateMauiApp builder with service registration
MainPage.xaml                  # ContentPage hosting BlazorWebView
MainPage.xaml.cs
Components/
  Layout/
    MainLayout.razor           # Shared layout with NavMenu
    NavMenu.razor              # Sidebar navigation component
  Pages/
    Home.razor                 # Routable page (@page "/")
    Items.razor                # @page "/items"
    Settings.razor             # @page "/settings"
  Shared/
    DataGrid.razor             # Reusable data table component
    ConfirmDialog.razor        # Modal confirmation dialog
    LoadingSpinner.razor
    ErrorBoundaryHandler.razor
  Features/
    Items/
      ItemList.razor           # Feature-specific components
      ItemDetail.razor
      ItemForm.razor
Services/
  IItemService.cs              # Service interface
  ItemService.cs               # Implementation using EF Core or Refit
  IDeviceService.cs            # Abstraction over MAUI Essentials
  DeviceService.cs             # Platform-specific device capabilities
  IPlatformStorageService.cs
  PlatformStorageService.cs    # File storage using MAUI FileSystem API
Store/
  Items/
    ItemsState.cs              # Fluxor state record
    ItemsActions.cs            # Action classes for state mutations
    ItemsReducers.cs           # Pure reducer functions
    ItemsEffects.cs            # Side-effect handlers (API calls, persistence)
  App/
    AppState.cs
    AppActions.cs
    AppReducers.cs
Models/
  Item.cs                      # Domain entity classes
  ApiResponse.cs               # Generic API response wrapper
Data/
  AppDbContext.cs               # EF Core DbContext
  Migrations/
wwwroot/
  css/
    app.css                    # Compiled styles and overrides
  index.html                   # Blazor root HTML (loaded by BlazorWebView)
```

## Architecture Rules

- All UI is Razor components rendered inside `BlazorWebView`; XAML is only used for the `MainPage.xaml` host
- Fluxor manages all shared application state; components dispatch actions and select state via `IState<T>`
- Services are registered in `MauiProgram.cs` and injected into Razor components or Fluxor effects
- Platform-specific code uses MAUI Essentials APIs (Geolocation, Camera, FileSystem) wrapped in service interfaces
- Razor components in Pages/ are routable (`@page "/path"`); components in Shared/ and Features/ are non-routable
- EF Core DbContext is registered as scoped; database file is stored in `FileSystem.AppDataDirectory`

## Coding Conventions

- Razor components use `@inject` for DI and `@inherits FluxorComponent` for automatic state subscription disposal
- Component parameters use `[Parameter]` attribute; cascading values use `[CascadingParameter]`
- Use `EventCallback<T>` for child-to-parent communication; never pass parent references to children
- Fluxor state classes are C# records for immutable state: `public record ItemsState(List<Item> Items, bool IsLoading)`
- Reducers are static pure functions: `[ReducerMethod] public static ItemsState On(ItemsState state, LoadItemsAction action)`
- Effects handle async operations: `[EffectMethod] public async Task Handle(LoadItemsAction action, IDispatcher dispatcher)`
- Use `@key` directive on list-rendered elements for efficient diffing

## Library Preferences

- State management: Fluxor for Blazor (Redux pattern with middleware support)
- API client: Refit 7 for typed REST API interfaces generated from C# interface definitions
- Database: EF Core 9 with SQLite (stored in MAUI FileSystem.AppDataDirectory)
- Validation: FluentValidation with Blazor integration for form validation
- Logging: Microsoft.Extensions.Logging with Serilog sink, writing to FileSystem.AppDataDirectory
- CSS: Bootstrap 5 loaded from wwwroot; no Tailwind (conflicts with Blazor rendering)
- Device APIs: MAUI Essentials (Connectivity, Geolocation, Preferences, SecureStorage)
- Mapping: AutoMapper for DTO-to-model conversions

## File Naming

- Razor pages: `FeatureName.razor` with optional `FeatureName.razor.cs` code-behind for complex logic
- Razor components: PascalCase `ComponentName.razor`
- Services: `IFeatureService.cs` (interface) + `FeatureService.cs` (implementation)
- Fluxor state: `FeatureState.cs`, `FeatureActions.cs`, `FeatureReducers.cs`, `FeatureEffects.cs`
- Models: singular `Item.cs`
- Platform-specific: kept in `Platforms/` folder structure managed by MAUI SDK

## NEVER DO THIS

1. Never use JavaScript interop for tasks that MAUI Essentials or Blazor can handle natively (e.g., clipboard, geolocation)
2. Never reference `Microsoft.Maui.*` namespaces directly in Razor components; use injected service abstractions for testability
3. Never mutate Fluxor state directly; always dispatch actions and handle mutations in reducers
4. Never use `StateHasChanged()` manually when using Fluxor; `FluxorComponent` base class handles re-renders automatically
5. Never store sensitive data in `Preferences`; use `SecureStorage` from MAUI Essentials which uses platform keychain
6. Never add platform-specific `#if` directives in Razor components; isolate platform logic in services behind interfaces
7. Never skip the `wwwroot/index.html` configuration; the BlazorWebView requires it as the Blazor entry point

## Testing

- Unit test Razor components with bUnit: `using var ctx = new TestContext();` and render with `ctx.RenderComponent<ItemList>()`
- Fluxor tests verify reducers as pure functions: pass state and action, assert returned state
- Fluxor effect tests use `FluxorTestStore` to dispatch actions and verify emitted follow-up actions
- Service tests mock EF Core with `InMemoryDatabase` provider or Moq/NSubstitute for interface mocks
- Refit API tests use `HttpMessageHandler` mocks with `MockHttp` library
- Run tests with `dotnet test`; bUnit tests run on the host machine, no device emulator needed
- Integration tests register services with test doubles in a fresh DI container
- Manual testing on each platform via `dotnet build -t:Run -f net9.0-android` and equivalent targets

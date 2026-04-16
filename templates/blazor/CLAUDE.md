# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Blazor (WebAssembly or Server)
- .NET 8+
- C# 12
- Razor components
- SignalR (for Server)

## Project Structure
```
├── Components/
│   ├── Layout/
│   │   └── MainLayout.razor
│   ├── Pages/
│   │   └── Index.razor
│   └── Shared/
│       └── Button.razor
├── Services/
│   └── ApiService.cs
├── Models/
│   └── User.cs
└── Program.cs
```

## Architecture Rules

- **Razor components.** UI defined in `.razor` files with HTML + C#.
- **WebAssembly vs Server.** WASM runs in browser, Server runs on server with SignalR.
- **Dependency injection.** Built-in DI for services.
- **Component parameters.** Pass data with `[Parameter]`.

## Coding Conventions

- Component: `@code { [Parameter] public string Title { get; set; } }`.
- Event: `@onclick="HandleClick"` with `void HandleClick() { ... }`.
- Service: `@inject IApiService Api` in component or constructor injection.
- Lifecycle: `OnInitialized()`, `OnParametersSet()`, `OnAfterRender()`.
- Routing: `@page "/users"` for route declaration.

## NEVER DO THIS

1. **Never mix WASM and Server in same app carelessly.** Different architectures.
2. **Never ignore prerendering in Server Blazor.** Handle both prerender and interactive phases.
3. **Never forget to dispose resources.** Implement `IDisposable` for cleanup.
4. **Never use large payloads with SignalR.** Server Blazor can hit message size limits.
5. **Never skip lazy loading for WASM.** Reduce initial download size.
6. **Never ignore the JavaScript interop cost.** Crossing boundary has overhead.
7. **Never forget about circuit disposal.** Server Blazor circuits can disconnect—handle it.

## Testing

- Test with bUnit for component testing.
- Test with Playwright for E2E.
- Test WASM separately from Server.


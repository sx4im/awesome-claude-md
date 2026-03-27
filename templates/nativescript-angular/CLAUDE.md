# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Framework: NativeScript 8 with Angular 17+
- Language: TypeScript 5.4+ in strict mode
- UI: NativeScript native UI components (no DOM, no HTML elements)
- State Management: NgRx Signal Store for reactive state
- Navigation: NativeScript Angular RouterModule with page-router-outlet
- Styling: NativeScript CSS subset + SCSS with platform-specific overrides
- Build: NativeScript CLI with webpack bundling
- HTTP: Angular HttpClient with interceptors

## Project Structure

```
src/
  app/
    app.module.ts               # Root NgModule with NativeScriptModule imports
    app-routing.module.ts       # Route definitions with loadChildren for lazy modules
    app.component.ts            # Root component with page-router-outlet
    core/
      services/
        api.service.ts          # HttpClient wrapper with base URL configuration
        auth.service.ts         # Token management, login/logout logic
        navigation.service.ts   # RouterExtensions wrapper for NativeScript navigation
      interceptors/
        auth.interceptor.ts     # Attaches Bearer token to outgoing requests
      guards/
        auth.guard.ts           # canActivate guard checking auth state
    shared/
      components/
        action-bar.component.ts   # Reusable ActionBar with back navigation
        loading-indicator.component.ts
      pipes/
        date-format.pipe.ts
      directives/
        platform.directive.ts   # *nsIfAndroid, *nsIfIos structural directives
    features/
      home/
        home.module.ts          # Lazy-loaded feature module
        home.component.ts       # Uses StackLayout, ListView, etc.
        home.component.css
        home.store.ts           # NgRx Signal Store for home feature
      detail/
        detail.module.ts
        detail.component.ts
        detail.component.css
    models/
      user.model.ts             # TypeScript interfaces for domain entities
      api-response.model.ts
  assets/
    fonts/                      # Custom font files (.ttf, .otf)
    images/                     # Platform-aware image resources
  App_Resources/
    Android/                    # Android-specific resources (AndroidManifest, drawables)
    iOS/                        # iOS-specific resources (Info.plist, LaunchScreen.storyboard)
nativescript.config.ts          # NativeScript project configuration
```

## Architecture Rules

- Use NativeScript layout containers (StackLayout, GridLayout, FlexboxLayout) instead of HTML elements
- Every feature is a lazy-loaded Angular module with its own routing, components, and store
- Services in core/ are singleton providers registered in AppModule; feature-specific services live in their module
- Navigation uses `RouterExtensions` from `@nativescript/angular` for native page transitions
- Platform-specific code uses `isAndroid` and `isIOS` from `@nativescript/core` or platform directives
- Never import `@angular/platform-browser`; use `@nativescript/angular` equivalents for all platform APIs

## Coding Conventions

- Components use `changeDetection: ChangeDetectionStrategy.OnPush` by default for performance
- Use Angular signals and the new `input()`, `output()`, `model()` functions instead of decorators where possible
- Templates use NativeScript XML markup: `<StackLayout>`, `<Label>`, `<Button>`, `<ListView>`
- Bind events with `(tap)` not `(click)`; NativeScript has no click event
- Use `<ng-container>` for structural directives to avoid unnecessary layout wrappers
- Apply `class` and NativeScript CSS properties for styling; use `.android.css` and `.ios.css` for platform overrides
- Access native APIs via `@nativescript/core` utilities or direct `java.lang` / `objc` bridge calls in services

## Library Preferences

- State: NgRx Signal Store (`@ngrx/signals`) for feature-level reactive state
- HTTP: Angular HttpClient (built-in); no Axios or other third-party HTTP libs
- Forms: Angular Reactive Forms with typed FormGroup via `FormBuilder.nonNullable`
- Camera: @nativescript/camera plugin
- Geolocation: @nativescript/geolocation
- Local storage: @nativescript/core ApplicationSettings (key-value) or SQLite plugin for structured data
- UI widgets: @nativescript-community packages (ui-collectionview, ui-drawer)

## File Naming

- Components: `feature-name.component.ts` with co-located `.html` (XML template) and `.css`
- Modules: `feature-name.module.ts` with `feature-name-routing.module.ts`
- Services: `purpose-name.service.ts`
- Stores: `feature-name.store.ts` (NgRx Signal Store)
- Models: `entity-name.model.ts`
- Guards/interceptors: `purpose-name.guard.ts`, `purpose-name.interceptor.ts`

## NEVER DO THIS

1. Never use HTML elements (`<div>`, `<span>`, `<p>`) in templates; NativeScript renders native widgets, not a WebView
2. Never import from `@angular/platform-browser` or `@angular/platform-browser-dynamic`; these are DOM-specific
3. Never use `document`, `window`, or any DOM API; they do not exist in the NativeScript runtime
4. Never use CSS properties unsupported by NativeScript (e.g., `float`, `display: grid`, `position: absolute` with `z-index`)
5. Never navigate with Angular's default `Router.navigate()`; use `RouterExtensions` for native back-stack integration
6. Never skip `App_Resources` platform configuration; missing entries cause build failures on device
7. Never use eager-loaded feature modules; lazy loading is critical for startup performance on mobile

## Testing

- Unit tests with Jasmine and Karma using `@nativescript/unit-test-runner`
- Test components by providing mock services and asserting template bindings
- NgRx Signal Store tests create the store with `TestBed` and verify computed signals and method effects
- Service tests mock `HttpClient` with `HttpClientTestingModule` and `HttpTestingController`
- Run unit tests on device or emulator: `ns test android` or `ns test ios`
- E2E tests use Appium with WebDriverIO for native UI automation
- Test platform-specific branches by mocking `isAndroid` / `isIOS` boolean imports

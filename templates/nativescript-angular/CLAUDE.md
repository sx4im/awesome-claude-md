# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Mobile)

### Release Discipline
- Protect offline/poor-network behavior and state recovery paths.
- Avoid platform-specific regressions by validating iOS/Android parity.
- Respect battery/performance constraints in background tasks.

### Merge/Release Gates
- Build and runtime smoke tests pass on target platforms.
- Crash-prone paths (auth, navigation, persistence) validated.
- No release with unresolved permission/security handling gaps.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

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

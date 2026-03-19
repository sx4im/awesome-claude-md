# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Angular 17+ (standalone components, signals)
- TypeScript (strict mode)
- Angular CLI for build and scaffolding
- RxJS 7 (used judiciously, signals preferred for state)
- Tailwind CSS or Angular Material
- NgRx (signal store) for complex state

## Project Structure

```
src/app/
├── core/
│   ├── guards/              # Route guards (auth, role-based)
│   ├── interceptors/        # HTTP interceptors (auth token, error handling)
│   ├── services/            # Singleton services (auth, api, storage)
│   └── models/              # Shared interfaces and types
├── features/
│   ├── dashboard/
│   │   ├── dashboard.component.ts    # Standalone component
│   │   ├── dashboard.component.html
│   │   ├── components/               # Feature-scoped child components
│   │   └── services/                 # Feature-scoped services
│   ├── users/
│   └── settings/
├── shared/
│   ├── components/          # Reusable UI components (ButtonComponent, ModalComponent)
│   ├── directives/          # Custom directives (highlight, autofocus)
│   ├── pipes/               # Custom pipes (dateFormat, truncate)
│   └── utils/               # Pure utility functions
├── app.component.ts         # Root component
├── app.routes.ts            # Route definitions (lazy-loaded)
└── app.config.ts            # Application providers config
```

## Architecture Rules

- **Standalone components only.** Every component uses `standalone: true`. No `NgModule` declarations. Import dependencies directly in the component's `imports` array. NgModules are legacy. don't create new ones.
- **Feature-first organization.** Each feature (`dashboard/`, `users/`, `settings/`) is a self-contained directory with its own components, services, and routes. Cross-feature code goes in `shared/` or `core/`.
- **Signals for reactive state.** Use `signal()`, `computed()`, and `effect()` for component state. RxJS is for streams (HTTP responses, WebSocket events, complex async orchestration). Don't use `BehaviorSubject` when a `signal` works.
- **Lazy-loaded routes.** Every feature route uses `loadComponent` or `loadChildren` for code splitting: `{ path: 'dashboard', loadComponent: () => import('./features/dashboard/dashboard.component') }`. Never eagerly import feature components.
- **Smart/dumb component pattern.** Container components (smart) inject services and manage state. Presentational components (dumb) receive data via `@Input` and emit events via `@Output`. Dumb components have zero injected services.

## Coding Conventions

- **Signals over RxJS for state.** `count = signal(0)`. `doubled = computed(() => this.count() * 2)`. `effect(() => console.log(this.count()))`. Reserve RxJS for HTTP, WebSocket, and complex event streams.
- **`inject()` function over constructor injection.** `private authService = inject(AuthService)`. Cleaner than constructor parameter lists, works with standalone components, and supports `inject` in functions.
- **Typed reactive forms.** Use `FormGroup`, `FormControl` with explicit types: `new FormControl<string>('')`. Never use untyped `FormBuilder.group({})`. the `nonNullable` builder gives strict types.
- **OnPush change detection.** Every component uses `changeDetection: ChangeDetectionStrategy.OnPush`. Combined with signals, this gives you fine-grained reactivity without zone.js overhead.
- **Route params via `input()`.** Angular 17+ can bind route params to component inputs: `id = input<string>()` with `withComponentInputBinding()` in the router config. Don't inject `ActivatedRoute` for simple params.

## Library Preferences

- **State management:** NgRx Signal Store for complex global state. Plain signals for component state. Not Akita (dying), not NGXS (niche). Not classic NgRx Store unless you need DevTools time-travel for a large app.
- **UI:** Angular Material 3 or Tailwind CSS. Not PrimeNG (heavy), not NG-ZORRO (unless building for Ant Design system).
- **HTTP:** Angular's built-in `HttpClient` with functional interceptors. Not Axios (HttpClient is RxJS-native and supports interceptors via Angular DI).
- **Forms:** Angular Reactive Forms (typed). Not template-driven forms for anything beyond trivial inputs.
- **Testing:** Jest (via `jest-preset-angular`). not Karma (slow, browser-based). Cypress or Playwright for E2E.

## NEVER DO THIS

1. **Never create NgModules for new features.** Standalone components replaced NgModules. A new `@NgModule` in a modern Angular project is technical debt from day one.
2. **Never use `any` for HTTP response types.** Type every API call: `this.http.get<User[]>('/api/users')`. Untyped responses propagate `any` throughout your components.
3. **Never subscribe to observables without unsubscribing.** Use `takeUntilDestroyed()` from `@angular/core/rxjs-interop`, `async` pipe, or `toSignal()`. Leaked subscriptions cause memory leaks and stale state.
4. **Never use `Default` change detection in new components.** `OnPush` is the standard. Default change detection runs on every event in the entire app. it's wasteful. Combine `OnPush` with signals for optimal performance.
5. **Never access DOM directly with `document.querySelector`.** Use `viewChild()`, `contentChild()`, or `ElementRef` injection. Direct DOM access breaks SSR and bypasses Angular's rendering pipeline.
6. **Never put business logic in components.** Components handle UI. Business logic lives in services. A component method that exceeds 10 lines is doing too much. extract to a service.
7. **Never use `BehaviorSubject` when `signal()` works.** Signals are simpler, don't require manual subscription management, and integrate with Angular's change detection. `BehaviorSubject` is the old pattern.

## Testing

- Unit tests with Jest: test services by injecting mock dependencies. Test components with `TestBed.configureTestingModule` and standalone component imports.
- Use `ComponentFixture` for component tests. Use `spectator` for cleaner component test API.
- E2E with Playwright (not Protractor. deprecated). Test user flows: login, CRUD, navigation.
- Test signal-based components by reading signal values directly in tests: `expect(component.count()).toBe(5)`.

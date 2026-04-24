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

## Production Delivery Playbook (Category: Frontend)

### Release Discipline
- Enforce performance budgets (bundle size, LCP, CLS) before merge.
- Preserve accessibility baselines (semantic HTML, keyboard nav, ARIA correctness).
- Block hydration/runtime errors with production build verification.

### Merge/Release Gates
- Typecheck + lint + unit tests + production build pass.
- Critical route smoke tests for navigation, auth, and error boundaries.
- No new console errors/warnings in key user flows.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Analog.js 1.x as the Angular meta-framework
- Angular 18 with signals and standalone components
- Vite 5 as the build system (via Analog's Vite plugin)
- File-based routing with Analog's filesystem router
- Nitro server engine for API routes and SSR
- Angular Material 18 for UI components
- TanStack Query (Angular) for server state management
- Zod 3 for runtime validation
- Tailwind CSS 4 for utility styling alongside Angular Material

## Project Structure

```
src/
  app/
    pages/
      index.page.ts             # Home page (maps to /)
      about.page.ts             # About page (maps to /about)
      products/
        index.page.ts           # Products list (maps to /products)
        [id].page.ts            # Product detail (maps to /products/:id)
      (auth)/
        login.page.ts           # Grouped auth pages
        register.page.ts
    components/                  # Shared standalone components
    layouts/                     # Layout components
    guards/                      # Route guards
    interceptors/                # HTTP interceptors
    models/                      # TypeScript interfaces and Zod schemas
    services/                    # Injectable Angular services
  server/
    routes/
      v1/
        users.ts                 # API route: /api/v1/users
        products.ts              # API route: /api/v1/products
    middleware/                   # Nitro server middleware
  styles.css                     # Global styles and Tailwind entry
  main.ts                        # Angular bootstrap
  app.config.ts                  # Application providers configuration
vite.config.ts                   # Vite + Analog plugin configuration
```

## Architecture Rules

- All components are standalone. NgModules are never used. Declare `imports` directly on the component decorator.
- Use Angular signals exclusively for reactive state: `signal()`, `computed()`, `effect()`. Never use RxJS `BehaviorSubject` for component state.
- RxJS is permitted only for event streams (WebSockets, complex async orchestration). Use `toSignal()` to convert observables to signals at service boundaries.
- Page components live in `src/app/pages/` following Analog file-based routing conventions. Route parameters use `[paramName]` bracket syntax.
- API routes in `src/server/routes/` use Nitro's `defineEventHandler`. They handle validation, database access, and return JSON.
- Dependency injection uses the `inject()` function, never constructor injection. Services use `providedIn: 'root'`.
- Change detection uses `OnPush` strategy on every component. Signals ensure automatic template updates.

## Coding Conventions

- Page components are defined in `.page.ts` files and export a default component.
- Components use the inline template style for small components (under 30 lines of template). Separate `.html` files for larger templates.
- Signal state is declared at the top of the component class, computed signals next, then effect registrations, then methods.
- Use `input()` and `output()` signal-based APIs for component I/O instead of `@Input()` and `@Output()` decorators.
- Forms use Angular Reactive Forms with Zod schemas for validation via a shared validator adapter.
- Template syntax uses `@if`, `@for`, `@switch` control flow blocks. Never use `*ngIf`, `*ngFor`, or `*ngSwitch` structural directives.
- Services that call API routes return `Promise` from `fetch` or use `HttpClient` piped through `toSignal()`.

## Library Preferences

- UI framework: Angular Material 18 with CDK for custom components
- State management: Angular signals + TanStack Query for server cache (never NgRx for this project scale)
- Forms: Angular Reactive Forms with Zod validation adapters
- HTTP: Angular HttpClient with interceptors for auth tokens
- Icons: Angular Material icons or unplugin-icons
- Dates: date-fns with Angular pipes wrapping format functions
- Testing mocks: ng-mocks for component shallow testing

## File Naming

- Pages: `kebab-case.page.ts` (Analog convention)
- Components: `kebab-case.component.ts`
- Services: `kebab-case.service.ts`
- Guards: `kebab-case.guard.ts`
- Interceptors: `kebab-case.interceptor.ts`
- Models: `kebab-case.model.ts`
- API routes: `kebab-case.ts` in `src/server/routes/`

## NEVER DO THIS

1. Never use NgModules or declare components in modules. Every component must be standalone with its own imports.
2. Never use `*ngIf`, `*ngFor`, or `*ngSwitch`. Use the built-in `@if`, `@for`, `@switch` template control flow blocks.
3. Never use `BehaviorSubject` for UI state. Use `signal()` and `computed()` for all reactive component state.
4. Never use constructor-based dependency injection. Use the `inject()` function in field initializers.
5. Never use `@Input()` and `@Output()` decorators. Use the signal-based `input()`, `output()`, and `model()` functions.
6. Never disable `OnPush` change detection. All components must use `changeDetection: ChangeDetectionStrategy.OnPush`.

## Testing

- Unit tests: Vitest with Analog's testing utilities and @testing-library/angular.
- Run unit tests with `npm run test` executing `vitest run`.
- Component tests use `render()` from @testing-library/angular with `providers` for injected dependencies.
- API route tests call `defineEventHandler` functions directly with mock H3 events.
- E2E tests: Playwright for user flows across file-based routes.
- Run e2e with `npm run test:e2e` executing `playwright test`.
- All page components must have at least one test verifying they render with route params.
- CI pipeline runs `tsc --noEmit` for type checking, then Vitest, then Playwright sequentially.

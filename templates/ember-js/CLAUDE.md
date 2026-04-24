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

- Ember.js 5.x with Glimmer components (template-only and class-based)
- Ember Data 5.x for API data management and caching
- Embroider optimized build system with Webpack
- TypeScript 5.4+ via ember-cli-typescript
- Ember Concurrency for async task management
- QUnit with Ember's testing infrastructure
- CSS Modules via ember-css-modules
- Ember Modifier for DOM manipulation

## Project Structure

```
app/
  components/
    ui/                    # Generic UI components (button, modal, input)
      button.gts
      modal.gts
    features/              # Feature-specific components
      user-profile.gts
      order-summary.gts
  routes/
    application/
      route.ts             # Application route (root)
      template.hbs
    dashboard/
      route.ts
      template.hbs
      controller.ts
    users/
      user/
        route.ts           # Dynamic segment route
        template.hbs
  models/
    user.ts                # Ember Data model definitions
    post.ts
  adapters/
    application.ts         # JSON:API adapter configuration
  serializers/
    application.ts         # JSON:API serializer configuration
  services/
    session.ts             # Authentication service
    notifications.ts       # Toast notification service
  helpers/                 # Template helpers
  modifiers/               # DOM modifiers
  utils/                   # Pure utility functions
  styles/                  # CSS Modules stylesheets
  router.ts                # Route map definition
tests/
  integration/
    components/            # Component rendering tests
  unit/
    models/                # Model unit tests
    services/              # Service unit tests
  acceptance/              # Full user flow tests
```

## Architecture Rules

- Components are Glimmer components using `.gts` (template tag) format. Template-only components are preferred when no backing class logic is needed.
- Use `<template>` tag syntax in `.gts` files for co-located templates. Only use separate `.hbs` files for route templates.
- Ember Data models define relationships with `@belongsTo` and `@hasMany`. The API must conform to JSON:API specification.
- Routes are responsible for data loading via the `model()` hook. Components receive data as arguments, never fetch directly.
- Services are singleton objects injected with the `@service` decorator. Use services for shared state (auth, notifications, feature flags).
- Async operations in components use `ember-concurrency` tasks with `@task` decorator instead of raw promises or async/await in actions.
- The Embroider build must remain in optimized mode with `staticAddonTrees: true` and `staticComponents: true` enabled.

## Coding Conventions

- Component files use kebab-case: `user-profile.gts`. Invocation in templates uses angle bracket syntax: `<UserProfile />`.
- Arguments passed to components are prefixed with `@`: `<UserProfile @user={{this.user}} />`. Local properties use `this.`.
- Use named blocks for component composition: `<Card><:header>Title</:header><:body>Content</:body></Card>`.
- Template helpers are pure functions registered via `helper()`. Side effects belong in modifiers.
- Modifiers handle DOM lifecycle: `{{did-insert}}`, `{{will-destroy}}`, or custom modifiers created via `modifier()`.
- Tracked properties use `@tracked` decorator. Only mark properties as tracked if they change after initial render.
- Controllers are used sparingly, only for query parameter handling. State management belongs in services or components.

## Library Preferences

- Async tasks: ember-concurrency (never raw setInterval or unmanaged promises)
- Data layer: Ember Data with JSON:API (never hand-roll API caching)
- Modifiers: ember-modifier for custom DOM behavior
- CSS: ember-css-modules for scoped styling
- Animations: ember-animated for route transitions and list animations
- Testing: QUnit with ember-test-helpers (never switch to Jest)
- Auth: ember-simple-auth with OAuth2 bearer token strategy
- Internationalization: ember-intl for translations and formatting

## File Naming

- Components: `kebab-case.gts` (Glimmer template tag)
- Route templates: `template.hbs` in route directories
- Models: `kebab-case.ts` (singular: `user.ts`, not `users.ts`)
- Services: `kebab-case.ts`
- Helpers: `kebab-case.ts`
- Modifiers: `kebab-case.ts`
- Tests: `kebab-case-test.ts` (Ember convention with `-test` suffix)

## NEVER DO THIS

1. Never use classic Ember components (`@ember/component`). Use Glimmer components from `@glimmerx/component` exclusively.
2. Never fetch data inside components. Data loading belongs in route `model()` hooks. Components receive data as `@args`.
3. Never use `{{action}}` helper or `{{mut}}` helper. Use `{{on}}` modifier with `{{fn}}` for event handling.
4. Never use mixins. They are deprecated. Extract shared behavior into services, helpers, or utility functions.
5. Never use observers (`addObserver`, `@observes`). Use `@tracked` properties and getters for derived state.
6. Never bypass Embroider's static analysis by using dynamic component invocation with string-based lookups.
7. Never use jQuery. Ember removed jQuery as a dependency. Use native DOM APIs in modifiers.

## Testing

- Integration tests: render components in isolation with `setupRenderingTest()` and assert DOM output with QUnit assertions.
- Unit tests: test services, models, and utilities with `setupTest()` and direct method invocation.
- Acceptance tests: simulate full user flows with `setupApplicationTest()`, `visit()`, `click()`, and `fillIn()` helpers.
- Run all tests with `ember test` or `ember test --server` for watch mode.
- Mock API responses using Mirage.js with factories and serializers matching the real JSON:API backend.
- Async assertions use `await settled()` to wait for all pending runloop work, promises, and ember-concurrency tasks.
- Test coverage is tracked with ember-cli-code-coverage, targeting 80% minimum.
- CI runs `ember test` in Chrome via `--launch=chrome` and validates the Embroider build succeeds.

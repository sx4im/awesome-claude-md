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

- Alpine.js 3.14 for declarative client-side interactivity
- Tailwind CSS 4 with @tailwindcss/cli
- Server-rendered HTML from any backend (Django, Laravel, Rails, or static)
- HTMX 2 for dynamic server interactions where Alpine alone is insufficient
- Alpine Plugins: @alpinejs/persist, @alpinejs/focus, @alpinejs/collapse, @alpinejs/morph
- Vite 5 for asset bundling (JS, CSS only; HTML comes from the server)
- ESLint with @typescript-eslint for the thin JS layer

## Project Structure

```
assets/
  js/
    app.js              # Alpine.js initialization and global stores
    components/         # Alpine.data() component definitions
      dropdown.js
      modal.js
      tabs.js
      search.js
    plugins/            # Custom Alpine plugins
    directives/         # Custom Alpine directives
  css/
    app.css             # Tailwind CSS entry point
templates/
  layouts/
    base.html           # Base HTML layout with Alpine/Tailwind loaded
  partials/
    _navbar.html        # Reusable HTML partials with Alpine markup
    _modal.html
    _toast.html
  pages/                # Full page templates
public/
  dist/                 # Vite build output (gitignored)
vite.config.js          # Vite config for JS/CSS bundling only
```

## Architecture Rules

- Alpine.js handles UI interactivity only: dropdowns, modals, tabs, form validation, and toggling visibility. Business logic stays on the server.
- Use `x-data` for component-local state. Keep `x-data` objects small (under 10 properties). Extract large components into `Alpine.data()` registrations.
- Use `Alpine.store()` for global state shared across multiple components (theme, toast notifications, auth status).
- Server-rendered HTML is the source of truth. Alpine enhances it with interactivity, it does not replace it.
- Progressive enhancement is mandatory: core content and navigation must work with JavaScript disabled.
- HTMX handles server roundtrips (form submissions, infinite scroll, live search). Alpine handles pure client-side state (tabs, accordions, toggles).
- Never build SPA-like client-side routing. Each page is a full server-rendered HTML document.

## Coding Conventions

- Inline `x-data` is acceptable for simple toggles: `x-data="{ open: false }"`.
- Components with more than 3 properties or any methods must use `Alpine.data('name', () => ({}))` pattern.
- Event communication between components uses `$dispatch` for child-to-parent and `@custom-event.window` for broadcast.
- Use `x-bind:class` with object syntax for conditional classes: `x-bind:class="{ 'active': isActive }"`.
- Use `x-cloak` on elements that should be hidden until Alpine initializes to prevent flash of unstyled content.
- Persist user preferences (theme, sidebar state) with `$persist` from @alpinejs/persist.
- Template expressions in `x-text` and `x-html` must be simple. Extract complex logic to component methods.

## Library Preferences

- Dropdowns/Popovers: @floating-ui/dom for positioning (never hand-roll positioning math)
- Icons: Heroicons via inline SVG in server templates (never icon fonts)
- Transitions: Alpine.js x-transition with Tailwind transition classes
- Form validation: client-side with Alpine, server-side validation is canonical
- Date formatting: Intl.DateTimeFormat (never moment.js or date-fns for display-only formatting)
- HTTP requests: HTMX for HTML fragment responses, native fetch for JSON-only needs
- Charts: Chart.js wrapped in Alpine.data() components

## File Naming

- Alpine components: `camelCase.js` in `assets/js/components/`
- Plugins: `camelCase.js` in `assets/js/plugins/`
- Templates: `snake_case.html` or `_snake_case.html` for partials (follows server framework convention)
- CSS: `kebab-case.css`
- Static assets: `kebab-case.ext` in `public/`

## NEVER DO THIS

1. Never use Alpine.js to build single-page application routing. Alpine is for progressive enhancement, not SPAs.
2. Never store sensitive data (tokens, user PII) in `Alpine.store()` or `$persist`. Keep secrets server-side in HTTP-only cookies.
3. Never use `x-html` with user-generated content. It enables XSS attacks. Use `x-text` for user content.
4. Never nest `x-data` scopes more than two levels deep. Flatten the component hierarchy or use `$dispatch` for communication.
5. Never import large JS libraries (React, Vue, lodash) alongside Alpine. Alpine's value is its small footprint.
6. Never use `x-init` for data fetching. Load data server-side in the HTML or use HTMX to fetch HTML fragments.
7. Never write Alpine expressions longer than one line inline. Extract to `Alpine.data()` methods for readability.

## Testing

- Alpine component logic is tested with Vitest by importing `Alpine.data()` definitions and calling methods directly.
- Run unit tests with `npx vitest run` targeting `assets/js/components/`.
- Integration testing uses Playwright to verify Alpine-enhanced interactions in a real browser.
- Test that all pages degrade gracefully: Playwright tests run with JavaScript disabled to verify core content renders.
- Accessibility testing uses axe-core via @axe-core/playwright on every page template.
- HTML validation runs via html-validate in CI on all server-rendered templates.
- Lighthouse CI checks confirm total JS bundle stays under 50KB gzipped (Alpine + app code).

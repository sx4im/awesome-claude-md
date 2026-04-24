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

- Lit 3.x for web component authoring
- TypeScript (strict mode)
- Shadow DOM for style encapsulation
- CSS custom properties for theming
- Vite 5.x for dev server and building
- Published as [npm package / internal component library]

## Project Structure

```
src/
├── components/
│   ├── my-button.ts           # Each component is one file
│   ├── my-card.ts
│   ├── my-dialog.ts
│   └── my-input.ts
├── styles/
│   ├── tokens.css             # Design tokens as CSS custom properties
│   └── shared.ts              # Shared Lit CSS (css`` tagged templates)
├── controllers/               # Reactive controllers for reusable logic
│   ├── fetch-controller.ts    # Data fetching controller
│   └── resize-controller.ts   # Resize observer controller
├── mixins/                    # Class mixins for shared behavior
│   └── form-associated.ts     # Form participation mixin
├── types/                     # Shared TypeScript interfaces
│   └── events.ts              # Custom event type definitions
├── utils/                     # Pure utility functions
│   └── validators.ts
├── index.ts                   # Barrel export for all components
└── custom-elements.json       # Custom Elements Manifest (generated)

stories/                       # Storybook stories for each component
├── my-button.stories.ts
└── my-card.stories.ts
```

## Architecture Rules

- **One component per file.** A file named `my-button.ts` exports one custom element class and calls `customElements.define('my-button', MyButton)` as a side effect. The tag name and filename must match.
- **Shadow DOM always.** Every component uses shadow DOM for style encapsulation. Never use `createRenderRoot() { return this; }` to disable shadow DOM. If you need external styling, expose CSS custom properties and `::part()`.
- **Reactive properties drive rendering.** Use `@property()` for public API (attributes + properties) and `@state()` for private internal state. When properties change, Lit batches and schedules a re-render automatically.
- **Composition over inheritance.** Share logic through reactive controllers, not deep class hierarchies. A `FetchController` is better than a `FetchableElement` base class. Inheritance beyond `LitElement` should be at most one level deep.
- **Events for child-to-parent communication.** Children dispatch custom events with `this.dispatchEvent(new CustomEvent('my-change', { detail, bubbles: true, composed: true }))`. Parents listen with `@my-change`. Never reach into a child's shadow DOM.

## Coding Conventions

- Component classes extend `LitElement`. Class name is PascalCase, tag name is `kebab-case` with a project prefix: `{prefix}-button`, `{prefix}-card`. Always register with `@customElement('prefix-name')` decorator.
- Properties: `@property({ type: String })` for public attributes. Use `reflect: true` only when the attribute value needs to be visible in the DOM for CSS selectors or accessibility. Reflecting objects or arrays is a performance mistake.
- Internal state: `@state()` for private reactive state that should not be exposed as an attribute. Name with a leading underscore convention: `@state() private _isOpen = false`.
- Render method returns `html` tagged template: `render() { return html\`<div>${this.name}</div>\`; }`. Never use `document.createElement` or `innerHTML` inside `render()`.
- Styles use `static styles = css\`...\``. Styles are adopted once per class, not per instance. Never use inline `<style>` tags in the template. Never import external CSS files into shadow DOM without the `css` tag.
- Events: always set `bubbles: true` and `composed: true` on custom events so they cross shadow DOM boundaries. Type events with a detail interface: `CustomEvent<{ value: string }>`.

## Library Preferences

- **Rendering:** Lit's `html` and `css` tagged template literals. Not JSX (Lit does not use a virtual DOM; tagged templates compile to efficient DOM operations). Not `htm` (adds unnecessary abstraction).
- **State across components:** Reactive controllers or Lit's `@lit/context` for dependency injection across the tree. Not Redux, not MobX. Web components communicate via properties down, events up.
- **Form integration:** `ElementInternals` API with `static formAssociated = true`. This lets custom elements participate in native `<form>` elements. Not wrapping hidden `<input>` elements inside shadow DOM.
- **Theming:** CSS custom properties defined in `tokens.css` and consumed inside shadow DOM. Not CSS-in-JS. Not global class-based themes. Custom properties penetrate shadow DOM boundaries by design.
- **Documentation:** Custom Elements Manifest (`custom-elements.json`) generated by `@custom-elements-manifest/analyzer`. It feeds Storybook, VS Code autocomplete, and documentation sites.
- **Dev/docs:** Storybook with `@storybook/web-components-vite`. Each component has a story showing all variants and states.

## File Naming

- Components: `kebab-case.ts` → `my-button.ts`, `my-card.ts` (matches tag name without prefix)
- Controllers: `kebab-case.ts` → `fetch-controller.ts`, `resize-controller.ts`
- Mixins: `kebab-case.ts` → `form-associated.ts`, `draggable.ts`
- Styles: `kebab-case.ts` or `.css` → `tokens.css`, `shared.ts`
- Stories: `kebab-case.stories.ts` → `my-button.stories.ts`
- Types: `kebab-case.ts` → `events.ts`, `theme.ts`
- Test files: co-located as `my-button.test.ts`

## NEVER DO THIS

1. **Never disable shadow DOM.** Overriding `createRenderRoot()` to return `this` breaks encapsulation and makes your components fragile to global CSS. If you need external styling, expose `::part()` attributes or CSS custom properties.
2. **Never reflect complex types as attributes.** `@property({ reflect: true, type: Object })` serializes your object to `[object Object]` in the DOM attribute. Only reflect primitives: strings, numbers, booleans. Complex data goes through properties only.
3. **Never use `querySelector` to reach into another component's shadow DOM.** `document.querySelector('my-card').shadowRoot.querySelector('.title')` is brittle and violates encapsulation. Use the component's public property API or listen for its events.
4. **Never use `innerHTML` in render.** Lit's `html` tagged templates handle efficient DOM updates. Using `innerHTML` bypasses Lit's diffing, causes XSS vulnerabilities, and destroys event listeners on every render.
5. **Never define styles in `render()`.** Styles must be in `static styles = css\`...\``. Defining styles in render creates a new stylesheet per render cycle, causes FOUC, and defeats adopted stylesheet caching.
6. **Never forget `composed: true` on custom events.** Without `composed: true`, events stop at the shadow DOM boundary. Parent components listening with `@my-event` will never receive them. Always: `new CustomEvent('name', { bubbles: true, composed: true, detail })`.
7. **Never use global IDs in shadow DOM templates.** `<div id="content">` inside shadow DOM does not conflict with outer DOM IDs, but using `document.getElementById('content')` won't find it. Use `this.renderRoot.querySelector('#content')` or template refs with `@query('#content')`.

## Testing

- Use `@open-wc/testing` with Vitest or Web Test Runner. It provides `fixture(html\`<my-button></my-button>\`)` for rendering components in tests.
- Test the public API: set properties, trigger events, assert on shadow DOM output. Never test internal state directly.
- Use `await el.updateComplete` after changing properties. Lit renders asynchronously. Asserting immediately after setting a property reads stale DOM.
- Accessibility: use `@open-wc/testing`'s `expect(el).to.be.accessible()` assertion. It runs axe-core against the component's shadow DOM.
- Visual regression: use Storybook + Chromatic or Percy. Each story is a visual test case. Component variants must have stories before they are considered complete.

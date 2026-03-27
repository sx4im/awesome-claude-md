# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Native Web Components with Custom Elements v1 API
- Shadow DOM for style encapsulation
- Lit-inspired patterns (reactive properties, declarative templates) without the Lit dependency
- TypeScript 5.4+ compiled to ES2022 modules
- Vite 5 for development server and production builds
- CSS custom properties (design tokens) for theming
- Web Test Runner with @open-wc/testing for component testing
- Custom Elements Manifest (CEM) for documentation and IDE support

## Project Structure

```
src/
  components/
    core/
      base-element.ts       # Base class with reactive property system
      styles.ts             # Shared style utilities and CSS helpers
    ui/
      app-button.ts         # Button component with variants
      app-input.ts          # Form input component
      app-modal.ts          # Modal dialog component
      app-card.ts           # Card container component
      app-tabs.ts           # Tab navigation component
    layout/
      app-header.ts         # Application header
      app-sidebar.ts        # Sidebar navigation
      app-layout.ts         # Page layout grid
    data/
      data-table.ts         # Data table with sorting/pagination
      data-list.ts          # Virtual scrolling list
  controllers/
    form-controller.ts      # Reusable form validation controller
    media-query-controller.ts
  directives/
    click-outside.ts        # Custom template directive
  mixins/
    focusable.ts            # Keyboard navigation mixin
    slottable.ts            # Slot change observation mixin
  styles/
    tokens.css              # Design token CSS custom properties
    reset.css               # Shadow DOM reset styles
    typography.css          # Typography system
  utils/
    dom.ts                  # DOM utility functions
    events.ts               # Custom event factory helpers
  index.ts                  # Public API barrel export
  define.ts                 # Custom element registration
custom-elements.json        # Custom Elements Manifest
```

## Architecture Rules

- All components extend `BaseElement` which provides a reactive property system, `render()` lifecycle, and `update()` batching using `requestAnimationFrame`.
- Shadow DOM is mandatory for all visual components. Use `this.attachShadow({ mode: 'open' })` in the constructor.
- Component styles are defined as `CSSStyleSheet` objects using `adoptedStyleSheets` for efficient style sharing across instances.
- Properties declared with the `@property` decorator (from BaseElement) trigger re-renders when changed. Attributes are reflected only for primitive types.
- Inter-component communication uses custom DOM events with `CustomEvent` and `detail` payload. Events bubble by default and are composed to cross shadow boundaries.
- Component registration is separated from definition. Components are defined as classes in their own files and registered in `define.ts` using `customElements.define()`.
- Slotted content uses named slots for composition: `<slot name="header">`, `<slot name="actions">`. Default slot for primary content.

## Coding Conventions

- Component class names use PascalCase: `AppButton`, `DataTable`. Custom element tags use `app-` prefix: `app-button`, `data-table`.
- The `render()` method returns an HTML string built with tagged template literals. Use a `html` tag function for syntax highlighting support.
- Lifecycle callbacks follow the spec: `connectedCallback`, `disconnectedCallback`, `attributeChangedCallback`, `adoptedCallback`.
- Private methods and properties use the `#` private class field syntax, not TypeScript `private` keyword.
- Event names use kebab-case with component prefix: `app-button-click`, `data-table-sort-change`.
- CSS custom properties for theming use the `--app-` namespace: `--app-color-primary`, `--app-spacing-md`, `--app-radius-sm`.
- Form-associated custom elements implement `static formAssociated = true` and use `ElementInternals` for form participation.

## Library Preferences

- Template rendering: tagged template literals with a lightweight `html` helper (never innerHTML with string concatenation)
- Reactive system: custom `@property` decorator with `MutationObserver` for attribute sync (not Lit's full reactive controller)
- Testing: @open-wc/testing with Web Test Runner (never Jest or jsdom for Web Component testing)
- Build: Vite with @custom-elements-manifest/analyzer for CEM generation
- Polyfills: none required, targeting evergreen browsers only (Chrome, Firefox, Safari, Edge)
- Documentation: custom-elements.json manifest consumed by Storybook Web Components or API doc generators
- Animation: Web Animations API (never GreenSock or anime.js)

## File Naming

- Components: `kebab-case.ts` matching the custom element tag (e.g., `app-button.ts` defines `<app-button>`)
- Controllers: `kebab-case-controller.ts`
- Mixins: `kebab-case.ts` in `mixins/`
- Styles: `kebab-case.css`
- Tests: `kebab-case.test.ts` co-located with component files
- Utilities: `camelCase.ts`

## NEVER DO THIS

1. Never use `innerHTML` for rendering templates. Use tagged template literals with proper escaping to prevent XSS vulnerabilities.
2. Never use `document.querySelector` to reach into another component's shadow DOM. Communicate via events and public properties.
3. Never create components without shadow DOM encapsulation. Light DOM components leak styles and break in composition.
4. Never use global CSS classes inside shadow DOM. Use CSS custom properties for theming and `::part()` for targeted external styling.
5. Never register custom elements at import time. Separate definition from registration so consumers control when elements are defined.
6. Never use synchronous `attributeChangedCallback` for expensive operations. Batch updates with microtask scheduling.
7. Never use framework-specific state management (Redux, MobX). Use component properties, events, and a lightweight reactive controller pattern.

## Testing

- Component tests use Web Test Runner with @open-wc/testing: `fixture(html`<app-button></app-button>`)`.
- Run tests with `npx web-test-runner --node-resolve` or `npm test`.
- Assertions use `@open-wc/testing` expect with custom matchers for shadow DOM queries: `el.shadowRoot.querySelector()`.
- Test user interactions with `@open-wc/testing`'s `oneEvent` helper to await custom events after simulated clicks.
- Accessibility tests use `@open-wc/testing`'s `isAccessible` assertion which runs axe-core on shadow DOM.
- Visual regression tests use Playwright with `page.evaluate()` to insert components and screenshot.
- The Custom Elements Manifest is validated in CI with `custom-elements-manifest-analyzer` ensuring all public APIs are documented.
- Cross-browser testing runs in Web Test Runner with Playwright launcher targeting Chrome, Firefox, and WebKit.

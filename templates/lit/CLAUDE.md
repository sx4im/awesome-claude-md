# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Lit v3 (Web Components library)
- TypeScript 5.x
- Web Components standards
- Reactive properties
- Scoped styles

## Project Structure
```
src/
├── components/
│   ├── my-button.ts            // Lit component
│   └── my-card.ts
├── styles/
│   └── shared-styles.ts        // CSS literals
└── index.ts                    // Component exports
```

## Architecture Rules

- **Standards-based.** Uses Web Components APIs directly.
- **Reactive properties.** `@property` decorated fields trigger re-renders.
- **Scoped styles.** CSS applies only to component shadow DOM.
- **Composable.** Components work in any framework or vanilla HTML.

## Coding Conventions

- Component: `@customElement('my-button') class MyButton extends LitElement { @property() label = 'Click'; render() { return html`<button>${this.label}</button>` } }`.
- Styles: `static styles = css` :host { display: block; } button { color: blue; } `;`.
- Property options: `@property({ type: String, reflect: true })`.
- Events: `this.dispatchEvent(new CustomEvent('my-click', { detail: data }))`.

## NEVER DO THIS

1. **Never mutate `this` in render.** Use reactive properties.
2. **Never skip the `static styles`.** Use for scoped CSS.
3. **Never forget to call `super` in lifecycle.** Required for proper behavior.
4. **Never use without understanding Shadow DOM.** Encapsulation implications.
5. **Never mix LitElement with reactive controllers blindly.** Understand patterns.
6. **Never ignore the `firstUpdated` callback.** For DOM measurements.
7. **Never forget to define the custom element.** `@customElement` or `customElements.define`.

## Testing

- Test with `@open-wc/testing`.
- Test in different browsers (Shadow DOM support).
- Test with and without Shadow DOM (light DOM mode).


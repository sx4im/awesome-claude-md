# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Goober (tiny CSS-in-JS)
- < 1KB runtime
- React/Preact/Vue/Svelte
- Critical CSS extraction
- Babel plugin for extraction

## Project Structure
```
src/
├── components/
│   └── Button.tsx              // Uses goober
├── styles/
│   └── global.ts               // Global styles
└── goober.config.js
```

## Architecture Rules

- **Smallest CSS-in-JS.** Under 1KB vs 10KB+ for alternatives.
- **CSS tagged template.** `` css`...` `` generates class names.
- **Styled components.** `styled('div')`...`` or `styled.div`...``.
- **Critical CSS.** `extractCss()` for SSR.

## Coding Conventions

- Setup: `import { css, styled } from 'goober'; setPragma(h);`.
- CSS: `const className = css`color: red; font-size: 16px;`;`.
- Styled: `const Button = styled('button')`background: blue; color: white;`;`.
- Dynamic: `const dynamic = css`color: ${props => props.color};`;` (runtime).
- Global: `css`@import url(...);`;` or `glob`body { margin: 0; }``.

## NEVER DO THIS

1. **Never forget `setPragma`.** Required for JSX integration.
2. **Never use without Babel plugin in production.** Critical CSS extraction.
3. **Never do heavy computations in template literals.** Runtime overhead.
4. **Never ignore the `target` option.** Set to `document.head` for shadow DOM.
5. **Never mix with other CSS-in-JS.** Pick one solution.
6. **Never forget keyframes.** `keyframes`...`` for animations.
7. **Never skip `extractCss()` in SSR.** Prevents flash of unstyled content.

## Testing

- Test bundle size is minimal.
- Test critical CSS extraction works.
- Test dynamic styles update correctly.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Astroturf (build-time CSS-in-JS)
- Webpack loader
- CSS modules under hood
- React/Vue
- Zero runtime overhead

## Project Structure
```
src/
├── components/
│   └── Button.tsx              // Uses astroturf
├── styles/
│   └── global.css              // Regular CSS imports
└── webpack.config.js
```

## Architecture Rules

- **CSS in tagged templates.** Extracted at build to CSS files.
- **CSS modules benefits.** Scoped, composable, extractable.
- **Webpack loader required.** Processes `css` tagged templates.
- **TypeScript support.** Generates `.d.ts` for CSS imports.

## Coding Conventions

- Import: `import { css } from 'astroturf'`.
- Component styles: `const styles = css` .button { color: red; } `;` generates `styles.button` class.
- Styled: `const Button = styled('button')` color: red; `;`.
- Composition: `const blueButton = css` composes: ${styles.button} from './button.css'; color: blue;`;`.

## NEVER DO THIS

1. **Never use without Webpack loader.** Essential for extraction.
2. **Never do dynamic interpolation.** Build-time only—no runtime vars.
3. **Never forget the `css` import.** Different from other CSS-in-JS.
4. **Never mix with other loaders carelessly.** Configure test regex properly.
5. **Never ignore the `loader` options.** Set `extension: '.module.css'`.
6. **Never use for highly dynamic styles.** CSS variables for those.
7. **Never skip source maps.** Enable for debugging.

## Testing

- Test CSS extracts to separate files.
- Test class names are scoped.
- Test composition works across files.


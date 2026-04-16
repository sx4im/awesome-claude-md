# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Linaria (zero-runtime CSS-in-JS)
- Build-time CSS extraction
- CSS modules features
- React/Preact/Any framework
- Babel/Vite/Webpack

## Project Structure
```
src/
├── components/
│   └── Button.tsx              // Uses linaria
├── styles/
│   └── tokens.ts               // Design tokens
├── .linariarc.json
└── vite.config.ts
```

## Architecture Rules

- **Zero runtime.** CSS extracted at build, no JS overhead.
- **Atomic CSS optional.** Can generate atomic classes.
- **Dynamic with CSS vars.** Props via CSS custom properties.
- **Source maps.** Original file locations preserved.

## Coding Conventions

- Import: `import { css } from '@linaria/core'; import { styled } from '@linaria/react';`.
- CSS: `const className = css`color: red;`;`.
- Styled: `const Button = styled.button`background: blue;`;`.
- Dynamic: Use CSS variables: `const Box = styled.div`background: var(--color);`;` then `<Box style={{ '--color': color }} />`.
- Atomic: `@linaria/atomic` for atomic CSS output.

## NEVER DO THIS

1. **Never use dynamic values in templates.** Runtime interpolation doesn't work.
2. **Never forget the extraction setup.** Configure build tool properly.
3. **Never ignore the `.linariarc` config.** Cache and other settings.
4. **Never use with complex logic in styles.** Evaluate before styled call.
5. **Never forget `cx` from `@linaria/core`.** For conditional classes.
6. **Never skip stylelint.** `@linaria/stylelint` for linting.
7. **Never use for highly dynamic values.** Runtime CSS-in-JS better for that.

## Testing

- Test CSS extracts to separate files.
- Test source maps point to correct locations.
- Test CSS variables update dynamically.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Emotion (CSS-in-JS library)
- React 18+
- @emotion/react and @emotion/styled
- Babel plugin for optimization
- Server-side rendering support

## Project Structure
```
src/
├── components/
│   └── Button.tsx              // Uses emotion
├── styles/
│   └── theme.ts                // Emotion theme
├── emotion.d.ts                // TypeScript declarations
└── App.tsx
```

## Architecture Rules

- **CSS prop for inline.** `<div css={{ color: 'red' }} />`.
- **Styled API for components.** `const Button = styled.button`...``.
- **Theme provider for tokens.** `<ThemeProvider theme={theme}>`.
- **Server extractCritical.** For SSR CSS extraction.

## Coding Conventions

- CSS prop: `<div css={css`color: red;`} />` or `<div css={{ color: 'red', '&:hover': { color: 'blue' } }} />`.
- Styled: `const Button = styled.button`background: ${props => props.theme.primary};`.
- Keyframes: `const fadeIn = keyframes`from { opacity: 0; }`;` then `animation: ${fadeIn} 1s;`.
- Global: `GlobalStyles` component with `css`@import ...``.

## NEVER DO THIS

1. **Never use without @emotion/babel-plugin.** Required for optimization.
2. **Never forget the css prop types.** `/// <reference types="@emotion/react/types/css-prop" />`.
3. **Never use dynamic values without memoization.** Prevents unnecessary recalculation.
4. **Never ignore the cache.** Emotion caches styles—understand invalidation.
5. **Never mix css prop with styled blindly.** Pick consistent approach.
6. **Never skip SSR extraction.** Use `extractCritical` for server rendering.
7. **Never use without understanding the label option.** Helps debugging with source maps.

## Testing

- Test styles apply correctly.
- Test theme values resolve properly.
- Test SSR extraction works.


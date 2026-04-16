# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Stitches (CSS-in-JS near-zero runtime)
- React/Next.js
- Variant-based API
- Token system
- Server-side rendering

## Project Structure
```
src/
├── stitches/
│   └── config.ts               // Stitches configuration
├── components/
│   └── Button.tsx              // Uses stitches
└── App.tsx
```

## Architecture Rules

- **Config-first.** Define tokens, breakpoints, utils in config.
- **Styled function.** `styled('element', { css: {}, variants: {} })`.
- **Variant props.** Type-safe component variants.
- **CSS function.** `css()` for one-off styles.

## Coding Conventions

- Config: `export const { styled, css } = createStitches({ theme: { colors: { primary: 'blue' }, space: { 1: '4px' } }, media: { sm: '(min-width: 640px)' } })`.
- Styled: `const Button = styled('button', { backgroundColor: '$primary', variants: { color: { primary: { backgroundColor: '$primary' } } } })`.
- Use: `<Button color="primary" css={{ padding: '$2' }}>Click</Button>`.
- CSS util: `const box = css({ padding: '$2', color: '$primary' }); <div className={box()} />`.

## NEVER DO THIS

1. **Never forget the `$` prefix.** `$primary` refers to theme tokens.
2. **Never use outside config scope.** Always use exported `styled`, `css`.
3. **Never ignore responsive variants.** `variants: { size: { sm: { '@sm': { ... } } } }`.
4. **Never skip the `createStitches` call.** Must create instance first.
5. **Never use runtime values in CSS template.** Use CSS vars for dynamic values.
6. **Never forget to handle the `as` prop.** For polymorphic components.
7. **Never mix Stitches with other CSS-in-JS.** Pick one solution.

## Testing

- Test variant props apply correctly.
- Test responsive styles at breakpoints.
- Test tokens resolve from theme.


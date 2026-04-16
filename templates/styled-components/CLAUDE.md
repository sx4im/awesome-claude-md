# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- styled-components v6 (CSS-in-JS)
- React 18+
- TypeScript 5.x
- Next.js 15+ (with configuration) or Vite
- Babel or SWC plugin for optimization

## Project Structure

```
src/
├── components/
│   ├── Button/
│   │   ├── index.tsx           # Component logic
│   │   └── styles.ts             # Styled definitions
│   ├── shared/                   # Shared styled components
│   │   ├── Layout.ts
│   │   └── Typography.ts
│   └── ...
├── styles/
│   ├── theme.ts                  # Theme object definition
│   ├── globalStyles.ts           # Global styles (createGlobalStyle)
│   └── mixins.ts                 # Reusable style functions
├── providers/
│   └── theme-provider.tsx      # ThemeProvider setup
└── lib/
    └── utils.ts
```

## Architecture Rules

- **ThemeProvider for theming.** Wrap your app in `ThemeProvider` with a theme object. Access via props or `useTheme` hook.
- **Define components with `styled`.** Use `styled.div`, `styled.button`, etc., for component-scoped styles.
- **Dynamic styles via props.** Pass props to styled components for conditional styling: `styled.div<{ $isActive: boolean }>`.
- **Global styles with `createGlobalStyle`.** CSS resets, font imports, and base styles go here.

## Coding Conventions

- Use transient props (prefix with `$`) for styling props that shouldn't reach the DOM: `$isActive`, `$variant`.
- Define styled components outside render functions. Inside render causes re-creation on every render.
- Type styled components: `styled.div<Props>` not `styled.div`.
- Use theme values via interpolation: `${props => props.theme.colors.primary}`.
- Create style utilities for repeated patterns (flex center, truncate text).

## Library Preferences

- **Theming:** ThemeProvider with custom theme object.
- **Animation:** `styled.keyframes` for animations. Framer Motion for complex transitions.
- **Icons:** Import as React components, style with styled-components wrapper.
- **CSS props:** Use the `css` prop from `@styled-system/css` for one-off overrides.

## File Naming

- Styled definitions: `styles.ts` or `[Component].styles.ts`
- Theme config: `theme.ts`
- Global styles: `globalStyles.ts`

## NEVER DO THIS

1. **Never use regular props for styling without `$` prefix.** `isActive` becomes a DOM attribute. Use `$isActive` (transient prop).
2. **Never define styled components inside components.** This creates new component types on every render, destroying React's optimization.
3. **Never forget the Next.js configuration.** styled-components requires the SWC plugin or Babel plugin for SSR. Without it, styles flash on load.
4. **Never use `!important` in styled-components.** Fix specificity with the `&&` selector pattern instead.
5. **Never mix `styled-components` with CSS Modules in the same component.** Pick one approach.
6. **Never ignore the flash of unstyled content (FOUC).** Ensure SSR is configured correctly for styled-components.
7. **Never use complex logic in template literals.** Extract to helper functions: `background: ${props => getColor(props)};`.

## Testing

- Use `jest-styled-components` for snapshot testing of CSS.
- Test theme switching by updating ThemeProvider value.
- Visual regression tests with Chromatic.
- SSR tests to verify styles are extracted correctly.


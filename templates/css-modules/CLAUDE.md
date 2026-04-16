# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- CSS Modules (scoped CSS)
- React 18+
- TypeScript 5.x
- Next.js 15+ or Vite
- PostCSS (optional)

## Project Structure

```
src/
├── components/
│   ├── Button/
│   │   ├── index.tsx           # Component
│   │   └── styles.module.css   # Scoped styles
│   ├── Card/
│   │   ├── index.tsx
│   │   └── styles.module.css
│   └── ...
├── styles/
│   ├── global.css              # Global styles, resets
│   ├── variables.css           # CSS custom properties
│   └── mixins.css              # Shared CSS patterns
└── lib/
    └── utils.ts
```

## Architecture Rules

- **One CSS Module per component.** Each component has its own `.module.css` file. Styles are scoped automatically.
- **Global styles for resets and variables.** `global.css` for CSS resets, CSS variables, and truly global styles.
- **Composition over duplication.** Use CSS custom properties for theming values. Reference them in modules.
- **Co-locate styles with components.** Keep `.module.css` files in the same directory as their component.

## Coding Conventions

- Import styles: `import styles from './styles.module.css'`.
- Apply classes: `className={styles.button}` or `className={styles['button-primary']}` for kebab-case.
- Use `clsx` or `cn()` for conditional classes: `className={clsx(styles.button, isActive && styles.active)}`.
- Define CSS variables in `:root` for global theming.
- Use camelCase for class names in modules: `.buttonPrimary` → `styles.buttonPrimary`.

## Library Preferences
- **Class merging:** `clsx` or `classnames` for conditional logic. Combine with your utility if needed.
- **CSS variables:** Native CSS custom properties for theming. No preprocessor required.
- **PostCSS plugins:** Autoprefixer, nesting support if needed.
- **No CSS-in-JS runtime.** CSS Modules compile at build time. No runtime overhead.

## File Naming
- Component directory: PascalCase → `Button/`, `Card/`
- CSS Module: `styles.module.css` or `[Component].module.css`
- Component file: `index.tsx` or `[Component].tsx`

## NEVER DO THIS

1. **Never use global selectors in CSS Modules.** `.button` in a module becomes `.Button_button__hash`. Don't target global elements like `body` or `h1`.
2. **Never forget to import the styles.** Without `import styles`, classes are just strings.
3. **Never use kebab-case class names without bracket notation.** `styles.button-primary` is invalid JS. Use `styles['button-primary']` or camelCase `.buttonPrimary`.
4. **Never duplicate global CSS in modules.** Variables belong in global CSS, not repeated in each module.
5. **Never nest selectors deeply.** CSS Modules scope automatically. Deep nesting makes debugging hard.
6. **Never use `compose` for unrelated styles.** CSS Modules `composes` is for shared styles, not arbitrary grouping.
7. **Never mix CSS Modules with styled-components in the same component.** Pick one approach per codebase.

## Testing

- Visual regression tests. CSS Modules compile to unique class names—verify output.
- Test that styles are correctly scoped (changes in one module don't affect others).
- Use Jest with `identity-obj-proxy` for CSS Module imports in unit tests.


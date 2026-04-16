# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- DaisyUI v4 (Tailwind CSS plugin)
- Tailwind CSS 3.x
- React 18+ or any framework
- TypeScript 5.x
- PostCSS

## Project Structure

```
src/
├── components/
│   └── *.tsx                   # Components using DaisyUI classes
├── app/
│   └── globals.css             # Tailwind + DaisyUI imports
├── lib/
│   └── utils.ts                # cn() helper
├── tailwind.config.ts          # DaisyUI plugin configuration
└── themes.ts                   # Custom theme definitions
```

## Architecture Rules

- **DaisyUI provides semantic class names.** Use `btn`, `card`, `modal` instead of composing Tailwind utilities for common components.
- **Theme with CSS variables.** DaisyUI uses CSS variables for theming. Configure in `tailwind.config.ts` or create custom themes.
- **Utility classes for layout, DaisyUI for components.** Use Tailwind for spacing, flexbox, grid. Use DaisyUI for buttons, inputs, cards.
- **Responsive modifiers work together.** DaisyUI components accept Tailwind responsive prefixes: `md:btn-lg`.

## Coding Conventions

- Install DaisyUI as a Tailwind plugin in `tailwind.config.ts`.
- Import themes in CSS: `@import "daisyui/dist/full.css"` or configure in Tailwind config.
- Use semantic class names: `btn btn-primary`, `card bg-base-100`, `input input-bordered`.
- Combine with Tailwind utilities: `card w-96 bg-base-100 shadow-xl`.

## Library Preferences

- **Icons:** Lucide React or Heroicons. DaisyUI doesn't include icons.
- **Animations:** Tailwind `animate-*` classes or `transition` utilities.
- **Forms:** Use DaisyUI form classes (`input`, `select`, `textarea`) with React Hook Form.
- **Themes:** Configure multiple themes in `tailwind.config.ts` for light/dark mode.

## File Naming

- Components: PascalCase → `Button.tsx`, `Card.tsx`
- Theme config: `themes.ts` or in `tailwind.config.ts`
- Utility: `utils.ts` or `cn.ts`

## NEVER DO THIS

1. **Never forget to add DaisyUI to Tailwind plugins.** Without the plugin, `btn`, `card` classes don't exist.
2. **Never override DaisyUI core variables blindly.** Customizing `--btn-padding` affects all buttons. Use modifier classes instead.
3. **Never mix DaisyUI with another component library.** Conflicting CSS variable names and class names create chaos.
4. **Never forget `data-theme` attribute.** DaisyUI themes require `<html data-theme="light">` or configured default.
5. **Never use `!important` with DaisyUI classes.** It breaks the CSS variable cascade.
6. **Never create custom component styles when DaisyUI provides them.** Check the full component list before building custom.
7. **Never ignore the `neutral` color role.** DaisyUI semantic colors (primary, secondary, accent, neutral) all serve purposes.

## Testing

- Visual regression tests. DaisyUI compiles to CSS—verify the output looks correct.
- Test theme switching by toggling `data-theme` attribute.
- Test responsive behavior with Tailwind breakpoints.


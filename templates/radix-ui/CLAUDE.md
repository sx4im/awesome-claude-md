# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Radix UI primitives (unstyled, accessible components)
- React 18+
- TypeScript 5.x
- Tailwind CSS or CSS Modules for styling
- React 18+ (concurrent features supported)

## Project Structure

```
src/
├── components/
│   ├── primitives/             # Styled wrappers around Radix
│   │   ├── Button.tsx
│   │   ├── Dialog.tsx
│   │   ├── DropdownMenu.tsx
│   │   └── ...
│   └── features/               # Domain-specific composed components
├── lib/
│   └── utils.ts                # cn() for class merging
└── styles/
    └── components.css          # Component-specific styles
```

## Architecture Rules

- **Radix provides behavior, you provide styles.** Radix handles accessibility, keyboard navigation, focus management, and ARIA. You add the visual layer.
- **Wrap Radix primitives in your own components.** Never use Radix components directly in feature code. Always create a styled wrapper that enforces your design system.
- **Expose Radix props through your wrapper.** Use `ComponentPropsWithoutRef` to forward Radix props while adding your own styling props.
- **Composition is key.** Radix components are designed to be composed. Use `asChild` to merge behaviors.

## Coding Conventions

- Import Radix primitives: `import * as Dialog from '@radix-ui/react-dialog'`
- Create compound component patterns matching Radix's API design.
- Use `forwardRef` for all component wrappers to maintain ref forwarding.
- Define explicit prop types that extend from Radix's prop types.
- Use CSS variables for theming within your styled wrappers.

## Library Preferences

- **Primitives:** Use Radix for DropdownMenu, Dialog, Popover, Tooltip, Select, Tabs, Accordion, etc.
- **Styling:** Tailwind CSS is most common, but any CSS-in-JS works. Radix is unstyled by design.
- **Icons:** Lucide React pairs well with Radix.
- **Animation:** Framer Motion for enter/exit animations. Radix provides `data-state` attributes for styling states.

## File Naming

- Primitive wrappers: PascalCase → `Dialog.tsx`, `DropdownMenu.tsx`
- Match the Radix component name for clarity.

## NEVER DO THIS

1. **Never use Radix primitives directly in pages/features.** Always go through your styled wrapper components. Direct usage bypasses your design system.
2. **Never ignore `data-state` attributes.** Radix components set `data-state="open"` or `data-state="closed"`. Use these for CSS transitions, not JavaScript state tracking.
3. **Never forget to style all states.** Radix handles the states, but if you don't style `data-state="checked"`, your Checkbox looks broken.
4. **Never skip the `asChild` prop when composing.** If you wrap a Radix trigger around a custom button without `asChild`, you get nested button elements (invalid HTML).
5. **Never override Radix's accessibility behavior.** Don't add your own `role` or `aria-*` attributes. Radix handles this correctly.
6. **Never use Radix without understanding the anatomy.** Each component has specific sub-components (Trigger, Content, Portal, etc.). Using them incorrectly breaks functionality.
7. **Never forget to install the right package.** Radix primitives are separate packages: `@radix-ui/react-dialog`, not a monolithic `@radix-ui/react`.

## Testing

- Test with keyboard navigation. Radix components are designed for keyboard use—test Tab, Enter, Escape, Arrow keys.
- Test with screen readers. Radix provides correct ARIA, verify your styles don't hide content from assistive tech.
- Use Testing Library's `userEvent` for realistic interaction testing.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- React Aria Components (unstyled, accessible primitives)
- React Stately (state management hooks)
- React 18+
- TypeScript 5.x
- Tailwind CSS or CSS Modules for styling

## Project Structure

```
src/
├── components/
│   ├── primitives/             # Styled wrappers around React Aria
│   │   ├── Button.tsx
│   │   ├── ListBox.tsx
│   │   ├── Select.tsx
│   │   └── ...
│   └── features/               # Domain-specific composed components
├── hooks/
│   └── useCustomState.ts       # Custom state hooks using React Stately
├── lib/
│   └── utils.ts                # cn() helper
└── styles/
    └── components.css          # Component-specific styles
```

## Architecture Rules

- **React Aria provides accessibility, you provide design.** It handles keyboard navigation, focus management, screen reader support, and mobile interactions.
- **Wrap primitives in your design system.** Never use `Button`, `Dialog`, `Select` from React Aria directly in feature code. Create styled wrappers.
- **Use React Stately for state.** Complex state (collections, selection, overlays) uses hooks from `@react-stately/*`.
- **Follow the collection pattern.** List components (Select, ComboBox, ListBox) use the `Item` and `Section` component patterns.

## Coding Conventions

- Import from `react-aria-components` (single package in v1.0+).
- Use render props for customization: `<Button>{(props) => <span>{props.children}</span>}</Button>`.
- Handle slots with `Slot` component for composing behaviors.
- Define explicit types extending from React Aria's prop types.

## Library Preferences

- **Icons:** Lucide React. React Aria is unstyled, so icons integrate seamlessly.
- **Animation:** CSS transitions or Framer Motion. React Aria provides `data-*` attributes for state-based styling.
- **Forms:** React Aria form components with your validation library.
- **Overlay:** Use `Popover`, `Modal`, `Tooltip` from React Aria Components.

## File Naming

- Primitive wrappers: PascalCase → `Button.tsx`, `Select.tsx`
- Match React Aria component names for clarity.

## NEVER DO THIS

1. **Never use React Aria components without styling.** They are completely unstyled. Unstyled buttons are invisible.
2. **Never ignore the render props pattern.** React Aria uses render props for full control. Don't skip them unless you understand the implications.
3. **Never forget to handle focus states.** React Aria manages focus, but you must style `data-focus` attributes.
4. **Never mix React Aria hooks with component APIs.** `useButton` is for headless implementations. Use `Button` component in most cases.
5. **Never skip the `id` prop on form components.** React Aria uses `id` for label association. Let it auto-generate or provide explicit ones.
6. **Never ignore virtual focus.** React Aria uses virtual focus for accessibility. Don't fight it with manual `tabIndex`.
7. **Never use `onClick` for selection.** React Aria uses `onSelectionChange` for collection components. `onClick` bypasses keyboard selection.

## Testing

- Test with keyboard navigation (Tab, Enter, Space, Arrow keys, Escape).
- Test with screen readers (NVDA, VoiceOver, JAWS).
- Use React Testing Library with `userEvent`. It simulates realistic interactions.
- Test mobile touch interactions with Playwright.


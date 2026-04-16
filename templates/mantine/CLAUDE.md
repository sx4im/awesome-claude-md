# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Mantine v7 (modern React components library)
- React 18+
- TypeScript 5.x
- PostCSS (required for Mantine styles)
- Next.js 15+ or Vite

## Project Structure

```
app/
├── layout.tsx                  # MantineProvider wrapper
├── globals.css                 # Tailwind or CSS imports
└── page.tsx
components/
├── ui/                         # Mantine component re-exports
└── custom/                     # Your components
lib/
├── theme.ts                    # Mantine theme customization
└── utils.ts
styles/
└── mantine.css                 # Mantine CSS imports
```

## Architecture Rules

- **MantineProvider is required.** Wrap your app in `MantineProvider` from `@mantine/core`. It provides theme context and CSS variables.
- **Import CSS files.** Mantine requires specific CSS imports: `@mantine/core/styles.css` and component-specific styles.
- **Theme customization via theme object.** Pass a custom theme to `MantineProvider` for colors, fonts, and component defaults.
- **Use Mantine hooks for common patterns.** `useDisclosure`, `useForm`, `useMediaQuery` replace custom implementations.

## Coding Conventions

- Import components from `@mantine/core`, hooks from `@mantine/hooks`, forms from `@mantine/form`.
- Use the `useMantineTheme` hook to access theme values programmatically.
- Responsive props use object syntax: `<Box w={{ base: 100, md: 200 }} />`.
- Forms use `@mantine/form` with validation through `zod-resolver` or `yup-resolver`.

## Library Preferences

- **Forms:** `@mantine/form` with Zod validation. Not React Hook Form (Mantine form is optimized for Mantine components).
- **Dates:** `@mantine/dates` for date pickers. Not separate date libraries.
- **Notifications:** `@mantine/notifications` for toasts.
- **Modals:** `@mantine/modals` for modal management.
- **Charts:** `@mantine/charts` for data visualization.

## File Naming

- Theme config: `theme.ts`
- Form schemas: `schema.ts` or `[feature]-schema.ts`
- Component wrappers: PascalCase matching Mantine component name.

## NEVER DO THIS

1. **Never forget to import Mantine styles.** Without `import '@mantine/core/styles.css'`, components are unstyled.
2. **Never mix Mantine and other component libraries blindly.** CSS variable conflicts can occur. Test thoroughly.
3. **Never skip the resolver for form validation.** Mantine forms need a resolver for Zod/Yup. Don't validate manually.
4. **Never use `className` for styling Mantine components.** Use style props or the `styles` prop. `className` should be for Tailwind/other CSS.
5. **Never forget `MantineProvider` in tests.** Wrap test renders with the provider or components will error.
6. **Never use `useState` for simple toggle states.** `const [opened, { toggle }] = useDisclosure()` is cleaner.
7. **Never ignore the `ref` prop.** Mantine components support ref forwarding. Use it for focus management.

## Testing

- Wrap component tests with `MantineProvider`. Create a test utility that renders with providers.
- Test form validation by simulating submissions and checking error messages.
- Test responsive behavior by mocking matchMedia.


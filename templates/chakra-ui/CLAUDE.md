# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Chakra UI v3 (Next-generation with Zag.js)
- React 18+
- TypeScript 5.x
- Next.js 15+ or Vite
- Emotion (CSS-in-JS)

## Project Structure

```
src/
├── app/
│   ├── layout.tsx              # Providers wrapper
│   └── page.tsx
├── components/
│   ├── ui/                     # Chakra UI components
│   └── custom/                 # Your composed components
├── theme/
│   ├── index.ts                # Theme export
│   ├── tokens.ts               # Colors, fonts, spacing tokens
│   └── recipes/                # Component style recipes
├── lib/
│   └── utils.ts
└── providers/
    └── chakra-provider.tsx     # ChakraProvider setup
```

## Architecture Rules

- **Use Chakra's composition patterns.** Chakra v3 uses recipes and parts for component styling. Define styles in `theme/recipes/` not inline.
- **Theme tokens first.** Define all colors, spacing, and typography in `theme/tokens.ts`. Reference these tokens in components, not raw values.
- **Style props for one-offs.** Use Chakra's style props (`color="primary.500"`) for simple overrides. Complex styles belong in recipes.
- **Slot recipes for compound components.** Components with multiple parts (Button with icon, Input with addon) use slot recipes.

## Coding Conventions

- Use the `Box` component as the layout primitive. Build other components on top of it.
- Responsive arrays: `<Box p={[2, 4, 6]} />` for mobile-first responsive design.
- Use `forwardRef` for custom components wrapping Chakra primitives.
- Import from `@chakra-ui/react` (single package in v3).
- Type custom component props with `ComponentProps` from Chakra.

## Library Preferences

- **Icons:** Lucide React or `@chakra-ui/icons`. Not mixed icon libraries.
- **Animation:** Framer Motion for complex animations. Chakra v3 uses Zag.js for component state machines.
- **Forms:** React Hook Form integrates well with Chakra's form components.
- **Typography:** Use theme tokens for font families and sizes.

## File Naming

- Theme files: camelCase → `tokens.ts`, `buttonRecipe.ts`
- Component files: PascalCase → `CustomButton.tsx`

## NEVER DO THIS

1. **Never use Chakra UI v2 patterns in v3.** v3 is a complete rewrite with different APIs. Check the v3 docs, not old blog posts.
2. **Never skip the ChakraProvider.** Components won't have access to theme tokens without it.
3. **Never use raw CSS values.** Always reference theme tokens. `padding="4"` not `padding="16px"`.
4. **Never create one-off styled components.** If a component needs custom styling, add a recipe to the theme.
5. **Never forget to configure the Next.js compiler.** Chakra v3 uses Emotion—ensure `transpilePackages` includes `@chakra-ui/react`.
6. **Never mix v2 and v3 imports.** `import { Box } from '@chakra-ui/react'` in v3, not from layout/react packages.
7. **Never ignore the recipe pattern.** Inline `sx` props are for prototyping. Production code uses defined recipes.

## Testing

- Use Testing Library. Chakra components render correctly in JSDOM.
- Test responsive behavior by mocking window dimensions.
- Verify theme token usage matches the design system.


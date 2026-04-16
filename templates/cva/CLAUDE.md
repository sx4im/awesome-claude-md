# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- CVA (Class Variance Authority)
- Tailwind CSS
- TypeScript 5.x
- Variant-based styling
- React/Vue/Svelte

## Project Structure
```
src/
├── components/
│   └── Button.tsx              // Uses cva
├── lib/
│   └── cva.ts                  // CVA utilities
└── styles/
    └── variants.ts             // Shared variants
```

## Architecture Rules

- **Variant-based API.** `intent`, `size`, `color` as typed props.
- **Compound variants.** Combinations like `intent: 'primary' + size: 'large'`.
- **Default variants.** Sensible defaults, easy overrides.
- **Type-safe.** Full TypeScript autocomplete for variants.

## Coding Conventions

- Define: `const button = cva(['base-classes'], { variants: { intent: { primary: 'bg-blue-500', secondary: 'bg-gray-500' }, size: { sm: 'text-sm', lg: 'text-lg' } }, defaultVariants: { intent: 'primary', size: 'sm' } })`.
- Use: `<button className={button({ intent: 'primary', size: 'lg' })} />`.
- Extend: `const iconButton = cva(['base'], { variants: button.variants, defaultVariants: button.defaultVariants })`.

## NEVER DO THIS

1. **Never use without `tailwind-merge` and `clsx`.** CVA expects them for proper class merging.
2. **Never skip `defaultVariants`.** Always provide defaults.
3. **Never make variants too granular.** Group related styles.
4. **Never ignore compound variants.** Handle conflicting combinations.
5. **Never forget to export the type.** `export type ButtonVariant = VariantProps<typeof button>`.
6. **Never use for one-off styles.** CVA shines for reusable components.
7. **Never ignore the `responsiveVariants` extension.** Use for breakpoint-based variants.

## Testing

- Test all variant combinations render correctly.
- Test TypeScript provides autocomplete.
- Test default variants apply when not specified.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Radix Colors
- Accessible color system
- Dark mode support
- Alpha variants
- CSS variables

## Project Structure
```
styles/
├── colors/
│   ├── blue.css                // Radix blue scale
│   ├── red.css
│   └── gray.css
└── theme.css                   // Custom theme using Radix
```

## Architecture Rules

- **27-step scales.** From 1 (background) to 12 (high contrast text).
- **Semantic naming.** `--blue-9` is the primary blue.
- **Dark mode built-in.** Dark scales with automatic switching.
- **Alpha variants.** Transparent overlays: `--blue-a5`.

## Coding Conventions

- Import: `@import '@radix-ui/colors/blue.css';` or `@import '@radix-ui/colors/blue-dark.css';`.
- Usage: `background-color: var(--blue-3); color: var(--blue-11); border-color: var(--blue-6);`.
- Semantic: `--color-background: var(--gray-1); --color-text: var(--gray-12);`.
- Alpha: `box-shadow: 0 2px 10px var(--black-a5);`.
- Theme: Use CSS variables to map Radix to semantic names.

## NEVER DO THIS

1. **Never skip contrast checking.** Radix is accessible but verify your combinations.
2. **Never mix light and dark scales.** Import only one set per theme.
3. **Never use high-scale colors for backgrounds.** Scale 1-3 for backgrounds.
4. **Never ignore the alpha scales.** Use for overlays and shadows.
5. **Never hardcode Radix values.** Always use CSS variables for theming.
6. **Never skip dark mode testing.** Verify both light and dark scales.
7. **Never use scale 12 for borders.** Too high contrast—use 6-7.

## Testing

- Test color contrast ratios pass WCAG.
- Test dark mode appearance.
- Test alpha overlays look correct.


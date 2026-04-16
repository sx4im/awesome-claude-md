# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Open Props (CSS custom properties)
- Vite/PostCSS integration
- Design token approach
- Subsettable imports

## Project Structure
```
src/
├── styles/
│   ├── props/
│   │   ├── index.css           // Import specific props
│   │   └── media.css           // Responsive props
│   └── globals.css             // Uses Open Props
└── main.ts
```

## Architecture Rules

- **CSS variables as tokens.** `--size-1`, `--color-blue-5`, etc.
- **Systematic scaling.** Predefined scales for size, color, shadow.
- **JIT-friendly.** Import only needed props.
- **No build step required.** Can use CDN version.

## Coding Conventions

- Import: `import 'open-props/style'` for all, or `import 'open-props/gray'` for specific.
- Usage: `font-size: var(--font-size-3); padding: var(--size-3);`.
- Gradients: `background: var(--gradient-1);`.
- Shadows: `box-shadow: var(--shadow-2);`.
- Animations: `animation: var(--animation-fade-in);`.
- Custom: Define your own on top: `--brand-color: var(--color-blue-5);`.

## NEVER DO THIS

1. **Never import all props without need.** Bundle size matters—subset.
2. **Never override Open Props directly.** Create semantic aliases.
3. **Never skip the normalize.** `open-props/normalize` provides base styles.
4. **Never use without understanding scales.** Learn the sizing/color scales.
5. **Never ignore the `oklch` colors.** Better perceptual uniformity.
6. **Never forget PostCSS plugin.** For JIT optimization if using build tools.
7. **Never mix with Tailwind blindly.** Different approaches—pick one.

## Testing

- Test CSS custom properties cascade correctly.
- Test animation performance.
- Test color contrast with OKLCH values.


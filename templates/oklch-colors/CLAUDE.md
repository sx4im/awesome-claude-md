# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- OKLCH color space
- CSS color-mix()
- CSS relative colors
- Lightness, chroma, hue
- Perceptually uniform

## Project Structure
```
styles/
├── theme.css                   // OKLCH color definitions
└── components.css              // Component styles using OKLCH
```

## Architecture Rules

- **Perceptually uniform.** Equal lightness steps look equal.
- **CSS native.** `oklch()` function in modern browsers.
- **Better gradients.** No dead gray zones.
- **Accessible by default.** Predictable lightness values.

## Coding Conventions

- Definition: `--color-primary: oklch(60% 0.2 250);` (lightness, chroma, hue).
- Variants: `--color-primary-light: oklch(70% 0.2 250); --color-primary-dark: oklch(50% 0.2 250);`.
- Mix: `background: color-mix(in oklch, var(--color-primary) 70%, white);`.
- Relative: `--color-primary-50: oklch(from var(--color-primary) 50% c h);`.

## NEVER DO THIS

1. **Never use OKLCH without checking browser support.** Safari, modern Chrome/Firefox.
2. **Never mix OKLCH with HSL carelessly.** Different color spaces.
3. **Never exceed chroma limits.** Depends on lightness and hue.
4. **Never skip fallback colors.** For older browsers.
5. **Never ignore the perceptual benefits.** Use for smooth gradients.
6. **Never use raw OKLCH in legacy codebases.** Gradual migration.
7. **Never forget about HDR displays.** OKLCH supports wide gamut.

## File Naming

- Theme files: `theme.css` or `tokens.css` for OKLCH color definitions
- Fallbacks: `fallback.css` for browsers without OKLCH support

## Testing

- Test OKLCH colors render correctly in browsers supporting the `oklch()` function.
- Test gradients appear smooth compared to equivalent HSL gradients.
- Test fallback colors display correctly in older browsers.
- Test wide-gamut colors on HDR displays.
- Test `color-mix()` produces expected intermediate values.


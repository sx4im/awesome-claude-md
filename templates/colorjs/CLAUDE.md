# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Color.js
- Color space conversions
- CSS Color Module Level 4/5
- Gamut mapping
- Accessibility calculations

## Project Structure
```
src/
├── lib/
│   └── colors.ts               // Color utilities
├── theme/
│   └── tokens.ts               // Color tokens
└── components/
```

## Architecture Rules

- **Universal color space.** Work in any color space.
- **Accurate conversions.** Standard-compliant algorithms.
- **Gamut handling.** Map colors to displayable ranges.
- **Delta E.** Perceptual difference calculations.

## Coding Conventions

- Create: `import Color from 'colorjs.io'; const red = new Color('red');` or `new Color('oklch(60% 0.2 250)')`.
- Convert: `const rgb = red.to('srgb'); const hsl = red.to('hsl');`.
- Mix: `const mixed = red.mix('blue', 0.5, { space: 'oklch' });`.
- Contrast: `const contrast = red.contrast('white', 'WCAG21');`.
- Gamut: `const inGamut = red.inGamut('p3'); const mapped = red.toGamut({ space: 'srgb' });`.

## NEVER DO THIS

1. **Never mix color spaces without conversion.** Convert first.
2. **Never ignore gamut limitations.** Check `inGamut()` before using.
3. **Never assume sRGB is universal.** Modern displays have wider gamuts.
4. **Never use imprecise contrast calculations.** Use proper Delta E.
5. **Never skip the `space` parameter in mix().** Different spaces = different results.
6. **Never use Color.js for runtime perf-critical code.** Computationally expensive.
7. **Never forget tree-shaking.** Import specific functions if bundle size matters.

## Testing

- Test color conversions are accurate.
- Test contrast calculations match standards.
- Test gamut mapping preserves hue.


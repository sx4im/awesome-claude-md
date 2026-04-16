# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Capsize
- Trimming whitespace
- Precise text layout
- Font metrics
- CSS-in-JS support

## Project Structure
```
src/
├── components/
│   └── Text.tsx                // Using Capsize
├── styles/
│   └── typography.ts           // Capsize styles
└── fonts/
    └── metrics.ts              // Font metrics
```

## Architecture Rules

- **Trim whitespace.** Remove font built-in line-height.
- **Predictable text layout.** Height matches exactly.
- **Font metrics based.** Use actual font measurements.
- **CSS generation.** Generates trim styles.

## Coding Conventions

- Create: `import { createStyleObject } from '@capsizecss/core'; import interMetrics from '@capsizecss/metrics/inter'; const styles = createStyleObject({ capHeight: 16, lineGap: 24, fontMetrics: interMetrics })`.
- Apply: `<span style={{ ...styles }}>Text</span>` or CSS-in-JS.
- Tailwind: Use `@capsizecss/tailwind` plugin.
- Vanilla Extract: `import { capsize } from '@capsizecss/vanilla-extract';`.

## NEVER DO THIS

1. **Never use without font metrics.** Required for calculations.
2. **Never mix with line-height tricks.** Capsize replaces those.
3. **Never forget the `lineGap` or `leading` option.** Controls spacing.
4. **Never use for body text without testing.** Readability impact.
5. **Never ignore the CSS output.** Understand what's generated.
6. **Never skip the `fontMetrics` package.** Common fonts provided.
7. **Never use without visual testing.** Verify text aligns correctly.

## Testing

- Test text aligns precisely to containers.
- Test different capHeight values.
- Test in different browsers.


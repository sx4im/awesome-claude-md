# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- PostCSS Preset Env
- Stage-based features
- CSS nesting, custom properties, color functions
- Autoprefixer included
- Browserslist integration

## Project Structure
```
├── src/
│   └── styles/
│       └── modern.css          // Modern CSS syntax
├── postcss.config.js
└── .browserslistrc
```

## Architecture Rules

- **Stage-based polyfills.** Stage 0 (experimental) to Stage 4 (stable).
- **Automatic feature detection.** Only polyfills needed for target browsers.
- **Native when possible.** Uses browser features if supported.
- **Browserslist-driven.** Config in package.json or .browserslistrc.

## Coding Conventions

- Config: `postcss.config.js`: `{ plugins: [require('postcss-preset-env')({ stage: 1 })] }`.
- Nesting: `.parent { & .child { color: red; } }`.
- Custom selectors: `@custom-selector :--heading h1, h2, h3; :--heading { ... }`.
- Media queries: `@custom-media --narrow (width < 600px);`.
- Color functions: `color: color-mod(red alpha(50%));` or `oklch()`.
- Logical properties: `margin-inline`, `padding-block`.

## NEVER DO THIS

1. **Never use stage 0 in production.** Too experimental, may change.
2. **Never ignore browserslist.** Critical for determining polyfills.
3. **Never skip the `preserve` option.** Set false to remove originals.
4. **Never use all features blindly.** Know what you're polyfilling.
5. **Never forget about bundle size.** Polyfills add CSS.
6. **Never mix with LightningCSS carelessly.** Similar features—pick one.
7. **Never ignore the `features` option.** Explicitly enable/disable features.

## Testing

- Test compiled CSS in target browsers.
- Test polyfills apply correctly.
- Test bundle size with different stage settings.


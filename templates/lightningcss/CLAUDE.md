# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- LightningCSS (CSS transformer)
- Vite/Webpack integration
- CSS nesting, custom media, color-mix
- Automatic vendor prefixing
- CSS modules support

## Project Structure
```
src/
├── styles/
│   ├── components/
│   │   └── button.css          // Modern CSS with nesting
│   └── globals.css
├── lightningcss.config.js
└── vite.config.ts
```

## Architecture Rules

- **Native CSS features.** Use nesting, `:is()`, `:has()` natively.
- **Automatic transforms.** LightningCSS compiles to browser-compatible CSS.
- **Bundle optimization.** Deduplicates, minifies, optimizes.
- **Draft features.** Enable CSS color-mix, custom media queries.

## Coding Conventions

- Nesting: `.button { &:hover { background: blue; } }`.
- Custom media: `@custom-media --narrow (width < 600px); @media (--narrow) { ... }`.
- Color-mix: `background: color-mix(in srgb, red 50%, blue);`.
- Logical props: `margin-inline`, `padding-block` for RTL support.

## NEVER DO THIS

1. **Never use without checking browser targets.** Configure browserslist.
2. **Never mix with PostCSS carelessly.** LightningCSS replaces many PostCSS plugins.
3. **Never ignore the `errorRecovery` option.** Set true for migration.
4. **Never use draft features without flag.** Enable `drafts` in config.
5. **Never forget CSS modules config.** Separate handling for `.module.css`.
6. **Never skip minification.** `minify: true` for production.
7. **Never ignore bundle analysis.** Check CSS output size.

## Testing

- Test compiled CSS in target browsers.
- Test CSS modules scope correctly.
- Test draft features transform properly.


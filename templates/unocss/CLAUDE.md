# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- UnoCSS (instant atomic CSS)
- Vite/Webpack integration
- Presets: @unocss/preset-wind, @unocss/preset-icons
- Attributify mode
- CSS shortcuts

## Project Structure
```
src/
├── components/
│   └── *.tsx                   // Uses UnoCSS classes
├── uno.config.ts               // UnoCSS configuration
└── main.ts
```

## Architecture Rules

- **Instant compilation.** No build-time CSS generation—CSS created on demand.
- **Atomic by default.** Single-purpose utility classes.
- **Attributify optional.** Use `flex="~ col"` instead of `flex flex-col`.
- **Icon preset.** Direct icon usage as classes: `i-carbon-logo-github`.

## Coding Conventions

- Config: `export default defineConfig({ presets: [presetWind(), presetIcons()] })`.
- Classes: `class="text-red-500 hover:text-red-700"` (same syntax as Tailwind).
- Attributify: `<div flex="~ col" gap="4" text="center" />`.
- Icons: `<div class="i-carbon-logo-github" />`.
- Shortcuts: `shortcuts: [['btn', 'px-4 py-2 rounded bg-blue-500 text-white']]`.

## NEVER DO THIS

1. **Never use without Vite/Webpack plugin.** UnoCSS requires build tool integration.
2. **Never mix with Tailwind blindly.** Similar but different—pick one.
3. **Never forget the attributify preset.** Must add separately to use.
4. **Never ignore the `safelist`.** Dynamic classes need pre-declaration.
5. **Never use arbitrary values excessively.** Define shortcuts instead.
6. **Never skip the reset.** Include `presetMini` for preflight reset.
7. **Never ignore DevTools.** Use `@unocss/devtools` for debugging.

## Testing

- Test generated CSS bundle size.
- Test all shortcut combinations render correctly.
- Test icon preset displays icons properly.


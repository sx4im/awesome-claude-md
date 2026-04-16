# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Windi CSS (on-demand Tailwind alternative)
- Vite/Webpack/Nuxt
- Attributify mode
- Typography plugin
- DevTools for debugging

## Project Structure
```
src/
├── components/
│   └── *.vue/tsx               // Uses Windi classes
├── windi.config.ts             // Windi configuration
└── main.ts
```

## Architecture Rules

- **On-demand generation.** Only used utilities are generated.
- **Faster than Tailwind JIT.** Written in Rust/Go.
- **Attributify built-in.** `flex="~ col"` syntax.
- **Full Tailwind compatible.** Same utility names.

## Coding Conventions

- Config: `export default defineConfig({ attributify: true, theme: { extend: {} } })`.
- Classes: `class="text-red-500 hover:text-red-700"` (same as Tailwind).
- Attributify: `<div flex="~ col" gap="4" />`.
- Shortcuts: `shortcuts: { btn: 'px-4 py-2 rounded bg-blue-500' }`.

## NEVER DO THIS

1. **Never use for new projects.** Windi is in maintenance mode—use UnoCSS.
2. **Never mix with Tailwind.** Pick one atomic CSS solution.
3. **Never forget `windi.css` import.** Usually in entry file.
4. **Never ignore the plugin setup.** Vite/Webpack needs configuration.
5. **Never use attributify without types.** Add `types/windi.d.ts`.
6. **Never skip `preflight`.** Include for CSS reset.
7. **Never forget about `safelist`.** Add dynamic classes.

## Testing

- Test generated CSS bundle size.
- Test attributify compiles correctly.
- Test DevTools show generated classes.
- Test attributify mode.


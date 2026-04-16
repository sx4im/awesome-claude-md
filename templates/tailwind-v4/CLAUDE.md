# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Tailwind CSS v4 (next-generation engine)
- PostCSS 8+
- Lightning CSS (built into Tailwind v4)
- CSS-first configuration
- Modern browser targets (Chrome 111+, Firefox 128+, Safari 16.4+)

## Project Structure

```
src/
├── app/
│   └── globals.css             # @import "tailwindcss" and theme config
├── components/
│   └── *.tsx                   # Component files using Tailwind classes
├── styles/
│   └── theme.css               # Custom CSS theme variables (optional)
├── css/
│   └── input.css               # Entry point if not using globals.css
└── ...
package.json
tsconfig.json
```

## Architecture Rules

- **CSS-first configuration.** Tailwind v4 moves configuration to CSS using `@theme` directive. No `tailwind.config.js` in most cases.
- **Import Tailwind via CSS.** Use `@import "tailwindcss"` in your CSS entry point. Not `tailwindcss` CLI on individual files.
- **Theme customization in CSS.** Define custom colors, fonts, and spacing using `@theme` blocks in your CSS, not a JS config file.
- **Lightning CSS for transforms.** Tailwind v4 uses Lightning CSS internally for vendor prefixing and syntax lowering.

## Coding Conventions

- CSS entry file:
  ```css
  @import "tailwindcss";
  
  @theme {
    --color-primary: #3b82f6;
    --color-secondary: #64748b;
    --font-sans: Inter, system-ui, sans-serif;
  }
  ```
- Use the `@apply` directive sparingly. Prefer utility classes in markup.
- Variants use stacked classes: `hover:focus:underline` (no `@` prefix needed in v4).
- Container queries: Use `@container` and `@min-*` / `@max-*` variants.

## Library Preferences

- **Build tool:** Vite 5+ or Next.js 15+ with built-in Tailwind support.
- **CSS processing:** Lightning CSS (included with Tailwind v4). No separate Autoprefixer needed.
- **Components:** shadcn/ui or custom Radix wrappers work seamlessly.
- **Typography:** `@tailwindcss/typography` plugin for prose content.

## File Naming

- CSS files can be named anything. The entry point just needs `@import "tailwindcss"`.
- No `tailwind.config.js` means no special naming conventions for config.

## NEVER DO THIS

1. **Never use `tailwind.config.js` with v4 unless necessary.** v4 is designed to be config-free. Only create `tailwind.config.js` for complex plugin setups.
2. **Never forget the `@import "tailwindcss"` directive.** Without this, Tailwind doesn't process your CSS.
3. **Never use `@tailwind` directives.** In v4, use `@import "tailwindcss"` instead of `@tailwind base; @tailwind components; @tailwind utilities`.
4. **Never target older browsers without checking.** Tailwind v4 uses modern CSS features (like cascade layers). Verify your browser support matrix.
5. **Never mix v3 and v4 patterns.** The `@apply` syntax is slightly different. Don't copy v3 examples blindly.
6. **Never ignore the `@theme` block.** This is where you customize in v4. Putting variables elsewhere may not work as expected.
7. **Never forget to update your build pipeline.** If migrating from v3, remove `tailwindcss` CLI from npm scripts. Use your bundler's CSS processing instead.

## Testing

- Visual regression testing with Chromatic or Percy. Tailwind classes compile to CSS—test the output.
- Test responsive designs at actual breakpoints. Use browser DevTools, not just resizing the window.
- Verify CSS variable usage in `@theme` blocks renders correctly across browsers.


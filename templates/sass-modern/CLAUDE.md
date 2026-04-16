# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Sass/SCSS (modern features)
- @use and @forward modules
- CSS custom properties
- Vite/Webpack integration
- Stylelint for linting

## Project Structure
```
src/
├── styles/
│   ├── abstracts/
│   │   ├── _index.scss         // Forward all
│   │   ├── _variables.scss     // CSS vars
│   │   ├── _functions.scss
│   │   └── _mixins.scss
│   ├── components/
│   │   └── _button.scss
│   └── main.scss               // Entry point
```

## Architecture Rules

- **Module system.** Use `@use` and `@forward`, not `@import`.
- **Namespacing.** `variables.$primary` or `use ... as *` to unnamespace.
- **CSS variables for theming.** Sass vars for static values, CSS vars for dynamic.
- **Partials with underscore.** `_partial.scss` imported without underscore.

## Coding Conventions

- Module: `@use 'variables'; .btn { color: variables.$primary; }`.
- Forward: `@forward 'variables' hide $internal;` in `_index.scss`.
- With config: `@use 'variables' with ($primary: blue);`.
- Mixins: `@mixin flex-center { display: flex; align-items: center; }`.
- Include: `@include mixins.flex-center;`.
- CSS vars: `--primary: #{$sass-var};` to expose Sass to CSS.

## NEVER DO THIS

1. **Never use `@import`.** Deprecated in favor of `@use`/`@forward`.
2. **Never use global variables.** Everything should be namespaced.
3. **Never skip the `_index.scss` pattern.** Clean API for consumers.
4. **Never forget `meta.load-css`.** For dynamic imports.
5. **Never use Sass for everything.** CSS nesting now native—use it.
6. **Never ignore the module cache.** Each `@use` is cached per file.
7. **Never forget `!default`.** Allow configuration overrides.

## Testing

- Test Sass compiles without warnings.
- Test CSS custom properties output correctly.
- Test module resolution works across files.


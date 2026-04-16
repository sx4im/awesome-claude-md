# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Parcel v2 (zero-config bundler)
- TypeScript/React/Vue/Svelte support
- Rust-based for performance
- Built-in optimizations

## Project Structure

```
src/
├── index.html                  # Entry point
├── index.ts                    # Main script
├── styles.css                  # Entry CSS
└── ...
dist/                           # Output (gitignored)
.parcel-cache/                  # Cache (gitignored)
package.json
```

## Architecture Rules

- **Zero configuration.** Parcel auto-detects entry points and dependencies.
- **HTML-first.** Entry point is an HTML file, not JS.
- **File system caching.** Fast rebuilds with `.parcel-cache`.
- **Scope hoisting.** Tree-shaking and optimization built-in.

## Coding Conventions

- Entry: `src/index.html` with `<script type="module" src="./index.ts">`.
- Automatic transforms: Import SCSS, TypeScript, React—it handles them.
- Dev server: `parcel src/index.html`.
- Production: `parcel build src/index.html`.
- Environment: `process.env.NODE_ENV` automatically set.

## NEVER DO THIS

1. **Never configure what you don't need to.** Parcel is zero-config by design.
2. **Never forget to use `.parcelrc` for advanced config.** Only when defaults don't work.
3. **Never ignore the cache.** Delete `.parcel-cache` if builds act strangely.
4. **Never use Parcel for libraries.** It's optimized for applications, not libraries.
5. **Never mix Parcel with manual bundlers.** Pick one approach.
6. **Never forget about image optimization.** Parcel has built-in image optimization—use it.
7. **Never ignore the `source` field in package.json.** It matters for library builds.

## Testing

- Build and verify output in `dist/`.
- Test dev server hot reloading.
- Test production build optimizations.


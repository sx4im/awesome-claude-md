# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- esbuild v0.20+ (ultra-fast JavaScript bundler)
- Go-based for speed
- TypeScript/JSX/JSON/CSS support
- ESM and CJS output

## Project Structure

```
src/
├── index.ts                    # Entry point
└── ...
dist/                           # Output (gitignored)
esbuild.config.ts               # Build script
package.json
```

## Architecture Rules

- **Speed first.** esbuild is 10-100x faster than other bundlers. Great for development.
- **Minimal configuration.** Sensible defaults, fewer options than Webpack/Rollup.
- **Native TypeScript.** Transpiles TypeScript without type checking.
- **Not a full replacement.** No type checking, limited plugin ecosystem.

## Coding Conventions

- CLI build: `esbuild src/index.ts --bundle --outfile=dist/bundle.js`.
- JavaScript API: `esbuild.build({ entryPoints: ['src/index.ts'], bundle: true })`.
- Watch mode: `esbuild.build({ ..., watch: true })`.
- Serve mode: Built-in dev server with watch.
- Plugins: Custom plugins for specific transformations.

## Library Preferences

- Built-in: TypeScript, JSX, CSS, JSON handling.
- Plugins for: Sass, PostCSS, ESLint integration.
- Use with: tsc for type checking (esbuild doesn't check types).

## NEVER DO THIS

1. **Never rely on esbuild for type checking.** It only transpiles. Run `tsc --noEmit` separately.
2. **Never expect Webpack-level customization.** esbuild is intentionally minimal.
3. **Never use for complex apps without plugins.** Basic apps work; complex apps need Vite/Webpack.
4. **Never ignore the `platform` option.** `browser` vs `node` affects polyfills and built-ins.
5. **Never forget to handle CSS if needed.** esbuild bundles CSS but doesn't process with PostCSS.
6. **Never use esbuild for libraries needing advanced tree-shaking.** Rollup may be better.
7. **Never mix esbuild dev with other bundlers.** Pick one for consistency.

## Testing

- Test build output runs correctly.
- Verify bundle size is acceptable.
- Test sourcemaps work in debugging.


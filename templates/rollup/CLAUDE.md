# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Rollup v4 (JavaScript module bundler)
- TypeScript (via plugins)
- ES modules output
- Tree-shaking by default

## Project Structure

```
src/
├── index.ts                    # Entry point
├── components/
│   └── *.ts
├── utils/
│   └── *.ts
dist/                           # Output (gitignored)
├── bundle.js
└── bundle.esm.js
rollup.config.ts                # Rollup configuration
package.json
```

## Architecture Rules

- **ESM-first bundler.** Rollup is designed for ES modules, optimal for libraries.
- **Tree-shaking.** Dead code elimination works best with ESM.
- **Code splitting.** Dynamic imports create separate chunks.
- **Plugin ecosystem.** Core is minimal; plugins handle transformations.

## Coding Conventions

- Config file: Export default config object or array.
- Input: `input: 'src/index.ts'`.
- Output: `output: { file: 'dist/bundle.js', format: 'esm' }`.
- External: Mark peer dependencies as `external: ['react', 'vue']`.
- Plugins: Use `@rollup/plugin-typescript`, `@rollup/plugin-node-resolve`, etc.

## Library Preferences

- **@rollup/plugin-typescript:** TypeScript support.
- **@rollup/plugin-node-resolve:** Resolve node_modules.
- **@rollup/plugin-commonjs:** Convert CommonJS to ESM.
- **@rollup/plugin-terser:** Minification.
- **rollup-plugin-dts:** Generate .d.ts bundles.

## NEVER DO THIS

1. **Never use Rollup for apps without consideration.** Vite, Webpack better for apps. Rollup excels at libraries.
2. **Never forget to mark peer dependencies external.** Including React in your bundle breaks consumer apps.
3. **Never mix CJS and ESM without commonjs plugin.** Most npm packages are CJS.
4. **Never ignore the `preserveModules` option.** For tree-shaking libraries, consider preserving module structure.
5. **Never skip sourcemaps in library builds.** Consumers need them for debugging.
6. **Never use default exports for libraries.** Named exports tree-shake better.
7. **Never forget `rollup-plugin-peer-deps-external`.** Automatically externalizes peer dependencies.

## Testing

- Build library and test output in test project.
- Verify tree-shaking by checking bundle contents.
- Test CJS/ESM dual output if publishing.


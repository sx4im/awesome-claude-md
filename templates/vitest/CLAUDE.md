# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Vitest v2 (Vite-native testing framework)
- TypeScript 5.x
- Vite projects
- Jest-compatible API
- Native ESM support

## Project Structure
```
src/
├── ...                         # Source files
├── utils.test.ts               # Co-located tests
└── components/
    └── Button.test.tsx
vitest.config.ts                # Vitest configuration
setup.ts                        # Test setup file
```

## Architecture Rules

- **Vite-native.** Uses Vite's config, plugins, and module resolution.
- **Fast by default.** Parallel execution, smart watcher.
- **Jest-compatible.** Familiar `describe`, `it`, `expect` API.
- **Native ESM.** No need for CommonJS transforms.

## Coding Conventions

- Config: `export default defineConfig({ test: { globals: true, environment: 'jsdom' }})`.
- Run: `npx vitest` for watch mode, `npx vitest run` for single run.
- Coverage: `npx vitest run --coverage` with `@vitest/coverage-v8`.
- Mocking: `vi.mock('./module')` for module mocks.
- Spies: `vi.fn()` for function mocks.
- Hooks: `beforeEach`, `afterAll`, etc.

## NEVER DO THIS

1. **Never mix Vitest with Jest in same project.** Pick one.
2. **Never ignore the `environment` option.** Node vs jsdom matters for DOM tests.
3. **Never forget to enable `globals` if desired.** Otherwise import from `vitest`.
4. **Never use `jest` globals without compatibility.** Vitest has `vi` instead of `jest`.
5. **Never skip the `include` config if tests aren't found.** Default is `**/*.test.ts`.
6. **Never forget to mock CSS imports.** `vi.mock('*.css', () => ({}))`.
7. **Never use `console.log` for debugging.** Vitest UI and `debug()` are better.

## Testing

- Test with `vitest --ui` for visual interface.
- Test with `vitest typecheck` for TypeScript checking.


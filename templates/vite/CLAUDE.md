# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Vite v5+ (next-gen frontend tooling)
- TypeScript 5.x
- Rollup (production build)
- esbuild (dev transforms)
- React/Vue/Svelte/Vanilla

## Project Structure

```
public/                         # Static assets (copied as-is)
src/
├── main.ts                     # Entry point
├── components/
│   └── *.tsx
├── styles/
│   └── *.css
└── lib/
    └── utils.ts
index.html                      # HTML entry
vite.config.ts                  # Vite configuration
.env                            # Environment variables
env.d.ts                        # Type declarations
```

## Architecture Rules

- **Dev server with HMR.** Vite provides instant hot module replacement in development.
- **ESM in development.** Native ES modules, no bundling during dev.
- **Rollup for production.** Optimized production builds with code splitting.
- **Plugin ecosystem.** Extend with Rollup-compatible plugins and Vite-specific plugins.

## Coding Conventions

- Entry HTML: `<script type="module" src="/src/main.ts"></script>`.
- Import assets: `import logo from './logo.svg'` for processed assets.
- Env variables: `import.meta.env.VITE_API_URL` (must start with `VITE_` for client).
- Dynamic imports: `const module = await import('./heavy.ts')` for code splitting.
- CSS imports: `import './styles.css'` for processed CSS.

## Library Preferences

- **@vitejs/plugin-react:** Fast Refresh support for React.
- **@vitejs/plugin-vue:** Vue 3 SFC support.
- **@vitejs/plugin-svelte:** Svelte support.
- **unplugin-auto-import:** Automatic import of common APIs.
- **vite-plugin-pwa:** PWA support.

## File Naming

- Config: `vite.config.ts` (not .js for TypeScript projects).
- Env files: `.env`, `.env.local`, `.env.production`.
- Entry HTML: `index.html` at project root.

## NEVER DO THIS

1. **Never import from `src/` with relative paths in production.** Use path aliases.
2. **Never use `require()` in Vite projects.** It's ESM-only. Use `import`.
3. **Never forget `import.meta.env` vs `process.env`.** Vite uses `import.meta.env`.
4. **Never use Node.js built-ins in browser code.** Vite doesn't polyfill by default.
5. **Never ignore the `build.target` config.** It affects browser compatibility.
6. **Never use `__dirname` or `__filename` in browser code.** They don't exist in ESM.
7. **Never forget to configure `base` for sub-path deployment.** Default is root-relative.

## Testing

- Use Vitest for unit testing (Vite-native test runner).
- Use Playwright/Cypress for E2E testing.
- Test build output with `vite preview` before deploying.


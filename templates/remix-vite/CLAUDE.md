# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Remix with Vite
- React 18+
- Vite 5.x
- SPA mode or SSR
- Future flags

## Project Structure
```
app/
├── routes/
│   ├── _index.tsx              // Home route
│   ├── about.tsx
│   └── api.webhook.ts          // Resource routes
├── components/
├── entry.client.tsx
├── entry.server.tsx
├── root.tsx
└── vite.config.ts
```

## Architecture Rules

- **Vite-native.** Uses Vite for dev and build instead of esbuild.
- **Remix future flags.** Enable for latest features.
- **SPA mode available.** `ssr: false` for client-only apps.
- **Resource routes.** API endpoints without UI.

## Coding Conventions

- Config: `remix({ future: { v3_fetcherPersist: true, v3_relativeSplatPath: true } })` in `vite.config.ts`.
- Route: Same as standard Remix—`export default function() { ... }`.
- Loader: `export const loader = async () => { return json(data) }`.
- Action: `export const action = async ({ request }) => { const formData = await request.formData(); ... return redirect('/') }`.

## NEVER DO THIS

1. **Never ignore future flags.** Required for v3 compatibility.
2. **Never mix Vite plugins carelessly.** Some conflict with Remix.
3. **Never skip `entry.client/server` in Vite.** Still required.
4. **Never use without `ssr: false` check for SPA mode.** Different behavior.
5. **Never ignore the `public` directory in Vite.** Vite handles static assets.
6. **Never forget to update `remix` package.** Vite support in recent versions.
7. **Never use esbuild config with Vite.** Vite replaces esbuild for Remix.

## Testing

- Test with Vitest instead of Jest.
- Test routes with `@remix-run/testing`.
- Test with actual Vite dev server.


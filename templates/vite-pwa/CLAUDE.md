# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Vite PWA
- vite-plugin-pwa
- Workbox
- Service Worker generation
- Web App Manifest

## Project Structure
```
public/
├── manifest.json               // Web App Manifest
└── icons/
src/
├── sw.ts                       // Custom service worker
└── main.tsx
vite.config.ts
```

## Architecture Rules

- **Auto-generated SW.** Workbox creates service worker.
- **Precache and runtime cache.** Static assets + dynamic content.
- **Manifest generation.** Automatic manifest with icons.
- **Offline ready.** App works without network.

## Coding Conventions

- Config: `VitePWA({ registerType: 'autoUpdate', manifest: { name: 'My App', short_name: 'MyApp', icons: [...] }, workbox: { globPatterns: ['**/*.{js,css,html,ico,png,svg}'] } })`.
- Register: `import { registerSW } from 'virtual:pwa-register'; registerSW({ immediate: true })`.
- Update: `const updateSW = registerSW({ onNeedRefresh() { if (confirm('New content available. Reload?')) { updateSW(true) } } })`.

## NEVER DO THIS

1. **Never skip HTTPS testing.** SW requires secure context.
2. **Never cache API responses blindly.** Configure runtimeCaching.
3. **Never forget to handle update flow.** Users may see stale content.
4. **Never ignore cache size limits.** Workbox manages but verify.
5. **Never skip manifest icons.** Required for installability.
6. **Never use `immediate: true` without considering UX.** Auto-reload can be jarring.
7. **Never test in Incognito.** SW often disabled in private mode.

## Testing

- Test Lighthouse PWA audit passes.
- Test offline functionality.
- Test update flow.


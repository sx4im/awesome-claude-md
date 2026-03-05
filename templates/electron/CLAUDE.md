# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- Electron 28+ (Chromium + Node.js)
- React 18 with TypeScript (strict mode) for renderer
- Vite for renderer bundling
- electron-builder for packaging and distribution
- IPC for main ↔ renderer communication

## Project Structure

```
src/
├── main/                    # Main process (Node.js)
│   ├── index.ts             # App entry: window creation, lifecycle
│   ├── ipc/                 # IPC handlers grouped by domain
│   │   ├── files.ts         # File system operations
│   │   └── settings.ts      # Settings read/write
│   ├── services/            # Backend logic (file ops, system, native)
│   ├── menu.ts              # Application menu definition
│   └── updater.ts           # Auto-update logic
├── renderer/                # Renderer process (browser/React)
│   ├── src/
│   │   ├── App.tsx          # Root component
│   │   ├── components/
│   │   ├── hooks/
│   │   │   └── useIpc.ts    # Typed IPC invocation hook
│   │   ├── stores/          # Zustand stores
│   │   └── pages/
│   ├── index.html
│   └── vite.config.ts
├── preload/
│   └── index.ts             # contextBridge — exposes IPC API to renderer
└── shared/
    └── types.ts             # Shared types between main and renderer
```

## Architecture Rules

- **Main and renderer are completely separate.** The main process (Node.js) handles file system, native APIs, and system access. The renderer process (browser) handles UI. They communicate only through IPC.
- **Context isolation is always enabled.** `contextIsolation: true` and `nodeIntegration: false` in every `BrowserWindow`. The renderer never accesses Node.js APIs directly.
- **The preload script is the bridge.** `preload/index.ts` uses `contextBridge.exposeInMainWorld()` to expose a typed API object. The renderer calls `window.api.readFile()` — it never sees `ipcRenderer` directly.
- **IPC channels are typed and centralized.** Define all channel names and payload types in `shared/types.ts`. Both main and renderer import from this file. No magic strings for channel names.
- **Main process handles all file I/O.** The renderer requests file operations through IPC. Never use `fs` in the renderer — it doesn't have access (and shouldn't).

## Coding Conventions

- IPC handler naming: `{domain}:{action}` → `files:read`, `files:write`, `settings:get`, `settings:set`. Define as a const enum in `shared/types.ts`.
- IPC handlers use `ipcMain.handle()` (async, returns a value) — not `ipcMain.on()` (fire-and-forget). The renderer uses `ipcRenderer.invoke()` through the preload bridge.
- The preload script exposes methods, not raw IPC access: `contextBridge.exposeInMainWorld('api', { readFile: (path: string) => ipcRenderer.invoke('files:read', path) })`.
- Renderer components use the `useIpc` hook: `const { data, invoke } = useIpc<FileContent>('files:read', filePath)`.
- All window management (open, close, resize) happens in the main process. The renderer requests it through IPC or the main process does it in response to app lifecycle events.

## Library Preferences

- **Renderer bundler:** Vite — not webpack (Vite has faster HMR and simpler config). Use `electron-vite` or configure Vite manually for the renderer.
- **State (renderer):** Zustand — not Redux. Same rationale as any React app. TanStack Query for API data if the app talks to a remote server.
- **Packaging:** electron-builder — not electron-forge (electron-builder has better cross-platform packaging and auto-update integration).
- **Auto-update:** `electron-updater` (part of electron-builder). Publish updates to GitHub Releases or an S3 bucket.
- **Database (local):** `better-sqlite3` for structured local data — not SQLite3 (better-sqlite3 is synchronous, faster, and easier to use in Electron's main process). For simple key-value, use `electron-store`.

## File Naming

- Main process: `camelCase.ts` → `index.ts`, `menu.ts`, `updater.ts`
- IPC handlers: `camelCase.ts` → `files.ts`, `settings.ts`
- Preload: `preload/index.ts` (single entry)
- Renderer components: `PascalCase.tsx` → `Sidebar.tsx`, `FileList.tsx`
- Shared: `camelCase.ts` → `types.ts`, `constants.ts`

## NEVER DO THIS

1. **Never enable `nodeIntegration` in the renderer.** It gives the browser full Node.js access — any XSS vulnerability becomes a full system compromise. Always use `contextIsolation: true` with a preload script.
2. **Never use `ipcRenderer` directly in React components.** The preload script exposes a typed API via `contextBridge`. Components call `window.api.doThing()` — they never import from `electron`.
3. **Never use string literals for IPC channels.** Define all channels in `shared/types.ts` as a const object. String typos in channel names cause silent failures — typed constants catch them at compile time.
4. **Never do heavy computation in the main process without a worker.** The main process runs the event loop for all windows. CPU-bound work (file parsing, image processing) should use `worker_threads` or `utilityProcess` (Electron 22+).
5. **Never store sensitive data in `localStorage` or `sessionStorage` in the renderer.** Local storage is unencrypted. Use `safeStorage` from Electron for encrypting secrets, or `electron-store` with encryption enabled.
6. **Never ship devtools enabled in production.** Remove `mainWindow.webContents.openDevTools()` in production builds. Use environment checks: `if (process.env.NODE_ENV === 'development')`.
7. **Never ignore auto-update error handling.** Updates can fail (network, corrupt file, permissions). Handle `error` events from `autoUpdater`, show user-friendly messages, and never force-quit the app on update failure.

## Testing

- Unit test renderer with Vitest + React Testing Library (same as any React app).
- Unit test main process services with Vitest — mock `fs`, `electron`, and IPC.
- Test IPC communication with Spectron or Playwright for Electron.
- Test the packaged app on all target platforms (macOS, Windows, Linux) before release.
- Use `electron-builder`'s `--dir` flag for fast test builds (no installer, just the app directory).

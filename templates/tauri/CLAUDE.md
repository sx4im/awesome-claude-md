# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- Tauri 2.x (Rust backend + Web frontend)
- React 18 + TypeScript for frontend
- Vite for frontend bundling
- Rust for backend commands and system access
- SQLite (via `rusqlite`) or file system for local data
- Tauri plugins for native features

## Project Structure

```
src-tauri/
├── src/
│   ├── main.rs              # Tauri app builder, plugin registration
│   ├── commands/            # IPC command handlers
│   │   ├── mod.rs
│   │   ├── files.rs         # File system operations
│   │   └── settings.rs      # App settings read/write
│   ├── state.rs             # Managed state (database, config)
│   └── error.rs             # Custom error types implementing Serialize
├── tauri.conf.json          # Tauri configuration (window, security, plugins)
├── capabilities/            # Permission capabilities (Tauri v2)
└── Cargo.toml
src/                         # Frontend (React + TypeScript)
├── components/
├── hooks/
│   └── useInvoke.ts         # Typed wrapper around Tauri invoke
├── lib/
│   └── commands.ts          # Typed command invocation functions
├── pages/
├── App.tsx
└── main.tsx
```

## Architecture Rules

- **Tauri commands are the API boundary.** The frontend calls `invoke<T>('command_name', { args })`. The Rust backend executes the command and returns typed data. All system access (files, network, OS) goes through commands — the frontend never accesses them directly.
- **Commands are thin.** A `#[tauri::command]` function extracts parameters, calls core logic, and returns a `Result<T, Error>`. Business logic lives in separate modules, not in command functions.
- **State is managed by Tauri.** Use `tauri::State<T>` for shared state (database connections, config). Register state in `main.rs` with `.manage(MyState::new())`. Never use `lazy_static` or global mutexes.
- **Frontend is a regular React SPA.** It knows nothing about Rust internals. Communication happens through the typed invoke wrapper in `lib/commands.ts`. The frontend never imports from `src-tauri/`.
- **Permissions are explicit.** Tauri v2 uses a capability system. Only enable the permissions your app needs in `capabilities/`. Never use `"permissions": ["*"]`.

## Coding Conventions

- **Typed invoke on frontend:** create a typed wrapper: `export async function readFile(path: string): Promise<string> { return invoke('read_file', { path }); }`. Never use raw `invoke` with string commands in components.
- **Error serialization:** command errors must implement `Serialize`. Define an error enum with `thiserror` + `serde::Serialize`. Tauri serializes errors to the frontend — raw Rust errors aren't serializable.
- **State mutation:** use `Mutex<T>` or `RwLock<T>` inside `tauri::State` for mutable state. The frontend triggers state changes via commands, then queries the new state.
- **Window management:** multi-window apps define window configs in `tauri.conf.json`. Create new windows from the Rust side with `tauri::WindowBuilder`. Never create windows from the frontend — the Rust side controls lifecycle.
- **File paths:** use Tauri's path resolver: `app.path().app_data_dir()`, `app.path().document_dir()`. Never hardcode paths — they differ per OS.

## Library Preferences

- **Frontend bundler:** Vite — built-in Tauri support, fast HMR. Not webpack.
- **Database:** `rusqlite` for local SQLite — not diesel (overkill for desktop app local storage). `serde_json` for simple config files. Not `electron-store` (that's Electron).
- **HTTP (from Rust):** `reqwest` — the standard Rust HTTP client. Use Tauri's HTTP plugin only if you need the frontend to make requests directly.
- **Notifications, dialogs, file picker:** Tauri plugins (`tauri-plugin-dialog`, `tauri-plugin-notification`). Not custom Rust code for native UI elements.

## NEVER DO THIS

1. **Never enable `dangerousRemoteDomainIpcAccess`.** It allows arbitrary remote pages to invoke Tauri commands. This is a full system compromise.
2. **Never use `.unwrap()` in command handlers.** Unwrap panics crash the entire application. Return `Result<T, Error>` and let the frontend handle errors gracefully.
3. **Never access the file system from the frontend.** All file operations go through Tauri commands. The frontend is sandboxed — direct `fs` access is a security boundary violation.
4. **Never expose broad permissions.** Each capability should list exactly which commands and scopes the frontend window can access. Start with zero permissions and add only what's needed.
5. **Never store sensitive data in plain files.** Use OS keychain integration (`tauri-plugin-stronghold` or platform keychains). Plaintext config files are readable by any app on the user's machine.
6. **Never use `std::process::exit()` to close the app.** Use the Tauri app handle: `app.exit(0)` or window close events. `process::exit()` skips cleanup handlers.
7. **Never bundle dev dependencies in the release build.** Check `Cargo.toml` — test utilities and dev tools should be in `[dev-dependencies]`. Audit the binary size with `cargo bloat`.

## Testing

- **Rust tests:** `#[cfg(test)]` modules for core logic. Test commands by calling the inner functions directly (not through Tauri IPC).
- **Frontend tests:** Vitest + React Testing Library. Mock the `invoke` function to test component behavior.
- **E2E tests:** WebDriver-based tests using `tauri-driver` or manual testing of packaged builds.
- Test on all target platforms (macOS, Windows, Linux) — platform-specific bugs are common in desktop apps.

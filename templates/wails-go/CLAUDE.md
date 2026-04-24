# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Desktop)

### Release Discipline
- Constrain file system and process execution permissions to least privilege.
- Treat local data persistence and migration as production data operations.
- Preserve cross-platform behavior for OS-specific integrations.

### Merge/Release Gates
- Packaging/build checks pass for target OSes.
- Install/update/uninstall paths tested for data safety.
- Critical menu/IPC/file operations validated end-to-end.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Backend: Go 1.22+ with Wails v2 runtime bindings
- Frontend: Svelte 5 with runes reactivity (or React 19 -- choose one per project)
- Build System: Wails CLI for development, building, and packaging
- Styling: Tailwind CSS 4 with PostCSS
- State (frontend): Svelte 5 runes ($state, $derived, $effect) or Zustand for React
- IPC: Wails bindings generate TypeScript wrappers for Go methods automatically
- Database: SQLite via mattn/go-sqlite3 or modernc.org/sqlite (CGo-free)
- Packaging: Wails v2 produces native .app, .exe, .AppImage bundles

## Project Structure

```
main.go                        # Wails app bootstrap: app.New, bind structs, run
app.go                         # App struct with OnStartup, OnShutdown lifecycle hooks
internal/
  services/
    item_service.go            # Business logic bound to Wails frontend
    file_service.go            # File dialog and filesystem operations via Wails runtime
    settings_service.go        # User preferences with JSON file persistence
  models/
    item.go                    # Domain structs and validation methods
    settings.go
  database/
    sqlite.go                  # Database connection, migration runner
    migrations/
      001_initial.sql          # SQL migration files applied in order
    queries/
      items.go                 # Query functions returning typed results
  util/
    paths.go                   # OS-specific config and data directory resolution
frontend/
  src/
    App.svelte                 # Root Svelte component
    lib/
      components/              # Reusable Svelte components (Button, Modal, DataTable)
      stores/
        items.ts               # Svelte store wrapping Wails-generated bindings
      wailsjs/                 # Auto-generated TypeScript bindings (do not edit)
        go/
          services/            # Generated TS functions matching Go methods
        runtime/               # Wails runtime helpers (EventsOn, EventsOff, etc.)
    routes/                    # Page-level components if using svelte-spa-router
    assets/
      global.css               # Tailwind directives and global styles
  index.html                   # Entry HTML loaded by Wails WebView
  vite.config.ts               # Vite config with Svelte plugin
  tailwind.config.ts
wails.json                     # Wails project configuration (name, frontend dir, build hooks)
build/                         # Platform-specific build assets (icons, manifests, Info.plist)
```

## Architecture Rules

- Go structs are bound to the frontend via `app.Bind(&services.ItemService{})` in main.go
- Every bound method must return either `(T, error)` or `error`; the TypeScript wrapper converts errors to rejected promises
- Use Wails runtime context (`ctx context.Context`) passed in `OnStartup` for runtime API calls (dialogs, events, menus)
- Frontend-to-backend communication is strictly through generated bindings; never use HTTP endpoints or WebSocket
- Backend-to-frontend communication uses Wails events: `runtime.EventsEmit(ctx, "event-name", data)`
- Frontend listens with `EventsOn("event-name", callback)` from `@wailsio/runtime`

## Coding Conventions

- Go services use struct methods with pointer receivers: `func (s *ItemService) GetAll() ([]models.Item, error)`
- Keep bound service structs focused; split into multiple services rather than creating one God struct
- Error handling in Go follows standard patterns: return errors up, wrap with `fmt.Errorf("context: %w", err)`
- Frontend components import from the generated `wailsjs/go/services` path for backend calls
- Use Wails runtime dialogs (`runtime.OpenFileDialog`, `runtime.SaveFileDialog`) instead of browser file inputs
- Svelte components use runes: `let count = $state(0)` and `let doubled = $derived(count * 2)`
- All user-facing strings on the frontend are in English by default; use a JSON i18n approach if multilingual

## Library Preferences

- Database: modernc.org/sqlite (pure Go, no CGo) for easy cross-compilation
- JSON handling: encoding/json from stdlib; use struct tags for serialization
- Logging: log/slog (structured logging from Go stdlib)
- Config files: JSON or TOML in OS-specific config directory (os.UserConfigDir)
- Frontend HTTP (if needed): native fetch API for external third-party API calls
- CSS framework: Tailwind CSS 4 with the Vite plugin
- Validation: go-playground/validator for Go struct validation

## File Naming

- Go files: snake_case (`item_service.go`, `sqlite.go`)
- Go packages: short lowercase names (`services`, `models`, `database`)
- Svelte components: PascalCase (`ItemList.svelte`, `SettingsPanel.svelte`)
- TypeScript files: camelCase (`itemStore.ts`, `utils.ts`)
- SQL migrations: numbered prefix (`001_initial.sql`, `002_add_tags.sql`)
- Wails-generated files in `wailsjs/`: never rename or edit; regenerated on build

## NEVER DO THIS

1. Never edit files in the `frontend/src/lib/wailsjs/` directory; they are auto-generated by `wails generate module`
2. Never use `net/http` to create an HTTP server; Wails provides its own IPC bridge via WebView bindings
3. Never use `os.Exit()` in services; return errors and let the Wails lifecycle handle shutdown gracefully
4. Never store sensitive data in plain text config files; use OS keychain via zalando/go-keyring
5. Never use `unsafe` package or CGo unless absolutely required; it breaks cross-compilation with Wails
6. Never call `runtime.Quit(ctx)` from a service method without user confirmation via a dialog first

## Testing

- Go unit tests in `_test.go` files adjacent to source: `item_service_test.go`
- Use `testing.T` with table-driven tests for service methods
- Database tests use an in-memory SQLite database (`file::memory:?cache=shared`)
- Mock the Wails runtime context by passing `context.Background()` in tests
- Frontend tests with Vitest and @testing-library/svelte (or @testing-library/react)
- Mock Wails bindings in frontend tests: `vi.mock('../lib/wailsjs/go/services/ItemService')`
- Run Go tests: `go test ./internal/...`; run frontend tests: `cd frontend && npm test`
- Build and smoke test with `wails build` to verify both Go and frontend compile cleanly

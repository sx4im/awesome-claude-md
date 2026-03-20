# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Obsidian Plugin API (desktop + mobile)
- TypeScript 5.x (strict mode)
- esbuild for bundling (Obsidian sample plugin config)
- CSS for styling (no preprocessors, Obsidian injects plugin CSS globally)
- Obsidian API types via `obsidian` package (dev dependency only)

## Project Structure

```
src/
├── main.ts                   # Plugin entry: extends Plugin, onload/onunload lifecycle
├── settings.ts               # Settings tab: extends PluginSettingTab
├── types.ts                  # Plugin settings interface, custom type definitions
├── views/
│   ├── [VIEW_NAME]-view.ts   # Custom views: extend ItemView for sidebar/tab panes
│   └── [MODAL_NAME]-modal.ts # Modals: extend Modal for dialogs
├── commands/
│   └── [COMMAND_NAME].ts     # Command definitions (addCommand registrations)
├── services/
│   └── [DOMAIN].ts           # Business logic separated from Obsidian API
├── utils/
│   ├── vault.ts              # Vault read/write helpers (TFile/TFolder operations)
│   └── markdown.ts           # Markdown parsing and transformation utilities
├── styles.css                # Plugin styles (loaded by Obsidian automatically)
manifest.json                 # Plugin metadata: id, name, minAppVersion
versions.json                 # Version-to-minAppVersion compatibility map
```

## Architecture Rules

- **`main.ts` is the only entry point.** It exports a default class extending `Plugin`. All commands, views, event listeners, and ribbon icons are registered in `onload()` and cleaned up in `onunload()`. Nothing else is auto-discovered.
- **Everything registered must be unregistered.** Event listeners added via `this.registerEvent()` are auto-cleaned. But if you use `addEventListener` directly on DOM elements or `window`, you must remove them in `onunload()`. Leaked listeners persist across plugin reloads and cause bizarre bugs.
- **Access the vault only through the Obsidian API.** Use `this.app.vault.read()`, `vault.modify()`, `vault.create()`. Never use Node.js `fs` directly. The vault API handles mobile compatibility, sync conflict avoidance, and metadata cache updates.
- **Settings are loaded/saved through `loadData()`/`saveData()`.** These serialize to `data.json` in the plugin folder. Always merge loaded data with defaults: `this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData())`. Never assume every field exists in saved data (users may upgrade from older versions).
- **Views are singletons per leaf type.** Register a view type with `registerView()`, then use `workspace.getLeaf()` to activate it. Never create multiple instances of the same view type manually.

## Coding Conventions

- **Commands include a human-readable `name` and machine `id`.** The `id` is prefixed with your plugin ID automatically. The `name` appears in the command palette. Make names action-oriented: "Insert template" not "Template inserter".
- **Settings UI uses the `Setting` class declaratively.** Each setting is a `new Setting(containerEl).setName().setDesc().addToggle/addText()` chain. Group related settings with `containerEl.createEl('h3')` headings.
- **Use `MarkdownRenderer.render()` for displaying markdown.** Never set `innerHTML` with raw markdown. The renderer handles internal links, embeds, and themes correctly.
- **File references use `TFile` objects, not string paths.** Get files via `vault.getAbstractFileByPath()` and type-check with `instanceof TFile`. String paths break when users rename files. Use `vault.on('rename')` to track moves.
- **CSS classes are prefixed with your plugin ID.** Use `.my-plugin-container` not `.container`. Obsidian injects all plugin CSS globally. Unprefixed classes collide with Obsidian's own styles or other plugins.

## Library Preferences

- **Bundler:** esbuild (the official sample plugin config). Not webpack, not Vite. Obsidian expects a single `main.js` output file.
- **UI rendering:** Obsidian's native DOM API (`createEl`, `createDiv`, `Setting`). Not React or Svelte unless the UI is genuinely complex. Adding a framework means bundling it into `main.js`, bloating the plugin.
- **Markdown processing:** Obsidian's built-in `MarkdownRenderer` and `MetadataCache`. Not `remark` or `marked`. Obsidian's renderer handles wiki-links, callouts, and custom syntax that external parsers miss.
- **Icons:** Obsidian's `setIcon()` with Lucide icon names. Not custom SVGs unless the icon truly doesn't exist in Lucide.

## File Naming

- Plugin entry: `main.ts` (required by Obsidian)
- Settings tab: `settings.ts`
- Views: `kebab-case-view.ts` → `timeline-view.ts`, `graph-view.ts`
- Modals: `kebab-case-modal.ts` → `search-modal.ts`, `confirm-modal.ts`
- Commands: `kebab-case.ts` → `insert-template.ts`, `toggle-sidebar.ts`
- Services: `kebab-case.ts` → `template-engine.ts`, `sync-service.ts`

## NEVER DO THIS

1. **Never use `document.querySelector` to find Obsidian UI elements.** Obsidian's DOM structure is internal and changes between versions. Use the Plugin API (`workspace.getActiveViewOfType`, `workspace.iterateAllLeaves`). Your plugin will break on the next Obsidian update if you depend on DOM structure.
2. **Never store absolute file paths.** Obsidian vaults are portable. Store vault-relative paths only. Use `file.path` (relative) not `vault.adapter.getFullPath(file)`.
3. **Never call `vault.modify()` inside a rapid loop without debouncing.** Each call triggers sync, metadata reindex, and file watchers. Batch changes or debounce to avoid freezing the UI and triggering sync conflicts.
4. **Never register commands conditionally inside `onload()` based on settings.** Commands registered in `onload()` are fixed for the plugin lifecycle. If a command should be conditional, register it always and check the setting inside the callback.
5. **Never forget `minAppVersion` in `manifest.json`.** If you use a newer API (e.g., `workspace.getActiveFileView()`), set `minAppVersion` to the version that introduced it. Users on older Obsidian versions will see cryptic errors otherwise.
6. **Never read `this.app.vault.adapter` internals.** The adapter differs between desktop (Node fs) and mobile (Capacitor). Code that works on desktop will crash on mobile. Stick to `vault.read()` and `vault.modify()`.
7. **Never add CSS that overrides Obsidian's theme variables.** Respect `--background-primary`, `--text-normal`, etc. Hardcoding `color: #333` breaks dark themes. Always use `var(--text-normal)` and similar CSS variables.

## Testing

- Use Vitest for unit testing services and utilities that don't depend on the Obsidian API.
- Mock the `App`, `Vault`, and `Workspace` objects for integration tests. Create thin mock classes that implement only the methods your plugin uses.
- Test settings serialization roundtrips: save settings, load them back, verify defaults merge correctly with partial saved data.
- Manual test on both desktop and mobile before release. Mobile has no `fs`, no `path`, and a different DOM rendering engine.
- Use the Obsidian developer console (`Ctrl+Shift+I`) to verify no console errors on plugin load/unload cycles.

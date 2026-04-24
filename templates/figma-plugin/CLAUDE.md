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

## Production Delivery Playbook (Category: Bots & Plugins)

### Release Discipline
- Constrain event handlers to explicit allowlists and permission scopes.
- Validate all external payloads and signatures where supported.
- Prevent runaway automation loops and duplicate side effects.

### Merge/Release Gates
- Webhook/event contract tests pass.
- Rate-limit and retry behavior validated.
- Security-sensitive commands reviewed for abuse paths.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Figma Plugin API (latest)
- TypeScript 5.x (strict mode)
- [UI_FRAMEWORK: Preact / Svelte] for plugin UI
- esbuild or Vite for bundling
- figma.ui ↔ figma.main message passing

## Project Structure

```
src/
├── main.ts                   # Plugin sandbox: figma.* API access, node manipulation
├── ui/
│   ├── index.html            # UI entry point (loaded by figma.showUI)
│   ├── App.[tsx|svelte]      # Root UI component
│   ├── components/           # UI components (inputs, previews, panels)
│   └── styles/               # CSS/SCSS for the UI iframe
├── shared/
│   ├── messages.ts           # Message type definitions (main ↔ UI protocol)
│   ├── constants.ts          # Shared constants (plugin dimensions, limits)
│   └── types.ts              # Shared types (node data shapes, settings)
├── services/
│   ├── nodes.ts              # Node creation and manipulation helpers
│   ├── styles.ts             # Style reading/application (fills, strokes, effects)
│   └── selection.ts          # Selection handling and validation
├── utils/
│   ├── color.ts              # Color conversion (hex ↔ RGB ↔ Figma RGBA 0-1)
│   └── units.ts              # Unit conversions (px, rem, design tokens)
manifest.json                 # Plugin manifest: id, name, api, editorType
```

## Architecture Rules

- **Two separate execution contexts.** `main.ts` runs in Figma's sandbox with access to the `figma.*` API and the document. `ui/` runs in an iframe with normal DOM access but zero `figma.*` access. They communicate exclusively via `figma.ui.postMessage()` and `figma.ui.onmessage`.
- **All `figma.*` calls happen in `main.ts`.** Never try to access `figma.currentPage` or `figma.createRectangle()` from UI code. The `figma` global does not exist in the iframe. If the UI needs node data, request it via a message.
- **Messages are the API contract.** Define a typed message protocol in `shared/messages.ts`. Every message has a `type` discriminator and a typed `payload`. Both sides switch on `type` and handle exhaustively. No untyped `postMessage({ action: 'doThing' })`.
- **Reads are cheap, writes are expensive.** Reading node properties is fast. Creating nodes, setting properties, and rearranging the tree trigger Figma's internal recalculation. Batch writes: build the full node tree, then append to the page once.
- **Always close the plugin.** Call `figma.closePlugin()` when the operation completes if the plugin is a run-once action. For persistent UI plugins, let the user close via the UI or the Figma chrome.

## Coding Conventions

- **Colors use Figma's 0-1 RGBA format.** Figma represents colors as `{ r: 0-1, g: 0-1, b: 0-1 }`. Never pass hex strings or 0-255 integers to Figma paint properties. Write explicit conversion functions: `hexToFigmaRGB('#FF0000')` → `{ r: 1, g: 0, b: 0 }`.
- **Node types are narrowed before access.** After `figma.currentPage.selection`, always check `node.type === 'FRAME'` before accessing frame-specific properties. The selection array contains `SceneNode`, which is a union of all node types.
- **Fonts are loaded before text operations.** Call `await figma.loadFontAsync({ family, style })` before setting `textNode.characters`. Forgetting this throws at runtime with an unhelpful error. Load fonts once at plugin start for known fonts.
- **UI dimensions are set in `figma.showUI()`.** Pass `{ width: <width>, height: <height> }` to `showUI`. Resize dynamically with `figma.ui.resize()`. Never rely on CSS to set the iframe size; Figma controls the frame dimensions.
- **Avoid sync property reads on large documents.** `figma.currentPage.findAll()` traverses the entire page. For large files, use `findAllWithCriteria()` with type filters or limit scope to the current selection.

## Library Preferences

- **UI framework:** Preact for React-like DX in a tiny bundle. Svelte if you prefer it. Not full React (too large for a plugin iframe, slow startup).
- **Bundler:** esbuild for speed. Vite if you want HMR for UI development. Not webpack (overkill for plugin-sized bundles).
- **CSS:** Vanilla CSS or CSS modules. Use `@figma/plugin-ds` design tokens to match Figma's native UI look. Not Tailwind (adds bundle size for a small UI).
- **Color math:** Write your own conversion utilities (hex ↔ Figma RGB is ~10 lines). Not `chroma-js` or `color` (heavy dependencies for simple math).

## File Naming

- Plugin sandbox: `main.ts` (single entry)
- UI entry: `ui/index.html` + `ui/App.tsx` or `ui/App.svelte`
- Components: `PascalCase.tsx` → `ColorPicker.tsx`, `LayerList.tsx`
- Services: `kebab-case.ts` → `node-builder.ts`, `style-extractor.ts`
- Shared: `kebab-case.ts` → `messages.ts`, `types.ts`

## NEVER DO THIS

1. **Never access `figma.*` from UI code.** The `figma` global does not exist in the iframe context. Your code will throw `ReferenceError: figma is not defined`. All document access goes through message passing.
2. **Never forget `await figma.loadFontAsync()` before modifying text.** Setting `textNode.characters` without loading the font first throws a runtime error. This is the single most common Figma plugin bug.
3. **Never pass non-cloneable objects via `postMessage`.** Figma nodes, functions, and circular references cannot be serialized. Extract plain data objects from nodes before sending to UI. `postMessage(figmaNode)` silently fails or throws.
4. **Never use 0-255 color values.** Figma uses 0-1 floats. Setting `{ r: 255, g: 0, b: 0 }` creates white, not red. Always divide by 255 when converting from standard RGB.
5. **Never traverse the entire document tree on startup.** `figma.root.findAll()` on a large file freezes Figma for seconds. Scope searches to `figma.currentPage` or `figma.currentPage.selection`. Use `findAllWithCriteria({ types: ['TEXT'] })` to limit scope.
6. **Never create nodes without setting position and size.** Nodes created via `figma.createRectangle()` default to (0,0) with 100x100. Always set `x`, `y`, `width`, `height` explicitly. Overlapping nodes at origin confuse users.
7. **Never ignore mixed values.** Properties like `fontSize` on a text node with multiple styles return `figma.mixed`. Checking `textNode.fontSize === 16` when the value is `mixed` evaluates to `false` silently. Always check for `figma.mixed` first.

## Testing

- Use Vitest to unit test services, color conversion utilities, and message handlers in isolation.
- Mock the `figma` global for main.ts tests: create a fake `figma` object with stubs for `createRectangle`, `currentPage`, `loadFontAsync`, etc.
- Test the message protocol by verifying that main.ts handlers produce correct responses for each UI message type and vice versa.
- Test UI components independently using your framework's testing tools (Preact Testing Library or Svelte Testing Library) without Figma.
- Manual testing is unavoidable: run the plugin in Figma with the developer console open. Check for font loading errors, selection edge cases, and large file performance.

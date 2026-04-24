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

## Production Delivery Playbook (Category: Platform & Framework Engineering)

### Release Discipline
- Preserve platform-specific lifecycle, build, and runtime constraints.
- Treat compatibility and upgrade paths as first-class requirements.
- Avoid hidden coupling that blocks portability or rollback.

### Merge/Release Gates
- Build/test matrix passes for supported targets.
- Critical startup/runtime flows validated under production-like config.
- Migration/rollback notes included for impactful framework changes.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Rust (stable toolchain, 2021 edition)
- wasm-bindgen for Rust ↔ JavaScript interop
- wasm-pack for building, packaging, and publishing
- web-sys for DOM/Web API bindings
- js-sys for JavaScript built-in object bindings
- [JS_FRAMEWORK: vanilla / React / Svelte] for the host application

## Project Structure

```
crate/
├── Cargo.toml                # [package] + wasm-bindgen, web-sys, js-sys dependencies
├── src/
│   ├── lib.rs                # #[wasm_bindgen] exports: public API surface
│   ├── core/
│   │   ├── mod.rs            # Core computation logic (pure Rust, no wasm-bindgen)
│   │   └── {domain}.rs       # Domain-specific algorithms and data structures
│   ├── bindings/
│   │   ├── mod.rs            # JavaScript interop wrappers
│   │   ├── imports.rs        # #[wasm_bindgen] extern blocks for JS functions
│   │   └── exports.rs        # #[wasm_bindgen] public structs and functions
│   ├── utils/
│   │   ├── console.rs        # web_sys::console::log wrappers
│   │   └── panic.rs          # console_error_panic_hook setup
│   └── types.rs              # Shared types, enums, error definitions
www/                          # JavaScript host application
├── index.html
├── index.js                  # Wasm module initialization and usage
└── package.json              # Dependencies including the wasm-pack output
```

## Architecture Rules

- **Core logic is pure Rust with no wasm-bindgen dependency.** The `core/` module contains algorithms, data structures, and transformations using only Rust types. The `bindings/` layer converts between JS types and Rust types. This lets you test core logic natively with `cargo test` without a browser.
- **The `#[wasm_bindgen]` boundary is narrow.** Expose the minimum API surface. Each exported function takes and returns simple types (numbers, strings, `JsValue`, typed arrays). Never export internal implementation structs that have no meaning to the JS caller.
- **Memory is explicitly managed at the boundary.** Rust owns its heap. JavaScript owns its heap. Data crosses via copy (for small values) or shared `Uint8Array` views (for large buffers). Never assume garbage collection frees Rust-allocated memory; call `.free()` on returned wasm-bindgen objects in JS.
- **`web-sys` features are opt-in.** Each Web API (Window, Document, HtmlCanvasElement) is a Cargo feature. Enable only what you use in `Cargo.toml`: `web-sys = { features = ["Document", "Element", "HtmlCanvasElement"] }`. Never enable the entire `web-sys` API.
- **Panics become JS exceptions.** Set up `console_error_panic_hook` in an init function so Rust panics produce readable stack traces in the browser console instead of "unreachable executed" errors.

## Coding Conventions

- **Export an `init()` function.** Use `#[wasm_bindgen(start)]` or an explicit `pub fn init()` to set up panic hooks and one-time initialization. The JS side calls this before any other exports.
- **Return `Result<T, JsValue>` for fallible operations.** wasm-bindgen converts `Err(JsValue)` into a thrown JS exception. Never panic on expected errors; return `Err(JsError::new("message").into())`.
- **Use `serde-wasm-bindgen` for complex data.** For passing structs and enums across the boundary, derive `Serialize`/`Deserialize` and use `serde_wasm_bindgen::to_value()` / `from_value()`. Not `JsValue::from_serde()` (deprecated since wasm-bindgen 0.2.90).
- **Large data uses zero-copy views.** For image buffers, audio data, or large arrays, return `Vec<u8>` and access it as `Uint8Array` on the JS side. Never serialize large binary data as JSON.
- **Feature-gate browser-specific code.** Use `#[cfg(target_arch = "wasm32")]` for code that only compiles for wasm. This lets `cargo test` run on native targets without web-sys compilation errors.

## Library Preferences

- **Interop:** `wasm-bindgen` (required). Not `stdweb` (abandoned). Not `wasm-pack` alternatives like `trunk` unless you want a full frontend framework.
- **Build tool:** `wasm-pack build --target web` for ES module output. Use `--target bundler` if integrating with webpack/Vite. Not `cargo build --target wasm32` raw (loses wasm-bindgen glue generation).
- **Serialization:** `serde` + `serde-wasm-bindgen` for structured data. Not `serde-json` string serialization (unnecessary parse step in JS, loses type info).
- **Random/crypto:** `getrandom` with the `"js"` feature for WASM random. Not `rand` with default features (it won't compile for wasm32 without `getrandom/js`).
- **Error handling:** `thiserror` for internal errors, converted to `JsError` at the boundary. Not `anyhow` (its `Display` output is less useful for JS callers).

## File Naming

- Rust modules: `snake_case.rs` → `image_processor.rs`, `color_space.rs`
- Exported functions: `snake_case` in Rust, wasm-bindgen converts to `camelCase` in JS
- JS wrapper: `index.js` or `wasm-loader.ts` for async init and re-exports
- Test files: `tests/` directory for integration tests, `#[cfg(test)] mod tests` for unit tests

## NEVER DO THIS

1. **Never forget to call `.free()` on wasm-bindgen objects in JS.** Objects returned by Rust are allocated on the wasm heap. The JS garbage collector does not free them. Store a reference and call `.free()` when done, or use wasm-bindgen's built-in destructor support.
2. **Never pass `String` across the boundary in hot loops.** Each `String` crossing the boundary allocates and copies UTF-8 ↔ UTF-16. For performance-critical code, pass `&[u8]` or numeric indices instead.
3. **Never enable all `web-sys` features.** `web-sys = { features = ["*"] }` adds hundreds of API bindings and massively inflates compile time and binary size. Enable only the specific APIs you use.
4. **Never use `println!` in wasm.** There is no stdout. Use `web_sys::console::log_1()` or the `console_log!` macro from `console_log` crate. `println!` silently does nothing or panics.
5. **Never block the main thread with heavy computation.** Long-running Rust functions block the JS event loop. For CPU-heavy work, run wasm in a Web Worker. Use `wasm-bindgen-rayon` for parallel computation.
6. **Never assume wasm has access to the filesystem or network.** There is no `std::fs`, no `std::net`. Use `web-sys`'s `fetch` API for network access and IndexedDB or the File API for storage.
7. **Never compile with debug symbols for production.** `wasm-pack build --release` strips debug info and runs `wasm-opt`. Debug builds can be 10x larger. Always profile the `.wasm` file size.

## Testing

- Use `cargo test` for pure Rust core logic. No browser needed since `core/` has no wasm-bindgen dependency.
- Use `wasm-pack test --headless --chrome` for integration tests that exercise the wasm-bindgen boundary and web-sys calls.
- Test JS-side integration by importing the wasm module in a test harness (Vitest or Jest) and calling exported functions.
- Benchmark with `console.time()` / `console.timeEnd()` on the JS side. Compare wasm performance against a pure JS implementation to validate the wasm approach.
- Check binary size after every change: `wasm-pack build --release && ls -la pkg/*.wasm`. Regressions above the target size in KB should be investigated.

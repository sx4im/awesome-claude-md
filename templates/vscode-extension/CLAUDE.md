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

## Production Delivery Playbook (Category: CLI & Tools)

### Release Discipline
- Commands must be predictable, script-safe, and non-interactive when required.
- Preserve backward compatibility for flags/output unless explicitly versioned.
- Fail fast with actionable errors and stable exit codes.

### Merge/Release Gates
- Golden tests pass for command output and exit codes.
- Help text/examples match implemented behavior.
- Dry-run mode validated for destructive operations.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- VS Code Extension API (vscode module)
- TypeScript (strict mode)
- esbuild for bundling (not webpack)
- Webview API for custom UI panels
- Language Server Protocol (LSP) via `vscode-languageserver` (if applicable)
- `@vscode/test-electron` for integration testing
- `vsce` for packaging and publishing

## Project Structure

```
src/
├── extension.ts               # activate() and deactivate() entry points
├── commands/                  # Command implementations (one file per command)
│   ├── formatDocument.ts
│   ├── generateSnippet.ts
│   └── openPreview.ts
├── providers/                 # VS Code API providers
│   ├── completionProvider.ts  # IntelliSense completions
│   ├── hoverProvider.ts       # Hover information
│   ├── codeActionProvider.ts  # Quick fixes and refactoring
│   └── treeDataProvider.ts    # Sidebar tree view
├── webview/                   # Webview panel code
│   ├── panels/                # Panel class implementations
│   │   └── PreviewPanel.ts    # Webview lifecycle management
│   └── ui/                    # Frontend HTML/CSS/JS for webviews
│       ├── main.ts            # Webview client script
│       └── styles.css
├── language-server/           # LSP server (runs in separate process)
│   ├── server.ts              # Language server entry point
│   └── analysis.ts            # Document analysis logic
├── config/                    # Extension configuration helpers
│   └── settings.ts            # Typed access to workspace settings
├── utils/
│   ├── disposables.ts         # Disposable management helpers
│   └── telemetry.ts           # Telemetry event tracking
└── test/
    ├── suite/                 # Integration tests
    │   └── extension.test.ts
    └── runTest.ts             # Test runner bootstrap
package.json                   # Extension manifest: contributes, activationEvents
```

## Architecture Rules

- **`activate()` is the entry point, keep it thin.** Register commands, providers, and event listeners. Never put logic in `activate()` beyond registration. Each registration delegates to a function in `commands/` or `providers/`.
- **Everything is a Disposable.** Every command registration, event listener, file watcher, and webview panel returns a `Disposable`. Push all disposables into `context.subscriptions` so they're cleaned up on deactivation. Leaked disposables cause memory leaks and zombie listeners.
- **Webview panels are isolated.** Webview content runs in a sandboxed iframe. Communication with the extension is via `postMessage` / `onDidReceiveMessage`. Never try to access the VS Code API from webview code -- it doesn't exist there. Always validate messages received from webviews.
- **Language Server runs in a separate process.** If you need document analysis, diagnostics, or completions for a custom language, use `vscode-languageserver` and `vscode-languageclient`. The server runs in its own Node process. Never do heavy computation in the extension host process -- it blocks the entire editor.
- **Configuration is reactive.** Read settings with `vscode.workspace.getConfiguration('{extension-name}')`. Listen for changes with `vscode.workspace.onDidChangeConfiguration`. Never cache configuration without a change listener -- users expect settings to take effect immediately.

## Coding Conventions

- Commands are registered in `package.json` under `contributes.commands` with a `command` ID: `{extension-name}.formatDocument`. The same ID is used in `vscode.commands.registerCommand()` in `extension.ts`.
- Activation events in `package.json`: use the narrowest trigger. `onLanguage:python` is better than `*`. `onCommand:` is better than `onStartupFinished`. Never use `*` unless the extension truly needs to run on every workspace.
- Use `vscode.window.showInformationMessage()` for success, `showWarningMessage()` for warnings, `showErrorMessage()` for errors. Never use `console.log()` for user-facing messages -- users don't see the debug console.
- Output channel for logs: `const log = vscode.window.createOutputChannel('{extension-name}')`. Use `log.appendLine()` for debug info visible in the Output panel. This is where diagnostic logs go.
- Status bar items: create with `vscode.window.createStatusBarItem()`, set `text`, `tooltip`, and `command`. Always dispose them. Don't create multiple status bar items that show the same information.

## Library Preferences

- **Bundler:** esbuild. Not webpack (slower, more complex config). The `@vscode/vsce` tool works with esbuild output. Configure in `esbuild.config.mjs` with `external: ['vscode']`.
- **Testing:** `@vscode/test-electron` for integration tests that need the full VS Code API. Mocha as the test framework (VS Code convention). Not Jest -- it conflicts with the VS Code test runner.
- **Webview UI:** `@vscode/webview-ui-toolkit` for VS Code-styled components (buttons, text fields, data grids). Not custom CSS that won't match the user's theme.
- **LSP:** `vscode-languageserver` + `vscode-languageclient`. Not a custom protocol -- LSP is the standard and enables compatibility with other editors.
- **Packaging:** `@vscode/vsce` for `.vsix` packaging and Marketplace publishing. Not manual zip files.

## File Naming

- Commands: `camelCase.ts` -> `formatDocument.ts`, `openPreview.ts`
- Providers: `camelCase.ts` -> `completionProvider.ts`, `hoverProvider.ts`
- Webview panels: `PascalCase.ts` -> `PreviewPanel.ts`, `SettingsPanel.ts`
- Tests: `kebab-case.test.ts` -> `extension.test.ts`, `commands.test.ts`
- Config: `package.json` is the extension manifest (not `extension.json`)

## NEVER DO THIS

1. **Never do synchronous I/O in the extension host.** `fs.readFileSync()`, `child_process.execSync()`, and synchronous network calls block the entire VS Code UI. Use `vscode.workspace.fs` (async) or `fs.promises`. Every blocking call freezes the editor for all users.
2. **Never use `*` activation event in production.** It loads your extension on every VS Code startup regardless of context. Use `onLanguage:`, `onCommand:`, `workspaceContains:`, or `onView:` to activate only when relevant.
3. **Never access `vscode` module from webview code.** Webviews are sandboxed. They communicate with the extension via `acquireVsCodeApi().postMessage()`. If you need VS Code data in the webview, send it as a message from the extension side.
4. **Never forget to dispose resources.** File watchers, event listeners, terminals, webview panels -- everything that implements `Disposable` must be pushed to `context.subscriptions` or manually disposed. Resource leaks cause the extension host to consume increasing memory.
5. **Never hardcode file system paths.** Use `vscode.Uri` and `vscode.workspace.fs` for file operations. The workspace might be remote (SSH, WSL, Codespaces). Hardcoded paths break on non-local filesystems.
6. **Never store secrets in settings.** Use `context.secrets` (SecretStorage API) for tokens and credentials. Settings are stored in plain JSON files visible to any process. Secrets use the OS keychain.
7. **Never bundle `node_modules` without tree-shaking.** Use esbuild to bundle only imported code. A full `node_modules` copy bloats the `.vsix` and slows install. Set `external: ['vscode']` since the `vscode` module is provided by the host.

## Testing

- Integration tests run in a real VS Code instance via `@vscode/test-electron`. The test runner launches VS Code, loads the extension, and executes Mocha tests with full API access.
- Test commands by executing them: `await vscode.commands.executeCommand('{extension-name}.formatDocument')` and asserting on the editor state.
- Test providers by triggering them: call `vscode.commands.executeCommand('vscode.executeCompletionItemProvider', uri, position)` and assert on the returned items.
- Test webview panels by verifying they create and dispose correctly. Message passing can be tested by mocking the webview's `postMessage` and `onDidReceiveMessage`.
- Run `vsce package` in CI to verify the extension packages without errors. A packaging failure means a missing file or bad dependency.
- Test with both the minimum VS Code version (declared in `engines.vscode`) and the latest version to catch compatibility issues.

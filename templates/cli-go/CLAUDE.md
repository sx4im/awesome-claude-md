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

- Go 1.22+
- Cobra for command/subcommand structure
- Viper for configuration (files, env vars, flags)
- Bubble Tea for interactive TUI (if applicable)
- Lip Gloss for terminal styling
- GoReleaser for cross-platform builds and distribution
- `testify` for test assertions

## Project Structure

```
cmd/
├── root.go                    # Root command: app name, global flags, PersistentPreRun
├── init.go                    # `<your-tool> init` subcommand
├── run.go                     # `<your-tool> run` subcommand
└── config.go                  # `<your-tool> config get/set` subcommand group
internal/
├── core/                      # Business logic (no Cobra/Viper imports)
│   ├── engine.go
│   └── validator.go
├── config/                    # Config loading, defaults, schema
│   └── config.go
├── tui/                       # Bubble Tea models and views
│   ├── model.go               # Main tea.Model implementation
│   ├── update.go              # Message handling (Update function)
│   └── view.go                # Rendering (View function)
├── output/                    # Formatters: table, JSON, plain text
│   ├── table.go
│   └── json.go
└── errors/                    # Typed error definitions
    └── errors.go
main.go                        # Entry point: calls cmd.Execute()
.goreleaser.yaml               # GoReleaser config
```

## Architecture Rules

- **`cmd/` is the CLI boundary.** Files in `cmd/` define Cobra commands, bind flags to Viper, and call functions in `internal/`. No business logic in `cmd/`. A `RunE` function should be 10-15 lines: parse flags, call core, format output, handle errors.
- **`internal/` is framework-agnostic.** Code in `internal/core/` never imports `cobra` or `viper`. It receives typed Go values (structs, strings, ints) and returns results or errors. This makes core logic testable without simulating CLI invocations.
- **Viper binds config sources in order:** defaults (code) -> config file (`~/.config/<your-tool>/config.yaml`) -> environment variables (`<tool-prefix>_*`) -> CLI flags. Bind flags to Viper in `init()` functions: `viper.BindPFlag("output", cmd.Flags().Lookup("output"))`.
- **Bubble Tea models are self-contained.** A TUI model implements `Init()`, `Update()`, and `View()`. It receives messages and returns commands. Never call `fmt.Println` inside a Bubble Tea program -- all output goes through the `View()` method. Cobra launches the TUI; the TUI does not call Cobra.
- **Errors flow up, formatting happens at the top.** Functions in `internal/` return `error`. The `RunE` function in `cmd/` decides how to display it (stderr message, exit code, JSON error object). Never call `os.Exit()` or `log.Fatal()` inside `internal/`.

## Coding Conventions

- Use `RunE` (returns `error`) on all Cobra commands. Not `Run` (no error return). `RunE` lets Cobra handle error formatting and exit codes consistently.
- Global flags go on the root command with `PersistentFlags()`: `--config`, `--output`, `--verbose`. Subcommand-specific flags use `Flags()`.
- Output format flag: `--output json|table|plain`. Default to `table` for humans, `json` for piped output (detect with `isatty`). Implement each format in `internal/output/`.
- Error messages start lowercase, no trailing period: `return fmt.Errorf("failed to read config: %w", err)`. Wrap errors with `%w` for `errors.Is()` and `errors.As()` support.
- Context propagation: pass `context.Context` from Cobra's `cmd.Context()` through to all core functions. This enables graceful cancellation with Ctrl+C.

## Library Preferences

- **CLI framework:** Cobra. Not `urfave/cli` (less ecosystem support, weaker subcommand model). Cobra is the standard for Go CLIs (kubectl, gh, docker all use it).
- **Config:** Viper. It integrates directly with Cobra's flag binding. Not `koanf` unless you need lighter weight.
- **TUI:** Bubble Tea + Lip Gloss + Bubbles (pre-built components). Not `tview` (immediate mode, harder to test). The Elm architecture of Bubble Tea makes TUIs testable.
- **Tables:** `lipgloss/table` or `tablewriter`. Not `tabwriter` (stdlib, too low-level for colored output).
- **Testing:** `testify/assert` and `testify/require`. Not raw `if got != want` blocks -- testify produces readable diffs on failure.
- **Builds:** GoReleaser. Not manual `go build` scripts. GoReleaser handles cross-compilation, checksums, archives, Homebrew taps, and GitHub releases.

## File Naming

- Commands: `snake_case.go` in `cmd/` -> `root.go`, `init.go`, `config.go`
- Internal packages: `snake_case.go` -> `engine.go`, `config.go`, `model.go`
- Test files: `snake_case_test.go` co-located -> `engine_test.go`, `config_test.go`
- TUI components: `model.go`, `update.go`, `view.go` in `internal/tui/`

## NEVER DO THIS

1. **Never call `os.Exit()` outside of `main.go`.** Use `RunE` to return errors. `os.Exit()` in a library function prevents deferred cleanup, breaks test coverage, and is impossible to test.
2. **Never use `log.Fatal()` in library code.** It calls `os.Exit(1)`. Return an error instead. `log.Fatal` is only acceptable in `main.go` as a last resort.
3. **Never use `init()` for business logic.** `init()` runs at import time, before `main()`. Use it only for Cobra flag registration and Viper bindings. Never open files, make HTTP calls, or allocate resources in `init()`.
4. **Never import `cmd/` from `internal/`.** Dependencies flow one way: `main.go` -> `cmd/` -> `internal/`. If `internal/` needs CLI context, pass it as function arguments. Circular imports don't compile in Go anyway, but the design intent matters.
5. **Never ignore errors.** Go has no exceptions. An unchecked error is a silent bug. If you genuinely don't care about an error (rare), assign it to `_` and add a comment explaining why.
6. **Never use `fmt.Println` in a Bubble Tea program.** All terminal output in a TUI goes through the `View()` return string. Direct prints corrupt the terminal state and produce garbled output.
7. **Never hardcode version strings.** Set the version at build time with `-ldflags`: `go build -ldflags "-X main.version=$(git describe --tags)"`. GoReleaser does this automatically.

## Testing

- Test core logic in `internal/` with standard Go tests. Pass typed inputs, assert outputs. No Cobra or Viper imports needed.
- Test Cobra commands by executing the root command with args: `rootCmd.SetArgs([]string{"run", "--input", "file.txt"})` and capturing stdout/stderr with `bytes.Buffer`.
- Test Bubble Tea models with `teatest`: send messages to `Update()`, assert on the returned model state and `View()` output. No terminal needed.
- Test config loading by writing temporary config files with `os.CreateTemp` and pointing Viper to them. Verify precedence: flag > env > file > default.
- Use `testify/assert` for value comparisons: `assert.Equal(t, expected, got)`. Use `testify/require` when a failure should stop the test immediately (setup steps).
- Run `go vet ./...` and `golangci-lint run` in CI. Fix all warnings before merging.

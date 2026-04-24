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

- Node.js 20+ with TypeScript 5.x (strict mode)
- Commander.js for command parsing
- Chalk for colored output
- Ora for spinners and progress
- Inquirer for interactive prompts
- tsup for building a single executable
- Published to npm as a global CLI

## Project Structure

```
src/
├── commands/
│   ├── init.ts              # `mycli init` command
│   ├── generate.ts          # `mycli generate` command
│   └── config.ts            # `mycli config` command
├── lib/
│   ├── config.ts            # Config file loading (~/.mycli/config.json)
│   ├── logger.ts            # Chalk-based logging (info, warn, error, success)
│   ├── fs.ts                # File system helpers (read, write, template)
│   └── prompts.ts           # Inquirer prompt compositions
├── templates/               # Template files for scaffolding (if applicable)
├── utils/
│   ├── validate.ts          # Input validation functions
│   └── format.ts            # Output formatting helpers
├── types/
│   └── index.ts             # Shared types and interfaces
└── index.ts                 # CLI entry point: Commander program setup
```

## Architecture Rules

- **One file per command.** `commands/init.ts` exports a function that registers the `init` command on the Commander program. Each command file is self-contained: options, arguments, and handler logic.
- **Commands call `lib/`. never the other way around.** Commands are the entry points that parse user input and orchestrate library functions. Library code (`lib/`) is reusable and never touches Commander directly.
- **All output goes through `lib/logger.ts`.** Never use `console.log` directly. The logger wraps Chalk for consistent coloring: `logger.info()`, `logger.success()`, `logger.warn()`, `logger.error()`. This makes output testable and redirect-friendly.
- **Config lives in `~/.mycli/`.** Use a JSON config file loaded via `lib/config.ts`. Provide sensible defaults. the CLI must work without any config file present.
- **Exit codes are meaningful.** `0` = success. `1` = user error (bad input, missing file). `2` = system error (network, permissions). Never call `process.exit()` inside library code. throw typed errors and handle exits in the command layer.

## Coding Conventions

- **The `bin` field in `package.json` points to the compiled output:** `"bin": { "mycli": "./dist/index.js" }`. The entry file starts with `#!/usr/bin/env node`.
- **Named exports for everything.** `export function registerInitCommand(program: Command)`. never `export default`.
- **Error messages are actionable.** Bad: `"Error: invalid input"`. Good: `"Error: config file not found at ~/.mycli/config.json. Run 'mycli init' to create one."`.
- **Non-interactive mode for CI.** All prompts have flag-based alternatives: `mycli init --name myproject --template react` should work without any prompts. Check `process.stdout.isTTY` to detect CI environments.
- **Verbose flag.** Support `--verbose` globally. In verbose mode, log every file operation, every network request, and every config read. In normal mode, show only the final result.

## Library Preferences

- **Command parsing:** Commander. not `yargs` (Commander has a simpler API and better TypeScript support). Not `meow` (too minimal for multi-command CLIs).
- **Output coloring:** Chalk 5+ (ESM). not `colors` (supply-chain compromised) and not `kleur` (Chalk is the standard).
- **Spinners:** Ora. not `cli-spinners` directly (Ora handles the terminal output management). Use spinners for any operation that takes more than 500ms.
- **Prompts:** Inquirer. not `prompts` (Inquirer has better TypeScript types). Use `@inquirer/prompts` (the newer modular API), not the legacy `inquirer` package.
- **Bundling:** tsup. compiles to a single CJS file for maximum compatibility with `node` runtimes. Set `target: 'node20'`.

## File Naming

- Commands: `camelCase.ts` → `init.ts`, `generate.ts`, `config.ts`
- Library modules: `camelCase.ts` → `config.ts`, `logger.ts`, `prompts.ts`
- Utils: `camelCase.ts` → `validate.ts`, `format.ts`
- Templates: descriptive names → `react-component.hbs`, `config.template.json`
- Tests: co-located → `init.test.ts`, `logger.test.ts`

## NEVER DO THIS

1. **Never use `console.log` for user-facing output.** All output goes through `lib/logger.ts`. This ensures consistent formatting, respects `--quiet` flags, and makes output testable.
2. **Never call `process.exit()` inside library code.** Throw typed errors. Command handlers catch them and call `process.exit()` with the appropriate code. Library functions that call `process.exit()` are untestable.
3. **Never assume interactive mode.** Check `process.stdout.isTTY` before showing prompts or spinners. In CI environments, use flag-based arguments and plain text output.
4. **Never hardcode file paths.** Use `os.homedir()` for `~`, `path.resolve()` for relative paths, and `process.cwd()` for the working directory. Hardcoded paths break across platforms.
5. **Never ship without a `--help` for every command.** Commander generates help automatically, but add `.description()` and `.example()` for every command and option. Users should never have to read source code to use the CLI.
6. **Never buffer unbounded output in memory.** If processing large files or many items, use Node.js streams. A CLI that OOMs on a large input is broken.
7. **Never ignore `SIGINT` and `SIGTERM`.** Clean up temp files, close connections, and exit gracefully. Users expect Ctrl+C to work. Register handlers in the entry file.

## Testing

- Use Vitest. Test commands by invoking their handler functions directly with mock arguments.
- Test library modules as pure functions. `parseConfig(input)` and assert the output.
- Test CLI output by capturing logger calls (mock `lib/logger.ts`).
- Integration test: run the compiled binary with `execa` and assert stdout, stderr, and exit code.
- Test both interactive (mocked Inquirer) and non-interactive (flag-based) flows.

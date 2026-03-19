# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Rust (latest stable, 2024 edition)
- clap v4 for argument parsing (derive API)
- tokio for async operations (if needed)
- serde + serde_json for serialization
- anyhow for error handling
- indicatif for progress bars
- crossterm for terminal manipulation

## Project Structure

```
src/
├── main.rs                  # Entry point: parse args, dispatch commands
├── cli.rs                   # clap derive structs (Args, Subcommands)
├── commands/
│   ├── mod.rs               # Command dispatch
│   ├── init.rs              # `mycli init` handler
│   ├── build.rs             # `mycli build` handler
│   └── config.rs            # `mycli config` handler
├── config/
│   ├── mod.rs
│   └── loader.rs            # Config file discovery and parsing
├── core/                    # Core business logic (framework-independent)
│   ├── mod.rs
│   └── processor.rs
├── output/
│   ├── mod.rs
│   ├── logger.rs            # Colored, leveled output
│   └── progress.rs          # Progress bars and spinners
├── error.rs                 # Custom error types with thiserror
└── lib.rs                   # Library crate root (for testing)
```

## Architecture Rules

- **`main.rs` is 10 lines.** Parse CLI args, call the command handler, handle the top-level Result. All logic lives in the library crate (`lib.rs`).
- **clap derive API for all argument parsing.** Define `#[derive(Parser)]` structs in `cli.rs`. Subcommands, flags, and arguments are all type-safe structs. Never parse `std::env::args()` manually.
- **Separate the library from the binary.** Business logic lives in `lib.rs` and its modules. `main.rs` is the binary entry that calls library functions. This makes the core logic testable without spawning a process.
- **Exit codes are explicit.** Define exit codes as constants: `EXIT_SUCCESS = 0`, `EXIT_USER_ERROR = 1`, `EXIT_SYSTEM_ERROR = 2`. Return them from `main()` via `std::process::ExitCode`. Never call `std::process::exit()` inside library code.
- **Config file discovery follows XDG.** Check `$XDG_CONFIG_HOME/mycli/config.toml`, then `~/.config/mycli/config.toml`, then `./.mycli.toml` in the current directory. Use the `dirs` crate for platform-correct paths.

## Coding Conventions

- **Error handling:** use `thiserror` for library error types (typed, matchable). Use `anyhow` only in `main.rs` and command handlers (when you don't need to match on specific errors). Never use `.unwrap()` except in tests.
- **Output through the logger.** All user-facing output goes through `output/logger.rs`. Support `--quiet` (errors only), default (progress + results), and `--verbose` (debug info). Check `atty::is(Stream::Stdout)` for TTY-aware formatting.
- **Use `PathBuf` for all file paths.** Never use `String` for paths. Use `std::fs` with proper error context: `.with_context(|| format!("reading config at {}", path.display()))?`.
- **Structured data output.** Support `--format json` for machine-readable output. Default to human-readable. Use `serde::Serialize` on output types so the same struct can be printed as a table or JSON.
- **Color is opt-out.** Color is enabled by default on TTYs, disabled on pipes. Support `--no-color` and `NO_COLOR` env var. Use `owo-colors` or `colored` crate.

## Library Preferences

- **Arg parsing:** clap v4 derive API. not structopt (merged into clap), not argh (fewer features). Derive API gives compile-time validation and auto-generated `--help`.
- **Errors:** thiserror for library errors, anyhow for application errors. not `Box<dyn Error>` (loses type info), not `panic!` (not recoverable).
- **Serialization:** serde + toml for config files, serde_json for JSON output. Not hand-parsed strings.
- **Progress:** indicatif. not raw `\r` printing. Indicatif handles multi-line progress bars, spinners, and terminal width detection.
- **File system:** `std::fs` + `walkdir` for directory traversal. Not `glob` (walkdir is faster for large trees).

## NEVER DO THIS

1. **Never use `.unwrap()` in library code.** It panics on errors instead of returning them. Use `?` operator with proper error types. `.unwrap()` is acceptable only in tests.
2. **Never use `println!` for user output.** Use the logger module which respects `--quiet`, `--verbose`, and `--no-color` flags. `println!` can't be controlled or tested.
3. **Never use `String` for file paths.** Paths are not guaranteed to be valid UTF-8. Use `PathBuf` and `Path` everywhere. Use `.display()` when you need to print a path.
4. **Never call `std::process::exit()` in library code.** Return errors and let `main()` decide the exit code. `process::exit()` skips destructors and can't be tested.
5. **Never hardcode colors without checking the terminal.** Piped output with ANSI color codes breaks downstream tools. Check `atty::is()` and respect `NO_COLOR` env var.
6. **Never read the entire file into memory without size checks.** Use `BufReader` for large files. A CLI that OOMs on a 2GB log file is broken.
7. **Never ignore `Ctrl+C`.** Install a `ctrlc` handler that cleans up temp files and exits gracefully. Default behavior terminates immediately, potentially leaving partial output.

## Testing

- Unit tests in `#[cfg(test)] mod tests` for core logic. Test pure functions with known inputs.
- Integration tests in `tests/` that invoke the CLI binary via `assert_cmd` crate. Assert stdout, stderr, and exit code.
- Use `tempfile` crate for tests that create files or directories. Never write to the real filesystem.
- Test both TTY and pipe output modes. Use `assert_cmd`'s `pipe_stdin` and capture stdout.

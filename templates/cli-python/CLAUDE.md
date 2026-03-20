# [PROJECT NAME] - Python CLI Application

## Tech Stack

- Python 3.11+
- Typer for CLI framework (built on Click)
- Rich for terminal output (tables, progress bars, panels)
- Pydantic v2 for configuration and data validation
- `pyproject.toml` for packaging and dependency management
- uv or pip for dependency installation
- pytest for testing

## Project Structure

```
[PACKAGE_NAME]/
├── __init__.py                # Package version: __version__ = "0.1.0"
├── __main__.py                # Entry point: `python -m [PACKAGE_NAME]`
├── cli.py                     # Typer app definition, top-level commands
├── commands/                  # Subcommand groups
│   ├── __init__.py
│   ├── init.py                # `[TOOL] init` command
│   ├── run.py                 # `[TOOL] run` command
│   └── config.py              # `[TOOL] config` command group
├── core/                      # Business logic (framework-agnostic)
│   ├── __init__.py
│   ├── engine.py              # Main processing logic
│   └── validator.py           # Input validation and checks
├── models/                    # Pydantic models for config and data
│   ├── __init__.py
│   └── config.py              # Config file schema
├── output/                    # Output formatting
│   ├── __init__.py
│   ├── console.py             # Rich console singleton
│   ├── tables.py              # Table renderers
│   └── progress.py            # Progress bar wrappers
└── utils/
    ├── __init__.py
    ├── fs.py                  # File system helpers
    └── errors.py              # Custom exception classes
tests/
├── conftest.py                # Shared fixtures
├── test_cli.py                # CLI invocation tests
└── test_core/                 # Business logic unit tests
pyproject.toml                 # Project metadata, dependencies, entry points
```

## Architecture Rules

- **CLI layer is thin.** Commands in `cli.py` and `commands/` parse arguments, call business logic in `core/`, and format output using `output/`. No business logic in command functions. If a command function is longer than 20 lines, the logic belongs in `core/`.
- **Rich console is a singleton.** Create one `Console()` instance in `output/console.py` and import it everywhere. Never instantiate `Console()` in multiple files -- it breaks stderr/stdout separation and test capture.
- **Exit codes are explicit.** Use `raise typer.Exit(code=1)` for errors. Map exit codes in a constant: `EXIT_OK = 0`, `EXIT_INPUT_ERROR = 1`, `EXIT_RUNTIME_ERROR = 2`. Never call `sys.exit()` directly -- Typer won't run cleanup callbacks.
- **Configuration is layered.** Default values in Pydantic model -> config file (`~/.config/[TOOL]/config.toml`) -> environment variables (`[TOOL_PREFIX]_*`) -> CLI flags. Later layers override earlier ones. Typer's `Option(envvar=...)` handles env vars.
- **All user-facing output goes through Rich.** Use `console.print()` for normal output, `console.print(..., style="red")` for errors, `rich.table.Table` for structured data. Never use bare `print()` -- it doesn't support colors, Unicode, or terminal width detection.

## Coding Conventions

- Type hints on all function signatures. Use `Annotated[str, typer.Argument(help="...")]` for CLI arguments. Not the old `typer.Argument(default=...)` positional style.
- Docstrings on every command function become the `--help` text. Write them as user-facing documentation, not developer notes. First line is the summary, rest is detail.
- Use `typer.Option` for flags with `--long-name` and `-s` short aliases. Boolean flags use `--flag / --no-flag` pattern: `verbose: Annotated[bool, typer.Option("--verbose / --no-verbose")] = False`.
- Errors directed to stderr: `console.print("[red]Error:[/red] File not found", stderr=True)`. Data output to stdout for piping. Use `rich.print` for stderr, raw `print` or `sys.stdout.write` for pipeable data.
- Use `pathlib.Path` for all file paths. Never use `os.path.join()`. Typer accepts `Path` as an argument type and validates existence.

## Library Preferences

- **CLI framework:** Typer. Not argparse (verbose, no type inference), not Click directly (Typer wraps Click with better ergonomics and type support).
- **Output:** Rich. Not colorama (low-level), not termcolor (no tables/progress). Rich handles tables, trees, progress bars, Markdown rendering, and syntax highlighting.
- **Config files:** tomllib (stdlib in 3.11+) for reading TOML. `tomli-w` for writing. Not YAML (security footguns with `yaml.load`), not JSON (no comments).
- **HTTP requests:** httpx. Not requests (no async support, no HTTP/2). httpx has an identical sync API: `httpx.get(url)`.
- **Packaging:** `pyproject.toml` with `[project.scripts]` entry point. Not `setup.py`. Use `uv` or `pip install -e .` for development.

## File Naming

- Modules: `snake_case.py` -> `cli.py`, `engine.py`, `config.py`
- Test files: `test_snake_case.py` -> `test_cli.py`, `test_engine.py`
- Package directory: `snake_case` matching the import name
- Config files: `pyproject.toml`, not `setup.py` or `setup.cfg`

## NEVER DO THIS

1. **Never use `click.echo()` in a Typer app.** Typer wraps Click, but you should use `rich.print()` or `typer.echo()`. Mixing Click and Typer output functions causes inconsistent formatting and breaks Rich's markup.
2. **Never use `sys.exit()` to handle errors.** Use `raise typer.Exit(code=1)` or `raise typer.Abort()`. `sys.exit()` bypasses Typer's error handling, skips cleanup callbacks, and breaks test runners.
3. **Never use bare `except Exception`.** Catch specific exceptions. CLI apps must provide useful error messages, not swallow errors silently. Log the traceback at debug level (`--verbose`) and show a clean message to the user.
4. **Never use `os.path` when `pathlib` exists.** `Path.home() / ".config" / TOOL_NAME / "config.toml"` is readable and cross-platform. `os.path.join(os.path.expanduser("~"), ".config", ...)` is not.
5. **Never put interactive prompts in library code.** `typer.confirm("Are you sure?")` belongs in the CLI command function, not in `core/`. Core logic must be callable without a terminal (in tests, scripts, or CI).
6. **Never print JSON with `json.dumps()` for machine output.** Use `rich.print_json()` for pretty terminal display. For piped output, write raw JSON to stdout and all human messages to stderr.
7. **Never skip the `--help` text.** Every command, argument, and option must have a `help=` string. Users will run `[TOOL] --help` before reading any documentation.

## Testing

- Test CLI commands with `typer.testing.CliRunner`: `result = runner.invoke(app, ["run", "--input", "file.txt"])`. Assert on `result.exit_code` and `result.output`.
- Test `core/` logic independently with pytest. These tests should not import Typer or Rich -- pure function inputs and outputs.
- Use `tmp_path` (pytest fixture) for tests that read/write files. Never write to the real filesystem.
- Use `monkeypatch.setenv()` for environment variable tests. Not `os.environ` assignment -- it leaks across tests.
- Snapshot test `--help` output to catch accidental changes to the CLI interface.
- Test piped output by capturing stdout separately from stderr. Machine-readable output (JSON, CSV) must be clean and parseable.

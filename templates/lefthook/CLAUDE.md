# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Lefthook (Git hooks manager)
- Fast (Go-based, parallel)
- Configurable
- Cross-platform
- Husky alternative

## Project Structure
```
lefthook.yml                    // Configuration
package.json
src/
```

## Architecture Rules

- **Fast hooks.** Go-based, runs commands in parallel.
- **Simple config.** YAML or JSON configuration.
- **Cross-platform.** Works on Windows, macOS, Linux.
- **Husky alternative.** Faster, simpler.

## Coding Conventions

- Config: `commit-msg: { commands: { lint: { run: 'commitlint --edit {1}' } } } pre-commit: { parallel: true, commands: { lint: { run: 'biome check --staged' }, typecheck: { run: 'tsc --noEmit' } } }`.
- Install: `lefthook install` (sets up Git hooks).
- Run: Commands run automatically on git hooks.
- Skip: `git commit -m "wip" --no-verify` (not recommended).

## NEVER DO THIS

1. **Never forget `lefthook install`.** Required to set up hooks.
2. **Never make hooks too slow.** Parallel helps, but keep commands fast.
3. **Never skip error handling in commands.** Non-zero exit fails commit.
4. **Never use `run:` with interactive tools.** Hooks run non-interactively.
5. **Never ignore the `parallel` option.** Speed up with parallel execution.
6. **Never commit with `--no-verify` habitually.** Bypasses important checks.
7. **Never forget to test hooks.** Make a test commit to verify.

## Testing

- Test with intentional lint error (should block commit).
- Test hook execution order.
- Test on Windows/macOS/Linux if team is mixed.
- Test hook execution time.
- Test with parallel command execution.

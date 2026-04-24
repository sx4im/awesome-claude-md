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

## Production Delivery Playbook (Category: Languages)

### Release Discipline
- Follow idiomatic language patterns and package ecosystem conventions.
- Prefer standard tooling for formatting, linting, and testing.
- Avoid introducing non-portable patterns without documented rationale.

### Merge/Release Gates
- Compiler/interpreter checks pass with strict settings where available.
- Core examples and sample usage remain executable.
- Dependency updates are pinned and reviewed for compatibility.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Language: Nim 2.x with ARC/ORC memory management
- Backend Framework: Jester 0.6 HTTP framework (built on httpbeast for async I/O)
- Frontend Framework: Karax for single-page applications compiled to JavaScript
- Build Tool: nimble for project management, nim compiler with --mm:orc flag
- Database: norm ORM for SQLite/PostgreSQL, or db_connector for raw queries
- Templating: Source code filters with nimja or htmlgen for server-rendered HTML
- Package Manager: nimble with .nimble file dependency declarations

## Project Structure

```
src/
  app.nim                   # Jester server entry, route definitions, middleware
  config.nim                # Configuration loading from environment and JSON
  routes/
    user_routes.nim          # /users endpoint handlers
    auth_routes.nim          # /auth login/register/logout handlers
    api_routes.nim           # REST API route group
  models/
    user.nim                 # User object type with norm annotations
    session.nim              # Session token type and validation procs
  services/
    user_service.nim         # User business logic, validation, hashing
    auth_service.nim         # JWT creation with nim-jwt, bcrypt password handling
  db/
    connection.nim           # Database pool setup, transaction helpers
    migrations.nim           # Schema migration runner
  middleware/
    auth_middleware.nim       # JWT verification, request context injection
    logging_middleware.nim    # Structured request/response logging
  frontend/
    app.nim                  # Karax main entry, buildHtml DSL
    components/
      navbar.nim             # Navigation component with routing
      user_list.nim          # User listing with virtual DOM diffing
    api_client.nim           # Ajax calls via Karax's kxi module
  utils/
    response.nim             # JSON response builders, error formatters
    validation.nim           # Input validation proc chains
app.nimble                   # Package manifest with dependencies and tasks
config.json                  # Default runtime configuration
```

## Architecture Rules

- Route handlers are thin: parse request parameters, call service procs, return JSON responses.
- Service procs contain all business logic and return Result types or raise specific exceptions via `CatchableError` subtypes.
- All database access goes through procs in `db/` and `models/` modules. Route handlers never import db_connector directly.
- Karax frontend follows the single-state model: one `State` object rendered by a top-level `createDom` proc.
- Use Nim's effect system: annotate procs with `{.raises: [].}` or `{.raises: [DbError, IoError].}` to document and enforce error handling.
- Separate compile targets: backend compiles to C with `nim c`, frontend compiles to JS with `nim js`.

## Coding Conventions

- Proc names: camelCase. Type names: PascalCase. Module names: snake_case. Constants: camelCase.
- Use `object` types with explicit fields; avoid tuples for domain data.
- Prefer `Option[T]` from std/options over nil checks. Use `result` type from std/results for error handling.
- Pragmas on public API procs: `{.gcsafe.}` for async code, `{.raises: [SpecificError].}` for documented failures.
- Use `func` instead of `proc` for procs with no side effects to enable compiler optimizations.
- String formatting: use `std/strformat` with `fmt` macro, e.g., `fmt"{user.name} ({user.email})"`.

## Library Preferences

- HTTP server: Jester on httpbeast for production async performance
- JSON: std/json for serialization, jsony for high-performance parsing
- Database ORM: norm for typed database access with SQLite and PostgreSQL
- JWT: nim-jwt for token creation and verification
- Password hashing: nimcrypto for bcrypt, or bcrypt nimble package
- Logging: chronicles for structured logging with topics and severity levels
- Testing: std/unittest with suite/test blocks, testament for advanced test runner
- WebSocket: ws nimble package for real-time communication

## File Naming

- Source files: snake_case matching module content: `user_service.nim`, `auth_routes.nim`.
- One module per file. Modules group related types and procs.
- Frontend components: one file per component in `src/frontend/components/`.
- Test files: `tests/test_<module>.nim` with `t` prefix for test directory convention.

## NEVER DO THIS

1. Never use raw `ptr` or `pointer` types for application data; use `ref object` for heap allocation with ARC/ORC tracking.
2. Never use `{.gcsafe.}` cast to silence thread safety warnings without verifying there is no shared mutable state.
3. Never use `cast` between unrelated types; use explicit conversion procs with validation.
4. Never import `db_connector` or `norm` in route handler files; all DB access goes through service or db module procs.
5. Never use global `var` for request-scoped state; pass context through proc parameters or Jester's request object.
6. Never compile the frontend with `nim c`; always use `nim js` for Karax code targeting the browser.
7. Never use `os.sleep` in async code; use `sleepAsync` from std/asyncdispatch.

## Testing

- Run tests: `nimble test` which discovers and runs all `tests/test_*.nim` files.
- Use `std/unittest` with `suite` and `test` blocks: `check(result == expected)`, `expect(ExceptionType)`.
- Test Jester handlers by importing route procs directly and constructing mock Request objects.
- Database tests use an in-memory SQLite database initialized fresh per test suite.
- Frontend tests: compile Karax components with `nim js` and test with a headless browser or Node.js runtime.
- Run static analysis: `nim check src/app.nim` for type checking without compilation.
- CI pipeline: `nimble install --depsOnly && nimble test && nim c -d:release src/app.nim`.

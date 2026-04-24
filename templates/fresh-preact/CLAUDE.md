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

## Production Delivery Playbook (Category: Frontend)

### Release Discipline
- Enforce performance budgets (bundle size, LCP, CLS) before merge.
- Preserve accessibility baselines (semantic HTML, keyboard nav, ARIA correctness).
- Block hydration/runtime errors with production build verification.

### Merge/Release Gates
- Typecheck + lint + unit tests + production build pass.
- Critical route smoke tests for navigation, auth, and error boundaries.
- No new console errors/warnings in key user flows.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Deno Fresh 2.x with Preact 10 for islands architecture
- Deno runtime 2.x (not Node.js) with built-in TypeScript
- Preact Signals for reactive state in island components
- Tailwind CSS via Fresh's built-in Tailwind plugin
- Fresh's file-based routing with layouts and route groups
- Deno KV for key-value data persistence
- Oak-compatible middleware for request processing
- JSX with Preact's `h` pragma (automatic JSX transform)

## Project Structure

```
routes/
  _app.tsx              # Root app wrapper (HTML shell)
  _layout.tsx           # Default layout with nav/footer
  _middleware.ts        # Global middleware (auth, logging)
  index.tsx             # Home page (/)
  about.tsx             # Static page (/about)
  api/
    users.ts            # API route: GET/POST /api/users
    users/[id].ts       # API route: /api/users/:id
  dashboard/
    _layout.tsx         # Dashboard-specific layout
    _middleware.ts       # Auth guard middleware
    index.tsx           # Dashboard page
    settings.tsx        # Settings page
islands/
  Counter.tsx           # Interactive island component
  SearchBar.tsx         # Client-side search with signals
  ThemeToggle.tsx       # Theme switching island
  DataTable.tsx         # Interactive data table
components/
  Header.tsx            # Static server-rendered component
  Footer.tsx            # Static server-rendered component
  Card.tsx              # Static presentational component
lib/
  db.ts                 # Deno KV database helpers
  auth.ts               # Authentication utilities
  validators.ts         # Zod-like validation schemas
static/
  logo.svg              # Static assets served directly
  favicon.ico
fresh.config.ts         # Fresh configuration
deno.json               # Deno configuration and import map
```

## Architecture Rules

- Components in `components/` are static, server-rendered, and ship zero JavaScript to the client. They are the default.
- Components in `islands/` are hydrated on the client and are the only place client-side interactivity exists. Minimize island count.
- Each island is independently hydrated. Islands cannot import other islands. Shared logic goes in `lib/` as plain functions.
- Route handlers define `GET`, `POST`, `PUT`, `DELETE` as named exports. The `handler` object pattern groups multiple methods.
- Data loading happens in route handler functions. Pass data to page components as props. Never fetch data inside islands.
- Deno KV is accessed through helper functions in `lib/db.ts` that abstract key schema and serialization.
- Middleware files (`_middleware.ts`) run before route handlers. Use them for auth checks, CORS headers, and request logging.
- All imports use Deno-style URLs or import maps defined in `deno.json`. No `node_modules` directory.

## Coding Conventions

- Server components use function syntax: `export default function PageName(props: PageProps) {}`.
- Island components use Preact Signals for state: `const count = signal(0)`. Never use `useState` from Preact hooks.
- Route handlers return `Response` objects directly or use `ctx.render()` for page rendering.
- Shared types are exported from `lib/types.ts` and imported by both routes and islands.
- Use `<Head>` component from Fresh to set page-specific `<title>` and meta tags.
- CSS uses Tailwind utility classes exclusively. No separate CSS files for individual components.
- API routes return `Response.json()` for JSON responses. Set appropriate status codes and headers.
- Form submissions from islands use `fetch()` to API routes. Non-interactive forms use standard HTML form actions.

## Library Preferences

- State management: @preact/signals (never Preact hooks useState/useReducer in islands)
- Validation: Zod (imported via npm: specifier in deno.json)
- Database: Deno KV for simple persistence, connect to PostgreSQL via deno-postgres for relational data
- Auth: Custom session management with Deno KV session storage
- Markdown: deno-gfm for rendering Markdown content in static pages
- Testing: Deno.test with built-in assertion library
- HTTP client: built-in Deno fetch API (never axios or node-fetch)

## File Naming

- Routes: `kebab-case.tsx` in `routes/` (maps directly to URL paths)
- Islands: `PascalCase.tsx` in `islands/` (one component per file)
- Static components: `PascalCase.tsx` in `components/`
- Library modules: `camelCase.ts` in `lib/`
- API routes: `kebab-case.ts` in `routes/api/`
- Middleware: `_middleware.ts` (underscore prefix, Fresh convention)
- Layouts: `_layout.tsx` (underscore prefix, Fresh convention)

## NEVER DO THIS

1. Never put interactive logic in `components/` directory. Only `islands/` components are hydrated on the client.
2. Never use `useState` or `useEffect` from Preact hooks. Use Preact Signals (`signal`, `computed`, `effect`) for all island state.
3. Never import Node.js built-in modules directly. Use Deno's standard library or `node:` prefixed compatibility imports.
4. Never create islands for components that do not need client-side interactivity. Prefer static server-rendered components.
5. Never use `npm install` or create a `package.json`. Dependencies are managed through `deno.json` import map.
6. Never share state between islands via global variables. Each island hydrates independently. Use server-side state or URL params.

## Testing

- Unit tests: `Deno.test()` with `assertEquals`, `assertThrows` from Deno standard library.
- Run tests with `deno test --allow-env --allow-read --allow-net`.
- Route handler tests create mock `Request` objects and assert on `Response` status and body.
- Island component tests use @testing-library/preact imported via npm: specifier.
- Integration tests for Deno KV operations use an in-memory KV store opened with `Deno.openKv(":memory:")`.
- Fresh provides `createHandler` test utility to test full request/response cycles with middleware.
- Static component tests verify HTML output by rendering to string with `preact-render-to-string`.
- CI runs `deno lint`, `deno fmt --check`, and `deno test` in the Deno runtime (not Node).

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

## Production Delivery Playbook (Category: Backend)

### Release Discipline
- Fail closed on authz/authn checks and input validation.
- Use explicit timeouts/retries/circuit-breaking for external dependencies.
- Preserve API compatibility unless breaking change is approved and documented.

### Merge/Release Gates
- Unit + integration tests and contract tests pass.
- Static checks pass and critical endpoint latency regressions reviewed.
- Structured error handling verified for all modified endpoints.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- TypeScript 5.4+ with strict mode
- OpenAPI 3.1 specification as the single source of truth
- openapi-typescript for generating TypeScript types from OpenAPI schemas
- openapi-fetch for type-safe HTTP client generation (pairs with openapi-typescript)
- Redocly CLI for OpenAPI linting, bundling, and documentation
- orval as an alternative generator for React Query hooks and Zod schemas
- Node.js 20 LTS for build tooling and scripts

## Project Structure

```
specs/
  openapi.yaml            # Root OpenAPI 3.1 spec (or split into multiple files)
  paths/
    users.yaml             # Path definitions split by domain
    orders.yaml
    products.yaml
  components/
    schemas/               # Reusable schema definitions
      User.yaml
      Order.yaml
    parameters/            # Shared parameter definitions
    responses/             # Shared response definitions (Error, Paginated)
generated/
  types.ts                 # Output from openapi-typescript (auto-generated, do not edit)
  client.ts                # Typed fetch client instance
  react-query/             # Generated React Query hooks (if using orval)
  zod/                     # Generated Zod schemas (if using orval)
src/
  client/
    index.ts               # Configured client with base URL, auth interceptors
    middleware.ts           # Request/response middleware (auth token, error handling)
  server/
    validators.ts          # Runtime request validation using generated Zod schemas
    handlers/              # Route handlers typed against OpenAPI operations
scripts/
  generate.sh              # Runs all code generation steps in order
  validate.sh              # Lints and bundles the OpenAPI spec
  diff.sh                  # Shows breaking changes between spec versions
redocly.yaml               # Redocly linting configuration
orval.config.ts            # Orval code generation configuration
```

## Architecture Rules

- The OpenAPI spec is the contract; all types, clients, and validators are generated from it, never hand-written
- Run `openapi-typescript specs/openapi.yaml -o generated/types.ts` to produce TypeScript types
- Create the fetch client with `createClient<paths>()` from openapi-fetch, parameterized by generated `paths` type
- Split large specs into multiple YAML files using `$ref`; bundle with `redocly bundle specs/openapi.yaml -o bundled.yaml`
- Generated files in `generated/` are committed to git so consumers do not need generation tooling
- Server-side handlers use generated types for request/response typing; Zod schemas for runtime validation
- API versioning follows URL path prefix (`/v1/`, `/v2/`) defined in the OpenAPI spec `servers` field

## Coding Conventions

- Run code generation in a pre-commit hook or CI step; never let generated files drift from the spec
- Client middleware handles auth token injection, 401 retry, and response error parsing
- Use `GET` operation types as: `client.GET("/users/{id}", { params: { path: { id } } })`
- Response types are extracted with `type User = components["schemas"]["User"]` from generated types
- Discriminated unions for polymorphic schemas use `oneOf` with `discriminator` in the OpenAPI spec
- Pagination follows cursor-based pattern with `next_cursor` field in response schemas
- Error responses use RFC 7807 Problem Details format: `{ type, title, status, detail, instance }`

## Library Preferences

- openapi-typescript + openapi-fetch over swagger-codegen or openapi-generator (lighter, type-safe, no runtime)
- orval for React Query hook generation with built-in Zod validation schemas
- Redocly CLI over Swagger Editor for linting and documentation generation
- oasdiff for detecting breaking changes between spec versions in CI
- Stoplight Prism for mock server generation from the OpenAPI spec during frontend development
- zod-openapi for defining schemas in Zod-first approach and generating OpenAPI from code

## File Naming

- OpenAPI spec files: kebab-case `.yaml` (not `.yml`)
- Schema component files: PascalCase `.yaml` matching the schema name
- Generated files: camelCase `.ts` in `generated/` directory
- Client modules: camelCase `.ts` in `src/client/`
- Server handlers: kebab-case matching the API domain, e.g., `user-handlers.ts`

## NEVER DO THIS

1. Never hand-edit files in the `generated/` directory; they will be overwritten on next generation run
2. Never define TypeScript types that duplicate OpenAPI schemas; always import from generated types
3. Never use `any` type for API responses; the entire point is end-to-end type safety from spec to client
4. Never add `additionalProperties: true` to schemas without explicit need; it weakens type generation
5. Never skip running `redocly lint` before committing spec changes; catch structural errors early
6. Never use OpenAPI 2.0 (Swagger) format; always use OpenAPI 3.1 which aligns with JSON Schema 2020-12
7. Never inline complex schemas in path definitions; extract to `components/schemas/` for reuse and clarity

## Testing

- Validate the OpenAPI spec on every CI run: `redocly lint specs/openapi.yaml` with zero warnings policy
- Detect breaking changes in PRs: `oasdiff breaking specs/openapi.yaml specs/openapi-main.yaml`
- Run a Prism mock server in E2E tests to validate client code against the spec without a real backend
- Contract tests verify that the real API responses match generated Zod schemas at runtime
- Type-check generated client usage with `tsc --noEmit` to catch spec-client mismatches at build time
- Test generated React Query hooks with MSW (Mock Service Worker) for component-level testing
- Generate and serve Redocly documentation in CI to verify docs build: `redocly build-docs specs/openapi.yaml`
- Version the spec with git tags; maintain a changelog of API changes per version

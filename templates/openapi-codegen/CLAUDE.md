# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

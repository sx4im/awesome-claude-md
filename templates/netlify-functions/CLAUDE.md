# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Runtime: Netlify Functions (AWS Lambda under the hood, Node.js 20)
- Language: TypeScript 5.x (strict mode)
- Function Format: Netlify Functions v2 (streaming and background support)
- Database: Supabase PostgreSQL or PlanetScale MySQL via serverless drivers
- Cache: Netlify Blob Store for persistent KV storage
- Auth: Netlify Identity or custom JWT via jose library
- Build: Netlify CLI (`netlify dev`) for local development
- Package Manager: pnpm
- Testing: Vitest
- Frontend: optional static site in publish directory

## Project Structure

```
netlify/
  functions/
    api.mts             # Main REST API handler (single catch-all function)
    webhook.mts         # Incoming webhook processor
    scheduled.mts       # Scheduled (cron) function
    background.mts      # Background function for long-running tasks
  edge-functions/
    geolocation.ts      # Deno-based edge function for geo-routing
src/                    # Frontend source (if applicable)
lib/
  db.ts                 # Database client setup and query helpers
  auth.ts               # JWT verification and user extraction
  validation.ts         # Zod schemas for API request validation
  response.ts           # Typed response builder helpers
  types.ts              # Shared type definitions
netlify.toml            # Netlify configuration (build, functions, redirects)
package.json
tsconfig.json
```

## Architecture Rules

- Use Netlify Functions v2 format: `export default async (req: Request, context: Context) => { ... }`.
- The `api.mts` function uses a URL pattern matcher to route requests internally -- avoids one Lambda per endpoint.
- Configure function paths in `netlify.toml` under `[[redirects]]` to map clean URLs to functions.
- Background functions return 202 immediately and process asynchronously. Name the file `*.background.mts` or use `config.type = 'background'`.
- Scheduled functions export a `config` with `schedule` property using cron syntax.
- Netlify Blob Store is available via `@netlify/blobs` for persistent key-value storage across deploys.
- Functions have a 10-second timeout on free tier, 26 seconds on Pro. Background functions get 15 minutes.

## Coding Conventions

- Export function config alongside the handler: `export const config: Config = { path: '/api/*', method: ['GET', 'POST'] }`.
- Use the Web API `Request` and `Response` objects (not AWS Lambda event/callback style).
- Parse URL: `const url = new URL(req.url); const path = url.pathname;`.
- Read JSON body: `const body = await req.json()`.
- Return responses: `return new Response(JSON.stringify(data), { status: 200, headers: { 'Content-Type': 'application/json' } })`.
- Access environment variables via `Deno.env.get()` in edge functions, `process.env` in serverless functions.
- Use `context.geo` for geolocation data (country, city, timezone) in edge functions.

## Library Preferences

- HTTP routing inside functions: URL pattern matching or Hono as a micro-router
- Database: @neondatabase/serverless or @planetscale/database (serverless-compatible drivers)
- Blob storage: @netlify/blobs (official SDK)
- Validation: Zod
- JWT: jose (lightweight, Web Crypto based, works in both Node and edge)
- Email: Resend or SendGrid via fetch
- Logging: structured JSON to stdout (Netlify captures function logs)

## File Naming

- Function files: camelCase with `.mts` extension for ESM TypeScript (`api.mts`, `webhook.mts`)
- Background functions: append `.background` before extension or set in config
- Edge functions: in `netlify/edge-functions/` directory, `.ts` extension
- Shared lib files: camelCase in `lib/` directory (`db.ts`, `auth.ts`)
- Config: `netlify.toml` at project root

## NEVER DO THIS

1. Never use the legacy Netlify Functions v1 format (`exports.handler = async (event, context)`) -- use v2 Web API format.
2. Never install express or heavy frameworks in functions -- use native Request/Response or a micro-router like Hono.
3. Never use traditional database drivers (pg, mysql2) in serverless functions -- use serverless-compatible drivers (@neondatabase/serverless).
4. Never put secrets in `netlify.toml` -- use the Netlify UI or `netlify env:set` to manage environment variables.
5. Never exceed the 50MB function bundle size limit -- tree-shake dependencies and avoid large packages.
6. Never use `node_modules` imports in edge functions -- edge functions run on Deno and use URL or npm: imports.
7. Never assume function state persists between invocations -- each request may run on a fresh Lambda instance.

## Testing

- Use Vitest for unit and integration testing of function handlers.
- Test functions by calling them with constructed `Request` objects: `const res = await handler(new Request('http://localhost/api/items'), mockContext)`.
- Mock the Netlify `Context` object with geo, site, and account properties as needed.
- Use `netlify dev` for local end-to-end testing with environment variables loaded.
- Test edge functions separately using `netlify dev --edge-inspect` for Deno debugging.
- Mock database calls by injecting the client module with `vi.mock()`.
- Test scheduled functions by calling the handler directly (the schedule config is declarative).
- Run `netlify build` locally to verify the full build pipeline before deploying.
- Assert response status, headers (Content-Type, CORS), and parsed JSON body.

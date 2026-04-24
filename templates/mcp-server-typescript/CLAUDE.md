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

- TypeScript 5.4+ with strict mode and ESM modules
- @modelcontextprotocol/sdk v1.x for MCP server implementation
- Node.js 20 LTS as the runtime
- Zod for tool input schema validation and type inference
- stdio transport (default) and SSE transport for remote hosting
- tsup for bundling the server into a single executable
- vitest for unit and integration testing

## Project Structure

```
src/
  index.ts              # Server entry point, transport setup, capability registration
  server.ts             # McpServer instance creation and configuration
  tools/
    index.ts            # Tool registry, exports all tool definitions
    search.ts           # Example: search tool implementation
    create.ts           # Example: create/write tool implementation
    analyze.ts          # Example: analysis tool implementation
  resources/
    index.ts            # Resource registry
    templates.ts        # Resource template definitions with URI patterns
    static.ts           # Static resource definitions
  prompts/
    index.ts            # Prompt registry
    summarize.ts        # Prompt template definitions
  lib/
    errors.ts           # MCP error code constants and error factory functions
    validators.ts       # Zod schemas for tool inputs
    logger.ts           # stderr-based logging (stdout is reserved for MCP protocol)
    config.ts           # Environment-based configuration
  types/
    index.ts            # Shared TypeScript types and interfaces
scripts/
  build.sh              # Build and package for distribution
  inspect.sh            # Launch with MCP Inspector for debugging
tsconfig.json
package.json            # bin field points to dist/index.js, type: "module"
```

## Architecture Rules

- The server uses `@modelcontextprotocol/sdk`'s `McpServer` class with declarative tool/resource/prompt registration
- All logging goes to `stderr` via `console.error()`; `stdout` is exclusively for JSON-RPC MCP protocol messages
- Tools define input schemas using Zod; the SDK automatically converts Zod schemas to JSON Schema for the client
- Every tool handler returns `{ content: [{ type: "text", text: string }] }` or `{ content: [{ type: "image", data: base64, mimeType: string }] }`
- Tools that can fail must set `isError: true` in the response content, not throw exceptions
- Resources use URI templates like `file:///{path}` with RFC 6570 syntax for dynamic resources
- Resource subscriptions notify clients of changes via `server.notification({ method: "notifications/resources/updated" })`

## Coding Conventions

- Each tool is defined in its own file exporting a registration function: `export function registerSearchTool(server: McpServer)`
- Tool names use kebab-case: `search-documents`, `create-record`, `analyze-data`
- Tool descriptions are concise but specific; include expected input format and output format
- Zod schemas for tool inputs include `.describe()` on every field to help LLM clients understand parameters
- Use `z.object({ query: z.string().describe("Search query string"), limit: z.number().optional().default(10).describe("Max results") })`
- Error responses include actionable messages: what went wrong and what the client should try instead
- Server capabilities are declared explicitly: `capabilities: { tools: {}, resources: { subscribe: true }, prompts: {} }`

## Library Preferences

- @modelcontextprotocol/sdk over raw JSON-RPC implementation
- Zod over JSON Schema for input validation (SDK handles conversion)
- tsup over tsc for production builds (tree-shaking, single file output)
- vitest over Jest for testing (faster, native ESM support)
- @modelcontextprotocol/inspector for interactive debugging during development
- undici for HTTP requests within tool handlers (Node.js built-in)
- better-sqlite3 or drizzle-orm for tools that need local data persistence

## File Naming

- Tool files: kebab-case matching the tool name, e.g., `search-documents.ts`
- Resource files: kebab-case by resource domain, e.g., `project-files.ts`
- Prompt files: kebab-case matching the prompt name, e.g., `summarize-code.ts`
- Type files: `index.ts` in `types/` directory
- Config and utility files: camelCase `.ts` in `lib/`

## NEVER DO THIS

1. Never write to `stdout` for logging or debugging; it corrupts the JSON-RPC protocol stream and breaks the MCP connection
2. Never throw unhandled exceptions from tool handlers; always catch errors and return `{ isError: true, content: [...] }`
3. Never define tool input schemas without `.describe()` on each field; LLM clients rely on descriptions to use tools correctly
4. Never register tools dynamically after server initialization without emitting a `tools/list_changed` notification
5. Never block the event loop in tool handlers with synchronous operations; use async/await for I/O-bound work
6. Never include sensitive data (API keys, tokens) in tool responses; filter them before returning content
7. Never use CommonJS `require()`; the project is ESM-only with `"type": "module"` in package.json

## Testing

- Unit test tool handlers by calling the handler function directly with mock inputs and asserting response content
- Use `@modelcontextprotocol/inspector` to manually test tools, resources, and prompts during development: `npx @modelcontextprotocol/inspector node dist/index.js`
- Integration test the full server by creating a client transport pair: `const [clientTransport, serverTransport] = createInMemoryTransport()`
- Test error paths: invalid input schemas, missing required fields, downstream service failures
- Test resource URI template matching with various path patterns
- Validate that all tool responses conform to the MCP content type schema (text, image, or resource)
- Run the server with `--inspect` flag and test with Claude Desktop by adding to `claude_desktop_config.json`
- CI runs `tsup` build and verifies the output starts cleanly with `node dist/index.js --help`

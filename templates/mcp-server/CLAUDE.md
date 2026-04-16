# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Model Context Protocol (MCP)
- TypeScript/Python
- stdio or HTTP transport
- Tool definitions for LLMs
- Resource exposure

## Project Structure
```
src/
├── server/
│   └── mcp-server.ts           // MCP server setup
├── tools/
│   ├── file-reader.ts          // Tool implementations
│   └── calculator.ts
├── resources/
│   └── templates/
└── transports/
    ├── stdio.ts
    └── http.ts
```

## Architecture Rules

- **Tools for actions.** Define functions LLM can invoke.
- **Resources for data.** Expose files, templates, context.
- **Prompts for guidance.** Pre-defined prompt templates.
- **Type-safe schemas.** Zod schemas for tool parameters.

## Coding Conventions

- Server: `const server = new Server({ name: 'my-server', version: '1.0.0' })`.
- Tool: `server.setRequestHandler(CallToolRequestSchema, async (request) => { if (request.params.name === 'calculate') { ... } })`.
- Schema: `const CalculateSchema = z.object({ operation: z.enum(['add', 'subtract']), a: z.number(), b: z.number() })`.
- Resource: `server.setRequestHandler(ReadResourceRequestSchema, async (request) => { ... })`.

## NEVER DO THIS

1. **Never expose sensitive operations.** Tools have LLM access—limit capabilities.
2. **Never skip input validation.** Validate all tool parameters strictly.
3. **Never block the transport.** Handle requests asynchronously.
4. **Never forget error handling.** Return proper error responses to LLM.
5. **Never expose raw errors.** Sanitize error messages before returning.
6. **Never ignore rate limiting.** Tools may be called rapidly—throttle if needed.
7. **Never skip documentation.** Tools need clear descriptions for LLM to use.

## Testing

- Test tool execution with valid/invalid inputs.
- Test resource reading/writing.
- Test with actual Claude Code integration.


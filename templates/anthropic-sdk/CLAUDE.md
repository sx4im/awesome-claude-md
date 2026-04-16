# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Anthropic TypeScript/Python SDK
- Claude 3.5/3/Opus/Sonnet/Haiku
- Streaming responses
- Tool use / function calling
- Vision capabilities

## Project Structure
```
src/
├── anthropic/
│   ├── client.ts               // SDK client setup
│   └── types.ts                // Type definitions
├── prompts/
│   └── templates.ts            // System/user prompts
├── tools/
│   └── definitions.ts          // Tool schemas
└── streaming/
    └── handler.ts              // Stream processing
```

## Architecture Rules

- **Async streaming.** Handle streaming responses for real-time UX.
- **Tool use for actions.** Define tools for external capabilities.
- **System prompts for context.** Set behavior and constraints.
- **Vision for images.** Pass images as base64 for analysis.

## Coding Conventions

- Client: `const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })`.
- Message: `const message = await anthropic.messages.create({ model: 'claude-3-5-sonnet-20241022', max_tokens: 1024, messages: [{ role: 'user', content: 'Hello' }] })`.
- Streaming: `const stream = anthropic.messages.stream({ ... }); for await (const event of stream) { ... }`.
- Tools: `tools: [{ name: 'get_weather', description: '...', input_schema: { type: 'object', properties: { ... } } }]`.

## NEVER DO THIS

1. **Never expose API keys client-side.** Proxy through server.
2. **Never ignore token limits.** Track usage to avoid truncation.
3. **Never skip error handling.** Rate limits, timeouts happen.
4. **Never use blocking waits for streaming.** Process chunks as they arrive.
5. **Never forget tool result formatting.** Return results in correct format.
6. **Never ignore the `max_tokens` limit.** Claude stops at limit—set appropriately.
7. **Never use without retry logic.** Network issues require graceful handling.

## Testing

- Test with different models (Haiku for fast, Opus for complex).
- Test streaming handler processes all events.
- Test tool use flow end-to-end.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- OpenAI SDK v4
- GPT-4o, GPT-4, GPT-3.5-turbo
- Streaming responses
- Function calling
- Assistants API

## Project Structure
```
src/
├── openai/
│   ├── client.ts               // OpenAI client setup
│   └── assistants.ts           // Assistants API helpers
├── chat/
│   ├── completions.ts          // Chat completion logic
│   └── streaming.ts            // Streaming handlers
├── functions/
│   └── definitions.ts          // Function schemas
└── embeddings/
    └── generator.ts            // Text embedding
```

## Architecture Rules

- **Streaming for UX.** Real-time token display improves perceived speed.
- **Function calling for actions.** Define schemas for external tool use.
- **Embeddings for search.** Generate embeddings for semantic search.
- **Assistants for stateful.** Thread-based conversations with tools.

## Coding Conventions

- Client: `const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })`.
- Chat: `const completion = await openai.chat.completions.create({ model: 'gpt-4o', messages: [{ role: 'user', content: 'Hello' }] })`.
- Streaming: `const stream = await openai.chat.completions.create({ ... , stream: true }); for await (const chunk of stream) { ... }`.
- Functions: `functions: [{ name: 'get_weather', description: '...', parameters: { type: 'object', properties: { ... } } }]`.
- Embeddings: `const embedding = await openai.embeddings.create({ model: 'text-embedding-3-small', input: text })`.

## NEVER DO THIS

1. **Never expose API keys client-side.** Always proxy through backend.
2. **Never ignore rate limits.** Implement exponential backoff.
3. **Never forget to handle finish_reason.** 'stop', 'length', 'function_call' matter.
4. **Never skip content filtering handling.** Moderation flags need attention.
5. **Never use exact token counts for billing.** They may vary slightly.
6. **Never ignore the system message.** Use it for behavior constraints.
7. **Never mix different API versions.** SDK v4 is different from v3.

## Testing

- Test streaming processes all chunks correctly.
- Test function calling flow with tool results.
- Test with different models for quality comparison.


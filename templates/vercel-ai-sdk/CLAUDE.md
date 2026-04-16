# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- AI SDK v4 by Vercel
- Next.js 15+ / React 19
- TypeScript 5.x
- Multiple LLM providers (OpenAI, Anthropic, etc.)
- Streaming by default

## Project Structure
```
src/
├── app/
│   ├── api/
│   │   └── chat/
│   │       └── route.ts        # API routes for AI
│   └── chat/
│       └── page.tsx            # Chat UI
├── components/
│   └── chat-message.tsx
├── lib/
│   ├── ai.ts                   # AI provider setup
│   └── tools.ts                # Tool definitions
└── hooks/
    └── use-chat.ts             # Custom chat hooks
```

## Architecture Rules

- **AI SDK Core for backend.** `generateText`, `streamText` in API routes.
- **AI SDK UI for frontend.** `useChat`, `useCompletion` hooks in React.
- **Streaming by default.** Responses stream in real-time.
- **Multi-provider support.** Switch OpenAI, Anthropic, etc. via provider config.

## Coding Conventions

- API route: `import { openai } from '@ai-sdk/openai'; import { streamText } from 'ai'`.
- Stream: `const result = streamText({ model: openai('gpt-4'), messages }); return result.toAIStreamResponse()`.
- Frontend: `import { useChat } from 'ai/react'; const { messages, input, handleInputChange, handleSubmit } = useChat()`.
- Tools: Define `tools: { weather: tool({ parameters: z.object(...), execute: async ({ city }) => ... }) }`.
- Object generation: `generateObject({ model, schema: z.object(...), prompt })`.

## NEVER DO THIS

1. **Never expose API keys client-side.** Proxy through API routes.
2. **Never forget to handle streaming errors.** Network interruptions happen.
3. **Never ignore the message format.** AI SDK expects specific message structure.
4. **Never skip rate limiting.** AI APIs are expensive—rate limit user requests.
5. **Never use without understanding the provider model.** `openai('gpt-4')` not just 'gpt-4'.
6. **Never forget about client-side caching.** `useChat` has caching—understand it.
7. **Never mix SDK v3 and v4 patterns.** v4 is a significant rewrite.

## Testing

- Test streaming with `result.toAIStreamResponse()`.
- Test tools execute correctly with parameters.
- Test error handling for API failures.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Framework: Next.js 15 (App Router, React Server Components)
- AI SDK: Vercel AI SDK 4.x (`ai` package) for streaming and multi-provider support
- LLM Providers: OpenAI (GPT-4o), Anthropic (Claude), Google (Gemini) via provider packages
- Language: TypeScript 5.x (strict mode)
- Styling: Tailwind CSS 4 with shadcn/ui components
- Database: Vercel Postgres (Neon) for chat history and user data
- ORM: Drizzle ORM
- Auth: NextAuth.js v5 (Auth.js)
- Hosting: Vercel (serverless and edge functions)
- Package Manager: pnpm
- Testing: Vitest and Playwright

## Project Structure

```
app/
  layout.tsx            # Root layout with providers
  page.tsx              # Landing page
  chat/
    page.tsx            # Chat interface (client component)
    actions.ts          # Server actions for chat operations
  api/
    chat/
      route.ts          # POST /api/chat -- streaming AI endpoint
    completion/
      route.ts          # POST /api/completion -- text completion endpoint
components/
  chat/
    ChatMessages.tsx    # Message list with streaming display
    ChatInput.tsx       # User input with submit handling
    MessageBubble.tsx   # Individual message rendering (markdown support)
  ui/                   # shadcn/ui components
lib/
  ai/
    providers.ts        # Multi-provider LLM configuration
    tools.ts            # AI SDK tool definitions (function calling)
    prompts.ts          # System prompts and prompt templates
  db/
    schema.ts           # Drizzle schema (users, conversations, messages)
    client.ts           # Drizzle client with Vercel Postgres
  auth.ts               # NextAuth configuration
  utils.ts              # Shared utility functions
```

## Architecture Rules

- AI streaming endpoints use `streamText()` from the AI SDK and return `result.toDataStreamResponse()`.
- Always define the model via provider packages: `import { openai } from '@ai-sdk/openai'` then `openai('gpt-4o')`.
- System prompts live in `lib/ai/prompts.ts` as template literal functions, not hardcoded in route handlers.
- Tool definitions use the AI SDK `tool()` helper with Zod schemas for parameters.
- Client-side chat uses the `useChat()` hook from `ai/react` -- never implement custom streaming logic.
- Persist conversations in the database after each completed message exchange via server actions.
- Route handlers at `api/chat/route.ts` must validate auth before calling the LLM.
- Rate limit AI endpoints using Vercel KV or upstash/ratelimit to prevent API key abuse.

## Coding Conventions

- Streaming route handler pattern:
  ```typescript
  const result = streamText({ model: openai('gpt-4o'), messages, system: getSystemPrompt(), tools });
  return result.toDataStreamResponse();
  ```
- Use `useChat({ api: '/api/chat' })` on the client. Access `messages`, `input`, `handleSubmit`, `isLoading`.
- Multi-provider switching: create a `getModel(provider, modelId)` factory in `lib/ai/providers.ts`.
- Tool results are automatically handled by the AI SDK. Define tools with `execute` async functions.
- Use `generateText()` for non-streaming server-side AI calls (background jobs, server actions).
- Use `generateObject()` with a Zod schema when you need structured JSON output from the LLM.

## Library Preferences

- AI SDK: `ai` (core), `@ai-sdk/openai`, `@ai-sdk/anthropic`, `@ai-sdk/google`
- UI chat hooks: `ai/react` (useChat, useCompletion, useObject)
- Markdown rendering: react-markdown with remark-gfm
- Code highlighting: shiki (used by react-markdown code blocks)
- UI components: shadcn/ui (not Material UI or Chakra)
- State management: React hooks and URL state (nuqs for search params)
- Auth: next-auth v5 with database adapter

## File Naming

- React components: PascalCase (`ChatMessages.tsx`, `MessageBubble.tsx`)
- Route handlers: `route.ts` inside the App Router directory structure
- Server actions: `actions.ts` colocated with the page that uses them
- Library files: camelCase (`providers.ts`, `prompts.ts`)
- Database schema: `schema.ts` in `lib/db/`
- Test files: `*.test.ts` or `*.test.tsx` colocated with source

## NEVER DO THIS

1. Never call LLM APIs directly with fetch -- always use the AI SDK's `streamText()`, `generateText()`, or `generateObject()`.
2. Never expose API keys to the client -- LLM calls must happen in route handlers or server actions, never in client components.
3. Never use `useChat` with `onFinish` to save messages client-side -- save on the server in the route handler using `onFinish` callback.
4. Never stream responses without error handling -- wrap `streamText()` in try/catch and return proper HTTP error responses.
5. Never hardcode model names in route handlers -- use the provider factory in `lib/ai/providers.ts` for easy model switching.
6. Never skip input sanitization -- validate and truncate user messages before sending to the LLM to prevent prompt injection.
7. Never use the Pages Router (`pages/api/`) -- use App Router `app/api/` route handlers exclusively.

## Testing

- Use Vitest for unit tests on AI utility functions, prompt templates, and tool definitions.
- Mock AI SDK calls with `vi.mock('ai')` and return mock `StreamTextResult` objects.
- Test route handlers by calling the handler function directly with constructed Request objects.
- Use Playwright for end-to-end tests of the chat interface (type message, verify streaming response appears).
- Test tool calling by verifying that tool execute functions are called with correct parsed parameters.
- Use `ai` SDK's `MockLanguageModelV1` for deterministic test responses.

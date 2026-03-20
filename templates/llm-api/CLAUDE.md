# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- [TypeScript/Python] with [Express/FastAPI] for API layer
- OpenAI SDK and/or Anthropic SDK for LLM providers
- Server-Sent Events (SSE) for streaming responses
- Redis for rate limiting, caching, and request queuing
- Zod (TS) / Pydantic (Python) for request/response validation
- [Prisma/SQLAlchemy] for conversation and usage persistence

## Project Structure

```
[PROJECT_ROOT]/
├── src/
│   ├── providers/
│   │   ├── base.ts                  # Abstract LLMProvider interface
│   │   ├── openai.ts                # OpenAI-specific implementation
│   │   ├── anthropic.ts             # Anthropic-specific implementation
│   │   └── router.ts                # Provider selection and failover logic
│   ├── tools/
│   │   ├── registry.ts              # Tool/function definition registry
│   │   ├── executor.ts              # Safe tool execution with timeouts
│   │   └── definitions/             # Individual tool schemas
│   ├── streaming/
│   │   ├── sse.ts                   # SSE connection management
│   │   └── transformer.ts           # Normalize provider stream formats
│   ├── middleware/
│   │   ├── rate-limiter.ts          # Token-bucket rate limiting
│   │   ├── auth.ts                  # API key validation
│   │   └── usage-tracker.ts         # Token counting and billing
│   ├── routes/
│   │   ├── chat.ts                  # /v1/chat/completions endpoint
│   │   └── tools.ts                 # /v1/tools endpoint
│   ├── schemas/
│   │   └── api.ts                   # Request/response Zod schemas
│   └── config.ts                    # Provider configs, model mappings
├── tests/
│   ├── providers/
│   ├── streaming/
│   └── fixtures/                    # Recorded API responses for replay
├── [tsconfig.json/pyproject.toml]
└── docker-compose.yml               # Redis, app, optional Postgres
```

## Architecture Rules

- **Provider abstraction is mandatory.** Every LLM provider implements a common `LLMProvider` interface with `complete()`, `stream()`, and `listModels()`. Route handlers never import provider SDKs directly. Swapping or adding providers must not change any route code.
- **Streaming is the default path.** All chat endpoints stream by default. Non-streaming is the special case (buffer the stream and return the final message). Never build non-streaming first and bolt streaming on later — the architecture inverts.
- **Tool calls are sandboxed.** Tool/function execution runs with timeouts, memory limits, and no access to provider credentials. Never pass raw LLM output to `eval()`, `exec()`, or shell commands. The LLM chooses which tool; your code validates arguments against the schema before execution.
- **Rate limiting is per-key, per-model.** Different models cost different amounts. Rate limits track token usage, not just request counts. A user streaming GPT-4 burns limits faster than one calling Haiku. Use sliding window counters in Redis.
- **Retry with exponential backoff.** Provider APIs return 429s and 500s. Implement retries with jitter at the provider layer, not in route handlers. Set a max retry count of 3. Never retry on 400-level errors other than 429.

## Coding Conventions

- **Normalize provider responses.** Map every provider's response format to a single internal `ChatCompletion` type. OpenAI returns `choices[0].message`, Anthropic returns `content[0].text`. Your API returns one consistent format regardless of backend provider.
- **Token counting happens before and after.** Count input tokens before sending (using tiktoken or provider tokenizer) to enforce limits. Count output tokens from the response for billing. Never estimate — count exactly.
- **Structured error responses.** Every error returns `{ error: { type, message, code, provider? } }`. Never leak raw provider error objects to clients. Map provider-specific errors to your API's error taxonomy.
- **API versioning from day one.** All routes live under `/v1/`. The response format is a contract. Breaking changes get `/v2/`. Never change response shapes in-place.
- **Environment-based provider config.** Model mappings, rate limits, API keys, and default parameters live in environment variables or a config service. Never hardcode `model: "gpt-4o"` in business logic.

## Library Preferences

- **HTTP client:** Native provider SDKs (openai, @anthropic-ai/sdk). Not raw fetch/axios to provider APIs — SDKs handle auth headers, retries, and type safety.
- **Streaming:** Native SDK streaming iterators. Not manual chunked transfer encoding parsing.
- **Rate limiting:** Redis with sliding window (redis-rate-limiter or custom Lua script). Not in-memory counters (lost on restart, don't work with multiple instances).
- **Validation:** Zod (TS) or Pydantic (Python) for all API boundaries. Not manual if-checks on request bodies.
- **Token counting:** tiktoken for OpenAI models, @anthropic-ai/tokenizer for Claude. Not character-count heuristics.

## File Naming

- Source files: `kebab-case.ts` or `snake_case.py`
- Tool definitions: `tool-name.ts` matching the tool's `name` field
- Test fixtures: `provider-name.response-type.json` (e.g., `openai.chat-completion.json`)
- Config files: `config.ts` at root, never `constants.ts` (config changes, constants don't)

## NEVER DO THIS

1. **Never expose provider API keys to clients.** Your service is a proxy. Clients authenticate with YOUR API keys. Provider keys live in server-side environment variables only. Never return them in error messages or logs.
2. **Never buffer entire streaming responses in memory.** Use async iterators and pipe chunks directly to the SSE response. A 100K token response buffered across 50 concurrent users will OOM your server.
3. **Never trust function call arguments from the LLM.** The model can hallucinate tool names, fabricate parameter values, and produce malformed JSON. Validate every tool call against the registered schema before execution. Treat LLM output as untrusted user input.
4. **Never ignore `finish_reason`.** Check whether the response ended due to `stop`, `length` (hit token limit), `tool_calls`, or `content_filter`. Each requires different handling. Silently truncated responses are worse than errors.
5. **Never hardcode model names in business logic.** Models get deprecated, renamed, and replaced. Use a model registry mapping logical names (`"fast"`, `"powerful"`) to provider-specific model IDs. Update the mapping without code changes.
6. **Never log full prompts or completions in production.** They contain user PII and potentially sensitive data. Log request metadata (model, token counts, latency, finish_reason) without content. Use a separate opt-in audit log for content debugging.
7. **Never share conversation context across users.** Each API key or session gets isolated message history. A multi-tenant system that leaks one user's conversation into another's is a security and privacy catastrophe.

## Testing

- Mock provider SDKs with recorded response fixtures. Never call real LLM APIs in CI — tests become slow, flaky, expensive, and non-deterministic.
- Test streaming by consuming the async iterator and asserting individual chunks arrive in order with correct delta content.
- Test tool calling end-to-end: send a message that triggers a tool call, verify the tool is invoked with validated arguments, and verify the tool result is sent back to the model.
- Test rate limiting by sending bursts of requests and asserting that the correct ones receive 429 responses with `Retry-After` headers.
- Test provider failover by mocking the primary provider to return 500s and asserting the fallback provider is called.

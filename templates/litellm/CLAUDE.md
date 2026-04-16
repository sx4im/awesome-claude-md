# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- LiteLLM (unified LLM API)
- Python 3.11+
- 100+ LLM providers
- OpenAI-compatible proxy
- Cost tracking and rate limiting

## Project Structure
```
src/
├── llm/
│   ├── client.py               # LiteLLM client setup
│   ├── router.py               # Multi-provider routing
│   └── failover.py             # Fallback configuration
├── proxy/
│   └── config.yaml             # Proxy configuration
├── cost/
│   └── tracking.py             # Usage tracking
└── config/
    └── models.json             # Model definitions
```

## Architecture Rules

- **Unified API for all providers.** Call OpenAI, Anthropic, Gemini with same interface.
- **Router for load balancing.** Distribute requests across providers.
- **Proxy for OpenAI compatibility.** Drop-in replacement for OpenAI SDK.
- **Cost tracking built-in.** Monitor spend across providers.

## Coding Conventions

- Completion: `from litellm import completion; response = completion(model="gpt-4", messages=[...])`.
- Async: `from litellm import acompletion; response = await acompletion(...)`.
- Proxy: `litellm --config config.yaml` to run OpenAI-compatible proxy.
- Router: `from litellm import Router; router = Router(model_list=[...])`.
- Fallbacks: Configure `fallbacks=[{"gpt-4": ["claude-3-opus"]}]` in router.

## NEVER DO THIS

1. **Never hardcode provider-specific code.** The point is abstraction—use unified interface.
2. **Never ignore rate limiting.** LiteLLM can rate limit per user/key.
3. **Never skip the proxy for existing OpenAI code.** Easiest migration path.
4. **Never forget to configure fallbacks.** Provider outages happen—have backups.
5. **Never ignore cost tracking.** Budget alerts prevent surprise bills.
6. **Never mix LiteLLM with direct SDKs carelessly.** Pick one approach per project.
7. **Never use without setting timeouts.** Some providers are slow—configure `request_timeout`.

## Testing

- Test each provider through unified interface.
- Test failover when primary provider fails.
- Test cost tracking accuracy.


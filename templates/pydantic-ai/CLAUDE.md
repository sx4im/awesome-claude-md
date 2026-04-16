# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- PydanticAI (agent framework)
- Python 3.11+
- Pydantic v2 for type safety
- Multiple LLM providers
- Structured output focus

## Project Structure
```
src/
├── agents/
│   ├── __init__.py
│   ├── support.py              # Support agent
│   └── research.py             # Research agent
├── models/
│   └── schemas.py              # Pydantic output models
├── tools/
│   └── web_search.py           # Agent tools
├── dependencies.py             # Dependency injection
└── main.py                     # Entry point
```

## Architecture Rules

- **Type-safe agents.** Pydantic models define inputs and outputs.
- **Dependency injection.** `RunContext` provides dependencies to agents.
- **Tool registration.** Functions decorated with `@support_agent.tool` become agent capabilities.
- **Result validation.** Agent outputs validated against Pydantic models.

## Coding Conventions

- Create agent: `support_agent = Agent('openai:gpt-4', result_type=SupportResult, deps_type=SupportDeps)`.
- Define result model: `class SupportResult(BaseModel): response: str; confidence: float`.
- Add tool: `@support_agent.tool async def get_customer(ctx: RunContext[SupportDeps], customer_id: int) -> Customer`.
- Run agent: `result = await support_agent.run('Help with order', deps=SupportDeps(db=db))`.
- Access result: `result.data` (typed SupportResult).

## NEVER DO THIS

1. **Never skip the result_type.** PydanticAI's value is structured, validated output.
2. **Never ignore dependency types.** Type-safe DI requires proper `deps_type` configuration.
3. **Never forget async/await.** PydanticAI is async-first.
4. **Never use tools without type hints.** Tool schemas derived from function signatures.
5. **Never ignore the context.** `RunContext` carries dependencies and message history.
6. **Never mix sync and async tools carelessly.** Convert sync tools properly.
7. **Never forget to handle validation errors.** Pydantic validation failures are possible.

## Testing

- Test agent with typed results.
- Test tool functions independently.
- Test dependency injection with mocks.


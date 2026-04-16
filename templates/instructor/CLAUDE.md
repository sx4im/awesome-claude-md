# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Instructor (structured outputs for LLMs)
- Python 3.11+
- OpenAI/Anthropic/Gemini
- Pydantic v2
- Function calling / tool use

## Project Structure
```
src/
├── extraction/
│   ├── client.py               # Instructor client setup
│   └── models.py               # Pydantic extraction models
├── prompts/
│   └── templates.py            # Extraction prompts
├── validators/
│   └── custom.py               # Pydantic validators
└── examples/
    └── *.jsonl                 # Few-shot examples
```

## Architecture Rules

- **Patch LLM client with Instructor.** `instructor.patch(OpenAI())` or `instructor.from_openai()`.
- **Pydantic models for outputs.** Define expected structure with validation.
- **Response model parameter.** Pass `response_model=MyModel` to completion calls.
- **Validation retries.** Instructor automatically retries on validation failures.

## Coding Conventions

- Patch client: `client = instructor.from_openai(OpenAI())`.
- Define model: `class User(BaseModel): name: str; age: int`.
- Extract: `user = client.chat.completions.create(model="gpt-4", response_model=User, messages=[...])`.
- Async: `client = instructor.from_openai(AsyncOpenAI())`.
- Iterable: `users = client.chat.completions.create(..., response_model=Iterable[User])` for multiple items.
- Partial: `Partial[User]` for streaming partial results.

## NEVER DO THIS

1. **Never use without Pydantic v2.** Instructor requires Pydantic v2 features.
2. **Never skip validation in models.** The point is reliable structured data—validate.
3. **Never ignore the `max_retries` parameter.** Set appropriate retry limits.
4. **Never forget `model_validator` for complex validation.** Cross-field validation is common.
5. **Never use for simple text generation.** Instructor adds overhead—use when structure matters.
6. **Never ignore validation errors.** Log and analyze failures to improve prompts.
7. **Never forget to handle partial results carefully.** Streaming partials may be incomplete.

## Testing

- Test extraction with varied inputs.
- Test validation edge cases.
- Test retry behavior with intentionally bad inputs.


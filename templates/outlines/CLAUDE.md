# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Outlines (guided text generation)
- Python 3.11+
- OpenAI, transformers, llama-cpp
- Regex/JSON/CFG constrained generation
- Guaranteed valid outputs

## Project Structure
```
src/
├── outlines/
│   ├── __init__.py
│   ├── generators.py           # Constrained generators
│   └── models.py                 # Model setup
├── schemas/
│   └── response_schemas.py       # Pydantic/JSON schemas
├── regex/
│   └── patterns.py               # Regex patterns
└── examples/
    └── prompts/
```

## Architecture Rules

- **Constrained generation.** Guarantee outputs match regex, JSON schema, or grammar.
- **No post-processing needed.** Generated text is always valid per constraints.
- **Multiple backends.** OpenAI API, Hugging Face transformers, llama.cpp.
- **Pydantic integration.** Generate Pydantic model instances directly.

## Coding Conventions

- Setup model: `from outlines import models; model = models.openai("gpt-4")`.
- Regex constraint: `from outlines import generate; generator = generate.regex(model, r"[A-Z]{3}\d{4}")`.
- JSON schema: `generator = generate.json(model, User)` where `User` is a Pydantic model.
- Generate: `result = generator("Generate a user:")`.
- Choice: `generator = generate.choice(model, ["option1", "option2"])`.

## NEVER DO THIS

1. **Never use without understanding the grammar backend.** Different backends have different capabilities.
2. **Never create overly complex regex patterns.** They can cause generation slowdowns.
3. **Never ignore the tokenization issues.** Some constraints may tokenize poorly.
4. **Never forget about context window.** Constraints consume context like any other tokens.
5. **Never use for open-ended generation.** Outlines is for structured output.
6. **Never skip schema validation after generation.** Although rare, verify in critical paths.
7. **Never ignore performance implications.** Constrained generation can be slower.

## Testing

- Test that all generated outputs match constraints.
- Test with edge case prompts.
- Test performance vs unconstrained generation.


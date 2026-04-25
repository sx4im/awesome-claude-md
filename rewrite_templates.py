#!/usr/bin/env python3
import os

def write_template(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

# Template 1: ai-prompt-engineering
write_template("templates/ai-prompt-engineering/CLAUDE.md", """# AI Prompt Engineering Best Practices

Design, test, and optimize LLM prompts with structured outputs, few-shot examples, chain-of-thought reasoning, and comprehensive evaluation frameworks.

## Tech Stack

- **Python 3.11+**: Primary language for prompt engineering pipelines
- **OpenAI/Anthropic SDK**: API clients for LLM interaction
- **Pydantic**: Structured output validation and schema enforcement
- **PromptLayer/LangSmith**: Prompt versioning, tracking, and observability
- **Weights & Biases**: Experiment tracking for prompt iterations
- **Jinja2**: Dynamic prompt templating with variable substitution
- **JSON Schema**: Output format validation and type safety

## Project Structure

```
prompts/
├── system/                     # System prompts defining assistant behavior
│   ├── coding-assistant.txt
│   ├── data-analyst.txt
│   └── creative-writer.txt
├── few-shot/                   # Curated example banks for in-context learning
│   ├── classification-examples.jsonl
│   ├── extraction-examples.jsonl
│   └── reasoning-examples.jsonl
├── templates/                  # Jinja2 templates with variable slots
│   ├── summarize-document.j2
│   ├── extract-entities.j2
│   └── generate-code.j2
├── schemas/                    # Pydantic models and JSON schemas
│   ├── output_schemas.py
│   └── validation_rules.py
├── evals/                      # Evaluation suites and benchmarks
│   ├── correctness_tests.py
│   ├── hallucination_tests.py
│   └── robustness_tests.py
└── registry/                   # Prompt metadata and versioning
    └── prompt_manifest.yaml
```

## Architecture Rules

- **Prompt versioning.** Every prompt change is versioned with semantic versioning. Tag prompts in registry before deployment.
- **Schema-first outputs.** Define Pydantic models or JSON schemas before writing prompts. The schema constrains the LLM output format.
- **Chain-of-thought for complex tasks.** Break reasoning into explicit intermediate steps. Use explicit reasoning sections.
- **Few-shot curation.** Select 3-5 diverse, high-quality examples. Order examples from simple to complex. Cover edge cases.
- **Separation of concerns.** System prompts define behavior, user prompts provide task context, assistant prompts demonstrate format.
- **Dynamic templating.** Use Jinja2 or similar for variable substitution. Validate all variables before prompt construction.

## Coding Conventions

- **XML tag delimiters.** Use `<input>`, `<context>`, `<instructions>` tags to structure prompt sections clearly.
- **JSON mode enforcement.** Set `response_format={"type": "json_object"}` for structured extraction tasks.
- **Temperature control.** Use temperature=0.0 for deterministic tasks. Use temperature=0.7-1.0 for creative tasks.
- **Max token budgets.** Always set `max_tokens` to prevent runaway generation. Budget 2x expected output length.
- **System prompt stability.** Keep system prompts static across sessions. Vary user prompts for A/B testing.

## NEVER DO THIS

1. **Never include PII in prompts.** Sanitize all user inputs before including in prompts. Use regex or NLP filters.
2. **Never rely on implicit formatting.** Always specify output format explicitly. LLMs default to unpredictable formatting without guidance.
3. **Never ignore prompt injection.** Implement input validation and output filtering. Use delimiters that are hard to confuse with user content.
4. **Never skip temperature tuning.** Using default temperature for all tasks yields inconsistent results. Match temperature to task type.
5. **Never hardcode examples.** Load few-shot examples from external files or databases for easy updates without code changes.
6. **Never neglect prompt caching.** Cache identical prompts when possible. Track cache hit rates in monitoring.
7. **Never deploy without evals.** Every prompt version must pass correctness, robustness, and safety evaluation suites before production.

## Testing

- **Correctness tests.** Gold-standard dataset with known correct outputs. Measure exact match, semantic similarity, and BLEU/ROUGE scores.
- **Hallucination detection.** Run prompts against adversarial inputs with known correct answers. Flag outputs that contradict ground truth.
- **Robustness tests.** Perturb inputs with typos, synonyms, and rephrasings. Verify output consistency across variations.
- **Latency benchmarks.** Track token generation speed and end-to-end latency. Set SLAs (e.g., p95 < 2s).
- **Cost tracking.** Log token usage per prompt template. Monitor cost per request and optimize verbose prompts.

## Claude Code Integration

- Use `@prompts/system/coding-assistant.txt` for coding context
- Reference `<instructions>` blocks when generating new prompts
- Apply schema-first approach for all structured output tasks
- Validate against NEVER DO THIS rules before finalizing prompts
""")

print("Template 1 done")

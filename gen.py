#!/usr/bin/env python3
import os

TMPL = """# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- {tech1}
- {tech2}
- {tech3}
- {tech4}
- {tech5}

## Project Structure

```
{structure}
```

## Architecture Rules

- **{rule1_title}** {rule1_desc}
- **{rule2_title}** {rule2_desc}
- **{rule3_title}** {rule3_desc}
- **{rule4_title}** {rule4_desc}

## Coding Conventions

- {conv1}
- {conv2}
- {conv3}
- {conv4}
- {conv5}

## NEVER DO THIS

1. **{never1}** {never1_desc}
2. **{never2}** {never2_desc}
3. **{never3}** {never3_desc}
4. **{never4}** {never4_desc}
5. **{never5}** {never5_desc}
6. **{never6}** {never6_desc}
7. **{never7}** {never7_desc}

## Testing

- {test1}
- {test2}
- {test3}
- {test4}
- {test5}

## Claude Code Integration

- Use `@` mentions to reference specific documentation sections
- Leverage context for framework-specific code generation
- Apply conventions when scaffolding new features
- Validate against NEVER DO THIS rules before generating code
"""

TEMPLATES = [
("ai-prompt-engineering","AI Prompt Engineering","LLM prompt design","Chain-of-thought patterns","Structured output schemas","Few-shot example curation","Prompt versioning","src/\nprompts/\n  ├── system/\n  │   └── coding-assistant.txt\n  ├── few-shot/\n  │   └── examples.jsonl\n  └── templates/\n      └── {task}-prompt.md","Prompt versioning","Track changes and A/B test prompt iterations for quality.","Chain-of-thought","Break complex reasoning into explicit intermediate steps.","Output schemas","Enforce structured formats with JSON schemas or Pydantic.","Guardrails","Add refusal patterns and content filtering to prompts.","Use XML tags for structure","Wrap variables in <input></input> tags for clarity.","Test with edge cases","Validate prompts with adversarial and boundary inputs.","Version in git","Store prompts as code with semantic versioning.",

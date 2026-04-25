#!/usr/bin/env python3
import os, textwrap

TEMPLATE = """# {title} - {subtitle}

## Tech Stack

- **{tech1}**
- **{tech2}**
- **{tech3}**
- **{tech4}**
- **{tech5}**

## Project Structure

```
{structure}
```

## Architecture Rules

- **{ar1_title}** {ar1_desc}
- **{ar2_title}** {ar2_desc}
- **{ar3_title}** {ar3_desc}
- **{ar4_title}** {ar4_desc}

## Coding Conventions

- **{cc1}**
- **{cc2}**
- **{cc3}**
- **{cc4}**
- **{cc5}**

## NEVER DO THIS

1. **{nd1_title}** {nd1_desc}
2. **{nd2_title}** {nd2_desc}
3. **{nd3_title}** {nd3_desc}
4. **{nd4_title}** {nd4_desc}
5. **{nd5_title}** {nd5_desc}
6. **{nd6_title}** {nd6_desc}
7. **{nd7_title}** {nd7_desc}

## Testing

- {t1}
- {t2}
- {t3}
- {t4}
- {t5}

## Claude Code Integration

- Use `@` mentions to reference specific docs for context
- Leverage project structure when scaffolding features
- Apply coding conventions to generated code
- Validate against NEVER DO THIS rules before accepting changes
"""

items = [
("ai-prompt-engineering","AI Prompt Engineering Best Practices","Prompt versioning and A/B testing","Chain-of-thought reasoning patterns","Structured output with JSON schemas","Few-shot example curation","Guardrails and safety filters","prompts/\n├── system/\n│   └── coding-assistant.txt\n├── few-shot/\n│   └── examples.jsonl\n└── templates/\n    └── {{task}}-prompt.md","Prompt versioning","Track changes in git and A/B test for quality improvements.","Chain-of-thought","Break complex reasoning into explicit intermediate steps.","Output schemas","Enforce JSON schemas or Pydantic models for structured responses.","Guardrails","Add refusal patterns and content filtering to all prompts.","XML tag structure","Wrap variables in tags for clarity and parsing reliability.","Edge case testing","Validate with adversarial and boundary-case inputs.","Version control","Store prompts as code with semantic versioning.","Prompt injection tests","Verify robustness against jailbreak attempts.","Chain validation","Test multi-step reasoning chains for correctness.","Few-shot accuracy","Measure example effectiveness with held-out test sets.","Schema compliance","Verify output always matches defined JSON schemas."),

("airbyte-etl","Airbyte Data Integration Platform","300+ source connectors","Incremental sync strategies","Schema evolution handling","Connection state management","Transformation with dbt","airbyte/\n├── connections/\n│   └── {{source}}-to-{{dest}}.yaml\n├── destinations/\n│   └── postgres.yaml\n└── transformations/\n    └── dbt-models/","Source connector selection","Choose certified connectors for production workloads.","Incremental sync","Use CDC or cursor-based sync for large tables.","Schema registry","Handle breaking schema changes with versioning.","State management","Persist sync state reliably across restarts.","Mixed sync modes","Avoid mixing full refresh and incremental without reason.","Untested connectors","Validate community connectors before production use.","Schema drift","Monitor and alert on upstream schema changes.","Hardcoded secrets","Use Airbyte's secret management or external vaults.","Manual sync scheduling","Automate with cron expressions or event triggers.","Connector validation","Test each connector with representative data samples.","Sync monitoring","Alert on failed syncs and schema mismatch errors.","State recovery","Test state restoration after interrupted syncs.","Transformation tests","Validate dbt model output against source data."),
]

def write(name, **kwargs):
    path = f"/home/saim/awesome-claude-md/templates/{name}/CLAUDE.md"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    content = TEMPLATE.format(**kwargs)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path} ({len(content.splitlines())} lines)")

for item in items:
    name = item[0]
    write(name, title=item[1], subtitle=item[2], tech1=item[3], tech2=item[4], tech3=item[5], tech4=item[6], tech5=item[7], structure=item[8], ar1_title=item[9], ar1_desc=item[10], ar2_title=item[11], ar2_desc=item[12], ar3_title=item[13], ar3_desc=item[14], ar4_title=item[15], ar4_desc=item[16], cc1=item[17], cc2=item[18], cc3=item[19], cc4=item[20], cc5=item[21], nd1_title=item[22], nd1_desc=item[23], nd2_title=item[24], nd2_desc=item[25], nd3_title=item[26], nd3_desc=item[27], nd4_title=item[28], nd4_desc=item[29], nd5_title=item[30], nd5_desc=item[31], nd6_title=item[32], nd6_desc=item[33], nd7_title=item[34], nd7_desc=item[35], t1=item[36], t2=item[37], t3=item[38], t4=item[39], t5=item[40])

print("Done")

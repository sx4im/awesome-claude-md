import os

# Helper to write template file
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"Written {path} ({len(content.splitlines())} lines)")

# 1. ai-prompt-engineering
write("templates/ai-prompt-engineering/CLAUDE.md", """# AI Prompt Engineering Best Practices

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

# 2. airbyte-etl
write("templates/airbyte-etl/CLAUDE.md", """# Airbyte Data Integration Platform

Open-source data integration platform with 300+ source connectors for ETL/ELT pipelines into data warehouses and lakes.

## Tech Stack

- **Airbyte Open Source/Cloud**: Core ETL/ELT platform (v0.63+)
- **Docker**: Containerized connector deployment with Compose
- **PostgreSQL**: Internal metadata database for Airbyte state
- **dbt Core**: Transformation layer (T in ELT) for warehouse modeling
- **Destination**: Snowflake / BigQuery / Redshift / Postgres
- **Orchestrator**: Airbyte API or Airflow DAGs for pipeline scheduling
- **Monitoring**: Datadog / Grafana for sync metrics and alerting

## Project Structure

```
airbyte/
├── sources/                    # Source connector configurations
│   ├── postgres-production.yaml
│   ├── salesforce-prod.yaml
│   └── stripe-events.yaml
├── destinations/               # Warehouse and lake configs
│   ├── snowflake-raw.yaml
│   └── bigquery-analytics.yaml
├── connections/                # Sync definitions linking source -> destination
│   ├── users-to-warehouse.yaml
│   └── events-to-lake.yaml
├── transformations/            # dbt models for ELT transforms
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
├── orchestration/              # Airflow DAGs or schedule configs
│   └── dags/
│       └── daily_syncs.py
└── tests/                      # Connector and sync validation
    └── sync_validation.py
```

## Architecture Rules

- **Certified connectors for production.** Only use Airbyte-certified connectors for critical paths. Community connectors require extra validation.
- **Incremental sync preferred.** Configure CDC or cursor-based incremental syncs to minimize warehouse load.
- **Raw landing zone.** Load all data into raw/staging tables before dbt transforms. Never transform during the extract phase.
- **Schema evolution handling.** Monitor source schema changes. Auto-propagation is risky—review and approve DDL changes.
- **Connection state management.** Sync state (cursors, CDC LSNs) is critical. Back up Airbyte's internal database for disaster recovery.
- **Separate sync per entity.** One connection per logical entity (users, orders) rather than one giant connection. Easier debugging and partial retry.

## Coding Conventions

- **YAML connection definitions.** Store all source, destination, and connection configs as YAML under version control.
- **dbt naming conventions.** `stg_` for staging models, `int_` for intermediate, `fct_` and `dim_` for marts.
- **Environment templating.** Use `${VAR}` substitution for all hostnames, credentials, and schema names. Never commit real values.
- **Connection IDs in orchestration.** Reference stable connection IDs (not names) in Airflow DAGs to survive renames.

## NEVER DO THIS

1. **Never use full refresh on large tables.** Full refresh replicates entire tables every sync. Use incremental or CDC for tables > 1M rows.
2. **Never sync directly to production marts.** Always land in a raw/staging schema first. dbt handles promotion to production.
3. **Never ignore sync failures.** Failed syncs halt downstream dbt runs. Set up PagerDuty/Slack alerts on failure.
4. **Never hardcode credentials in connection YAML.** Use Airbyte's secret management or external secret stores.
5. **Never skip schema drift monitoring.** Source schema changes can break dbt models. Add tests for schema contract compliance.
6. **Never run transformations in the extract phase.** Keep Airbyte as pure ELT—Extract and Load. Transform belongs in dbt.
7. **Never forget to back up state.** Airbyte's internal DB contains sync cursors. Losing it means re-syncing everything.

## Testing

- **Connector validation tests.** Test each connector with representative data volumes (1K, 1M, 10M rows). Verify data type fidelity.
- **Sync correctness tests.** Row count checks, column checksums, and sampled record comparisons between source and destination.
- **dbt model tests.** Add `unique`, `not_null`, `accepted_values`, and `relationships` tests to all staging and mart models.
- **SLA monitoring.** Track sync latency from source change to warehouse availability. Alert if p95 > 4 hours for daily syncs.
- **Disaster recovery drills.** Quarterly restore of Airbyte state DB and verification that incremental syncs resume correctly.

## Claude Code Integration

- Use `@sources/` and `@destinations/` configs as context for pipeline changes
- Reference connection YAML when generating new sync configurations
- Apply dbt naming conventions when suggesting transformations
- Validate against NEVER DO THIS rules before modifying sync strategies
""")

print("Templates 1-2 done")

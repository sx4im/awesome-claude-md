# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: AI & ML)

### Release Discipline
- Never expose raw secrets, prompts, or proprietary training data.
- Validate model outputs before side effects (tool calls, writes, automations).
- Track model/version/config used in each production-impacting change.

### Merge/Release Gates
- Evaluation set checks pass on quality, safety, and regression thresholds.
- Hallucination-sensitive flows have deterministic fallback behavior.
- Prompt/template changes include before/after examples.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Python 3.11+
- Dagster 1.7+ as the orchestration framework
- Dagster UI (dagit) for development and monitoring
- dagster-dbt for dbt integration
- dagster-duckdb or dagster-postgres for IO managers
- dagster-aws for S3 and cloud resources
- Polars or pandas for in-memory data transformations
- Docker for deployment with dagster-daemon and dagster-webserver

## Project Structure

```
project/
├── definitions.py               # Definitions entry point for dagster
├── assets/
│   ├── ingestion/
│   │   ├── raw_orders.py        # Source asset from external API
│   │   ├── raw_customers.py     # Source asset from database
│   │   └── raw_products.py      # Source asset from S3
│   ├── staging/
│   │   ├── stg_orders.py        # Cleaned orders asset
│   │   └── stg_customers.py     # Cleaned customers asset
│   ├── marts/
│   │   ├── revenue_daily.py     # Daily revenue mart
│   │   └── customer_ltv.py      # Customer lifetime value
│   └── reporting/
│       └── executive_summary.py # Final reporting asset
├── resources/
│   ├── database.py              # Database resource (DuckDB/Postgres)
│   ├── storage.py               # S3/GCS storage resource
│   ├── api_client.py            # External API client resource
│   └── config.py                # Resource configuration by environment
├── io_managers/
│   ├── parquet_io.py            # Parquet file IO manager
│   └── duckdb_io.py             # DuckDB table IO manager
├── partitions/
│   ├── daily.py                 # Daily partition definitions
│   └── monthly.py               # Monthly partition definitions
├── sensors/
│   ├── s3_sensor.py             # S3 new file sensor
│   └── api_sensor.py            # External API sensor
├── schedules/
│   └── daily_refresh.py         # Daily materialization schedule
├── jobs/
│   └── full_refresh.py          # Manual full refresh job
├── utils/
│   ├── transforms.py            # Pure data transformation functions
│   └── validators.py            # Asset check helpers
└── tests/
    ├── test_assets.py
    ├── test_resources.py
    └── test_io_managers.py
```

## Architecture Rules

- Every data artifact is a `@asset`; never use raw ops unless wrapping a non-data side effect (email, Slack notification).
- Assets must declare their dependencies via function parameters, not by reading shared state or files directly.
- All external system access (databases, APIs, S3) must go through Dagster resources injected via the `resources` parameter.
- IO managers handle all serialization and deserialization; assets return and receive Python objects (DataFrames), never file paths.
- Use `@asset_check` for data quality assertions (null checks, uniqueness, row count thresholds) attached to the asset they validate.
- Partition definitions live in `partitions/` and are shared across assets in the same lineage path.
- `definitions.py` is the single entry point; it collects all assets, resources, schedules, and sensors into one `Definitions` object.

## Coding Conventions

- Asset function names become the asset key; name them as nouns matching the data they produce: `raw_orders`, `stg_customers`, `revenue_daily`.
- Group related assets with `group_name` parameter: `@asset(group_name="staging")`.
- Use `MetadataValue` to attach row counts, schema info, and sample data to asset materializations.
- Configure resources per environment using `configured` or `EnvVar`: separate dev (DuckDB local) from prod (Postgres).
- Use `AssetSelection.groups("staging")` in schedules and jobs, not individual asset lists.
- Type-annotate asset return values: `-> pl.DataFrame` or `-> pd.DataFrame`.

## Library Preferences

- Dagster-native IO managers over custom file writing; use `dagster-duckdb` IO manager for analytical workloads.
- Polars for data transformations within assets; pandas only if a dependency requires it.
- dagster-dbt for dbt model orchestration rather than shelling out to the dbt CLI.
- Dagster sensors over cron schedules when triggering on external events (new S3 files, API webhooks).

## File Naming

- Asset files: snake_case noun matching the asset key (`raw_orders.py`, `revenue_daily.py`).
- Resource files: snake_case noun describing the external system (`database.py`, `storage.py`).
- One asset per file for complex assets; multiple related assets per file only if they share private helper functions.

## NEVER DO THIS

1. Never read or write files directly in asset functions; use IO managers to handle persistence so assets remain environment-agnostic.
2. Never hardcode connection strings or credentials; inject them via resources using `EnvVar("DATABASE_URL")`.
3. Never create circular dependencies between assets; the asset graph must be a DAG.
4. Never use `@op` and `@graph` for data pipelines; they are legacy patterns superseded by the asset-based API.
5. Never skip `MetadataValue` on materializations; row counts and schema metadata are critical for debugging and lineage.
6. Never put business logic inside asset functions; extract pure transformation functions into `utils/transforms.py` for testability.

## Testing

- Test assets by calling the function directly with mock resources: `result = raw_orders(context=build_asset_context(), api_client=mock_client)`.
- Use `build_asset_context()` to create test context objects with controlled partition keys and config.
- Test IO managers by round-tripping: write an object, read it back, assert equality.
- Test resources in isolation: instantiate with test config and verify connection or API call behavior.
- Use `materialize([my_asset], resources={"db": test_db})` for integration tests that exercise the full asset + IO manager path.
- Assert asset checks pass on known-good fixture data and fail on intentionally bad data.

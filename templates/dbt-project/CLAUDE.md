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

- dbt Core 1.8+ (or dbt Cloud)
- Target warehouse: Snowflake, BigQuery, Redshift, or Postgres (configured in profiles.yml)
- SQLFluff for SQL linting with dbt templating support
- dbt-expectations package for advanced data testing
- dbt-utils package for surrogate keys, date spines, and pivot macros
- pre-commit hooks for model YAML validation and SQLFluff
- GitHub Actions or dbt Cloud CI for pull request checks

## Project Structure

```
dbt_project/
├── dbt_project.yml               # Project configuration and vars
├── profiles.yml                  # Connection profiles (gitignored)
├── packages.yml                  # dbt package dependencies
├── models/
│   ├── staging/
│   │   ├── stripe/
│   │   │   ├── _stripe__models.yml   # Model docs and tests
│   │   │   ├── _stripe__sources.yml  # Source definitions
│   │   │   ├── stg_stripe__payments.sql
│   │   │   └── stg_stripe__customers.sql
│   │   └── shopify/
│   │       ├── _shopify__models.yml
│   │       ├── _shopify__sources.yml
│   │       ├── stg_shopify__orders.sql
│   │       └── stg_shopify__products.sql
│   ├── intermediate/
│   │   ├── _int__models.yml
│   │   ├── int_orders_pivoted.sql
│   │   └── int_payments_aggregated.sql
│   └── marts/
│       ├── finance/
│       │   ├── _finance__models.yml
│       │   ├── fct_revenue.sql
│       │   └── dim_customers.sql
│       └── marketing/
│           ├── _marketing__models.yml
│           └── fct_campaign_performance.sql
├── macros/
│   ├── generate_schema_name.sql  # Custom schema name logic
│   ├── cents_to_dollars.sql      # Currency conversion macro
│   └── test_row_count_delta.sql  # Custom generic test
├── seeds/
│   ├── country_codes.csv         # Static reference data
│   └── currency_rates.csv        # Exchange rates seed
├── snapshots/
│   └── snap_customers.sql        # SCD Type 2 customer snapshot
├── tests/
│   └── assert_revenue_positive.sql  # Singular data test
├── analyses/
│   └── ad_hoc_revenue_check.sql
└── target/                       # Compiled SQL output (gitignored)
```

## Architecture Rules

- Follow the staging -> intermediate -> marts layering strictly. Staging models select from sources only. Intermediate models join staging models. Marts expose final business entities.
- Every source must have a `_<source>__sources.yml` file with `loaded_at_field` and `freshness` checks.
- Staging models are 1:1 with source tables: rename columns, cast types, add surrogate keys. No joins, no aggregations.
- Mart models are organized by business domain directory (`finance/`, `marketing/`).
- All models must have a YAML file with `description`, `columns`, and at least `not_null` + `unique` tests on primary keys.
- Use `ref()` for model references and `source()` for raw table references; never hardcode schema-qualified table names.

## Coding Conventions

- Model naming: `stg_<source>__<entity>`, `int_<entity>_<verb>`, `fct_<entity>`, `dim_<entity>`.
- YAML files: `_<directory>__models.yml` and `_<source>__sources.yml` with leading underscore.
- SQL style: leading commas, lowercase keywords, four-space indentation, one CTE per logical step.
- Every model starts with a `with` block containing at least one CTE; never write a bare `SELECT` as the full model.
- Use `{{ config(materialized='view') }}` for staging, `{{ config(materialized='table') }}` for marts, `{{ config(materialized='ephemeral') }}` for intermediate unless performance requires table.
- Surrogate keys via `{{ dbt_utils.generate_surrogate_key(['col1', 'col2']) }}`.

## Library Preferences

- dbt-utils for `surrogate_key`, `date_spine`, `unpivot`, `star`, and `get_column_values`.
- dbt-expectations for `expect_column_values_to_be_between`, `expect_table_row_count_to_be_between`, and distribution tests.
- SQLFluff with `dbt` templater and `snowflake` (or target) dialect for linting.
- Custom generic tests in `macros/` for project-specific validation logic.

## File Naming

- SQL model files: `stg_<source>__<table>.sql`, `int_<description>.sql`, `fct_<noun>.sql`, `dim_<noun>.sql`.
- YAML files: `_<group>__models.yml` or `_<source>__sources.yml` with leading underscore.
- Macros: snake_case verb-noun: `cents_to_dollars.sql`, `generate_schema_name.sql`.
- Seeds: snake_case descriptive noun: `country_codes.csv`.

## NEVER DO THIS

1. Never use hardcoded table references like `raw.stripe.payments`; always use `{{ source('stripe', 'payments') }}` or `{{ ref('stg_stripe__payments') }}`.
2. Never put joins or aggregations in staging models; staging is only for renaming, casting, and filtering deleted records.
3. Never skip YAML documentation; every model must have a corresponding entry in a `_*__models.yml` file with column descriptions.
4. Never write DML statements (`INSERT`, `UPDATE`, `DELETE`) in models; dbt handles materialization.
5. Never use `{{ this }}` in staging or intermediate models; it is only appropriate in incremental model merge logic.
6. Never commit `profiles.yml` with real credentials to version control; use environment variables with `{{ env_var('DB_PASSWORD') }}`.

## Testing

- Every primary key must have `unique` and `not_null` tests defined in YAML.
- Every foreign key must have a `relationships` test pointing to the referenced model.
- Use `dbt test --select staging` in CI to validate staging layer independently.
- Use `dbt build --select state:modified+` in CI to test only changed models and their downstream dependents.
- Write singular tests in `tests/` for complex business rule assertions that span multiple models.
- Run `dbt source freshness` daily to alert on stale upstream data.
- Validate SQL style with `sqlfluff lint models/` in pre-commit hooks.

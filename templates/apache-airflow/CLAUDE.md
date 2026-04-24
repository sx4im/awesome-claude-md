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
- Apache Airflow 2.9+ with the TaskFlow API
- PostgreSQL as the Airflow metadata database
- Celery executor for production, Local executor for development
- Docker Compose for local Airflow environment
- AWS provider package (apache-airflow-providers-amazon) for S3, Redshift, Glue
- dbt provider package for dbt task orchestration
- Slack provider for alerting on task failures

## Project Structure

```
airflow/
├── dags/
│   ├── daily/
│   │   ├── dag_ingest_orders.py       # Daily order ingestion
│   │   ├── dag_transform_revenue.py   # Revenue transformation
│   │   └── dag_export_reports.py      # Report generation and export
│   ├── hourly/
│   │   └── dag_streaming_sync.py      # Hourly data sync
│   ├── weekly/
│   │   └── dag_data_quality.py        # Weekly data quality checks
│   └── common/
│       ├── task_groups.py             # Reusable TaskGroup definitions
│       ├── callbacks.py              # on_failure, on_success callbacks
│       └── constants.py              # DAG default args, schedules, tags
├── plugins/
│   ├── operators/
│   │   └── custom_s3_operator.py     # Custom S3 operator
│   ├── sensors/
│   │   └── api_sensor.py            # Custom API availability sensor
│   └── hooks/
│       └── custom_hook.py           # Custom connection hook
├── include/
│   ├── sql/
│   │   ├── staging/                  # Staging SQL templates
│   │   └── marts/                    # Mart SQL templates
│   └── scripts/
│       └── data_validation.py        # Validation helper scripts
├── tests/
│   ├── dags/
│   │   └── test_dag_integrity.py     # DAG import and cycle tests
│   └── operators/
│       └── test_custom_s3.py
├── docker-compose.yaml
├── Dockerfile
└── requirements.txt
```

## Architecture Rules

- Every DAG must use the `@dag` decorator (TaskFlow API), not the classic `DAG()` context manager.
- Every task must use the `@task` decorator for Python callables; use pre-built operators only for external system interactions (S3, database, Slack).
- DAG files must contain only DAG definition and task orchestration; all business logic lives in `include/scripts/` or imported packages.
- Each DAG file defines exactly one DAG; never put multiple DAGs in a single file.
- Use `TaskGroup` for logical grouping of related tasks; define reusable groups in `dags/common/task_groups.py`.
- All DAGs must set `catchup=False` unless historical backfill is explicitly required and tested.
- Use Airflow Connections and Variables for all external system credentials; never hardcode secrets.

## Coding Conventions

- DAG file naming: `dag_<verb>_<noun>.py` (e.g., `dag_ingest_orders.py`).
- DAG ID must match the filename without the `.py` extension: `dag_ingest_orders`.
- Set `default_args` with `owner`, `retries=2`, `retry_delay=timedelta(minutes=5)`, and `on_failure_callback` pointing to the Slack alerting function.
- Use `logical_date` (not `execution_date`) for date-based partitioning via Jinja templating: `{{ ds }}`.
- Pass data between tasks using XCom via TaskFlow return values; keep payloads under 48KB.
- Tag all DAGs with team and domain: `tags=["data-eng", "orders"]`.
- Schedule intervals as cron strings, not `timedelta`, for clarity: `schedule="0 6 * * *"`.

## Library Preferences

- TaskFlow API `@task` decorator over classic `PythonOperator`.
- `S3Hook` and `PostgresHook` from official provider packages for AWS and database access.
- Slack webhook via `SlackWebhookOperator` for failure alerts, not email.
- Jinja-templated SQL files in `include/sql/` loaded with `PostgresOperator(sql="sql/staging/query.sql")`.

## File Naming

- DAG files: `dag_<action>_<subject>.py` in schedule-based subdirectories.
- SQL templates: snake_case matching the target table (`stg_orders.sql`).
- Custom operators/sensors: descriptive snake_case with type suffix (`api_sensor.py`).

## NEVER DO THIS

1. Never import heavyweight libraries (pandas, numpy, scikit-learn) at the DAG file top level; import inside `@task` functions to avoid slowing down the DAG parser.
2. Never use `depends_on_past=True` without a clear timeout; it silently stalls pipelines when a past run fails.
3. Never pass large datasets (over 48KB) through XCom; write to S3 or a database and pass the reference path.
4. Never use `catchup=True` on a new DAG without first testing a manual backfill on a limited date range.
5. Never hardcode connection strings or API keys; use `Connection` and `Variable` from the Airflow metadata store.
6. Never use `trigger_rule="all_done"` unless you explicitly handle upstream failures in the task logic.
7. Never run `pip install` inside a task at runtime; bake all dependencies into the Docker image or virtual environment.

## Testing

- Run `python -c "import dags.daily.dag_ingest_orders"` for every DAG file in CI to catch import errors and circular dependencies.
- Test DAG integrity: assert no import errors, no cycles, correct task count, and expected dependencies using `dag.test()`.
- Unit test business logic functions (in `include/scripts/`) independently of Airflow.
- Test custom operators with mocked hooks: patch `S3Hook.load_file` and assert the operator calls it with correct parameters.
- Use `dag.test()` in local development to run a DAG end-to-end with a single command.
- Assert all DAGs have `tags`, `owner`, and `on_failure_callback` set in a parametrized CI test.

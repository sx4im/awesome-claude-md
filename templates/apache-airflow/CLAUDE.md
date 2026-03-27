# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

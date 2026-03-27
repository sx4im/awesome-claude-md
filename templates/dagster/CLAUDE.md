# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

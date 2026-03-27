# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+
- DuckDB 1.x as the analytical SQL engine (embedded, no server)
- DuckDB Python client for all SQL execution
- PyArrow for zero-copy data interchange and Parquet I/O
- Jinja2 for SQL templating in complex queries
- pandas or Polars for final result manipulation when needed
- Ibis as optional DataFrame API over DuckDB
- pytest-duckdb fixtures for testing

## Project Structure

```
src/
├── main.py                    # CLI entry point for analysis runs
├── queries/
│   ├── staging/
│   │   ├── stg_orders.sql     # Staging query for orders
│   │   └── stg_customers.sql  # Staging query for customers
│   ├── marts/
│   │   ├── revenue.sql        # Revenue aggregation
│   │   └── cohorts.sql        # Cohort analysis
│   └── ad_hoc/
│       └── exploration.sql    # Scratch queries
├── pipeline/
│   ├── connection.py          # DuckDB connection factory
│   ├── loader.py              # Data ingestion (Parquet, CSV, S3)
│   ├── runner.py              # Query execution and result handling
│   └── exporter.py            # Result export (Parquet, CSV, Excel)
├── macros/
│   ├── date_spine.sql         # Reusable date spine macro
│   └── deduplicate.sql        # Deduplication macro
├── schemas/
│   └── tables.py              # CREATE TABLE/VIEW DDL statements
├── utils/
│   ├── config.py              # Data paths, S3 buckets, defaults
│   └── logging.py             # Query timing and logging
├── data/
│   ├── raw/                   # Source Parquet/CSV files
│   └── output/                # Analysis output files
├── notebooks/
│   └── exploration.ipynb      # Jupyter notebooks using DuckDB
└── tests/
    ├── conftest.py            # DuckDB in-memory fixtures
    ├── test_staging.py
    └── test_marts.py
```

## Architecture Rules

- Use a single DuckDB connection per process, created via `connection.py` factory function; never create ad-hoc connections in query files.
- Store all SQL in `.sql` files under `queries/`; Python code reads and executes these files, never constructs SQL strings inline.
- Organize queries in staging/marts layers: staging queries clean raw data, marts queries build business logic on top of staging views.
- Use DuckDB `CREATE OR REPLACE VIEW` for staging layers and `CREATE OR REPLACE TABLE` for materialized marts.
- Read Parquet files directly with `read_parquet()` and CSV with `read_csv_auto()`; avoid loading into pandas first.
- For S3/GCS access, configure DuckDB extensions (`httpfs`, `aws`) at connection time in `connection.py`.

## Coding Conventions

- Write SQL in uppercase keywords, lowercase identifiers: `SELECT order_id FROM staging.orders WHERE status = 'active'`.
- Use CTEs liberally for readability; avoid nested subqueries deeper than one level.
- Parameterize queries with `$1, $2` positional params or named `$param` syntax via DuckDB prepared statements.
- In Python, always use `conn.execute(sql, params).fetchdf()` for parameterized queries; never use f-strings for SQL interpolation.
- Name views and tables with layer prefix: `stg_orders`, `mart_revenue_daily`.
- Use `QUALIFY` clause with window functions instead of wrapping in a subquery.

## Library Preferences

- DuckDB native `read_parquet()` and `read_csv_auto()` for file ingestion; not pandas `read_csv`.
- PyArrow Tables as the interchange format between DuckDB and other tools via `conn.execute().fetch_arrow_table()`.
- Jinja2 for SQL templating only when queries need dynamic column lists or conditional clauses; prefer static SQL otherwise.
- DuckDB `COPY ... TO` for export to Parquet, CSV, or JSON; avoid writing custom export logic.

## File Naming

- SQL files: snake_case matching the view or table name they create (`stg_orders.sql`).
- Python pipeline files: action-based naming (`loader.py`, `runner.py`, `exporter.py`).
- Test files: `test_` prefix followed by the query layer name.

## NEVER DO THIS

1. Never construct SQL queries with Python f-strings or string concatenation; always use parameterized queries or Jinja2 templates.
2. Never open multiple DuckDB connections to the same database file; DuckDB has a single-writer model and concurrent connections cause locking errors.
3. Never load a large CSV into pandas and then insert into DuckDB; use `read_csv_auto()` directly for orders-of-magnitude better performance.
4. Never use `SELECT *` in production queries; list columns explicitly for schema stability.
5. Never skip the staging layer; raw data should always pass through a staging view before mart queries reference it.
6. Never store intermediate results as pandas DataFrames between SQL steps; use DuckDB views or CTEs to keep computation in the engine.

## Testing

- Use an in-memory DuckDB connection (`duckdb.connect()`) for all tests; never touch disk.
- Create small fixture tables in `conftest.py` with `conn.execute("CREATE TABLE ... AS SELECT ...")` from literal values.
- Test each SQL query file by loading it, executing against fixtures, and asserting row counts and column values.
- Test parameterized queries with multiple parameter sets to verify correctness.
- Assert output schema (column names and types) using `conn.execute(sql).description`.
- Integration test: run the full staging -> mart pipeline on a 100-row fixture dataset and validate final output.

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+
- Polars 1.x as the primary DataFrame library (never pandas for new code)
- Polars lazy API for all multi-step transformations
- PyArrow for Parquet I/O and Arrow IPC interchange
- DuckDB for ad-hoc SQL queries on Polars DataFrames when SQL is clearer
- connectorx for fast database reads into Polars
- Great Expectations or Pandera (polars backend) for data validation
- pytest with Polars assertion helpers for testing

## Project Structure

```
src/
├── main.py                    # CLI entry point for pipeline runs
├── pipelines/
│   ├── ingest.py              # Raw data ingestion (CSV, Parquet, DB)
│   ├── transform.py           # Core transformation logic (lazy frames)
│   ├── aggregate.py           # Aggregation and summary statistics
│   └── export.py              # Output writing (Parquet, CSV, DB)
├── expressions/
│   ├── dates.py               # Reusable date/time expressions
│   ├── strings.py             # String cleaning expressions
│   ├── numeric.py             # Numeric binning, rounding expressions
│   └── validators.py          # Data quality check expressions
├── schemas/
│   ├── raw.py                 # Schema definitions for raw input data
│   └── cleaned.py             # Schema definitions for cleaned output
├── utils/
│   ├── io.py                  # File path resolution and glob helpers
│   ├── logging.py             # Structured logging setup
│   └── config.py              # Pipeline configuration constants
├── data/
│   ├── raw/                   # Raw input files (gitignored)
│   └── processed/             # Output files (gitignored)
└── tests/
    ├── conftest.py            # Small fixture LazyFrames and DataFrames
    ├── test_transform.py
    ├── test_expressions.py
    └── test_aggregate.py
```

## Architecture Rules

- Build all transformation chains using `LazyFrame` and call `.collect()` only at pipeline boundaries (read -> transform -> write).
- Define reusable column expressions as functions returning `pl.Expr` in the `expressions/` directory; never inline complex expressions in pipeline code.
- Schemas must be defined as `dict[str, pl.DataType]` in `schemas/` and enforced with `.cast()` at ingestion time.
- Each pipeline step is a function taking a `pl.LazyFrame` and returning a `pl.LazyFrame`; steps compose via method chaining or sequential calls.
- Never convert to pandas; if a library requires pandas input, use `.to_pandas()` at the boundary and document why.
- Use `pl.scan_parquet()` and `pl.scan_csv()` to leverage predicate and projection pushdown.

## Coding Conventions

- Prefer `pl.col("name")` over `df["name"]` for all column references in expressions.
- Use `.with_columns()` for adding or transforming columns, never `.apply()` or `.map_elements()` unless calling non-vectorizable external code.
- Chain `.filter()`, `.with_columns()`, `.group_by().agg()` in a single lazy pipeline; avoid intermediate `.collect()` calls.
- Use `pl.when().then().otherwise()` for conditional logic, never Python if/else with scalar extraction.
- Name computed columns descriptively: `revenue_rolling_7d`, `user_count_distinct`, `is_active_flag`.
- Always specify `schema_overrides` when scanning CSVs to prevent type inference surprises.

## Library Preferences

- Polars native I/O (`scan_parquet`, `scan_csv`, `sink_parquet`) over PyArrow direct calls.
- connectorx for database reads: `pl.read_database_uri()` with connectorx engine.
- DuckDB integration via `duckdb.sql("SELECT ... FROM df")` only for complex window functions that are clearer in SQL.
- hvPlot or Altair for quick visualization of Polars DataFrames; do not convert to pandas for plotting.

## File Naming

- Pipeline step files: verb describing the action (`ingest.py`, `transform.py`, `aggregate.py`).
- Expression files: domain grouping in snake_case (`dates.py`, `strings.py`).
- Schema files: data stage name (`raw.py`, `cleaned.py`).

## NEVER DO THIS

1. Never use `.apply()` or `.map_elements()` with a Python lambda for operations achievable with Polars expressions; it disables vectorization and is orders of magnitude slower.
2. Never call `.collect()` in the middle of a transformation chain; keep the pipeline lazy until the final output step.
3. Never use `df[0, "col"]` for scalar extraction in a loop; use `.group_by().agg()` or `.over()` for grouped operations.
4. Never import pandas for data manipulation; use Polars expressions for all transformations.
5. Never rely on CSV type inference for production data; always provide `schema_overrides` or `dtypes`.
6. Never use positional column indexing (`df[:, 2]`); always reference columns by name.
7. Never mutate a DataFrame in place; Polars DataFrames are immutable, so always assign the result.

## Testing

- Test transformation functions by building small `pl.LazyFrame` fixtures (3-5 rows) with `pl.LazyFrame({"col": [values]})`.
- Assert output schemas match expected column names and types using `frame.collect_schema()`.
- Test expression functions by applying them to a single-column DataFrame and comparing with `assert_frame_equal`.
- Use `pytest.approx` for floating point comparisons in aggregation tests.
- Test lazy pipeline correctness by comparing `.collect()` output against a hand-computed expected DataFrame.
- Performance regression tests: assert that a 1M-row synthetic pipeline completes under 5 seconds.

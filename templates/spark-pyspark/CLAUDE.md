# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+
- Apache Spark 3.5+ with PySpark
- Delta Lake 3.x for ACID table storage
- Structured Streaming for real-time data pipelines
- Spark SQL for declarative transformations
- Hive Metastore or Unity Catalog for table metadata
- pytest-spark for testing with local SparkSession
- Poetry or pip-tools for Python dependency management

## Project Structure

```
src/
├── main.py                       # Entry point: SparkSession init and job dispatch
├── jobs/
│   ├── batch/
│   │   ├── ingest_raw.py         # Raw data ingestion job
│   │   ├── transform_silver.py   # Bronze-to-silver transformation
│   │   └── aggregate_gold.py     # Silver-to-gold aggregation
│   └── streaming/
│       ├── kafka_ingest.py       # Kafka to bronze streaming job
│       └── enrichment.py         # Stream enrichment with static join
├── transformations/
│   ├── cleaning.py               # Data cleaning functions (DataFrame -> DataFrame)
│   ├── enrichment.py             # Join and lookup transformations
│   ├── aggregations.py           # Window functions and group-by logic
│   └── schema.py                 # StructType schema definitions
├── io/
│   ├── readers.py                # Parameterized read functions (Delta, Parquet, Kafka)
│   ├── writers.py                # Parameterized write functions with merge logic
│   └── sources.py                # Source path and table name constants
├── quality/
│   ├── expectations.py           # Data quality check functions
│   └── quarantine.py             # Bad record quarantine logic
├── utils/
│   ├── session.py                # SparkSession builder with standard config
│   ├── logging.py                # Spark log4j logging wrapper
│   └── config.py                 # Job configuration loader (YAML/env vars)
├── configs/
│   ├── dev.yaml                  # Dev cluster and path config
│   └── prod.yaml                 # Prod cluster and path config
└── tests/
    ├── conftest.py               # Shared SparkSession fixture
    ├── test_cleaning.py
    ├── test_aggregations.py
    └── test_readers.py
```

## Architecture Rules

- Follow the medallion architecture: bronze (raw), silver (cleaned), gold (aggregated). Each layer writes to Delta Lake tables.
- Every transformation function takes a `DataFrame` and returns a `DataFrame`; never access SparkSession or read/write data inside transformation functions.
- Schema definitions must be explicit `StructType` objects in `transformations/schema.py`; never rely on schema inference for production reads.
- SparkSession creation happens once in `utils/session.py` and is passed to all jobs; never call `SparkSession.builder.getOrCreate()` in multiple places.
- Streaming jobs must define explicit watermarks and output modes; never use `append` mode without a watermark on the event time column.
- All writes to Delta tables must use `MERGE INTO` (upsert) or `INSERT OVERWRITE` by partition; never use plain append for idempotency.

## Coding Conventions

- Use DataFrame API over raw SQL for transformations; use `spark.sql()` only for complex window expressions that are more readable in SQL.
- Chain transformations with `.transform()`: `df.transform(clean_nulls).transform(add_timestamps).transform(validate_schema)`.
- Column references use `F.col("name")` from `pyspark.sql.functions as F`; never use string-based column access in transformations.
- Partition Delta tables by date: `.partitionBy("event_date")` for time-series data.
- Set `spark.sql.shuffle.partitions` based on data size: 200 for large batch, 8 for small datasets and tests.
- Use `F.when().otherwise()` for conditional columns; never use UDFs for logic expressible with built-in functions.

## Library Preferences

- Delta Lake for all persistent table storage; do not use plain Parquet for tables that receive updates.
- Structured Streaming over Spark Streaming DStreams; DStreams are deprecated.
- Built-in `pyspark.sql.functions` over UDFs whenever possible; UDFs disable Catalyst optimization.
- YAML configuration files over command-line arguments for job parameters.
- log4j via PySpark's `_jvm.org.apache.log4j` for logging, not Python `logging` module in driver code.

## File Naming

- Job files: `<verb>_<layer>.py` describing the action and target layer (`ingest_raw.py`, `transform_silver.py`).
- Transformation files: domain-grouped snake_case (`cleaning.py`, `aggregations.py`).
- Config files: environment name (`dev.yaml`, `prod.yaml`).

## NEVER DO THIS

1. Never use Python UDFs for operations available in `pyspark.sql.functions`; UDFs serialize data to Python and back, destroying performance.
2. Never call `.collect()` or `.toPandas()` on large DataFrames; these pull all data to the driver and cause out-of-memory crashes.
3. Never rely on schema inference (`inferSchema=True`) for production data; always provide explicit `StructType` schemas.
4. Never use `repartition()` without reason; prefer `coalesce()` for reducing partitions and `repartition()` only before writes that need balanced partition sizes.
5. Never use `foreach` or `forEachBatch` with external API calls without rate limiting and error handling.
6. Never skip watermarking in streaming joins; without watermarks, state grows unbounded and crashes the job.
7. Never hardcode file paths; use configuration files that vary by environment.

## Testing

- Use a module-scoped `SparkSession` fixture in `conftest.py` with `spark.sql.shuffle.partitions=2` and `local[2]` master for speed.
- Test transformation functions with small hand-built DataFrames (3-10 rows) created via `spark.createDataFrame(data, schema)`.
- Assert output schemas with `df.schema == expected_schema` and row counts with `df.count()`.
- Test Delta write/read round-trips using `tmp_path` fixture for a temporary Delta table directory.
- Test streaming jobs with `spark.readStream.format("rate")` as a synthetic source and `format("memory")` as a test sink.
- Never test against a real cluster in unit tests; use local mode exclusively.

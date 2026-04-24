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

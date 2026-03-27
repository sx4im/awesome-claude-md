# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- ClickHouse 24.x with ReplicatedMergeTree for production, MergeTree for development
- Python 3.11+ with clickhouse-connect 0.7.x as the primary client (HTTP interface)
- dbt-clickhouse for transformation layer and materialized view management
- Apache Superset or Metabase for dashboarding connected via the ClickHouse JDBC driver
- Protobuf for ingest message schemas, Kafka engine tables for streaming ingestion
- pytest with ClickHouse testcontainers for integration tests

## Project Structure

```
src/
  ingest/
    kafka_consumers.py       # Kafka engine table definitions
    batch_loader.py          # CSV/Parquet bulk insert via clickhouse-connect
    stream_processor.py      # Real-time event processing
  schemas/
    events.sql               # CREATE TABLE statements
    materialized_views.sql   # MV definitions with target tables
    dictionaries.sql         # Dictionary definitions (flat, hashed, complex_key)
    migrations/
      001_create_events.sql
      002_add_mv_daily_stats.sql
  queries/
    dashboards/
      daily_active_users.sql
      revenue_by_region.sql
      funnel_analysis.sql
    ad_hoc/
      cohort_retention.sql
  transforms/
    dbt_project/
      models/
        staging/
        intermediate/
        marts/
  config/
    cluster.py               # Connection settings, cluster topology
    settings.py              # ClickHouse server settings overrides
  utils/
    query_runner.py           # Parameterized query execution wrapper
    partition_manager.py      # TTL and partition drop utilities
tests/
  test_queries/
  test_ingest/
  fixtures/
```

## Architecture Rules

- Use ReplicatedMergeTree with a partition key based on event date (usually `toYYYYMM(event_date)`). Never partition by high-cardinality columns like user_id.
- Materialized views must write to explicit target tables (`TO target_table`), not use the implicit `.inner` table. This allows independent schema evolution.
- All dictionaries sourced from external databases must have a `LIFETIME(MIN 300 MAX 600)` to auto-refresh. Use `dictGet()` in queries, never join against the source table.
- Ingest data through Kafka engine tables with a materialized view that transforms and writes to the final MergeTree table. The Kafka table is the consumer, the MV is the transform, and the MergeTree is the store.
- Use AggregatingMergeTree with `-State`/`-Merge` combinators for pre-aggregated rollup tables. Define `AggregateFunction(sum, UInt64)` columns, not plain `UInt64`.
- TTL rules must be defined at the table level for data lifecycle management. Production tables retain raw data for 90 days and aggregated data for 2 years.

## Coding Conventions

- Write all SQL in uppercase keywords with lowercase identifiers: `SELECT user_id FROM events WHERE event_date = today()`.
- Always use parameterized queries via clickhouse-connect's `query()` method with the `parameters` dict. Never format strings into SQL.
- Use `LowCardinality(String)` for columns with fewer than 10,000 distinct values (country, browser, status). This reduces storage by 5-10x.
- Define `ORDER BY` clauses to match the most common query filter patterns. The primary key is the prefix of the `ORDER BY` columns.
- Use `FINAL` keyword sparingly; prefer `GROUP BY` with `argMax()` for deduplication in queries.
- Comment every materialized view with its purpose, refresh behavior, and downstream dependencies.

## Library Preferences

- clickhouse-connect over clickhouse-driver (HTTP is more firewall-friendly and supports compression)
- dbt-clickhouse for transformation pipelines over raw SQL scripts
- Apache Superset over Grafana for ClickHouse dashboards (better SQL editor, native ClickHouse support)
- Protobuf over JSON for Kafka message serialization into ClickHouse

## File Naming

- SQL files use snake_case: `daily_active_users.sql`, `create_events.sql`
- Migration files are numbered sequentially: `001_description.sql`, `002_description.sql`
- Python files use snake_case: `kafka_consumers.py`, `partition_manager.py`

## NEVER DO THIS

1. Never use `ALTER TABLE DELETE` or `ALTER TABLE UPDATE` for routine operations. These are expensive mutations that rewrite parts. Use TTL or ReplacingMergeTree for data lifecycle.
2. Never create a table without specifying `ORDER BY`. ClickHouse performance depends entirely on the sort order matching query patterns.
3. Never use `SELECT *` in production queries. Always list columns explicitly to avoid reading unnecessary data from disk.
4. Never use `String` type for columns that are always numeric. Use `UInt32`, `Float64`, or `Decimal` for proper compression and arithmetic.
5. Never run `OPTIMIZE TABLE FINAL` in production during peak hours. This forces a merge of all parts and blocks inserts.
6. Never insert data row-by-row. Batch inserts with a minimum of 1,000 rows per insert to avoid creating too many parts.
7. Never use `JOIN` with large tables on both sides without ensuring the right table fits in memory. Use `dictGet()` or `IN` subqueries instead.

## Testing

- Use testcontainers with the official ClickHouse Docker image for integration tests. Create tables in `beforeAll`, insert fixture data, run queries, drop tables in `afterAll`.
- Test materialized views by inserting data into the source table and asserting the target table contains the expected aggregated rows.
- Test dictionary lookups by loading fixture data into the dictionary source table and verifying `dictGet()` returns correct values.
- Validate query performance by running `EXPLAIN PIPELINE` and asserting that index pruning eliminates at least 90% of granules for filtered queries.
- Test partition management utilities by creating tables with TTL, inserting old data, and verifying `SYSTEM STOP MERGES` / `ALTER TABLE DROP PARTITION` behavior.
- Every dbt model must have a schema test for uniqueness and not-null on key columns.

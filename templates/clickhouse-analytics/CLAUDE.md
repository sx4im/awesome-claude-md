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

## Production Delivery Playbook (Category: Database & Messaging)

### Release Discipline
- Protect data correctness with transactional boundaries and idempotent consumers.
- Preserve migration safety (forward + rollback) for schema/index changes.
- Handle poison messages and dead-letter routing explicitly.

### Merge/Release Gates
- Migration dry-run reviewed; no destructive change without backup plan.
- Consumer/producer contract tests pass.
- Data integrity checks and replay strategy documented.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

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

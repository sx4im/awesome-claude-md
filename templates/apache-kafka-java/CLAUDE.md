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

- Apache Kafka 3.7+ with KRaft mode (no ZooKeeper dependency)
- Java 21 with Kafka Clients 3.7.x for producers and consumers
- Kafka Streams 3.7.x for stateful stream processing applications
- Confluent Schema Registry with Avro serialization (io.confluent:kafka-avro-serializer)
- Gradle 8.x with the Kotlin DSL for build configuration
- JUnit 5 with TopologyTestDriver for Kafka Streams unit tests
- Testcontainers with the Confluent Kafka module for integration tests

## Project Structure

```
src/
  main/
    java/com/project/
      producer/
        EventProducer.java           # Generic Avro producer with callbacks
        PartitionStrategy.java       # Custom partitioner implementations
      consumer/
        EventConsumer.java           # Poll loop with graceful shutdown
        DeserializationHandler.java  # Dead-letter routing for bad records
      streams/
        TopologyBuilder.java         # Kafka Streams topology definition
        processors/
          EnrichmentProcessor.java   # Stateful KV store lookups
          AggregationProcessor.java  # Windowed aggregations
        serdes/
          CustomSerdes.java          # Avro + JSON serde factories
      config/
        KafkaConfig.java             # Centralized producer/consumer config
        StreamsConfig.java           # Streams-specific configuration
      model/
        avro/                        # Generated Avro classes (build output)
    resources/
      avro/
        user-event.avsc
        order-event.avsc
      application.properties
  test/
    java/com/project/
      streams/
        TopologyTest.java
      producer/
        EventProducerTest.java
      integration/
        KafkaIntegrationTest.java
```

## Architecture Rules

- All messages use Avro schemas registered in Schema Registry. Never use plain JSON or String serialization in production topics.
- Producers must set `acks=all`, `enable.idempotence=true`, and `retries=Integer.MAX_VALUE` for exactly-once semantics. These are non-negotiable for data integrity.
- Consumers must commit offsets manually after successful processing. Set `enable.auto.commit=false` and call `commitSync()` after each batch.
- Kafka Streams applications must use a unique `application.id` per logical application. State stores use RocksDB by default; configure `state.dir` to a persistent volume.
- Use the Schema Registry subject naming strategy `TopicRecordNameStrategy` to allow multiple schemas per topic. Configure this in producer and consumer properties.
- Dead-letter topics follow the naming convention `{original-topic}.DLT`. Every consumer group must route unprocessable records to a DLT instead of dropping them.
- Topic naming convention: `{domain}.{entity}.{event-type}`, e.g., `orders.payment.completed`. Use dots, not dashes.

## Coding Conventions

- Use `try-with-resources` for all Producer and Consumer instances. They implement `Closeable` and must be closed to flush buffers.
- Producer callbacks must log failures at ERROR level and increment a Micrometer counter for monitoring. Never silently ignore send failures.
- Consumer poll loops must handle `WakeupException` for graceful shutdown. Register a shutdown hook that calls `consumer.wakeup()`.
- Kafka Streams processors must be stateless functions where possible. Use `Materialized.as()` with named state stores only when aggregation or joining requires it.
- Configuration values come from `application.properties` loaded via a custom `KafkaConfig` class. Never hardcode broker addresses or topic names.
- Use `KafkaTemplate` only in Spring Boot projects. For plain Java applications, use the raw `KafkaProducer` and `KafkaConsumer` clients.

## Library Preferences

- Confluent Avro Serializer over custom serializers for schema evolution support
- Kafka Streams over Apache Flink for stream processing within the Kafka ecosystem
- Micrometer with Prometheus registry for Kafka client metrics export
- Testcontainers (ConfluentKafkaContainer) over EmbeddedKafka for integration tests
- Gradle over Maven for build tooling

## File Naming

- Java classes use PascalCase: `EventProducer.java`, `TopologyBuilder.java`
- Avro schemas use kebab-case: `user-event.avsc`, `order-event.avsc`
- Configuration files use kebab-case: `application.properties`, `log4j2.xml`
- Test classes mirror source with `Test` suffix: `TopologyBuilderTest.java`

## NEVER DO THIS

1. Never set `auto.offset.reset=latest` without understanding the data loss implications. Use `earliest` for consumers that must process all historical data.
2. Never produce messages without a key when ordering matters. Kafka guarantees ordering only within a partition, and keys determine partition assignment.
3. Never increase partition count on a topic that uses key-based routing. This changes the key-to-partition mapping and breaks ordering guarantees.
4. Never use `consumer.seek()` to skip messages without logging the skipped offset range. This makes debugging data gaps impossible.
5. Never use `Thread.sleep()` in consumer poll loops for backpressure. Use `pause()` and `resume()` on topic partitions instead.
6. Never deploy Schema Registry without compatibility mode set. Use `BACKWARD` compatibility as the default for all subjects.
7. Never run Kafka Streams with `processing.guarantee=exactly_once` without also configuring `transaction.timeout.ms` appropriate to your processing latency.

## Testing

- Use `TopologyTestDriver` for unit testing Kafka Streams topologies. It runs the topology in-memory without a broker, verifying input/output records.
- Use `MockProducer` and `MockConsumer` from the Kafka clients library for unit testing producer/consumer logic without a broker.
- Integration tests use Testcontainers to start a Kafka broker and Schema Registry. Wait for `AdminClient.describeCluster()` to succeed before running tests.
- Test schema evolution by registering a v1 schema, producing records, evolving to v2, and verifying that old consumers can still deserialize with `BACKWARD` compatibility.
- Test consumer rebalancing by starting two consumer instances in the same group and verifying partition assignment changes when one instance is stopped.
- Verify dead-letter routing by sending a message with an incompatible schema and asserting it appears on the `.DLT` topic.

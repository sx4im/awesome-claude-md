# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- RabbitMQ 3.13+ with the management plugin enabled for monitoring
- Node.js 20 LTS with amqplib 0.10.x as the AMQP 0-9-1 client
- TypeScript 5.x with strict mode for all application code
- Zod for message payload validation before publishing and after consuming
- Winston for structured logging with correlation IDs through message headers
- Jest for unit tests, Testcontainers for integration tests with RabbitMQ
- pnpm for package management

## Project Structure

```
src/
  connection/
    manager.ts             # Connection and channel lifecycle management
    topology.ts            # Exchange, queue, and binding declarations
    heartbeat.ts           # Connection health monitoring
  producers/
    base.producer.ts       # Abstract producer with confirm mode
    order.producer.ts      # Order event publisher
    notification.producer.ts
  consumers/
    base.consumer.ts       # Abstract consumer with prefetch and retry
    order.consumer.ts      # Order event handler
    notification.consumer.ts
    strategies/
      retry.strategy.ts    # Exponential backoff via dead-letter exchanges
      dlq.strategy.ts      # Dead-letter queue processing
  exchanges/
    definitions.ts         # Exchange name constants and types
  schemas/
    order-events.schema.ts # Zod schemas for order message payloads
    notification.schema.ts
  config/
    rabbitmq.config.ts     # Connection URI, prefetch, retry settings
  utils/
    correlation.ts         # Correlation ID generation and propagation
    serialization.ts       # JSON serialization with Date handling
tests/
  unit/
  integration/
  fixtures/
```

## Architecture Rules

- Use topic exchanges as the default exchange type. Direct exchanges only for simple point-to-point routing. Fanout exchanges only for broadcast scenarios with no filtering.
- Every queue must have a dead-letter exchange (`x-dead-letter-exchange`) and dead-letter routing key configured. Failed messages must never be silently dropped.
- Implement retry with exponential backoff using a chain of dead-letter exchanges with per-message TTL. Three retry queues: `{queue}.retry.1` (5s), `{queue}.retry.2` (30s), `{queue}.retry.3` (300s).
- Use publisher confirms (confirm mode) for all producers. Call `channel.waitForConfirms()` or handle the `confirm` event before considering a message published.
- Set `prefetch` (QoS) to a value between 10 and 50 per consumer. Never use unlimited prefetch; it causes memory exhaustion under load.
- All messages must include these headers: `correlationId`, `timestamp`, `messageType`, `version`. This enables tracing and schema evolution.
- Declare all topology (exchanges, queues, bindings) at application startup in a single `topology.ts` file. Never declare queues lazily on first publish.

## Coding Conventions

- Use one channel per producer and one channel per consumer. Never share channels between producers and consumers.
- Always acknowledge messages explicitly with `channel.ack(msg)` after successful processing. Use `channel.nack(msg, false, false)` to dead-letter a message (do not requeue).
- Serialize message bodies as JSON with `Buffer.from(JSON.stringify(payload))`. Validate with Zod on both publish and consume boundaries.
- Handle the `close` and `error` events on both connection and channel objects. Implement automatic reconnection with exponential backoff starting at 1 second, capping at 30 seconds.
- Use `x-message-deduplication` header with a UUID to enable idempotent consumers. Check for duplicates using a Redis set with a 1-hour TTL before processing.
- Naming conventions for exchanges: `{domain}.events` (topic), `{domain}.commands` (direct). For queues: `{service}.{action}`.

## Library Preferences

- amqplib over rascal or rabbit.js (amqplib is the most maintained and lowest-level)
- Zod over Joi for message schema validation
- Winston over pino for logging (better transport ecosystem for RabbitMQ correlation)
- Testcontainers over mock AMQP servers for integration tests
- node-cron for scheduled queue maintenance tasks

## File Naming

- All files use kebab-case with dot-separated type suffix: `order.producer.ts`, `retry.strategy.ts`
- Schema files end with `.schema.ts`: `order-events.schema.ts`
- Test files mirror source structure: `tests/unit/producers/order.producer.test.ts`

## NEVER DO THIS

1. Never publish messages without confirm mode enabled. Unconfirmed publishes can be silently lost if the broker restarts or the connection drops.
2. Never use `noAck: true` (auto-ack) for consumers that process messages with side effects. Always manually acknowledge after the operation completes.
3. Never requeue a message indefinitely with `channel.nack(msg, false, true)`. This creates an infinite retry loop that consumes CPU and fills logs.
4. Never create exclusive or auto-delete queues for durable workloads. These are only appropriate for temporary reply queues in RPC patterns.
5. Never set message TTL at the queue level when different messages need different TTLs. Use per-message TTL in the `expiration` property instead.
6. Never connect to RabbitMQ without setting the heartbeat interval. Use `heartbeat: 60` in the connection options to detect dead connections.

## Testing

- Use Testcontainers with the `rabbitmq:3-management` image for integration tests. Wait for the management API to respond at port 15672 before running tests.
- Unit test producers by mocking the amqplib channel and asserting that `publish()` is called with the correct exchange, routing key, and headers.
- Unit test consumers by creating a mock message object and calling the handler function directly. Assert acknowledgment calls.
- Integration tests must verify the full dead-letter chain: publish a message that will fail processing, assert it appears in the retry queues with increasing delays, and finally lands in the DLQ.
- Test topology declarations by connecting to the management API and verifying exchanges, queues, and bindings exist after startup.
- Test connection recovery by stopping and restarting the RabbitMQ container during an active consumer test and verifying messages are processed after reconnection.

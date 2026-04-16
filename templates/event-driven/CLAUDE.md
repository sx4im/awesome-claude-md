# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Event-Driven Architecture
- Event bus (Kafka, RabbitMQ, EventBridge)
- TypeScript/Python/Go
- Event schema validation
- Async message processing

## Project Structure
```
src/
├── events/                     // Event definitions
│   ├── types/
│   │   └── order-events.ts
│   ├── schema/
│   │   └── order-created.json
│   └── serializers/
│       └── avro.ts
├── producers/                  // Event publishers
│   └── order-producer.ts
├── consumers/                  // Event subscribers
│   ├── email-consumer.ts
│   └── inventory-consumer.ts
└── lib/
    └── event-bus.ts            // Message broker client
```

## Architecture Rules

- **Events as API contracts.** Schema is the contract between services.
- **Async decoupling.** Producers don't know consumers.
- **Event schema versioning.** Events evolve—version schemas.
- **At-least-once delivery.** Idempotent consumers handle duplicates.

## Coding Conventions

- Event: `interface OrderCreated { eventId; timestamp; correlationId; version: 1; payload: { orderId, customerId, amount } }`.
- Publish: `await eventBus.publish('orders.created', orderCreatedEvent)`.
- Subscribe: `eventBus.subscribe('orders.created', async (event) => { await sendEmail(event.payload) })`.
- Schema registry: Register Avro/JSON Schema for validation.

## NEVER DO THIS

1. **Never mix command and event names.** `CreateOrder` (command) vs `OrderCreated` (event).
2. **Never forget event versioning.** Always include version field.
3. **Never include sensitive data in events.** Filter PII from event payloads.
4. **Never process events without idempotency.** Expect duplicate delivery.
5. **Never ignore dead letter queues.** Failed events need handling.
6. **Never use events for synchronous requirements.** Events are async by nature.
7. **Never skip event schema validation.** Validate before publishing/consuming.

## Testing

- Test event schema compliance.
- Test producer publishes correct events.
- Test consumer handles events idempotently.
- Test dead letter queue behavior.


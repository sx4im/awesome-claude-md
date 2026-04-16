# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- CQRS (Command Query Responsibility Segregation)
- TypeScript/Python/Any language
- Event store (EventStoreDB, PostgreSQL)
- Read models (Redis, Elasticsearch)
- Message bus (RabbitMQ, Kafka)

## Project Structure
```
src/
├── commands/                   # Command handlers
│   ├── handlers/
│   │   └── create-order.ts
│   └── types/
│       └── create-order.ts
├── queries/                    # Query handlers
│   ├── handlers/
│   │   └── get-order.ts
│   └── types/
│       └── get-order.ts
├── events/                     # Domain events
│   └── order-created.ts
├── domain/                     # Aggregates
│   └── order.ts
├── projections/                # Read model builders
│   └── order-projection.ts
└── infrastructure/
    └── event-store.ts
```

## Architecture Rules

- **Separate write and read models.** Commands change state, queries return data.
- **Commands are intent.** Named as imperative: `CreateOrder`, `ShipOrder`.
- **Events are facts.** Immutable records of what happened: `OrderCreated`, `OrderShipped`.
- **Projections build read models.** Asynchronous denormalization for queries.

## Coding Conventions

- Command: `interface CreateOrderCommand { type: 'CreateOrder'; payload: { customerId, items } }`.
- Command handler: `async function handleCreateOrder(command: CreateOrderCommand, deps): Promise<void>`.
- Event: `interface OrderCreatedEvent { type: 'OrderCreated'; aggregateId; payload }`.
- Aggregate: `class Order { private events: DomainEvent[]; create(data) { this.apply(new OrderCreatedEvent(data)) } }`.
- Projection: `async function projectOrderCreated(event: OrderCreatedEvent) { await db.orders.create({ ...event.payload }) }`.

## NEVER DO THIS

1. **Never return data from commands.** Commands return void or commandId only.
2. **Never modify read models directly.** Always via projections from events.
3. **Never skip event versioning.** Events evolve—version them for backwards compatibility.
4. **Never ignore eventual consistency.** Read models lag behind writes—design for it.
5. **Never use CQRS for simple CRUD.** Adds complexity—only use when benefits justify.
6. **Never forget idempotency for projections.** Same event processed twice shouldn't corrupt data.
7. **Never mix command and query logic in same handler.** Keep them strictly separated.

## Testing

- Test command handlers verify business rules.
- Test aggregates emit correct events.
- Test projections update read models correctly.
- Test eventual consistency behavior.


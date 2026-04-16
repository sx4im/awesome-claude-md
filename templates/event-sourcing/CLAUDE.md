# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Event Sourcing (state as event stream)
- EventStoreDB or PostgreSQL
- TypeScript/Python
- Snapshots for performance
- Projections for queries

## Project Structure
```
src/
├── aggregates/                 # Domain aggregates
│   └── order.ts
├── events/                     # Domain events
│   ├── order-created.ts
│   └── order-shipped.ts
├── event-store/                # Event persistence
│   ├── client.ts
│   └── streams.ts
├── projections/                # Read models
│   └── order-summary.ts
└── snapshots/                  # Aggregate snapshots
    └── store.ts
```

## Architecture Rules

- **State from events.** Current state is fold/reduce of all past events.
- **Append-only event store.** Never delete or modify events.
- **Event stream per aggregate.** `order-123`, `user-456` as stream IDs.
- **Snapshots for performance.** Periodically save aggregate state to avoid replaying all events.

## Coding Conventions

- Event: `interface OrderCreated { eventId; aggregateId; version; timestamp; payload }`.
- Append: `await eventStore.append('order-123', [new OrderCreated(data)], expectedVersion)`.
- Read: `const events = await eventStore.readStream('order-123')`.
- Fold: `const order = events.reduce((state, event) => applyEvent(state, event), initialState)`.
- Snapshot: `await snapshotStore.save('order-123', version, orderState)`.

## NEVER DO THIS

1. **Never delete events.** Event store is immutable—deletion breaks the pattern.
2. **Never forget optimistic concurrency.** Include expected version when appending.
3. **Never store derived data in events.** Events record facts, not computed values.
4. **Never skip snapshotting for long streams.** Replaying 10,000 events per read is slow.
5. **Never use without understanding GDPR implications.** Right to erasure conflicts with immutable events.
6. **Never ignore event schema evolution.** Events live forever—plan for schema changes.
7. **Never mix event sourcing with CRUD carelessly.** Pick one pattern per aggregate.

## Testing

- Test event appending with concurrency.
- Test state reconstruction from events.
- Test snapshot save/restore.
- Test event schema migration.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Domain-Driven Design (DDD)
- TypeScript/Python/Java
- Bounded contexts, aggregates, entities
- Ubiquitous language focus
- Repository pattern

## Project Structure
```
src/
├── bounded-contexts/           # Separate contexts
│   ├── ordering/
│   │   ├── domain/
│   │   │   ├── aggregates/
│   │   │   │   └── order.ts    # Order aggregate root
│   │   │   ├── entities/
│   │   │   │   └── order-item.ts
│   │   │   └── value-objects/
│   │   │       └── address.ts
│   │   ├── application/
│   │   │   └── services/
│   │   └── infrastructure/
│   └── inventory/
│       └── ...
├── shared-kernel/              # Shared concepts
└── context-map.ts              # Context relationships
```

## Architecture Rules

- **Bounded contexts are boundaries.** Each context has its own ubiquitous language and model.
- **Aggregates enforce invariants.** Cluster of entities/value objects with aggregate root.
- **Entities have identity.** Distinguishable by ID, not attributes.
- **Value objects are immutable.** Compared by properties, not identity.
- **Ubiquitous language everywhere.** Code reflects domain terminology.

## Coding Conventions

- Aggregate root: `class Order { private id: OrderId; private items: OrderItem[]; addItem(item: OrderItem): void }`.
- Value object: `class Money { constructor(readonly amount: number, readonly currency: string) {} equals(other: Money): boolean }`.
- Entity ID: `type OrderId = Brand<string, 'OrderId'>` to prevent mixing IDs.
- Repository: `interface OrderRepository { findById(id: OrderId): Promise<Order | null>; save(order: Order): Promise<void> }`.
- Domain events: `domainEvents.push(new OrderSubmittedEvent(this.id))` from aggregate.

## NEVER DO THIS

1. **Never cross bounded context boundaries directly.** Use anti-corruption layer or integration events.
2. **Never modify aggregates directly from outside.** Use aggregate root methods.
3. **Never skip the ubiquitous language discussion.** Domain experts must agree on terms.
4. **Never make value objects mutable.** Immutability is key to their safety.
5. **Never expose internal aggregate state.** Return copies or DTOs, not direct references.
6. **Never use anemic domain models.** Models should have behavior, not just data.
7. **Never ignore context mapping.** Understand how contexts relate (shared kernel, customer-supplier, etc.).

## Testing

- Test aggregate invariants are enforced.
- Test value object equality correctly implemented.
- Test domain events are raised appropriately.


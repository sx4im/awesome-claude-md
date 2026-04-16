# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Hexagonal Architecture (Ports and Adapters)
- TypeScript/Python/Go
- Domain in center, adapters on edges
- Dependency injection
- Interface-driven design

## Project Structure
```
src/
├── domain/                     # Core business logic
│   ├── entities/
│   │   └── order.ts
│   ├── value-objects/
│   │   └── money.ts
│   └── services/
│       └── pricing-service.ts
├── ports/                      # Interfaces (driven and driving)
│   ├── driven/
│   │   └── for-order-repository.ts
│   └── driving/
│       └── for-creating-order.ts
├── adapters/                   # Implementations
│   ├── driven/
│   │   ├── postgres-order-repo.ts
│   │   └── stripe-payment.ts
│   └── driving/
│       └── http-order-controller.ts
└── config/
    └── wiring.ts               # DI configuration
```

## Architecture Rules

- **Domain has no external dependencies.** Core is pure business logic.
- **Ports are interfaces.** Define what the domain needs (driven) and offers (driving).
- **Adapters implement ports.** Concrete implementations of interfaces.
- **Dependency direction inward.** Adapters depend on domain, not vice versa.

## Coding Conventions

- Port (interface): `interface ForOrderRepository { save(order: Order): Promise<void>; findById(id: OrderId): Promise<Order | null> }`.
- Domain service: `class OrderService { constructor(private repo: ForOrderRepository, private payment: ForPayment) {} }`.
- Adapter: `class PostgresOrderRepository implements ForOrderRepository { ... }`.
- Wiring: `const repo = new PostgresOrderRepository(db); const service = new OrderService(repo, stripe)`.

## NEVER DO THIS

1. **Never let domain import adapters.** Only interfaces (ports) enter the domain.
2. **Never put framework code in domain.** No `@Entity`, no `req`, no `db` in domain.
3. **Never skip the interface abstraction.** Direct adapter coupling violates the pattern.
4. **Never create bidirectional dependencies.** Domain doesn't know about outer layers.
5. **Never ignore the testing benefit.** Mock ports easily for domain unit tests.
6. **Never use for simple CRUD apps.** The abstraction has overhead—use when beneficial.
7. **Never forget the primary port vs secondary distinction.** Driving vs driven differs.

## Testing

- Test domain logic with mocked ports.
- Test adapters in integration tests.
- Test wiring/dependency injection.


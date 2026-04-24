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

## Production Delivery Playbook (Category: Architecture & Domain Patterns)

### Release Discipline
- Preserve domain invariants and explicit command/query/event boundaries.
- Maintain idempotency and ordering guarantees in event-driven paths.
- Avoid coupling domain rules to transport/framework details.

### Merge/Release Gates
- Critical business invariants tested across happy and failure paths.
- Replay/rebuild behavior validated where events are source of truth.
- Backward compatibility verified for contracts and event schemas.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

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

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- PHP 8.3+ with strict types, readonly classes, and enums
- Symfony 7.1+ as the full-stack framework
- Doctrine ORM 3.x for database abstraction and entity mapping
- Symfony Messenger for async message handling and CQRS
- Twig 3.x for server-side HTML templating
- PostgreSQL 16 as the primary database
- Redis for cache (Symfony Cache) and Messenger transport
- PHPUnit 11 for testing with Symfony's WebTestCase
- PHPStan level 9 for static analysis

## Project Structure

```
src/
  Controller/
    Api/                    # JSON API controllers (returns JsonResponse)
    Web/                    # HTML controllers (returns Twig Response)
  Entity/                   # Doctrine ORM entities with PHP 8 attributes
  Repository/               # Doctrine repositories extending ServiceEntityRepository
  Message/
    Command/                # Write-side messages (CreateOrder, UpdateUser)
    Query/                  # Read-side messages (GetUserById, ListOrders)
    Event/                  # Domain events (OrderPlaced, UserRegistered)
  MessageHandler/
    Command/                # Command handlers, one per command
    Query/                  # Query handlers
    Event/                  # Event subscribers for side effects
  DTO/
    Request/                # Request DTOs with Symfony Validator constraints
    Response/               # Response DTOs for API serialization
  Service/                  # Domain services with business logic
  EventListener/            # Symfony kernel event listeners
  Security/
    Voter/                  # Access decision voters for authorization
config/
  packages/
    doctrine.yaml           # Doctrine connection and mapping config
    messenger.yaml          # Transport routing (sync, async, failed)
    security.yaml           # Firewall, providers, access control
  routes/
    api.yaml                # API route prefix /api
    web.yaml                # Web route definitions
migrations/                 # Doctrine migration files
templates/                  # Twig templates organized by controller
tests/
  Unit/                     # Pure unit tests, no container
  Integration/              # Tests with service container
  Functional/               # WebTestCase with HTTP client
```

## Architecture Rules

- Controllers are thin; inject a `MessageBusInterface` and dispatch Command/Query messages for all business logic
- Every write operation dispatches a Command message; every read dispatches a Query message (lightweight CQRS)
- Entities use PHP 8 attributes for Doctrine mapping: `#[ORM\Entity]`, `#[ORM\Column]`, `#[ORM\ManyToOne]`
- Entities are always created via named constructors or factory methods, never public property assignment
- Request DTOs use `#[Assert\NotBlank]`, `#[Assert\Email]` attributes; validated automatically via `#[MapRequestPayload]`
- Services are autowired and autoconfigured; use constructor promotion with `readonly` for all dependencies
- Messenger transports: `sync` for queries, `async` (Redis) for commands and events, `failed` for dead letter queue
- Domain events are dispatched from entities via `EventDispatcherInterface` or collected and dispatched post-flush

## Coding Conventions

- All classes declare `declare(strict_types=1)` at the top of every PHP file
- Use constructor property promotion with `readonly` for dependency injection in services and handlers
- Entities use private setters; expose state changes through domain methods: `$order->markAsShipped()` not `$order->setStatus('shipped')`
- Repositories return typed results: `findOneById(Uuid $id): ?User` not generic `find($id)`
- API controllers return `JsonResponse` with Symfony Serializer; use DTO classes, never serialize entities directly
- Use `Uuid` from `symfony/uid` for entity identifiers, not auto-increment integers
- Routes defined via PHP attributes: `#[Route('/api/users', methods: ['GET'])]`
- Enum classes for all fixed value sets: `OrderStatus::Pending`, `UserRole::Admin`

## Library Preferences

- Symfony Messenger over RabbitMQ direct or custom event bus implementations
- Doctrine ORM over Eloquent or raw PDO for database access
- Symfony Serializer over JMS Serializer for DTO serialization
- Symfony Validator over custom validation logic for request validation
- Symfony Security voters over role hierarchy for fine-grained authorization
- PHPStan (level 9) + phpstan-symfony + phpstan-doctrine for static analysis
- symfony/uid over ramsey/uuid for UUID generation
- Symfony Mailer over SwiftMailer for email delivery

## File Naming

- PHP classes: PascalCase matching the class name, one class per file
- Entity files: singular noun, e.g., `User.php`, `Order.php`, `OrderItem.php`
- Command/Query messages: imperative verb phrase, e.g., `CreateOrder.php`, `GetUserById.php`
- Handlers: message name + `Handler` suffix, e.g., `CreateOrderHandler.php`
- Twig templates: snake_case `.html.twig`, organized by controller name
- Config: kebab-case `.yaml` in `config/packages/`

## NEVER DO THIS

1. Never inject `EntityManagerInterface` into controllers; use Messenger bus or dedicated repository methods
2. Never serialize Doctrine entities directly to JSON responses; always map to Response DTOs to avoid lazy-load issues and data leaks
3. Never put business logic in controllers or event listeners; dispatch messages and handle in dedicated handler classes
4. Never use Doctrine's `ArrayCollection` methods for filtering in PHP; use DQL or QueryBuilder for database-side filtering
5. Never use `public` properties on entities; use getter methods and domain-specific mutation methods
6. Never suppress PHPStan errors with `@phpstan-ignore`; fix the type issue or add proper type annotations
7. Never use `container->get()` for service location; rely on constructor injection and autowiring

## Testing

- Unit tests for message handlers: mock repository interfaces, assert side effects and return values
- Integration tests boot the Symfony kernel; use `KernelTestCase` to test services with real container wiring
- Functional tests use `WebTestCase` with `$client->request('GET', '/api/users')` for full HTTP stack testing
- Doctrine tests use a SQLite in-memory database configured in `config/packages/test/doctrine.yaml`
- Test Messenger handlers by dispatching messages to the bus and asserting transport contents with `TransportInterface::get()`
- Factories for test data use `zenstruck/foundry` with Doctrine entity factories
- Run PHPStan in CI: `vendor/bin/phpstan analyse src tests --level 9` with zero errors policy
- Code coverage gate: minimum 80% line coverage enforced in CI with `--coverage-clover`

# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- PHP 8.2+
- Laravel 11.x
- Eloquent ORM + PostgreSQL or MySQL
- Laravel Queues (Redis or database driver)
- Blade templates or Inertia.js + Vue/React for frontend
- Deployed on Forge, Vapor, or Docker

## Project Structure

```
app/
├── Http/
│   ├── Controllers/         # Thin controllers — calls actions, returns responses
│   │   ├── UserController.php
│   │   └── OrderController.php
│   ├── Requests/            # Form request validation classes
│   │   ├── StoreUserRequest.php
│   │   └── UpdateOrderRequest.php
│   ├── Resources/           # API resource transformations
│   │   ├── UserResource.php
│   │   └── OrderResource.php
│   └── Middleware/
├── Actions/                 # Single-responsibility action classes
│   ├── CreateUserAction.php
│   └── ProcessOrderAction.php
├── Models/                  # Eloquent models
│   ├── User.php
│   └── Order.php
├── Services/                # Complex business logic spanning multiple actions
├── Enums/                   # PHP 8.1+ backed enums
│   ├── OrderStatus.php
│   └── UserRole.php
├── Notifications/           # Email, SMS, push notifications
├── Jobs/                    # Queued jobs for async processing
├── Policies/                # Authorization policies per model
└── Exceptions/              # Custom exception classes
```

## Architecture Rules

- **Thin controllers, action classes for logic.** Controllers validate the request (via Form Request), call an Action or Service, and return a response. No business logic in controllers — they're routing glue.
- **Action classes are single-operation.** `CreateUserAction` handles one thing: creating a user. It takes typed parameters (not Request objects) so it's callable from controllers, commands, and other actions. One class, one `__invoke()` method.
- **Form Requests for all validation.** Never use `$request->validate()` inline in controllers. Create a dedicated `StoreUserRequest` class with `rules()` and `authorize()` methods. This keeps validation testable and reusable.
- **API Resources for all JSON output.** Never return Eloquent models directly from API endpoints: `return UserResource::make($user)`. Resources control exactly which fields and relationships are serialized.
- **PHP 8.1+ enums for all status fields and categories.** Never use string constants or integer flags for enums. `OrderStatus::Pending` is type-safe, autocompletable, and refactor-proof.

## Coding Conventions

- **Strict types everywhere.** Every PHP file starts with `declare(strict_types=1)`. All method parameters and return types are explicitly typed. No `mixed` unless genuinely needed.
- **Model conventions:** use `$casts` for date/enum casting, `$fillable` (never `$guarded = []`), and scopes for reusable query logic: `Order::query()->pending()->forUser($userId)->get()`.
- **Route naming:** `{resource}.{action}` → `users.store`, `orders.index`, `orders.show`. Use resource routes: `Route::apiResource('users', UserController::class)`.
- **Config over env in code.** Access `config('services.stripe.key')` — never `env('STRIPE_KEY')` outside of `config/` files. `env()` only works reliably in config files. In any other context it returns `null` when config is cached.
- **Eager load relationships.** Use `->with(['orders', 'profile'])` on every query that uses relationships. Check queries with `DB::enableQueryLog()` or Laravel Debugbar. N+1 queries are the #1 performance issue.

## Library Preferences

- **Auth:** Laravel's built-in auth with Sanctum for API tokens, or Laravel Breeze/Jetstream for full auth scaffolding. Not Passport (Sanctum is simpler for most apps — Passport is for full OAuth2 servers).
- **Queues:** Redis-backed queues via Laravel Horizon for monitoring. Not database driver in production (too slow). Not SQS unless you're on AWS and need it.
- **Admin:** Filament — not Nova (Filament is free, open-source, and more actively developed). Not building admin CRUD by hand.
- **Testing:** Pest — not PHPUnit directly (Pest wraps PHPUnit with a cleaner syntax). Use `RefreshDatabase` trait for DB tests.
- **IDE support:** Laravel IDE Helper (`barryvdh/laravel-ide-helper`) — generates model stubs for autocompletion. Run `php artisan ide-helper:models` after every migration.

## File Naming

- Controllers: `PascalCase` → `UserController.php`, `OrderController.php`
- Actions: `PascalCase` → `CreateUserAction.php`, `ProcessPaymentAction.php`
- Form Requests: `PascalCase` → `StoreUserRequest.php`, `UpdateOrderRequest.php`
- Models: singular `PascalCase` → `User.php`, `OrderItem.php`
- Migrations: auto-generated → `2024_01_15_create_orders_table.php`
- Enums: singular `PascalCase` → `OrderStatus.php`, `UserRole.php`
- Jobs: verb + noun → `ProcessPaymentJob.php`, `SendWelcomeEmailJob.php`
- Tests: `PascalCase` + `Test` → `UserControllerTest.php`, `CreateUserActionTest.php`

## NEVER DO THIS

1. **Never use `env()` outside of config files.** When you run `php artisan config:cache`, `env()` returns `null` everywhere except `config/` files. Always use `config()` helper in application code — it reads from the cached config.
2. **Never use `$guarded = []` on Eloquent models.** It disables mass assignment protection entirely. Use `$fillable` to explicitly list which fields can be mass-assigned. One malicious request payload away from overwriting `is_admin`.
3. **Never return Eloquent models from API endpoints.** Use API Resources. Models expose database column names, hidden fields, and relationship structure that consumers shouldn't see or depend on.
4. **Never write business logic in controllers.** Controllers call Actions. A controller method that exceeds 15 lines is doing too much. Extract logic into an Action class with typed parameters.
5. **Never use string comparisons for status fields.** `if ($order->status === 'pending')` breaks when someone typos 'pendng'. Use backed enums: `if ($order->status === OrderStatus::Pending)`.
6. **Never skip authorization.** Every controller action checks authorization via Form Request's `authorize()` or Policy. Never assume "this route is internal so auth doesn't matter." Use `$this->authorize('update', $order)` or Gate checks.
7. **Never run queue jobs synchronously in production.** Set `QUEUE_CONNECTION=redis` (not `sync`). Sync queues block the HTTP request. Email sending, PDF generation, and webhook processing must run on a worker.

## Testing

- Use Pest with `RefreshDatabase` trait. Each test gets a clean database.
- Test Actions by calling `(new CreateUserAction)->execute($params)` directly — no HTTP request needed.
- Test API endpoints with `$this->postJson('/api/users', $data)->assertStatus(201)`.
- Factory classes for every model: `User::factory()->create()`. Never construct test data with raw `Model::create()` calls.
- Test notifications and jobs with `Notification::fake()` and `Queue::fake()`. Assert they were dispatched without actually sending.

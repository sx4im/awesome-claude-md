# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- AdonisJS 6+ (full-stack TypeScript Node.js framework)
- Lucid ORM (Active Record pattern, built-in)
- Edge template engine (server-rendered views)
- VineJS (validation, built-in)
- Japa (testing framework, built-in)
- PostgreSQL/MySQL/SQLite

## Project Structure

```
app/
├── controllers/http/          # HTTP controllers ([features]_controller.ts)
├── models/                    # Lucid models (user.ts, [feature].ts)
├── middleware/                # Custom middleware (auth_middleware.ts)
├── validators/                # VineJS schemas ([feature].ts)
├── services/                  # Business logic ([feature]_service.ts)
├── exceptions/                # handler.ts + custom exceptions
├── mails/                     # Mailer classes
└── policies/                  # Bouncer authorization policies
config/                        # app.ts, database.ts, auth.ts, hash.ts, mail.ts
database/
├── migrations/                # [timestamp]_create_[table].ts
├── seeders/                   # [feature]_seeder.ts
└── factories/                 # Model factories for testing
resources/views/
├── layouts/main.edge          # Base layout
├── pages/[feature]/           # index.edge, show.edge, edit.edge
└── components/                # Reusable Edge components
start/
├── routes.ts                  # All route definitions
├── kernel.ts                  # Middleware registration
└── events.ts                  # Event listeners
```

## Architecture Rules

- **Controllers handle HTTP, services handle logic.** Controllers extract request data, call validators, invoke services, and return responses or render views. Business logic, database queries, and external API calls belong in services. Never put query logic in controllers.
- **VineJS validates all input.** Every controller action that accepts user input MUST validate through a VineJS schema. Define validators in `app/validators/`. VineJS runs on the server and strips unknown fields by default.
- **Lucid models are Active Record.** Models define schema, relationships, hooks, and scopes on the class itself. Use `Model.create()`, `model.save()`, `Model.query().where()`. Never use raw `db` queries for standard CRUD.
- **Bouncer policies for authorization.** Define authorization rules in `app/policies/`. Apply with `@bouncer.authorize('policyAction')` in controllers. Never put `if (user.role !== 'admin')` checks in controllers or services.
- **Edge templates for server-rendered HTML.** Use Edge's `@component`, `@section`, `@layout` tags. Pass data from controllers with `view.render('pages/feature/index', { data })`. Never use React/Vue for server-rendered pages.

## Coding Conventions

- **File naming: snake_case everywhere.** AdonisJS uses `snake_case` for all filenames: `users_controller.ts`, `create_user_validator.ts`, `user_policy.ts`. Never use camelCase or PascalCase for files.
- **Controller methods map to resourceful actions.** Use `index`, `create`, `store`, `show`, `edit`, `update`, `destroy`. Register with `router.resource('features', FeaturesController)`. Never invent custom action names for CRUD operations.
- **Use `async` on all controller methods.** Controller methods receive `HttpContext` as the first parameter: `async index({ request, response, view, auth, bouncer }: HttpContext)`. Always destructure what you need.
- **Preload relationships explicitly.** Use `Model.query().preload('relation')` to avoid N+1 queries. Lucid does NOT lazy-load relationships by default. Accessing an unloaded relation returns `undefined` silently.
- **Migrations use `this.schema`.** Define tables with `this.schema.createTable('users', (table) => { ... })`. Use Knex's schema builder API. Always provide both `up()` and `down()` methods.

## Library Preferences

- **Auth:** AdonisJS Auth package with session guard (web) or API tokens (API). Configured in `config/auth.ts`. Never use Passport.js or custom JWT.
- **Validation:** VineJS (built-in, successor to Indicative). Never use Joi, Yup, or Zod—VineJS is deeply integrated with AdonisJS's request lifecycle.
- **Email:** `@adonisjs/mail` with [SMTP/SES/Mailgun]. Use Mail classes in `app/mails/`. Never use Nodemailer directly.
- **File uploads:** `@adonisjs/drive` with [local/S3/GCS]. Use `request.file()` with validation rules. Never use Multer.
- **Hashing:** `@adonisjs/hash` with scrypt (default) or bcrypt. Never import `bcrypt` directly.
- **Testing:** Japa (built-in). Never use Jest or Mocha—Japa integrates with AdonisJS's IoC container and lifecycle.

## File Naming

- Controllers: `app/controllers/http/[features]_controller.ts` (plural)
- Models: `app/models/[feature].ts` (singular)
- Validators: `app/validators/[feature].ts`
- Policies: `app/policies/[feature]_policy.ts`
- Migrations: `database/migrations/[timestamp]_create_[features]_table.ts`
- Factories: `database/factories/[feature]_factory.ts`
- Views: `resources/views/pages/[feature]/[action].edge`

## NEVER DO THIS

1. **Never use camelCase for filenames.** AdonisJS resolves controllers, middleware, and validators by filename. Using `usersController.ts` instead of `users_controller.ts` will cause resolution failures.
2. **Never access relationships without `preload()` or `load()`.** Lucid does not lazy-load. `user.posts` returns `undefined` unless you called `user.preload('posts')` or `await user.load('posts')`. This is the most common AdonisJS bug.
3. **Never use Express/Fastify middleware.** AdonisJS has its own middleware system with `HttpContext`. Express-style `(req, res, next)` middleware will not work. Write AdonisJS middleware implementing the `handle` method.
4. **Never skip the `down()` method in migrations.** Lucid migrations require both `up()` and `down()` for rollbacks. An empty `down()` makes it impossible to undo schema changes in development.
5. **Never use `response.json()` when rendering Edge views.** For HTML pages, use `view.render()`. For API endpoints, use `response.json()`. Mixing them in a single controller causes content-type confusion.
6. **Never import from `@ioc:` in AdonisJS 6.** The `@ioc:` import prefix was AdonisJS 5 syntax. AdonisJS 6 uses standard ESM imports from package names (e.g., `import hash from '@adonisjs/core/services/hash'`). Using `@ioc:` will throw module-not-found errors.
7. **Never bypass VineJS for "simple" inputs.** Even single-field inputs like an ID param should go through `vine.compile(vine.object({ id: vine.number() }))`. Unvalidated IDs cause SQL injection or Lucid errors on non-numeric input.

## Testing

- **Use Japa's `test` function.** Define tests with `test('description', async ({ assert, client }) => { ... })`. The `client` helper makes HTTP requests against the AdonisJS app without starting a server.
- **Use model factories for test data.** Define factories in `database/factories/`. Call `await UserFactory.create()` or `await UserFactory.merge({ name: 'Test' }).createMany(5)`. Never insert test data with raw queries.
- **Database transactions for test isolation.** Use the `@japa/plugin-adonisjs` database plugin to wrap each test in a transaction that rolls back automatically. Never rely on truncation between tests.
- **Test authentication.** Use `client.loginAs(user)` to simulate authenticated requests. Never set session cookies or tokens manually in test requests.
- Run tests: `node ace test` (all), `node ace test --files="tests/functional/[feature]"` (specific), `node ace test --watch` (watch mode).

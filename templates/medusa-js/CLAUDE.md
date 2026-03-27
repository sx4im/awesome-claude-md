# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Medusa.js 2.x e-commerce backend framework
- TypeScript throughout with strict compiler options
- PostgreSQL as the primary database via MikroORM
- Redis for event bus, caching, and background job processing
- Medusa's Module architecture for business domain separation
- Medusa Workflows for multi-step transactional operations

## Project Structure

```
src/
  modules/
    loyalty/
      index.ts
      service.ts
      models/
        loyalty-points.ts
      migrations/
        Migration20240101.ts
    custom-fulfillment/
      index.ts
      service.ts
  workflows/
    create-order-with-loyalty/
      index.ts
      steps/
        validate-loyalty-points.ts
        deduct-loyalty-points.ts
        create-order.ts
  subscribers/
    order-placed.ts
    payment-captured.ts
  api/
    store/custom/loyalty/
      route.ts
    admin/custom/analytics/
      route.ts
    middlewares.ts
  admin/
    widgets/
      loyalty-widget.tsx
    routes/analytics/
      page.tsx
  jobs/
    sync-inventory.ts
  links/
    loyalty-to-customer.ts
medusa-config.ts
tsconfig.json
```

## Architecture Rules

- Custom business logic encapsulated in Medusa Modules with their own models, services, migrations
- Multi-step operations that span modules use Workflows with compensating steps for rollback
- Subscribers react to domain events (order.placed, payment.captured) for side effects
- API routes in src/api/ follow Medusa's file-based routing: folder structure defines URL paths
- Module services extend MedusaService with typed model generics for CRUD operations
- Links connect entities across modules without tight coupling (defined in src/links/)

## Coding Conventions

- Module services export a class extending MedusaService<typeof ModelName>
- Workflow steps created with createStep() with input/output type parameters
- Workflows composed with createWorkflow() chaining steps with .next()
- Subscribers export default a config object with event name and handler function
- API route handlers receive MedusaRequest and MedusaResponse typed generics
- Use Medusa's container resolution (req.scope.resolve) for accessing services in routes
- Module models use MikroORM decorators: @Entity, @Property, @PrimaryKey

## Library Preferences

- ORM: MikroORM as required by Medusa 2.x — never use Prisma or TypeORM
- Payment: Medusa payment modules (Stripe via @medusajs/payment-stripe)
- Fulfillment: Custom fulfillment modules extending AbstractFulfillmentService
- Search: MeiliSearch via @medusajs/plugin-meilisearch for product search
- File storage: S3 module via @medusajs/file-s3 or local file module for dev
- Admin: Medusa Admin UI with React extensions using @medusajs/admin-sdk

## File Naming

- Module entry points: src/modules/module-name/index.ts exports module definition
- Module services: src/modules/module-name/service.ts (singular service file)
- Workflow step files: kebab-case descriptive names (validate-loyalty-points.ts)
- Subscriber files: kebab-case matching the event domain (order-placed.ts)
- API routes: route.ts inside folder structure matching the URL path
- Model files: kebab-case in models/ directory (loyalty-points.ts)

## NEVER DO THIS

1. Never access another module's database tables directly — use the module's service or a link
2. Never perform multi-module mutations outside of a Workflow — partial failures leave inconsistent state
3. Never import internal Medusa module code — use the container and dependency injection
4. Never skip compensating steps in Workflows — every mutating step needs a compensation
5. Never modify core Medusa modules — extend them or create custom modules instead
6. Never use setTimeout for background tasks — use Medusa's scheduled jobs system
7. Never hardcode prices or currencies — use Medusa's pricing module with currency-aware calculations

## Testing

- Use Jest with ts-jest for unit and integration testing
- Test modules in isolation by instantiating their service with a test database
- Test workflows using Medusa's workflow testing utilities with mocked step contexts
- Test API routes using supertest against a Medusa test instance
- Test subscribers by emitting events through the test event bus and asserting side effects
- Seed test data using module services in beforeAll hooks, clean up in afterAll
- Run tests with: npx jest --runInBand --forceExit

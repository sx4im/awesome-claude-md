# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Runtime: Azure Functions v4 (Node.js 20 programming model v4)
- Language: TypeScript 5.x (strict mode)
- Database: Azure Cosmos DB (NoSQL API, point reads preferred)
- Storage: Azure Blob Storage for files, Table Storage for simple KV
- Messaging: Azure Service Bus for async messaging
- Auth: Azure AD / Entra ID via @azure/identity
- CLI: Azure Functions Core Tools v4 (`func`) and Azure CLI (`az`)
- Package Manager: npm
- Testing: Vitest
- Bundler: esbuild (configured in package.json scripts)

## Project Structure

```
src/
  functions/
    httpTrigger.ts      # HTTP-triggered functions (REST endpoints)
    timerTrigger.ts     # Scheduled CRON functions
    queueTrigger.ts     # Service Bus queue-triggered functions
    blobTrigger.ts      # Blob Storage event-triggered functions
  services/
    cosmos.ts           # Cosmos DB container client and query helpers
    storage.ts          # Blob Storage upload/download helpers
    serviceBus.ts       # Service Bus sender helpers
  models/
    schemas.ts          # Zod schemas for request/response validation
    entities.ts         # Cosmos DB document type definitions
  middleware/
    auth.ts             # Token validation and role checking
    errorHandler.ts     # Standardized error responses
  utils/
    config.ts           # Typed access to app settings
host.json               # Function host configuration (logging, extensions)
local.settings.json     # Local environment variables (gitignored)
package.json
tsconfig.json
```

## Architecture Rules

- Use the v4 programming model: register functions with `app.http()`, `app.timer()`, `app.serviceBusQueue()` etc.
- Every HTTP function explicitly sets `authLevel: 'anonymous'` or `'function'` -- never leave it unspecified.
- Cosmos DB queries must always specify a partition key. Cross-partition queries are forbidden in production.
- Use `DefaultAzureCredential` from `@azure/identity` for all Azure service authentication -- never hardcode connection strings for managed services.
- Keep function execution under 5 minutes for Consumption plan; use Durable Functions for longer workflows.
- Cosmos DB documents must include a `partitionKey` field and a `type` discriminator field.

## Coding Conventions

- Register HTTP functions inline: `app.http('getFoo', { methods: ['GET'], route: 'foo/{id}', handler })`.
- Handler signature: `async (request: HttpRequest, context: InvocationContext) => HttpResponseInit`.
- Return `{ status: 200, jsonBody: { data } }` for success responses.
- Return `{ status: 400, jsonBody: { error: 'message', code: 'VALIDATION_ERROR' } }` for errors.
- Use `context.log()` for structured logging (integrates with Application Insights).
- Access app settings via `process.env` but wrap in a typed config module.
- Use `@azure/cosmos` v4 client with `container.item(id, partitionKey).read()` for point reads.

## Library Preferences

- Cosmos DB: @azure/cosmos (official SDK)
- Blob Storage: @azure/storage-blob
- Service Bus: @azure/service-bus
- Auth: @azure/identity (DefaultAzureCredential)
- Validation: Zod
- HTTP client: native fetch
- Monitoring: Application Insights via host.json auto-instrumentation

## File Naming

- Function files: camelCase by trigger type (`httpTrigger.ts`, `timerTrigger.ts`)
- Service files: camelCase by Azure service (`cosmos.ts`, `storage.ts`)
- Config files: `host.json`, `local.settings.json` at project root
- Test files: `*.test.ts` colocated with source files

## NEVER DO THIS

1. Never commit `local.settings.json` to version control -- it contains connection strings and secrets.
2. Never use Cosmos DB cross-partition queries -- always design data access around a single partition key.
3. Never use `@azure/functions` v3 programming model (module.exports) -- use v4 `app.http()` registration.
4. Never create a new Cosmos DB client per function invocation -- use a module-level singleton for connection pooling.
5. Never hardcode Azure resource connection strings -- use Managed Identity with `DefaultAzureCredential`.
6. Never use `context.done()` callback pattern -- use async/await and return the response directly.
7. Never set function timeout above 10 minutes on Consumption plan -- it will be killed. Use Premium plan or Durable Functions.

## Testing

- Use Vitest for unit and integration tests.
- Mock `HttpRequest` using the constructor: `new HttpRequest({ method: 'GET', url: 'http://localhost/api/foo', params: { id: '123' } })`.
- Mock `InvocationContext` with a simple object: `{ log: vi.fn(), invocationId: 'test' } as unknown as InvocationContext`.
- Mock Cosmos DB calls by injecting the service module and using `vi.mock()`.
- Test timer triggers by calling the handler directly with a mock `Timer` object.
- Use Azurite (local Azure Storage emulator) for integration tests against Blob and Table Storage.
- Run `func start` for local end-to-end testing with all triggers.
- Assert response status codes, jsonBody structure, and that Cosmos operations received correct partition keys.

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fastify API documentation
- @fastify/swagger
- @fastify/swagger-ui
- JSON Schema
- OpenAPI 3.0

## Project Structure
```
src/
├── routes/
│   └── users.ts                // Schemas and routes
├── schemas/
│   └── user.json               // JSON schemas
└── app.ts
```

## Architecture Rules

- **JSON Schema validation.** Defines request/response formats.
- **Automatic documentation.** Schema generates Swagger UI.
- **TypeScript types.** Generate from schemas if possible.
- **Route documentation.** `schema` option per route.

## Coding Conventions

- Register: `app.register(swagger, { openapi: { info: { title: 'API', version: '1.0.0' } } }); app.register(swaggerUI, { routePrefix: '/docs' })`.
- Schema: `app.get('/users', { schema: { description: 'Get users', response: { 200: { type: 'array', items: { type: 'object', properties: { id: { type: 'number' }, name: { type: 'string' } } } } } } }, handler)`.
- Tags: Add `tags: ['users']` to schema for grouping.
- Security: `security: [{ bearerAuth: [] }]` for protected routes.

## NEVER DO THIS

1. **Never skip response schemas.** Documentation incomplete without them.
2. **Never expose internal error details.** Sanitize in production.
3. **Never forget to document auth requirements.** Security schemes.
4. **Never use example values that don't validate.** Must match schema.
5. **Never skip the `routePrefix` config.** UI needs accessible URL.
6. **Never document deprecated routes without marking.** Use `deprecated: true`.
7. **Never ignore response codes.** Document 400, 401, 404, 500 errors.

## Testing

- Test Swagger UI renders correctly.
- Test request/response schemas validate.
- Test with Swagger Editor for compliance.


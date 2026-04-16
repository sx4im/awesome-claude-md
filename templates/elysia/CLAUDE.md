# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Elysia v1 (Bun-first web framework)
- TypeScript 5.x
- Bun runtime (Node.js alternative)
- TypeBox for validation
- End-to-end type safety

## Project Structure

```
src/
├── index.ts                    # Elysia app entry
├── routes/                     # Route modules
│   ├── users.ts
│   └── posts.ts
├── models/                     # TypeBox schemas
│   ├── user.ts
│   └── post.ts
├── services/                   # Business logic
│   └── user-service.ts
└── lib/
    └── database.ts
```

## Architecture Rules

- **End-to-end type safety.** Elysia infers types from TypeBox schemas automatically.
- **Validation built-in.** Define schemas with TypeBox, Elysia validates automatically.
- **Bun-native performance.** Optimized for Bun's JavaScript runtime.
- **Eden Treaty for client types.** Generate type-safe API clients.

## Coding Conventions

- Create app: `new Elysia().get('/', () => 'Hello')`.
- With validation: `.post('/users', ({ body }) => createUser(body), { body: t.Object({ name: t.String() }) })`.
- Type inference: Body type is automatically inferred from TypeBox schema.
- Group routes: `new Elysia({ prefix: '/api' })` or `.group('/api', app => app.get('/users', ...))`.
- Plugins: Use `.use(plugin)` for shared functionality.

## NEVER DO THIS

1. **Never forget to install Bun.** Elysia requires Bun runtime, not Node.js.
2. **Never skip TypeBox validation.** Elysia's power is automatic validation. Use it.
3. **Never mix Node.js and Bun APIs carelessly.** Some Node.js modules don't work in Bun.
4. **Never ignore the type inference.** Let TypeScript infer from schemas; don't manually type.
5. **Never use callbacks.** Elysia is promise-based. Use async/await.
6. **Never forget about Eden Treaty.** Generate type-safe clients for consuming your API.
7. **Never use Elysia without understanding Bun's differences.** Not all npm packages work in Bun.

## Testing

- Use Bun's test runner: `bun:test`.
- Test Elysia handlers directly—they're async functions.
- Integration tests with `fetch` to running server.


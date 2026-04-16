# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- MSW (Mock Service Worker)
- Browser and Node.js support
- REST and GraphQL mocking
- TypeScript support
- Service Worker based

## Project Structure
```
src/
├── mocks/
│   ├── browser.ts              # Browser mock setup
│   ├── server.ts               # Node/server mock setup
│   ├── handlers.ts             # Request handlers
│   └── data/
│       └── users.json          # Mock data
src/
├── main.tsx                    # Initialize mocks in dev
└── test/
    └── setup.ts                # Test server setup
```

## Architecture Rules

- **Intercept requests at network level.** Mock actual HTTP requests, not fetch wrapper.
- **Handlers define responses.** `rest.get('/api/users', (req, res, ctx) => res(ctx.json(data)))`.
- **Browser and server modes.** Same handlers work in browser (dev) and Node (tests).
- **Type-safe mocking.** TypeScript types for request/response.

## Coding Conventions

- Handler: `rest.get('/api/users', (req, res, ctx) => { return res(ctx.status(200), ctx.json(users)) })`.
- Params: `const { id } = req.params` from path like `/api/users/:id`.
- Query: `const page = req.url.searchParams.get('page')`.
- Request body: `const { name } = await req.json()`.
- Browser setup: `worker.start()` in `main.tsx` conditional on `process.env.NODE_ENV === 'development'`.
- Server setup: `server.listen()` in Jest/Vitest setup file.
- Reset: `afterEach(() => server.resetHandlers())` to clean up test-specific handlers.

## NEVER DO THIS

1. **Never commit service worker to production.** Only enable in development/testing.
2. **Never mock your entire API.** Mock what you need for the feature being developed.
3. **Never forget to reset handlers between tests.** Leaked handlers cause test pollution.
4. **Never ignore the `ctx` argument.** It provides delay, status, json, etc.
5. **Never use MSW for production fallbacks.** It's for development and testing only.
6. **Never forget `server.close()` in test cleanup.** Prevents open handle warnings.
7. **Never mock responses that don't match real API structure.** Keep mocks realistic.

## Testing

- Test with `server.use()` for one-off handler overrides.
- Test error scenarios with `res(ctx.status(500))`.
- Test with `delay()` to simulate loading states.


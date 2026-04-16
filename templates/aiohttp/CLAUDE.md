# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- aiohttp v3.9+ (async Python HTTP client/server)
- Python 3.11+
- Async client and server
- WebSocket support
- Pluggable middleware

## Project Structure

```
app/
├── __init__.py
├── main.py                     # App factory
├── routes.py                   # Route definitions
├── views/                      # View classes
│   ├── __init__.py
│   ├── users.py
│   └── websocket.py
├── middlewares/
│   ├── __init__.py
│   ├── auth.py
│   └── error.py
└── models/
    └── user.py
```

## Architecture Rules

- **Application and routes.** Create `web.Application()`, add routes, run with `web.run_app`.
- **View classes or handlers.** Use `aiohttp.web.View` for class-based or functions.
- **Request object rich.** `request.match_info`, `request.query`, `request.json()`.
- **Middleware stack.** Process requests before/after handlers.

## Coding Conventions

- Create route: `app.router.add_get('/users', list_users)`.
- Handler function: `async def list_users(request): return web.json_response(data)`.
- View class: `class UserView(web.View): async def get(self): ...`.
- Path params: `request.match_info['user_id']`.
- WebSocket: `ws = web.WebSocketResponse(); await ws.prepare(request)`.

## NEVER DO THIS

1. **Never use sync I/O in handlers.** aiohttp is async. Blocking calls freeze the loop.
2. **Never forget to await `request.json()`.** It's a coroutine, not a property.
3. **Never ignore middleware ordering.** Middleware executes in add order for request, reverse for response.
4. **Never use aiohttp without understanding the event loop.** Know when to use `asyncio.create_task`.
5. **Never mix client and server code carelessly.** `aiohttp.ClientSession` vs `web` module.
6. **Never forget cleanup.** `app.on_cleanup.append(close_db)` for resource cleanup.
7. **Never ignore graceful shutdown.** Handle `SIGTERM` for clean WebSocket closures.

## Testing

- Use `aiohttp.test_utils.AioHTTPTestCase` or `pytest-aiohttp`.
- Create test app with test routes.
- Test WebSockets with test client WebSocket API.


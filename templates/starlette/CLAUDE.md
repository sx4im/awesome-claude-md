# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Starlette v0.35+ (ASGI framework)
- Python 3.11+
- Uvicorn (ASGI server)
- Optional: Jinja2, databases, HTTPX

## Project Structure

```
app/
├── __init__.py
├── main.py                     # Starlette app
├── routes/                     # Route definitions
│   ├── __init__.py
│   ├── users.py
│   └── endpoints/
│       └── websocket.py
├── middleware/
│   ├── __init__.py
│   └── cors.py
├── templates/
│   └── index.html
└── static/
    └── styles.css
```

## Architecture Rules

- **Pure ASGI framework.** Starlette is minimal, focused on ASGI primitives.
- **Class-based or function routes.** Use `Route`, `WebSocketRoute`, `Mount` for routing.
- **Middleware as ASGI apps.** Middleware wraps the ASGI application.
- **Background tasks.** `BackgroundTask` for operations after response is sent.

## Coding Conventions

- Create app: `app = Starlette(routes=routes)`.
- Define routes: `Route('/users', endpoint=list_users, methods=['GET'])`.
- Endpoint functions: `async def list_users(request): return JSONResponse(data)`.
- WebSocket: `async def websocket_endpoint(websocket): await websocket.accept()`.
- Static files: `Mount('/static', app=StaticFiles(directory='static'))`.

## NEVER DO THIS

1. **Never confuse Starlette with FastAPI.** FastAPI builds on Starlette but adds validation, docs.
2. **Never forget request/response types.** Starlette uses `Request` and `Response` classes.
3. **Never use WSGI middleware.** Starlette is ASGI. Use ASGI-compatible middleware.
4. **Never ignore background tasks.** Use them for post-response work like sending emails.
5. **Never skip exception handling.** Register error handlers with `app.add_exception_handler`.
6. **Never mix sync and async carelessly.** Starlette is async-first. Sync I/O blocks.
7. **Never forget that Starlette is lower-level.** You may need to add validation libraries yourself.

## Testing

- Use Starlette's `TestClient` from `starlette.testclient`.
- Test ASGI apps directly with `async` test functions.
- Test WebSockets with `client.websocket_connect()`.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Robyn (async Python web framework)
- Python 3.11+
- Rust-based runtime
- Optional: SQLAlchemy, Pydantic

## Project Structure

```
app/
├── __init__.py
├── main.py                     # Robyn app entry
├── routes/
│   ├── __init__.py
│   ├── users.py
│   └── items.py
├── models/
│   └── user.py
├── middleware/
│   └── auth.py
└── lib/
    └── database.py
```

## Architecture Rules

- **Function-based routes.** Robyn uses decorators on functions, not class-based controllers.
- **Async handlers.** All route handlers are `async def`.
- **Rust runtime performance.** Robyn uses Rust for HTTP handling, Python for business logic.
- **WebSocket support built-in.** Use `@websocket` decorator for WebSocket handlers.

## Coding Conventions

- Create app: `app = Robyn(__file__)`.
- Define routes: `@app.get('/users') async def get_users() -> dict`.
- Path parameters: `@app.get('/users/:id') async def get_user(request: Request)` then `request.path_params['id']`.
- Query params: `request.queries` for query parameters.
- Middleware: `@app.before_request()` and `@app.after_request()`.

## NEVER DO THIS

1. **Never use sync handlers.** Robyn is async-only. Sync handlers block the event loop.
2. **Never forget the Rust dependency.** Robyn requires Rust toolchain for installation.
3. **Never ignore request/response types.** Use type hints for better IDE support.
4. **Never use blocking libraries in handlers.** Use async libraries for DB, HTTP, etc.
5. **Never forget WebSocket handling.** Robyn handles WebSocket at Rust level—different from HTTP.
6. **Never mix Robyn with Flask patterns.** Robyn has unique async patterns.
7. **Never ignore startup/shutdown events.** Use `@app.startup_handler` and `@app.shutdown_handler`.

## Testing

- Use pytest with async support: `pytest-asyncio`.
- Test routes by calling handler functions directly with mock requests.
- Integration tests require running server or using `TestClient`.


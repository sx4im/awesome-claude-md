# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Sanic v23+ (async Python web framework)
- Python 3.11+
- UVLoop (default event loop)
- Optional: SQLAlchemy, Redis, JWT

## Project Structure

```
app/
├── __init__.py
├── main.py                     # Sanic app factory
├── blueprints/                 # Blueprints for route grouping
│   ├── __init__.py
│   ├── users.py
│   └── api.py
├── middleware/
│   ├── auth.py
│   └── logging.py
├── models/
│   └── user.py
└── services/
    └── user_service.py
```

## Architecture Rules

- **Blueprints for modularity.** Group related routes in Blueprints, register with app.
- **Request/Response objects.** Sanic provides rich request and response objects.
- **Middleware for cross-cutting.** Authentication, logging, CORS in middleware.
- **Exception handling.** Custom error handlers for different exception types.

## Coding Conventions

- Create app: `app = Sanic('MyApp')`.
- Define routes: `@app.route('/users') async def users(request): return json(data)`.
- Blueprints: `bp = Blueprint('users', url_prefix='/users')` then `app.register_blueprint(bp)`.
- Request access: `request.args`, `request.json`, `request.form`.
- Middleware: `@app.middleware('request')` or `@app.on_request()`.

## NEVER DO THIS

1. **Never use sync I/O in handlers.** Sanic is async. Blocking calls freeze the server.
2. **Never forget that Sanic is strict about async.** Even `time.sleep` blocks—use `asyncio.sleep`.
3. **Never share mutable state between workers.** Sanic runs multiple processes. Use external storage.
4. **Never ignore request validation.** Sanic doesn't validate automatically. Use Pydantic or marshmallow.
5. **Never use global variables for request-scoped data.** Use `request.ctx` for request-level storage.
6. **Never forget to handle exceptions.** Sanic has built-in handlers; customize for your needs.
7. **Never use Flask patterns blindly.** Similar but different: blueprints vs blueprints, contexts differ.

## Testing

- Use `pytest-sanic` for async testing.
- Test blueprints independently with test clients.
- Test middleware by simulating requests.


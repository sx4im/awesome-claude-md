# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Quart v0.19 (async Flask-like framework)
- Python 3.11+
- ASGI-compatible
- Optional: SQLAlchemy, Jinja2

## Project Structure

```
app/
├── __init__.py
├── main.py                     # Quart app factory
├── routes/
│   ├── __init__.py
│   ├── users.py
│   └── api.py
├── templates/                  # Jinja2 templates
│   └── base.html
├── static/
│   └── style.css
└── extensions/
    └── db.py                   # DB extension
```

## Architecture Rules

- **Flask-compatible API.** Quart mimics Flask's API but with async support.
- **Async route handlers.** Use `async def` for routes that do I/O.
- **ASGI deployment.** Deploy with Hypercorn or Uvicorn, not WSGI servers.
- **Extensions work with caveats.** Many Flask extensions work; some need async alternatives.

## Coding Conventions

- Create app: `app = Quart(__name__)`.
- Define routes: `@app.route('/users') async def users(): return jsonify(data)`.
- Async database: `await db.fetch_all(query)` with asyncpg or similar.
- Templates: `await render_template('index.html', data=data)`.
- Request context: `request.args`, `request.form`, `request.json` (all async-compatible).

## NEVER DO THIS

1. **Never use Flask extensions that do I/O without checking async support.** Some Flask extensions block.
2. **Never forget `await` in templates.** Database queries in templates need async handling.
3. **Never deploy with WSGI.** Quart is ASGI-only. Use Hypercorn, Uvicorn, or Daphne.
4. **Never use sync database drivers.** Use `asyncpg`, `aiomysql`, etc.
5. **Never mix sync and async carelessly.** Async code calling sync I/O blocks the loop.
6. **Never ignore the `async` in template rendering.** `await render_template()`, not `render_template()`.
7. **Never use Flask's `g` without understanding Quart's context locals.** Similar but not identical.

## Testing

- Use Quart's test client: `app.test_client()`.
- Test async routes with `pytest-asyncio`.
- Test that sync I/O doesn't block (measure response times).


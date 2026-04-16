# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Bottle v0.13 (micro Python web framework)
- Python 3.11+
- Single-file framework (zero dependencies)
- Optional: Jinja2, SQLAlchemy

## Project Structure

```
app.py                          # Single-file app (common)
or
app/
├── __init__.py
├── main.py                     # Bottle app
├── routes.py                   # Route definitions
├── views/
│   └── templates/
│       └── base.tpl
└── static/
    └── style.css
```

## Architecture Rules

- **Single-file simplicity.** Bottle fits in one file with no dependencies.
- **Decorator routing.** Use `@route`, `@get`, `@post` decorators.
- **Built-in template engine.** SimpleTemplate included; Jinja2 optional.
- **Request/Response objects.** Access via `request`, `response` or function parameters.

## Coding Conventions

- Create route: `@route('/hello') def hello(): return 'Hello'`.
- Dynamic routes: `@route('/user/<name>') def user(name): ...`.
- Templates: `template('hello', name=name)` with SimpleTemplate.
- Forms: `request.forms.get('username')` for POST data.
- Query: `request.query.get('page')` for GET params.

## NEVER DO THIS

1. **Never use Bottle for large applications.** It's designed for micro-apps and prototypes.
2. **Never forget Bottle is single-threaded.** Use with WSGI server for production (gunicorn, etc.).
3. **Never ignore security defaults.** Bottle is minimal—you must add CSRF, security headers.
4. **Never use Bottle for complex routing.** It has basic routing. Use Flask/FastAPI for complex needs.
5. **Never mix sync and async carelessly.** Bottle is sync. Use proper WSGI server.
6. **Never forget about plugins.** Bottle has plugin system. Use for database integration.
7. **Never use development server in production.** `run()` is for dev only. Use gunicorn/uwsgi.

## Testing

- Use `webtest` or Bottle's testing utilities.
- Test routes by calling decorated functions.
- Mock request/response objects for unit tests.


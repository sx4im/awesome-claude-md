# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Falcon v4 (high-performance Python framework)
- Python 3.11+
- ASGI/WSGI compatible
- Cython for performance (optional)

## Project Structure

```
app/
├── __init__.py
├── main.py                     # Falcon app
├── resources/                  # Resource classes
│   ├── __init__.py
│   ├── users.py
│   └── items.py
├── middleware/
│   ├── __init__.py
│   └── auth.py
└── lib/
    └── database.py
```

## Architecture Rules

- **Resource classes for routes.** Falcon uses class-based resources with `on_get`, `on_post` methods.
- **RESTful by design.** Built for REST APIs, not general web apps.
- **Minimalist framework.** No ORM, no template engine, no validation. You bring your own.
- **High performance.** One of the fastest Python frameworks.

## Coding Conventions

- Create resource: `class UserResource: def on_get(self, req, resp): resp.media = data`.
- Add route: `app.add_route('/users', UserResource())`.
- Request access: `req.params`, `req.media`, `req.get_header()`.
- Response building: `resp.status = falcon.HTTP_200`, `resp.media = data`.
- Hooks: `@falcon.before(authenticate)` for pre-processing.

## NEVER DO THIS

1. **Never expect batteries included.** Falcon is minimal. Bring your own ORM, validation, etc.
2. **Never use Falcon for server-rendered apps.** It's designed for APIs, not HTML rendering.
3. **Never forget method naming convention.** `on_get`, `on_post`, `on_put`, `on_delete` are required.
4. **Never ignore the `resp` object.** Falcon uses `resp` for output, not return values.
5. **Never use blocking I/O in ASGI mode.** Use async handlers with async libraries.
6. **Never mix sync and async handlers carelessly.** Understand your deployment mode.
7. **Never skip request validation.** Falcon doesn't validate. Use marshmallow, pydantic, etc.

## Testing

- Use `falcon.testing.TestClient`.
- Test resources by instantiating and calling `on_get`, etc.
- Test with various content types Falcon handles.


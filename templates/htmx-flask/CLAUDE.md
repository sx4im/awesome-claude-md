# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Flask 3.1 with Blueprints for modular route organization
- HTMX 2.0 for dynamic server-driven UI updates
- Jinja2 templates with template inheritance
- SQLAlchemy 2.0 with Flask-SQLAlchemy for ORM
- Alembic for database migrations via Flask-Migrate
- WTForms with Flask-WTF for server-side form validation
- Tailwind CSS 4 via standalone CLI for styling
- SQLite for development, PostgreSQL for production
- Gunicorn with gevent workers for production serving

## Project Structure

```
app/
  __init__.py              # Flask app factory (create_app)
  models/
    __init__.py
    user.py                # SQLAlchemy model definitions
    post.py
  views/
    __init__.py
    main.py                # Main blueprint routes
    auth.py                # Authentication blueprint
    api.py                 # JSON API blueprint (non-HTMX clients)
  forms/
    auth.py                # WTForms form classes
    post.py
  templates/
    base.html              # Root layout with HTMX script, Tailwind CSS
    partials/              # HTMX partial HTML fragments
      _post_list.html
      _post_form.html
      _toast.html
      _search_results.html
    pages/                 # Full page templates
      index.html
      login.html
  static/
    css/
      output.css           # Tailwind compiled output
    js/
      app.js               # Minimal JS (HTMX extensions, Alpine.js init)
  services/
    __init__.py
    auth_service.py        # Business logic layer
    post_service.py
  extensions.py            # Flask extension instances (db, migrate, login)
config.py                  # Configuration classes (Dev, Prod, Test)
migrations/                # Alembic migration versions
tests/
  conftest.py              # Pytest fixtures (app, client, db)
  test_views/
  test_models/
  test_services/
```

## Architecture Rules

- Flask views return full HTML pages for standard GET requests and HTML fragments for HTMX requests. Check `request.headers.get('HX-Request')` to distinguish.
- Business logic lives in `app/services/`, never in view functions. Views handle HTTP concerns (request parsing, response formatting) and delegate to services.
- HTMX partial templates live in `templates/partials/` prefixed with underscore. They render a single UI component without the base layout.
- Use `hx-swap="innerHTML"` as the default swap strategy. Use `hx-swap="outerHTML"` only when replacing the triggering element itself.
- All form submissions use `hx-post` with WTForms validation on the server. Return the form partial with errors on validation failure (422 status).
- Use `HX-Trigger` response headers to emit events for toast notifications, modal closures, and list refreshes.
- Database queries go through SQLAlchemy ORM. Use `db.session.execute(select(...))` style (SQLAlchemy 2.0 query syntax), never the legacy `Model.query` interface.

## Coding Conventions

- View functions are decorated with `@bp.route()` and use descriptive names: `list_posts`, `create_post`, `delete_post`.
- HTMX attributes are placed on HTML elements in a consistent order: `hx-verb`, `hx-target`, `hx-swap`, `hx-trigger`, `hx-indicator`.
- Template naming: pages use `noun.html`, partials use `_noun_action.html` (e.g., `_post_list.html`, `_post_form.html`).
- Use `url_for()` in all templates for URL generation. Never hardcode URL paths.
- Flash messages are rendered via HTMX OOB swaps using `hx-swap-oob="innerHTML:#toast-container"` in response partials.
- SQLAlchemy models define `__repr__` and use `Mapped[type]` annotations for all columns.
- Configuration uses environment variables loaded via `python-dotenv`. Never commit `.env` files.

## Library Preferences

- Forms: Flask-WTF with WTForms (never hand-roll form validation)
- Auth: Flask-Login for session management, Werkzeug for password hashing
- Database: Flask-SQLAlchemy 3.x with SQLAlchemy 2.0 syntax
- Migrations: Flask-Migrate wrapping Alembic
- Email: Flask-Mail with Jinja2 email templates
- Task queue: Celery with Redis for background jobs
- Rate limiting: Flask-Limiter with Redis backend
- CORS: Flask-CORS for API blueprint only

## File Naming

- Python modules: `snake_case.py`
- Templates: `snake_case.html`, partials prefixed with `_underscore.html`
- Blueprints: `snake_case.py` in `app/views/`
- Models: singular `snake_case.py` (e.g., `user.py`, `post.py`)
- Tests: `test_snake_case.py` mirroring source structure

## NEVER DO THIS

1. Never return JSON from a view that HTMX targets. HTMX expects HTML fragments. Use a separate API blueprint for JSON responses.
2. Never use `Model.query` legacy syntax. Use `db.session.execute(select(Model))` for all database queries (SQLAlchemy 2.0 style).
3. Never put business logic in Jinja2 templates. Templates render data; logic belongs in services or view functions.
4. Never use inline `<script>` tags for interactivity. Use HTMX attributes declaratively or Alpine.js for client-side state.
5. Never skip CSRF protection. All HTMX POST/PUT/DELETE requests must include the CSRF token via `hx-headers` or meta tag configuration.
6. Never use `hx-boost` on forms with file uploads. Use standard `hx-post` with `hx-encoding="multipart/form-data"` instead.
7. Never commit the SQLite database file or `.env` to version control.

## Testing

- Unit tests: pytest with Flask test client for view testing, isolated service tests with mocked repositories.
- Run tests with `pytest -v --tb=short`.
- Fixtures in `conftest.py` provide `app`, `client`, `db`, and `authenticated_client` for logged-in requests.
- View tests assert both HTTP status codes and check for expected HTML fragments in the response body.
- HTMX-specific tests set `HX-Request: true` header and verify partial HTML responses (not full pages).
- Model tests verify constraints, relationships, and `__repr__` output.
- Coverage target is 85% minimum, enforced with `pytest-cov` in CI.
- Factory Boy generates test data via model factories in `tests/factories.py`.

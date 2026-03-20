# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+ with Flask 3+
- SQLAlchemy 2.0+ (ORM with mapped_column style)
- Marshmallow 3+ (serialization/validation)
- Flask-Migrate (Alembic-based migrations)
- Celery + [Redis/RabbitMQ] (background tasks)
- pytest + pytest-flask

## Project Structure

```
src/
├── app/
│   ├── __init__.py            # Application factory (create_app)
│   ├── config.py              # Config classes (Dev, Test, Prod)
│   ├── extensions.py          # db, migrate, ma, celery instances
│   ├── models/                # SQLAlchemy models (user.py, [feature].py)
│   ├── schemas/               # Marshmallow schemas (user.py, [feature].py)
│   ├── blueprints/
│   │   ├── auth/              # __init__.py, routes.py
│   │   └── [feature]/         # __init__.py, routes.py, services.py
│   ├── tasks/                 # Celery task definitions
│   └── utils/                 # errors.py, decorators.py
├── migrations/                # Alembic migrations (auto-generated)
├── tests/
│   ├── conftest.py            # Fixtures (app, client, db session)
│   ├── factories/             # Factory Boy model factories
│   └── test_[feature]/        # test_routes.py, test_services.py
├── celery_worker.py           # Celery app entry point
└── wsgi.py                    # WSGI entry point for production
```

## Architecture Rules

- **Application factory pattern.** Always use `create_app()` in `__init__.py`. Initialize extensions in `extensions.py` and call `ext.init_app(app)` inside the factory. Never create a global `app = Flask(__name__)` at module level.
- **Blueprint pattern for route organization.** Every feature is a Blueprint registered in `create_app()`. Never define routes on the app object directly. Blueprints enable independent testing and lazy loading.
- **Service layer for business logic.** Route handlers parse requests, call service functions, and return responses. Services contain business logic and database operations. Never put query logic in route handlers.
- **SQLAlchemy 2.0 style only.** Use `Mapped[type]`, `mapped_column()`, and `select()` statements. Never use legacy `Column()`, `Query.filter()`, or implicit `session.query(Model)` patterns.
- **Marshmallow for all serialization.** Every API response passes through a Marshmallow schema. Never return `model.__dict__` or hand-built dicts. Marshmallow handles validation, nesting, and field filtering.

## Coding Conventions

- **Route handlers are thin.** A route handler: (1) extracts input from request, (2) validates via Marshmallow `schema.load()`, (3) calls a service function, (4) serializes result via `schema.dump()`, (5) returns response. That is all.
- **Use `@bp.errorhandler` and global error handlers.** Register error handlers for `ValidationError`, `404`, `500` in `utils/errors.py`. Never return raw exception messages to clients.
- **Database sessions via Flask-SQLAlchemy.** Use `db.session` for all queries. Never create `Session()` instances manually. Commit in service functions, not in route handlers.
- **Explicit relationship loading.** Use `selectinload()`, `joinedload()`, or `lazy="selectin"` for relationships. Never rely on lazy loading in API contexts—it causes N+1 queries that silently destroy performance.
- **Environment config via classes.** Define `DevelopmentConfig`, `TestingConfig`, `ProductionConfig` in `config.py`. Load with `app.config.from_object()`. Never use `app.config["KEY"] = value` scattered throughout code.

## Library Preferences

- **ORM:** SQLAlchemy 2.0 with Flask-SQLAlchemy 3+. Never use raw SQL except for complex analytics queries.
- **Serialization:** Marshmallow 3+ with `flask-marshmallow`. Never use `jsonify(model.to_dict())`.
- **Migrations:** Flask-Migrate (Alembic). Run `flask db migrate` then `flask db upgrade`. Never modify the database schema manually.
- **Auth:** [Flask-Login] for sessions or [Flask-JWT-Extended] for token auth. Never implement custom token logic.
- **Task queue:** Celery with [Redis] broker. Never use threading or `multiprocessing` for background work in a WSGI app.
- **Testing:** pytest + pytest-flask + Factory Boy. Never use unittest.TestCase.

## File Naming

- Models: `app/models/[feature].py` (singular: `user.py`, `order.py`)
- Schemas: `app/schemas/[feature].py` (matching model names)
- Blueprints: `app/blueprints/[feature]/routes.py`
- Services: `app/blueprints/[feature]/services.py`
- Tasks: `app/tasks/[feature].py`
- Tests: `tests/test_[feature]/test_routes.py`

## NEVER DO THIS

1. **Never use `app = Flask(__name__)` at module level.** This prevents testing with different configs, breaks Celery integration, and causes circular imports. Always use the application factory pattern.
2. **Never use `db.Model.query` (legacy query interface).** Use `db.session.execute(select(Model).where(...))` (SQLAlchemy 2.0 style). The legacy interface is deprecated and will be removed.
3. **Never return `jsonify(model.__dict__)`.** Model `__dict__` contains SQLAlchemy internals (`_sa_instance_state`) and exposes all fields including passwords. Always use Marshmallow schemas.
4. **Never use `lazy="dynamic"` or default lazy loading in API code.** It causes N+1 queries. Use `selectinload()` or `joinedload()` in your `select()` statements.
5. **Never run Celery tasks synchronously with `.apply()` in production.** Use `.delay()` or `.apply_async()`. Synchronous execution blocks the web worker and defeats the purpose of a task queue.
6. **Never commit database sessions in route handlers.** Commit in service functions. If a route calls multiple services, use a unit-of-work pattern or explicit transaction management with `db.session.begin()`.
7. **Never use `*` imports from models or schemas.** Explicit imports prevent circular dependencies and make it clear which models are used in each module.

## Testing

- **Use the `app` and `client` fixtures from `conftest.py`.** The `app` fixture creates a test app with `TestingConfig`. The `client` fixture provides `client.get()`, `client.post()`, etc.
- **Use Factory Boy for test data.** Define factories in `tests/factories/`. Use `factory.create()` for DB-persisted objects, `factory.build()` for transient ones. Never seed data with raw SQL.
- **Test services independently of routes.** Import service functions and call them directly with a test app context. This tests business logic without HTTP overhead.
- **Celery task tests:** Use `CELERY_ALWAYS_EAGER=True` in test config to execute tasks synchronously. Assert on side effects (DB changes, emails sent), not task return values.
- Run tests: `pytest` (all), `pytest tests/test_[feature]/` (feature), `pytest -x --tb=short` (fail-fast).

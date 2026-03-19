# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+
- FastAPI 0.100+
- SQLAlchemy 2.0 (async, mapped classes)
- Pydantic v2 for request/response models
- Alembic for database migrations
- PostgreSQL 15+
- UV or pip for dependency management

## Project Structure

```
app/
├── api/
│   ├── v1/
│   │   ├── users.py        # Router for /api/v1/users
│   │   ├── orders.py       # Router for /api/v1/orders
│   │   └── __init__.py     # Collects all v1 routers
│   └── deps.py             # Shared dependencies (get_db, get_current_user)
├── models/                  # SQLAlchemy ORM models
│   ├── user.py
│   └── order.py
├── schemas/                 # Pydantic v2 models
│   ├── user.py              # UserCreate, UserUpdate, UserResponse
│   └── order.py
├── services/                # Business logic layer
│   ├── user_service.py
│   └── order_service.py
├── core/
│   ├── config.py            # Settings via pydantic-settings
│   ├── security.py          # JWT, password hashing
│   └── database.py          # AsyncSession factory
├── migrations/              # Alembic migrations
└── main.py                  # FastAPI app factory
```

## Architecture Rules

- **One router per domain.** `api/v1/users.py` handles all user endpoints. Never put multiple unrelated domains in one router file.
- **Three-layer architecture:** Router → Service → Model. Routers validate input and call services. Services contain business logic and call the ORM. Never do ORM queries directly in router functions.
- **All route handlers are `async def`.** FastAPI runs sync handlers in a threadpool, which is slower. Use async natively.
- **Dependency injection via `Depends()`.** Database sessions, auth, and pagination are all injected. Never instantiate them manually inside route handlers.
- **Pydantic models are the contract.** API consumers see Pydantic schemas, never SQLAlchemy models. Map between them explicitly in the service layer.

## Coding Conventions

- Pydantic schema naming: `{Entity}Create`, `{Entity}Update`, `{Entity}Response`, `{Entity}InDB`. Example: `UserCreate`, `UserUpdate`, `UserResponse`.
- Route function naming: `create_user`, `get_user`, `list_users`, `update_user`, `delete_user`. Verb first, noun second.
- Use `Annotated[type, Depends(...)]` for dependency injection. not raw `Depends()` as a default parameter. This enables proper type inference.
- Error responses: raise `HTTPException` with specific status codes and detail messages. Never return raw dicts with error info.
- Environment config: use `pydantic-settings` with a `Settings` class in `core/config.py`. Access via `get_settings()` dependency. Never use `os.getenv()` directly.

## Library Preferences

- **ORM:** SQLAlchemy 2.0 with `MappedAsDeclarativeBase`. not SQLAlchemy 1.x legacy patterns. Use `Mapped[type]` for column annotations, not `Column(Integer)`.
- **Migrations:** Alembic with `--autogenerate`. Name migrations descriptively: `add_user_email_verification_fields`, not `update_001`.
- **Validation:** Pydantic v2. not v1. v2 is faster and uses `model_validator`/`field_validator` decorators, not the old `@validator`.
- **Password hashing:** `passlib[bcrypt]` with `CryptContext`. Not custom hashing logic.
- **Testing:** `pytest` + `httpx.AsyncClient`. Not `requests`. it doesn't support async.
- **Dates:** `datetime` from stdlib with UTC-aware timestamps. Store as `timestamp with time zone` in PostgreSQL.

## File Naming

- All files: `snake_case.py` → `user_service.py`, `order_router.py`
- Alembic migrations: auto-generated with descriptive message → `add_created_at_to_orders.py`
- Test files: `test_` prefix → `test_user_service.py`, `test_users_api.py`
- Config files: descriptive → `config.py`, `database.py`, `security.py`

## NEVER DO THIS

1. **Never use mutable default arguments.** `def create_user(tags: list = [])` is a classic Python bug. the list is shared across all calls. Use `tags: list | None = None` and initialize inside the function body.
2. **Never do ORM queries in routers.** Routers call services, services call the ORM. This separation makes testing possible without spinning up a full API server.
3. **Never return SQLAlchemy models from endpoints.** Always map to a Pydantic `Response` schema. SQLAlchemy models expose internal IDs, relationships, and columns that API consumers shouldn't see.
4. **Never use global mutable state.** No module-level variables that get mutated at runtime. Use dependency injection for shared state like database connections.
5. **Never hardcode connection strings.** Database URLs, API keys, and secrets always come from environment variables via `pydantic-settings`. Never commit them, never pass them as function arguments.
6. **Never use `print()` for logging.** Use Python's `logging` module with structured output. Configure it in `core/config.py` with appropriate levels per environment.
7. **Never use synchronous database drivers in async code.** Use `asyncpg` for PostgreSQL, not `psycopg2`. Mixing sync I/O in async handlers blocks the event loop.

## Testing

- Use `pytest` with `pytest-asyncio` for async tests.
- Create a test database with a fixture that runs migrations and truncates tables between tests.
- Test API endpoints with `httpx.AsyncClient` hitting the actual FastAPI app (not mocking FastAPI itself).
- Test services independently by injecting a mock database session.
- Name test files to mirror the module they test: `test_user_service.py` tests `user_service.py`.

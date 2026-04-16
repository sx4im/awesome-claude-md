# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Litestar v2 (async Python framework)
- Python 3.11+
- Pydantic v2 for validation
- SQLAlchemy 2.0 or advanced-alchemy
- Uvicorn (ASGI server)

## Project Structure

```
app/
├── __init__.py
├── main.py                     # Litestar app factory
├── controllers/                # Route controllers
│   ├── __init__.py
│   ├── users.py
│   └── items.py
├── models/                     # Database models
│   ├── __init__.py
│   └── user.py
├── dto/                        # Data Transfer Objects
│   ├── __init__.py
│   └── user.py
├── services/                   # Business logic
│   ├── __init__.py
│   └── user_service.py
└── lib/
    ├── database.py             # DB connection
    └── dependencies.py         # DI dependencies
```

## Architecture Rules

- **Controllers for route grouping.** Use `@get`, `@post`, etc. decorators on controller methods.
- **DTOs for input/output.** Define Pydantic models for request/response validation.
- **Dependency injection built-in.** Use `Provide` for injecting services, database sessions.
- **Async-first design.** All route handlers should be `async def`.

## Coding Conventions

- Create controller: `class UserController(Controller): path = '/users'` with route methods.
- Define routes: `@get('/') async def list_users(self) -> list[UserDTO]`.
- Use DTOs: `async def create_user(self, data: UserCreateDTO) -> UserDTO`.
- Dependency injection: `async def get_db() -> AsyncSession` then `@get('/', dependencies={'db': Provide(get_db)})`.

## Library Preferences

- **advanced-alchemy:** Litestar's SQLAlchemy integration.
- **pydantic:** Validation and serialization.
- **uvicorn:** ASGI server.
- **structlog:** Structured logging.

## NEVER DO THIS

1. **Never use sync database drivers.** Litestar is async. Use `asyncpg`, not `psycopg2`.
2. **Never skip DTO validation.** Litestar validates automatically with Pydantic. Don't manually validate.
3. **Never ignore the DI system.** Dependencies are resolved automatically. Don't instantiate services manually.
4. **Never forget to handle exceptions.** Use exception handlers for consistent error responses.
5. **Never use global state.** Use dependency injection for shared resources.
6. **Never mix Litestar with Flask patterns.** Litestar has its own patterns. Don't port Flask code blindly.
7. **Never ignore async context managers.** Database sessions should use `async with`.

## Testing

- Use Litestar's test client: `TestClient(app)`.
- Test controllers by calling methods with mock dependencies.
- Test DTOs by validating sample data.


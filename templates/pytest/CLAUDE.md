# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- pytest v8 (Python testing framework)
- Python 3.11+
- pytest-asyncio for async
- pytest-cov for coverage
- fixtures for dependency injection

## Project Structure
```
src/
├── ...                         # Source code
tests/
├── conftest.py                 # Shared fixtures
├── test_module.py              # Test modules
└── integration/
    └── test_api.py
pytest.ini                      # Pytest configuration
pyproject.toml                  # Alternative config location
```

## Architecture Rules

- **Fixtures for setup/teardown.** Reusable test dependencies.
- **Parametrize for data-driven tests.** Run same test with different inputs.
- **Plugins extend functionality.** Coverage, asyncio, mock support.
- **Simple assert statements.** No special assertion methods needed.

## Coding Conventions

- Run: `pytest` discovers and runs tests.
- Fixture: `@pytest.fixture def db(): ... yield db ... cleanup()`.
- Use fixture: `def test_user(db): ...` (argument name matches fixture name).
- Parametrize: `@pytest.mark.parametrize("input,expected", [("3+5", 8), ("2+4", 6)])`.
- Async: `@pytest.mark.asyncio async def test_async(): ...`.
- Mock: `monkeypatch.setattr(module, 'function', mock)` or `unittest.mock`.

## NEVER DO THIS

1. **Never use `print` for debugging.** Use `pytest -s` or `breakpoint()`.
2. **Never skip `conftest.py` for shared fixtures.** It's the idiomatic way to share.
3. **Never forget to clean up in fixtures.** Use `yield` and cleanup after.
4. **Never ignore `pytest.raises` for exceptions.** Test that code raises expected errors.
5. **Never use global state in tests.** Tests should be isolated—use fixtures.
6. **Never skip `tmp_path` fixture.** Temporary directories are built-in.
7. **Never mix sync and async tests carelessly.** Use `pytest-asyncio` properly.

## Testing

- Test with `pytest -v` for verbose output.
- Test with `pytest --cov=src` for coverage.
- Test with `pytest -x` to stop on first failure.


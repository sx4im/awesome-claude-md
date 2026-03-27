# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.11+ with redis-py 5.x as the primary Redis client
- hiredis-py for C-based protocol parsing (10x faster than pure Python parser)
- Redis 7.2+ with Redis Stack for JSON, Search, and TimeSeries modules
- Pydantic v2 for data validation before cache writes
- pytest with fakeredis for unit tests, testcontainers-redis for integration tests
- Poetry for dependency management, Ruff for linting

## Project Structure

```
src/
  cache/
    __init__.py
    backends.py        # RedisBackend, RedisClusterBackend classes
    decorators.py      # @cached, @cache_aside, @write_through decorators
    serializers.py     # JSON, MessagePack, Pickle serializers
    key_builder.py     # Deterministic cache key generation
  pubsub/
    __init__.py
    publisher.py       # Event publishing with retry logic
    subscriber.py      # Consumer groups and message handlers
    channels.py        # Channel name constants and patterns
  streams/
    __init__.py
    producer.py        # XADD with MAXLEN trimming
    consumer.py        # XREADGROUP with pending message recovery
    processors.py      # Stream message processing pipelines
  models/
    __init__.py
    schemas.py         # Pydantic models for cached entities
  config.py            # Redis connection settings via pydantic-settings
  connection.py        # Connection pool and Sentinel setup
tests/
  conftest.py
  test_cache/
  test_pubsub/
  test_streams/
```

## Architecture Rules

- Always use connection pools; never create ad-hoc Redis connections. Initialize a single `redis.asyncio.ConnectionPool` at startup and share it across the application.
- Use Redis pipelines for any operation that issues 3 or more commands in sequence. This reduces round-trips from N to 1.
- All cache keys must be namespaced with the format `{service}:{entity}:{identifier}`, e.g., `users:profile:42`.
- Set explicit TTLs on every key. No key should live forever unless it is a configuration value stored in a Redis hash.
- Use Lua scripts via `register_script()` for any read-modify-write operation that must be atomic.
- Pub/Sub subscribers must handle reconnection automatically using the `redis.asyncio.client.PubSub` retry mechanism.
- Stream consumers must use consumer groups with explicit ACK. Always call `XACK` after successful processing.

## Coding Conventions

- Use `redis.asyncio` (async client) for all I/O-bound operations. The sync client is only acceptable in CLI scripts.
- Type-annotate all function signatures. Use `redis.asyncio.Redis` as the type, not `redis.Redis`.
- Wrap all Redis calls in try/except for `redis.ConnectionError` and `redis.TimeoutError`. Never let connection failures crash the application.
- Use MessagePack (`msgpack`) for serialization of cached objects; fall back to JSON only for human-readable debug caches.
- Log every cache miss at DEBUG level and every connection failure at ERROR level using structlog.

## Library Preferences

- redis-py 5.x over aioredis (which is now merged into redis-py)
- hiredis for protocol parsing in production
- msgpack over pickle for serialization (safer, cross-language compatible)
- fakeredis over mockredispy for testing
- redis-om-python only if you need ActiveRecord-style ORM; prefer raw redis-py otherwise

## File Naming

- All Python files use snake_case: `cache_backends.py`, `stream_consumer.py`
- Test files mirror source: `src/cache/decorators.py` -> `tests/test_cache/test_decorators.py`
- Lua scripts go in `src/lua/` with `.lua` extension and are loaded at module init

## NEVER DO THIS

1. Never use `KEYS *` in production. Use `SCAN` with a cursor for key enumeration to avoid blocking the server.
2. Never store objects larger than 512KB in a single key. Break large objects into hashes or use Redis JSON.
3. Never use `FLUSHDB` or `FLUSHALL` outside of test fixtures. Gate destructive commands behind environment checks.
4. Never rely on Redis as a primary data store without persistence configured. Always treat Redis as ephemeral unless AOF with `appendfsync everysec` is enabled.
5. Never subscribe to patterns (`PSUBSCRIBE`) when exact channel names are known. Pattern subscriptions are slower and harder to debug.
6. Never use `SELECT` to switch databases. Use key namespacing instead; multiple databases are deprecated in Redis Cluster.
7. Never block the event loop with synchronous Redis calls in an async application. Always use `redis.asyncio`.

## Testing

- Use `fakeredis.aioredis.FakeRedis` for unit tests that need a Redis-like interface without a running server.
- Use `testcontainers.redis.RedisContainer` for integration tests that require real Redis behavior (Lua scripts, modules).
- Every cache decorator must have tests for hit, miss, and expiration scenarios.
- Test Pub/Sub handlers by publishing to a channel and asserting the handler was called within a 2-second timeout.
- Stream consumer tests must verify that pending messages are recovered after a simulated crash (XPENDING + XCLAIM).
- Run `redis-cli --latency` checks in CI to catch performance regressions in pipeline-heavy code paths.

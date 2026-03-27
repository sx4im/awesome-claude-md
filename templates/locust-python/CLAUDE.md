# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Python 3.12+ with type hints throughout
- Locust 2.29+ as the distributed load testing framework
- gevent for coroutine-based concurrency (Locust's underlying engine)
- requests (via Locust HttpUser) for HTTP testing
- grpc + locust-plugins for gRPC protocol testing
- Faker for realistic test data generation
- pandas for post-test result analysis
- Docker Compose for local distributed mode (1 master + N workers)

## Project Structure

```
locustfiles/
  api/
    user_crud.py        # User CRUD endpoint tasks
    checkout.py         # Checkout flow tasks
    search.py           # Search and filtering tasks
  web/
    browsing.py         # Page browsing simulation
shapes/
  ramp_up.py            # Custom LoadTestShape for gradual ramp
  spike.py              # Spike pattern shape
  diurnal.py            # 24-hour traffic pattern simulation
lib/
  base_user.py          # Base HttpUser with auth, headers, logging
  data_pool.py          # Thread-safe test data pool with recycling
  checks.py             # Response validation helpers
  events.py             # Custom event listeners for metrics
config/
  environments.py       # Host URLs and environment settings
  __init__.py
data/
  users.csv             # Pre-created test user credentials
  products.json         # Product catalog for search/cart tests
scripts/
  run_distributed.sh    # Launch master + workers locally
  analyze_results.py    # Parse CSV results into summary report
conftest.py             # Shared pytest fixtures for unit testing tasks
docker-compose.yml      # Distributed mode: master + 4 workers
```

## Architecture Rules

- All user classes inherit from a project-specific `BaseUser` that handles authentication and default headers
- Use `@task(weight)` decorators with explicit weights to control traffic distribution across endpoints
- Define `on_start()` for per-user setup (login, token refresh) and `on_stop()` for cleanup
- Use `TaskSet` classes to group related tasks; nest them for multi-step user journeys
- Custom `LoadTestShape` classes define traffic patterns; never rely on command-line ramp parameters for repeatable tests
- Fire custom events via `self.environment.events.request.fire()` for tracking business metrics alongside latency
- Use `self.client.request()` with `catch_response=True` for custom pass/fail logic on response content

## Coding Conventions

- One locustfile per API domain or user journey; combine via `locust -f locustfiles/` directory mode
- Type annotate all functions and class attributes; use `typing.Protocol` for shared interfaces
- Task methods are named `task_<action>_<resource>`, e.g., `task_create_order`, `task_search_products`
- Response validation uses `catch_response=True` context manager to mark failures with descriptive messages
- Environment config accessed via `self.environment.parsed_options` or custom `--config` argument
- Log at WARNING level for unexpected responses, ERROR for unrecoverable failures, DEBUG for request details
- Use `between(1, 5)` for wait_time; never set `wait_time = constant(0)` unless testing pure throughput

## Library Preferences

- locust-plugins for additional protocols (gRPC, Kafka, WebSocket, MongoDB)
- Faker over hand-rolled random data for realistic payloads
- pandas for result CSV analysis; matplotlib for charts in reports
- tenacity for retry logic in on_start authentication flows
- orjson over stdlib json for faster serialization in high-throughput scenarios
- structlog for structured logging in distributed worker output

## File Naming

- Locustfiles: snake_case matching the domain, e.g., `user_crud.py`, `checkout.py`
- Shape classes: snake_case in `shapes/` directory, e.g., `ramp_up.py`
- Library modules: snake_case in `lib/`
- Data files: snake_case with `.csv` or `.json` extension
- Config: `environments.py` with dataclass-based settings per stage

## NEVER DO THIS

1. Never use `time.sleep()` in tasks; Locust uses gevent, so use `gevent.sleep()` or rely on `wait_time`
2. Never share mutable state between users without `gevent.lock.Semaphore`; users run as greenlets
3. Never hardcode host URLs in locustfiles; always use `self.host` which comes from `--host` or config
4. Never skip response validation; always use `catch_response=True` and check status codes and body content
5. Never run distributed mode without verifying master-worker connectivity first via `locust --master --expect-workers=N`
6. Never store large datasets in memory per user; use `itertools.cycle` with a shared data pool in module scope

## Testing

- Unit test task logic by calling task methods directly with a mocked `self.client` using `unittest.mock`
- Smoke test every locustfile with `locust -f <file> --headless -u 1 -t 10s` before committing
- Validate custom LoadTestShape tick output with a unit test that asserts `(user_count, spawn_rate)` at each second
- Run distributed smoke: `docker-compose up --scale worker=2` with 10 users for 30 seconds
- Export results with `--csv=results/run` flag; parse `results/run_stats.csv` for CI threshold checks
- Threshold gates in CI: p95 latency under 500ms, error rate under 1%, achieved RPS within 10% of target
- Compare results across runs using `scripts/analyze_results.py` which reads CSV and produces a delta report

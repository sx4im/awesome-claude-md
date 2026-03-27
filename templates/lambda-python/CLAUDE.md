# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Runtime: AWS Lambda Python 3.12
- IaC: AWS SAM (template.yaml)
- API Layer: API Gateway REST API with Lambda Proxy Integration
- Database: DynamoDB (single-table design, on-demand capacity)
- AWS SDK: boto3 and botocore (included in Lambda runtime)
- Validation: Pydantic v2 for request/response models
- Logging: AWS Lambda Powertools for Python (structured JSON logging)
- Package Manager: pip with requirements.txt per function
- Testing: pytest with moto for AWS service mocking
- Linting: Ruff (linter and formatter in one tool)
- Type Checking: mypy (strict mode)

## Project Structure

```
src/
  handlers/
    get_item.py         # GET /items/{id} handler
    list_items.py       # GET /items handler
    create_item.py      # POST /items handler
    delete_item.py      # DELETE /items/{id} handler
    process_queue.py    # SQS queue consumer handler
  models/
    item.py             # Pydantic models for Item entity
    api.py              # Pydantic models for API request/response
  services/
    dynamodb.py         # DynamoDB table resource and query helpers
    sqs.py              # SQS send_message helpers
    s3.py               # S3 upload/download helpers
  utils/
    response.py         # API Gateway proxy response builder
    decorators.py       # Custom decorators (error handling, validation)
    env.py              # Typed environment variable access
  __init__.py
tests/
  unit/
    test_get_item.py    # Unit tests per handler
    test_create_item.py
  integration/
    conftest.py         # Shared fixtures (DynamoDB table setup via moto)
    test_api.py         # Integration tests
template.yaml           # SAM template with all Lambda functions and resources
samconfig.toml          # SAM deployment configuration
pyproject.toml          # Ruff, mypy, and pytest configuration
requirements.txt        # Shared dependencies (pydantic, powertools)
```

## Architecture Rules

- Every handler function has the signature `def handler(event: dict, context: LambdaContext) -> dict`.
- Use the Powertools `@event_source` decorator to parse API Gateway events into typed objects.
- DynamoDB uses single-table design: all entities in one table with `PK` and `SK` string attributes.
- Composite keys follow the pattern: `PK=USER#<user_id>`, `SK=ITEM#<item_id>`.
- boto3 clients and resources are created at module level (outside the handler) for connection reuse across warm invocations.
- Keep Lambda deployment packages under 50MB (250MB unzipped). Use Lambda Layers for shared dependencies.
- All responses go through `response.py` helper to ensure consistent headers, CORS, and JSON serialization.

## Coding Conventions

- Handler pattern: parse event, validate input with Pydantic, call service, return response.
- Use Powertools Logger: `logger = Logger(service="my-service")` and decorate handlers with `@logger.inject_lambda_context`.
- Use Powertools Tracer: `tracer = Tracer()` and decorate handlers with `@tracer.capture_lambda_handler`.
- Pydantic models for all API input: `item = ItemCreate.model_validate_json(event["body"])`.
- DynamoDB operations use the Table resource (high-level): `table.get_item(Key={"PK": pk, "SK": sk})`.
- Environment variables accessed via typed helper: `settings = Settings()` using Pydantic BaseSettings.
- Use `decimal.Decimal` for DynamoDB number types, never float.

## Library Preferences

- Validation: Pydantic v2 (not marshmallow, cerberus, or attrs)
- Logging/Tracing: aws-lambda-powertools (not raw logging module)
- AWS mocking: moto (not localstack for unit tests)
- HTTP client: httpx (async support) or urllib3 (already in Lambda runtime)
- Date/time: standard library datetime with timezone-aware objects (UTC)
- Linting: Ruff (replaces flake8, isort, black in a single tool)
- Type checking: mypy with strict mode enabled

## File Naming

- All Python files: snake_case (`get_item.py`, `dynamodb.py`)
- Test files: `test_<module>.py` prefix (pytest convention)
- Handler files: named after the operation (`create_item.py`, `process_queue.py`)
- Model files: named by entity (`item.py`, `user.py`)
- Configuration: `pyproject.toml` for all tool configuration (Ruff, mypy, pytest)

## NEVER DO THIS

1. Never create boto3 clients or resources inside the handler function -- create them at module level for connection reuse.
2. Never use `print()` for logging -- use Powertools Logger for structured JSON logs that work with CloudWatch Insights.
3. Never use `float` for DynamoDB numbers -- use `decimal.Decimal` to avoid precision loss.
4. Never catch bare `Exception` without re-raising or logging -- always catch specific exceptions (`ClientError`, `ValidationError`).
5. Never use `os.environ.get()` without a default or validation -- use Pydantic BaseSettings for typed env access.
6. Never install boto3 in requirements.txt -- it is included in the Lambda runtime and pinning it bloats the package.
7. Never use synchronous HTTP calls in handlers that process multiple items -- use `concurrent.futures.ThreadPoolExecutor` for parallel API calls.

## Testing

- Use pytest as the test runner with fixtures defined in `conftest.py`.
- Mock AWS services with moto: `@mock_aws` decorator creates in-memory DynamoDB, S3, SQS.
- Create DynamoDB table fixtures that match the `template.yaml` table definition exactly.
- Test handlers by constructing API Gateway event dicts with `pathParameters`, `body`, and `headers`.
- Assert on response `statusCode`, parsed `body` JSON, and `headers` (CORS).
- Use `pytest.mark.parametrize` for testing multiple input scenarios per handler.
- Integration tests use `sam local invoke` or `sam local start-api` with Docker.
- Run the full suite: `pytest tests/ -v --cov=src --cov-report=term-missing` and `ruff check src/ tests/` in CI.

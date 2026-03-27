# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Runtime: AWS Lambda Node.js 20.x
- Language: TypeScript 5.x (strict mode, ES2022 target)
- IaC: AWS SAM (template.yaml)
- API Layer: API Gateway REST API (not HTTP API)
- Database: DynamoDB (single-table design)
- Package Manager: pnpm with workspace support
- Bundler: esbuild via SAM build
- Testing: Jest with @aws-sdk/client-mock
- Linting: ESLint with @typescript-eslint
- Logging: Powertools for AWS Lambda (structured JSON logs)

## Project Structure

```
src/
  handlers/
    getItem.ts          # GET /items/{id} handler
    listItems.ts        # GET /items handler
    createItem.ts       # POST /items handler
    deleteItem.ts       # DELETE /items/{id} handler
  middleware/
    validation.ts       # Middy middleware for input validation
    errorHandler.ts     # Centralized error handling middleware
  services/
    dynamodb.ts         # DynamoDB DocumentClient singleton and helpers
    sqs.ts              # SQS send message helpers
  models/
    item.ts             # Zod schemas and TypeScript types
  utils/
    response.ts         # API Gateway proxy response builder
    env.ts              # Typed environment variable access
tests/
  unit/                 # Unit tests per handler
  integration/          # Tests against local DynamoDB
template.yaml           # SAM template with all resources
samconfig.toml          # SAM deployment configuration
tsconfig.json
```

## Architecture Rules

- Every Lambda handler exports a single `handler` function wrapped with Middy middleware stack.
- Use the Middy middleware pattern: `middy(baseHandler).use(validator()).use(errorHandler())`.
- DynamoDB access goes through `services/dynamodb.ts` -- never instantiate clients in handlers directly.
- Single-table design: all entities share one DynamoDB table with `PK` and `SK` attributes.
- Use composite keys: `PK=USER#<userId>`, `SK=ITEM#<itemId>` for entity relationships.
- Lambda functions must complete within 29 seconds (API Gateway timeout). Set handler timeout to 30s.
- Environment variables are defined in `template.yaml` and accessed through typed `env.ts` helper.

## Coding Conventions

- Handler signature: `APIGatewayProxyHandler` from `aws-lambda` types.
- Return responses using the builder: `response(200, { data })` which sets CORS headers and serializes JSON.
- Parse path parameters from `event.pathParameters`, query strings from `event.queryStringParameters`.
- Use Powertools Logger: `const logger = new Logger({ serviceName: 'my-service' })`.
- Add correlation IDs via Powertools: `logger.addContext(context)` in every handler.
- Define DynamoDB operations with the v3 SDK: `@aws-sdk/client-dynamodb` and `@aws-sdk/lib-dynamodb`.

## Library Preferences

- Middleware: @middy/core with @middy/http-json-body-parser
- Validation: Zod (not Joi or Yup)
- AWS SDK: v3 only (@aws-sdk/*), never v2 (aws-sdk)
- Observability: @aws-lambda-powertools/logger, @aws-lambda-powertools/tracer
- HTTP client: native fetch (available in Node 20)
- UUID: crypto.randomUUID() (built into Node 20)

## File Naming

- Handler files: camelCase matching the operation (`getItem.ts`, `createUser.ts`)
- Test files: `<handler>.test.ts` in the tests/ directory mirroring src/ structure
- Model files: singular noun in camelCase (`item.ts`, `user.ts`)
- SAM template: always `template.yaml` at project root

## NEVER DO THIS

1. Never use `aws-sdk` v2 -- always use modular `@aws-sdk/client-*` v3 packages to keep bundle size small.
2. Never create DynamoDB client instances inside handler functions -- use a module-level singleton for connection reuse.
3. Never use `console.log` -- use Powertools Logger for structured JSON logs that work with CloudWatch Insights.
4. Never store secrets in environment variables in template.yaml -- use AWS Secrets Manager or SSM Parameter Store with dynamic references.
5. Never use `callback` style handlers -- always use async/await and return the response object directly.
6. Never deploy with `sam deploy` without `--guided` on first deploy or without `samconfig.toml`.

## Testing

- Unit tests mock AWS SDK calls using `@aws-sdk/client-mock` (mockClient from `aws-sdk-client-mock`).
- Create a mock DynamoDB client: `const ddbMock = mockClient(DynamoDBDocumentClient)` and set up `.on(GetCommand).resolves({...})`.
- Test handlers by constructing `APIGatewayProxyEvent` objects with the needed path parameters and body.
- Integration tests use `sam local invoke` or Docker-based local DynamoDB (`amazon/dynamodb-local`).
- Run `sam build && sam local start-api` for local API testing.
- Assert on response statusCode, parsed JSON body, and that DynamoDB commands were called with expected parameters.
- Aim for 80%+ coverage on handler logic; skip coverage on thin AWS SDK wrapper code.

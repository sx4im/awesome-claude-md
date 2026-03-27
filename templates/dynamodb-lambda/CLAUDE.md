# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- AWS DynamoDB with on-demand capacity mode for unpredictable workloads, provisioned mode with auto-scaling for steady-state
- AWS Lambda with Node.js 20.x runtime and ES modules
- AWS SDK v3 (@aws-sdk/client-dynamodb and @aws-sdk/lib-dynamodb) with the DynamoDBDocumentClient
- TypeScript 5.x with strict mode
- SST (Serverless Stack) v3 for infrastructure-as-code and local development
- Vitest for unit tests, aws-sdk-client-mock for DynamoDB client mocking
- esbuild for Lambda bundling via SST

## Project Structure

```
packages/
  core/
    src/
      entities/
        user.ts              # Entity definition with key schema
        order.ts
        product.ts
      access-patterns/
        user-queries.ts      # All access patterns for user entity
        order-queries.ts
      table/
        design.ts            # Single-table key schema definitions
        gsi.ts               # GSI definitions (GSI1, GSI2, GSI3)
        projections.ts       # Attribute projections per GSI
      utils/
        expressions.ts       # Expression builder helpers
        batch.ts             # BatchWrite/BatchGet with retry
        transaction.ts       # TransactWrite helpers
        pagination.ts        # Cursor-based pagination with LastEvaluatedKey
  functions/
    src/
      api/
        create-order.ts      # API Gateway Lambda handler
        get-user.ts
        list-orders.ts
      streams/
        order-stream.ts      # DynamoDB Streams processor
        aggregate.ts         # Stream-based aggregation updater
      triggers/
        ttl-cleanup.ts       # TTL deletion stream handler
  infra/
    dynamo.ts                # Table and GSI definitions in SST
    api.ts                   # API Gateway routes
    streams.ts               # Stream event source mappings
```

## Architecture Rules

- Use single-table design. All entities share one DynamoDB table with overloaded partition and sort keys. The table has a primary key `PK` (String) and sort key `SK` (String).
- Define up to 3 GSIs named `GSI1`, `GSI2`, `GSI3` with keys `GSI1PK`/`GSI1SK`, etc. Each GSI enables a specific access pattern documented in `access-patterns/`.
- Entity key patterns follow `{ENTITY}#{id}` format. Example: `PK=USER#123, SK=USER#123` for user, `PK=USER#123, SK=ORDER#2024-01-15#456` for orders belonging to a user.
- Use DynamoDB Streams with `NEW_AND_OLD_IMAGES` for change data capture. Stream processors update denormalized data and aggregation counters.
- All write operations that modify multiple items must use `TransactWriteItems` to ensure atomicity. Never perform multi-item writes without transactions.
- Use sparse GSIs for query patterns that apply only to a subset of items. Only populate the GSI key attributes on items that should appear in the index.

## Coding Conventions

- Use `DynamoDBDocumentClient` (from `@aws-sdk/lib-dynamodb`) for automatic marshalling. Never manually construct `{ S: "value" }` attribute maps.
- Build filter, condition, and projection expressions using helper functions that generate `ExpressionAttributeNames` and `ExpressionAttributeValues`. Never hardcode expression strings.
- Lambda handlers follow the pattern: validate input with Zod, call the access pattern function, return formatted API Gateway response with proper status code.
- Always set `ReturnConsumedCapacity: 'TOTAL'` in development to monitor read/write capacity consumption per operation.
- Use `ExpressionAttributeNames` with `#` prefixes for all attribute names, even non-reserved words, for consistency: `#pk`, `#status`, `#createdAt`.
- Handle `ConditionalCheckFailedException` explicitly in every conditional write. Map it to a 409 Conflict HTTP response.

## Library Preferences

- @aws-sdk/lib-dynamodb (Document Client) over raw @aws-sdk/client-dynamodb
- SST v3 over Serverless Framework or AWS SAM for IaC and local dev
- Vitest over Jest for faster test execution with native ESM support
- aws-sdk-client-mock over aws-sdk-mock for SDK v3 compatibility
- Zod over class-validator for Lambda input validation
- ElectroDB or dynamodb-toolbox as optional entity modeling helpers

## File Naming

- All files use kebab-case: `create-order.ts`, `user-queries.ts`
- Lambda handlers: `{verb}-{entity}.ts` (e.g., `create-order.ts`, `get-user.ts`, `list-orders.ts`)
- Stream processors: `{entity}-stream.ts`
- Infrastructure: `dynamo.ts`, `api.ts`, `streams.ts`

## NEVER DO THIS

1. Never use `Scan` for application queries. Every query must use `Query` on the table or a GSI. Scans are only acceptable for data migration scripts run offline.
2. Never store items larger than 100KB. If an item approaches this size, move large attributes to S3 and store the S3 key in DynamoDB.
3. Never use `BatchWriteItem` when you need atomicity. Batch operations are not transactional; individual items can fail. Use `TransactWriteItems` instead.
4. Never hardcode table names in Lambda functions. Pass the table name as an environment variable set by SST.
5. Never use `ConsistentRead: true` on GSIs. GSIs only support eventually consistent reads; attempting consistent reads throws an error.
6. Never use monotonically increasing partition keys like auto-increment IDs. This creates hot partitions. Use ULIDs or composite keys that distribute writes evenly.

## Testing

- Unit test access pattern functions using aws-sdk-client-mock to mock DynamoDB responses. Assert that the correct `KeyConditionExpression` and `FilterExpression` are sent.
- Test transaction helpers by mocking `TransactWriteCommand` and verifying all items in the `TransactItems` array.
- Test DynamoDB Streams handlers by passing mock `DynamoDBStreamEvent` objects directly to the Lambda handler function.
- Integration tests use SST's local development mode which proxies Lambda invocations to your local machine against a real DynamoDB table.
- Test pagination by mocking a response with `LastEvaluatedKey` and verifying the next request passes it as `ExclusiveStartKey`.
- Validate single-table design by writing a test that performs every documented access pattern and asserts correct results.

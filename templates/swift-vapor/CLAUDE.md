# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Swift 5.9+ with strict concurrency checking enabled
- Vapor 4 web framework with async/await throughout
- Fluent ORM with PostgreSQL driver (fluent-postgres-driver)
- Redis for session storage and caching (vapor/redis)
- JWT for authentication (vapor/jwt), Queues framework for background jobs

## Project Structure

```
Sources/
  App/
    Controllers/
      UserController.swift
      AuthController.swift
    Models/
      User.swift
      Token.swift
    Migrations/
      CreateUser.swift
      CreateToken.swift
    DTOs/
      UserDTO.swift
      CreateUserRequest.swift
    Middleware/
      JWTAuthMiddleware.swift
    Jobs/
      EmailJob.swift
    Extensions/
      Request+Services.swift
    configure.swift
    routes.swift
  Run/
    main.swift
Tests/
  AppTests/
    UserControllerTests.swift
Package.swift
```

## Architecture Rules

- Every route handler must be in a Controller conforming to RouteCollection
- All database models use UUID as the primary key type, never Int
- Use Content protocol for request/response DTOs, keep them separate from Fluent models
- All Fluent queries must use async/await, never EventLoopFuture
- Middleware goes on route groups, not globally, unless it applies to every route
- Database transactions wrap multi-step mutations: use db.transaction {}

## Coding Conventions

- Use Swift's structured concurrency: async let for parallel work, TaskGroup for dynamic concurrency
- Mark all Fluent model properties with @ID, @Field, @OptionalField, @Parent, @Children, @Siblings
- Validate request payloads by conforming DTOs to Validatable
- Throw Abort errors with meaningful HTTP status codes and reason strings
- Use Environment.get() for configuration, never hardcode secrets

## Library Preferences

- HTTP client: Vapor's built-in AsyncHTTPClient, not URLSession
- Testing: XCTest with XCTVapor for integration tests
- Password hashing: Bcrypt via Vapor's built-in support
- Serialization: Codable with custom CodingKeys when API naming differs from Swift conventions

## File Naming

- Models: singular PascalCase (User.swift, OrderItem.swift)
- Controllers: PascalCase with Controller suffix (UserController.swift)
- Migrations: verb-noun pattern (CreateUser.swift, AddEmailToUser.swift)
- DTOs: PascalCase with purpose suffix (CreateUserRequest.swift, UserResponse.swift)
- Tests: mirror source structure with Tests suffix (UserControllerTests.swift)

## NEVER DO THIS

1. Never use .wait() on an EventLoopFuture — it will deadlock the event loop
2. Never access req.db outside of the request lifecycle — pass the database reference explicitly
3. Never store request-scoped state in a Controller property — controllers are shared across requests
4. Never skip Fluent migrations or edit existing ones after deployment — create new migrations instead
5. Never use raw SQL when Fluent query builder supports the operation
6. Never return Fluent models directly from routes — map to DTOs to control the API surface
7. Never disable TLS verification in production HTTPClient configurations

## Testing

- Use XCTVapor's app.test() for integration tests that hit real route handlers
- Test against a separate PostgreSQL database configured via TEST_DATABASE_URL
- Use app.autoMigrate() in setUp and app.autoRevert() in tearDown
- Write unit tests for business logic that does not depend on Vapor or Fluent
- Mock external HTTP calls by injecting a test-specific HTTPClient
- Run tests with: swift test --parallel

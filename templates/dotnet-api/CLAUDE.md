# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- .NET 8+ with C# 12
- ASP.NET Core Minimal APIs (or Controllers for large projects)
- Entity Framework Core 8 + PostgreSQL
- MediatR for CQRS
- FluentValidation for request validation
- Serilog for structured logging

## Project Structure

```
src/
├── Api/                     # HTTP layer (endpoints, middleware, filters)
│   ├── Endpoints/           # Minimal API endpoint classes grouped by feature
│   │   ├── UserEndpoints.cs
│   │   └── OrderEndpoints.cs
│   ├── Middleware/
│   └── Program.cs           # App startup and DI configuration
├── Application/             # Use cases, handlers, DTOs
│   ├── Users/
│   │   ├── Commands/        # CreateUser, UpdateUser (MediatR commands)
│   │   ├── Queries/         # GetUser, ListUsers (MediatR queries)
│   │   └── Dtos/
│   └── Common/
│       ├── Behaviors/       # MediatR pipeline (validation, logging)
│       └── Interfaces/      # Repository interfaces
├── Domain/                  # Entities, value objects, domain events
│   ├── Entities/
│   ├── ValueObjects/
│   └── Exceptions/
├── Infrastructure/          # EF Core, external services, email
│   ├── Persistence/
│   │   ├── AppDbContext.cs
│   │   ├── Configurations/  # EF Fluent API configs per entity
│   │   └── Migrations/
│   └── Services/
└── Tests/
```

## Architecture Rules

- **Clean Architecture layers.** Domain has zero dependencies. Application depends on Domain. Infrastructure implements Application interfaces. Api wires everything with DI.
- **CQRS with MediatR.** Every use case is a command (`CreateUserCommand`) or query (`GetUserQuery`) handled by a dedicated handler class. Endpoints dispatch requests through MediatR. they never call services directly.
- **Minimal APIs for new endpoints.** Group endpoints by feature using static classes with `MapGroup`. Use `TypedResults` for compile-time response type checking. Controllers only if you need filters or model binding that Minimal APIs don't support.
- **Entity Framework configuration via Fluent API.** One `IEntityTypeConfiguration<T>` per entity in `Infrastructure/Persistence/Configurations/`. Never use data annotations (`[Required]`, `[MaxLength]`) on domain entities. keep the domain layer persistence-ignorant.
- **Repository pattern for complex queries.** Simple CRUD can use `DbContext` directly in handlers. Complex queries with joins, projections, or dynamic filters get a repository interface in Application and implementation in Infrastructure.

## Coding Conventions

- **File-scoped namespaces.** `namespace Api.Endpoints;`. not the block-scoped `namespace Api.Endpoints { }`. One less level of indentation everywhere.
- **Primary constructors for DI.** `public class UserHandler(IUserRepository repo, ILogger<UserHandler> logger)`. not separate constructor + field assignment boilerplate.
- **Nullable reference types enabled.** `<Nullable>enable</Nullable>` in `.csproj`. Every reference type that can be null is `string?`. No more `NullReferenceException` surprises.
- **`record` types for DTOs and commands.** `public record CreateUserCommand(string Name, string Email) : IRequest<UserDto>;`. Immutable, concise, pattern-matchable.
- **Async all the way.** Every I/O method is `async Task<T>`. Never call `.Result` or `.Wait()` on Tasks. it deadlocks ASP.NET's synchronization context.

## Library Preferences

- **Validation:** FluentValidation. not data annotations (FluentValidation is composable, testable, and keeps validation outside domain entities). Wire into MediatR pipeline with a validation behavior.
- **Logging:** Serilog. not built-in `ILogger` alone (Serilog has structured logging, sinks for Seq/Elasticsearch/Console, and enrichers). Configure in `Program.cs` with `UseSerilog()`.
- **Mapping:** Mapperly. not AutoMapper (Mapperly generates code at compile time via source generators, zero runtime reflection). Not manual mapping unless trivial.
- **CQRS:** MediatR. lightweight, no ceremony. Pipeline behaviors replace cross-cutting concerns (validation, logging, transaction management).

## NEVER DO THIS

1. **Never use `async void`.** It swallows exceptions and can't be awaited. Use `async Task` for everything. The only exception is event handlers in UI frameworks. not applicable in APIs.
2. **Never call `.Result` or `.Wait()` on async code.** It deadlocks in ASP.NET. Use `await` everywhere. If you're in synchronous code that must call async, you have an architecture problem.
3. **Never put EF data annotations on domain entities.** `[Required]`, `[MaxLength(100)]` on domain classes couples them to persistence. Use Fluent API in `IEntityTypeConfiguration<T>`.
4. **Never use `DbContext` as a singleton.** It's scoped per request by default. Changing this causes concurrency bugs because `DbContext` is not thread-safe.
5. **Never return `IQueryable` from repositories.** It leaks data access concerns into application layer. Return `IReadOnlyList<T>`, `T?`, or `PagedResult<T>`.
6. **Never hardcode connection strings.** Use `IConfiguration` with environment-specific `appsettings.{Environment}.json`. Secrets go in user secrets (dev) or environment variables (prod).
7. **Never throw generic `Exception`.** Create domain-specific exceptions (`UserNotFoundException`, `InsufficientBalanceException`) and map them to proper HTTP status codes in middleware.

## Testing

- **Unit tests:** xUnit + NSubstitute (not Moq. licensing concerns). Test handlers in isolation by mocking repository interfaces.
- **Integration tests:** `WebApplicationFactory<Program>` for in-memory API testing. Use Testcontainers for real PostgreSQL.
- **Architecture tests:** NetArchTest to enforce layer dependency rules (Domain doesn't reference Infrastructure).
- Name tests: `MethodName_Should_ExpectedResult_When_Condition`.

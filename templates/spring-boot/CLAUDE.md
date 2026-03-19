# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Java 21+ (or Kotlin)
- Spring Boot 3.2+
- Spring Data JPA + Hibernate
- PostgreSQL 15+
- Spring Security + JWT
- Gradle (Kotlin DSL) or Maven
- Flyway for database migrations

## Project Structure

```
src/main/java/com/company/project/
├── config/                  # Security, CORS, OpenAPI, bean definitions
│   ├── SecurityConfig.java
│   └── OpenApiConfig.java
├── controller/              # REST controllers (thin: delegates to service)
│   ├── UserController.java
│   └── OrderController.java
├── service/                 # Business logic layer
│   ├── UserService.java
│   └── OrderService.java
├── repository/              # Spring Data JPA repositories
│   ├── UserRepository.java
│   └── OrderRepository.java
├── model/
│   ├── entity/              # JPA entities
│   │   ├── User.java
│   │   └── Order.java
│   ├── dto/                 # Request/response DTOs
│   │   ├── UserRequest.java
│   │   └── UserResponse.java
│   └── mapper/              # Entity ↔ DTO mappers (MapStruct)
├── exception/               # Custom exceptions + global handler
│   ├── ResourceNotFoundException.java
│   └── GlobalExceptionHandler.java
└── Application.java         # Main class
```

## Architecture Rules

- **Controller → Service → Repository.** Controllers handle HTTP and validation. Services contain business logic. Repositories do data access. Nothing bypasses this chain.
- **DTOs at the boundary, entities inside.** Controllers accept and return DTOs. Services can work with entities internally. Never return JPA entities from REST endpoints. they leak database structure and cause lazy loading exceptions.
- **MapStruct for entity ↔ DTO mapping.** Generate mappers at compile time. Never write manual mapping code with 20 getter/setter lines. Define a `@Mapper(componentModel = "spring")` interface and let MapStruct implement it.
- **Records for DTOs.** Use Java `record` types for request and response DTOs. They're immutable, auto-generate `equals`/`hashCode`/`toString`, and work natively with Jackson.
- **Constructor injection only.** Never use `@Autowired` on fields. Use `@RequiredArgsConstructor` (Lombok) or explicit constructors. Field injection hides dependencies and breaks testability.

## Coding Conventions

- **Package by feature, not by layer** when the project grows beyond 10 entities. Move from `controller/`, `service/`, `repository/` to `user/`, `order/`, `payment/` packages where each contains its own controller, service, and repository.
- **Bean Validation on DTOs.** Use `@Valid` on controller parameters. Annotate DTO fields: `@NotBlank`, `@Email`, `@Size(min = 8)`. Never validate manually in service code when annotations work.
- **Use `Optional` correctly.** Return `Optional<T>` from repository methods only. Never use `Optional` as a method parameter or field. In service code, use `.orElseThrow(() -> new ResourceNotFoundException("User", id))`.
- **Logging with SLF4J.** Use `@Slf4j` (Lombok) and structured messages: `log.info("User created: userId={}", user.getId())`. Never use `System.out.println`.
- **Application properties:** use `application.yml` (not `.properties`). Profile-specific configs in `application-dev.yml`, `application-prod.yml`.

## Library Preferences

- **Mapping:** MapStruct. Not ModelMapper (MapStruct generates code at compile time, ModelMapper uses reflection at runtime. slower, harder to debug).
- **Boilerplate reduction:** Lombok (`@Data`, `@Builder`, `@Slf4j`, `@RequiredArgsConstructor`). use sparingly on entities, freely on DTOs.
- **Migrations:** Flyway. not Liquibase (Flyway uses plain SQL migrations, easier to review). Name migrations `V1__create_users_table.sql`.
- **API docs:** SpringDoc OpenAPI. not Swagger 2 / SpringFox (SpringFox is abandoned).
- **Testing:** JUnit 5 + Mockito + Testcontainers. Not JUnit 4.

## NEVER DO THIS

1. **Never return JPA entities from controllers.** Entities have bidirectional relationships, lazy proxies, and internal fields. One accidental serialization and you get infinite recursion or `LazyInitializationException`. Map to DTOs.
2. **Never use `@Autowired` field injection.** It's untestable without Spring context. Use constructor injection. the compiler ensures all dependencies are provided.
3. **Never catch generic `Exception` in controllers.** Use a `@RestControllerAdvice` global exception handler that maps specific exceptions to proper HTTP status codes and error response DTOs.
4. **Never use `CrudRepository` when `JpaRepository` exists.** `JpaRepository` extends `CrudRepository` with flush, batch operations, and pagination. There's no reason to use the limited interface.
5. **Never put business logic in controllers.** A controller method should be 5-10 lines: validate, call service, return response. If you're writing `if` chains in a controller, extract to service.
6. **Never use `spring.jpa.hibernate.ddl-auto=update` in production.** Use Flyway migrations. `ddl-auto=update` doesn't handle column renames, data migrations, or index changes safely.
7. **Never store secrets in `application.yml`.** Use environment variables: `${DB_PASSWORD}` in YAML, actual values in deployment config. Never commit credentials.

## Testing

- **Unit tests:** Mockito for service tests. Mock repositories, verify interactions.
- **Integration tests:** `@SpringBootTest` with Testcontainers for real PostgreSQL. Use `@Transactional` for automatic rollback.
- **Controller tests:** `@WebMvcTest` with `MockMvc`. Test request validation, response shape, and status codes without starting the full app.
- **Repository tests:** `@DataJpaTest` with an in-memory H2 or Testcontainers PostgreSQL.
- Name tests: `{method}_should{ExpectedBehavior}_when{Condition}` → `createUser_shouldReturn201_whenValidRequest`.

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Scala 3.3+ (LTS)
- Play Framework 3.0+ (based on Pekko, the Apache fork of Akka)
- Slick 3.5+ for database access
- PostgreSQL 15+
- Apache Pekko for actors and streaming (replaces Akka)
- sbt 1.9+ build tool
- play-json for JSON serialization

## Project Structure

```
app/
├── controllers/
│   ├── UserController.scala       # Action methods, thin: parse → service → Ok(json)
│   └── AuthController.scala
├── services/
│   ├── UserService.scala          # Business logic, returns Future[Either[AppError, T]]
│   └── AuthService.scala
├── repositories/
│   ├── UserRepository.scala       # Slick queries, returns Future[Option[User]]
│   └── Tables.scala               # Slick table definitions (code-generated or manual)
├── models/
│   ├── User.scala                 # Case classes for domain models
│   ├── dto/                       # Request/response case classes with Reads/Writes
│   └── errors/
│       └── AppError.scala         # Sealed trait error hierarchy
├── filters/                       # Request logging, auth, CORS filters
├── modules/
│   └── AppModule.scala            # Guice bindings (or compile-time DI wiring)
└── util/
    └── JsonFormats.scala          # Shared implicit Reads/Writes/Formats
conf/
├── application.conf               # HOCON config: DB, secrets, play settings
├── routes                         # Play routes file: GET /api/users controllers.UserController.list
└── evolutions/default/            # Database evolution scripts (ups and downs)
test/                              # Mirrors app/ structure with *Spec.scala files
project/
├── build.properties               # sbt version
└── plugins.sbt                    # Play plugin, sbt-scalafix, etc.
build.sbt                          # Project definition, library deps
```

## Architecture Rules

- **Controllers are thin.** Parse request with `Action.async(parse.json)`, validate with `json.validate[CreateUserRequest]`, call service, pattern match on `Either[AppError, T]`, return `Ok(Json.toJson(result))` or error response. No business logic.
- **Services return `Future[Either[AppError, T]]`.** Never throw exceptions for expected failures. Use `Left(AppError.NotFound(...))` for domain errors. `Right(user)` for success. Exceptions are only for unexpected failures (database down, network errors).
- **Repositories return `Future[Option[T]]` or `Future[Seq[T]]`.** Repos contain only Slick queries. No business logic. No HTTP concepts. `findById` returns `Future[Option[User]]`, never throws on missing.
- **Dependency injection via Guice or compile-time DI.** Controllers take services as constructor parameters: `@Inject() class UserController(userService: UserService, cc: ControllerComponents)`. Never use `Play.application` global state.
- **Routes file is the API contract.** Every endpoint is declared in `conf/routes`. Use proper HTTP methods. Type parameters in routes: `GET /api/users/:id controllers.UserController.get(id: Long)`. Never use catch-all routes.

## Coding Conventions

- **Scala 3 syntax:** Use `given`/`using` instead of `implicit`. Use `enum` for sealed type hierarchies: `enum AppError { case NotFound(msg: String); case Conflict(msg: String) }`. Use extension methods instead of implicit classes.
- **JSON serialization:** Use play-json with `Reads`, `Writes`, and `Format` type classes. Define in companion objects: `object User { given Format[User] = Json.format[User] }`. Use `Json.toJson(obj)` and `request.body.validate[T]`.
- **For-comprehensions for Future chains.** Chain `Future[Either[AppError, T]]` with `EitherT` from cats, or use nested for-comprehensions with early return on `Left`. Never use nested `.flatMap` callbacks more than 2 levels deep.
- **Slick queries:** Use compiled queries for parameterized lookups: `val findById = Compiled((id: Rep[Long]) => users.filter(_.id === id))`. Compiled queries are precompiled and cached.
- **Error responses:** Define a `toResult` method on `AppError`: `NotFound → NotFound(json)`, `Conflict → Conflict(json)`, `ValidationError → UnprocessableEntity(json)`. Use pattern matching in controllers.

## Library Preferences

- **Framework:** Play 3.0+ (Pekko-based). Not Play 2.x (Akka licensing issues). Not http4s (different paradigm—Play is better for MVC teams).
- **Database:** Slick. Not Doobie (Slick integrates natively with Play's async model). Not Anorm (raw SQL without type safety).
- **JSON:** play-json. Not circe (play-json integrates natively, zero setup). Not spray-json (unmaintained).
- **Actors/streaming:** Pekko (Apache fork of Akka). Not Akka (BSL license since 2.7+). Pekko is API-compatible and Apache-licensed.
- **Testing:** ScalaTest with Play's test helpers.

## File Naming

- Source files: `PascalCase.scala` matching the primary type → `UserController.scala`, `UserService.scala`
- One primary type per file. Companion objects live in the same file as their class.
- Test files: `PascalCaseSpec.scala` → `UserControllerSpec.scala`
- Config: `application.conf` (HOCON), `routes` (no extension)
- Evolutions: `{number}.sql` in `conf/evolutions/default/` → `1.sql`, `2.sql`

## NEVER DO THIS

1. **Never use Akka 2.7+ in new projects.** Akka switched to BSL (Business Source License). Use Apache Pekko instead—it's API-compatible with Akka 2.6 and Apache-licensed. Play 3.0 already uses Pekko.
2. **Never block inside a `Future`.** Calling `Await.result` inside an `Action.async` blocks the thread pool and causes deadlocks under load. If you need the result, keep it in the `Future` chain with `.map` and `.flatMap`.
3. **Never use `Play.application` or `Play.current`.** These are deprecated global accessors. Use dependency injection. If you need `Configuration`, inject it: `@Inject() class MyService(config: Configuration)`.
4. **Never use `implicit` in Scala 3 code.** Use `given`/`using` for type class instances and context parameters. `implicit` still compiles but is deprecated style and will confuse tooling.
5. **Never write raw SQL strings with string interpolation in Slick.** Use Slick's query DSL or `sql"..."` interpolator with typed parameters. String concatenation in SQL is an injection vulnerability.
6. **Never skip database evolutions.** Play evolutions track schema versions. Every schema change gets a numbered evolution file with `# --- !Ups` and `# --- !Downs` sections. Never modify the database schema by hand in production.
7. **Never use `Action { }` (synchronous) for I/O operations.** Use `Action.async { }` with `Future`. Synchronous actions block the default thread pool. Every handler that calls a service or database must be async.

## Testing

- Use `PlaySpec` with `GuiceOneAppPerSuite` for integration tests that need a running application.
- Use `WithApplication` for controller tests: inject the controller, call action methods, assert on status and JSON body.
- Slick repository tests: use an in-memory H2 database or Testcontainers with PostgreSQL. Run evolutions before each test suite.
- Mock services with ScalaMock or hand-written fakes. Keep mocks at service boundaries only.
- Run `sbt test`, `sbt scalafmtCheck`, and `sbt "scalafixAll --check"` in CI.

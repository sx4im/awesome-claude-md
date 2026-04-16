# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Martini (classy Go web framework)
- Go 1.22+
- Dependency injection
- Minimalist design
- Middleware stack

## Project Structure
```
cmd/
└── server/
    └── main.go                 // Entry point
handlers/
└── handlers.go                 // Route handlers
middleware/
└── middleware.go               // Custom middleware
```

## Architecture Rules

- **Dependency injection.** Services injected into handlers.
- **Middleware stack.** `Use()` adds handlers to stack.
- **Reflection-based DI.** Type-based service resolution.
- **Minimalist.** Small, focused API surface.

## Coding Conventions

- Handler: `func Hello(res http.ResponseWriter, req *http.Request, db *sql.DB) { res.Write([]byte("Hello")) }`. Services injected by type.
- Route: `m.Get("/", Hello)`.
- Service: `m.Map(&db)` maps a *sql.DB instance for injection.
- Middleware: `m.Use(func(res http.ResponseWriter, req *http.Request) { ... })`.

## NEVER DO THIS

1. **Never use Martini for new projects.** No longer maintained—use Gin or Echo.
2. **Never ignore the DI overhead.** Reflection has performance cost.
3. **Never forget service mapping order.** Map before routes that use them.
4. **Never skip error handling in middleware.** Can break the chain.
5. **Never use without understanding `martini.Classic()`.** Sets up logging, recovery, static.
6. **Never forget handler signature matters.** Must match injected services.
7. **Never ignore the `ReturnHandler`.** For custom return types.

## Testing

- Test handlers with injected mocks.
- Test middleware chain.
- Note: Consider migrating to actively maintained framework.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Gorilla Mux (Go URL router)
- Go 1.22+
- Standard library compatible
- Path matching, variables
- Middleware support

## Project Structure
```
cmd/
└── server/
    └── main.go                 // Entry point
internal/
├── handlers/
│   └── api.go                  // HTTP handlers
├── middleware/
│   └── logging.go
└── routes/
    └── routes.go               // Mux setup
```

## Architecture Rules

- **Stdlib compatible.** Works with `net/http.Handler`.
- **Powerful routing.** Path variables, regex, methods.
- **Subrouters.** Route groups with prefixes and middleware.
- **Middleware chain.** `Use()` for per-route or subrouter middleware.

## Coding Conventions

- Router: `r := mux.NewRouter()`.
- Route: `r.HandleFunc("/users/{id}", getUser).Methods("GET")`.
- Vars: `vars := mux.Vars(r); id := vars["id"]`.
- Subrouter: `api := r.PathPrefix("/api").Subrouter(); api.Use(authMiddleware)`.
- Middleware: `r.Use(loggingMiddleware)` where `func loggingMiddleware(next http.Handler) http.Handler { return http.HandlerFunc(...) }`.

## NEVER DO THIS

1. **Never forget `Methods()` constraint.** Without it, route matches all methods.
2. **Never use without `StrictSlash`.** Configure trailing slash behavior.
3. **Never ignore path cleaning.** `UseEncodedPath()` for encoded paths.
4. **Never skip middleware ordering.** Order matters in chain.
5. **Never use regex routes excessively.** Performance impact.
6. **Never forget `Walk` for route inspection.** Useful for debugging.
7. **Never ignore `NotFoundHandler`.** Custom 404 handling.

## Testing

- Test with `httptest.NewRecorder`.
- Test path variables extraction.
- Test middleware chain execution.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Echo (Go web framework)
- Go 1.22+
- High performance
- Middleware system
- HTTP/2 support

## Project Structure
```
cmd/
└── server/
    └── main.go                 // Entry point
internal/
├── handlers/
│   └── user.go                 // HTTP handlers
├── middleware/
│   └── auth.go
└── routes/
    └── routes.go               // Route registration
```

## Architecture Rules

- **Minimalist design.** Fewer features than Gin, more than stdlib.
- **Middleware chain.** `Use()` adds middleware to routes.
- **Context-centric.** `echo.Context` carries request/response.
- **Auto TLS.** Automatic HTTPS via Let's Encrypt.

## Coding Conventions

- Handler: `func getUser(c echo.Context) error { id := c.Param("id"); return c.JSON(200, user) }`.
- Route: `e.GET("/users/:id", getUser)`.
- Middleware: `e.Use(middleware.Logger()); e.Use(middleware.Recover())`.
- Group: `api := e.Group("/api"); api.Use(authMiddleware)`.
- Binding: `var u User; if err := c.Bind(&u); err != nil { return err }`.

## NEVER DO THIS

1. **Never ignore error returns.** Echo handlers return errors.
2. **Never skip middleware recovery.** `middleware.Recover()` catches panics.
3. **Never use without `c.Validate()`.** Echo supports validation—use it.
4. **Never forget context cancellation.** Check `c.Request().Context()`.
5. **Never use `c.String()` for APIs.** Use `c.JSON()` for consistency.
6. **Never ignore the `Binder` interface.** Customize binding for complex inputs.
7. **Never skip rate limiting.** Use `middleware.RateLimiter()` or external.

## Testing

- Test with `net/http/httptest`.
- Test middleware chain order.
- Test handler error responses.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Gin (Go web framework)
- Go 1.22+
- Martini-inspired API
- Fast HTTP router
- Middleware support

## Project Structure
```
cmd/
└── api/
    └── main.go                 // Entry point
internal/
├── handlers/
│   └── user.go                 // Route handlers
├── models/
│   └── user.go                 // Data models
├── middleware/
│   └── logger.go
└── router/
    └── router.go               // Route setup
```

## Architecture Rules

- **Fast routing.** Radix tree based, faster than stdlib `net/http`.
- **Middleware system.** Global and per-route middleware.
- **JSON validation.** Built-in binding and validation.
- **Error management.** Collect and format errors.

## Coding Conventions

- Handler: `func getUser(c *gin.Context) { id := c.Param("id"); c.JSON(200, gin.H{"user": user}) }`.
- Route: `router.GET("/users/:id", getUser)`.
- Group: `v1 := router.Group("/v1"); v1.Use(authMiddleware)`.
- Middleware: `func authMiddleware(c *gin.Context) { ... c.Next() }`.
- Binding: `type Login struct { User string `json:"user" binding:"required"`; Password string `json:"password" binding:"required"` }`.

## NEVER DO THIS

1. **Never use `c.String` for JSON APIs.** Use `c.JSON` consistently.
2. **Never ignore binding errors.** `if err := c.ShouldBind(&json); err != nil { c.JSON(400, gin.H{"error": err.Error()}) }`.
3. **Never use global middleware for all routes.** Be selective with `Use()`.
4. **Never forget to validate input.** Use `binding:"required"` tags.
5. **Never use `c.MustBind` in production.** Panics on error—handle gracefully.
6. **Never ignore the `Abort()` method.** Stop middleware chain when needed.
7. **Never skip security headers.** Add `Secure`, `X-Content-Type-Options`, etc.

## Testing

- Test with `net/http/httptest`.
- Test binding validation rules.
- Test middleware execution order.


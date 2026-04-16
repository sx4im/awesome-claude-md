# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Iris (fast Go web framework)
- Go 1.22+
- High performance
- MVC and API modes
- Websocket support

## Project Structure
```
cmd/
└── server/
    └── main.go                 // Entry point
controllers/
└── users_controller.go         // MVC controllers
models/
└── user.go                     // Data models
views/
└── *.html                      // Templates
```

## Architecture Rules

- **Fastest Go framework.** Optimized for performance.
- **MVC or API.** Choose pattern per route.
- **Party subdomains.** Route groups with domain/subdomain.
- **Access log and recovery.** Built-in middleware.

## Coding Conventions

- App: `app := iris.New()`.
- Handler: `app.Get("/users/{id:uint64}", getUser)` where `func getUser(ctx iris.Context) { id := ctx.Params().GetUint64Default("id", 0) }`.
- MVC: `mvc.New(app.Party("/users")).Register(userService).Handle(new(UserController))`.
- Template: `ctx.View("user.html")` or `ctx.JSON(user)`.
- Party: `api := app.Party("/api"); api.Use(myMiddleware)`.

## NEVER DO THIS

1. **Never ignore the `ctx` object.** Central to Iris—learn its methods.
2. **Never skip `app.Run` configuration.** `iris.Addr(":8080")` or `iris.TLS`.
3. **Never forget type assertions in params.** `GetUint64Default`, `GetInt`, etc.
4. **Never use MVC for simple APIs.** Direct handlers are faster for APIs.
5. **Never ignore `hero` dependency injection.** For clean handlers.
6. **Never skip error handling.** `ctx.StopWithError` for early returns.
7. **Never use without profiling.** Iris is fast—verify with benchmarks.

## Testing

- Test with `httptest`.
- Test MVC binding.
- Test performance benchmarks.


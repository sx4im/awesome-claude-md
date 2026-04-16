# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Buffalo (Go web framework)
- Go 1.22+
- Full-stack Go
- Webpack asset pipeline
- Pop ORM

## Project Structure
```
actions/
├── app.go                      // App setup
├── home.go                     // Handlers
└── render.go                   // Template config
assets/
├── css/
├── js/
└── images/
models/
└── user.go                     // Pop models
templates/
└── *.html                      // Plush templates
```

## Architecture Rules

- **Rails-inspired.** Convention over configuration.
- **Asset pipeline.** Webpack for JS/CSS compilation.
- **Pop ORM.** ActiveRecord-like ORM for Go.
- **Generators.** CLI scaffolding for rapid development.

## Coding Conventions

- Handler: `func HomeHandler(c buffalo.Context) error { return c.Render(200, r.HTML("index.html")) }`.
- Model: `type User struct { ID uuid.UUID; Name string; CreatedAt time.Time; UpdatedAt time.Time }`.
- Route: `APP.GET("/", HomeHandler)`.
- Middleware: `APP.Use(someMiddleware)`.

## NEVER DO THIS

1. **Never ignore the `buffalo` CLI.** `buffalo dev` for development.
2. **Never skip database migrations.** Use `buffalo pop` for migrations.
3. **Never mix models and handlers.** Keep MVC separation.
4. **Never forget the `render` setup.** Required for templates.
5. **Never use without understanding `context`.** Buffalo's `Context` is central.
6. **Never skip `database.yml` config.** Required for Pop ORM.
7. **Never ignore the asset pipeline.** Use `buffalo build` for production.

## Testing

- Test with `buffalo test`.
- Test models with test database.
- Test handlers with `buffalo.Request`.


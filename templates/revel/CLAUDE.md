# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Revel (high-productivity Go framework)
- Go 1.22+
- Hot code reload
- Comprehensive stack
- Convention-based

## Project Structure
```
app/
├── controllers/
│   └── app.go                  // Controllers
├── models/
│   └── user.go                 // Models
├── views/
│   └── App/
│       └── Index.html          // Templates
├── init.go                     // Initialization
└── routes                      // Routes file
conf/
└── app.conf                    // Configuration
```

## Architecture Rules

- **Hot reload.** Code changes reflected immediately.
- **Comprehensive.** Includes routing, MVC, ORM, testing, caching.
- **Interceptors.** Before/after filters for controllers.
- **Validation.** Built-in validation framework.

## Coding Conventions

- Controller: `type App struct { *revel.Controller } func (c App) Index() revel.Result { return c.Render() }`.
- Route: `GET / App.Index` in `conf/routes`.
- Model: `type User struct { Id int; Name string; validator.Validator }`.
- Validation: `func (user *User) Validate(v *revel.Validation) { v.Check(user.Name, validator.Required{}, validator.Match{regexp.MustCompile("[a-zA-Z]+")) }`.

## NEVER DO THIS

1. **Never use without `revel` CLI.** `revel run` for development.
2. **Never skip the `init.go` file.** App initialization required.
3. **Never ignore interceptor order.** `revel.BEFORE`, `revel.AFTER`.
4. **Never mix validation with controller logic.** Use model validation.
5. **Never forget `results` configuration.** `conf/results` for custom results.
6. **Never skip testing framework.** Revel has built-in testing.
7. **Never use for small APIs.** Revel is comprehensive—use for full apps.

## Testing

- Test with `revel test`.
- Test controllers with `revel.TestRequest`.
- Test models with validation.


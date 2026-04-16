# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Beego (Go web framework)
- Go 1.22+
- MVC architecture
- ORM included
- Hot reload

## Project Structure
```
conf/
└── app.conf                    // Configuration
controllers/
├── default.go                  // Controllers
└── user.go
models/
└── user.go                     // Models
routers/
└── router.go                   // Route registration
views/
└── index.tpl                   // Templates
main.go                         // Entry point
```

## Architecture Rules

- **MVC pattern.** Models, views, controllers separation.
- **Bee tool.** CLI for scaffolding and hot reload.
- **Built-in ORM.** Database operations without external libs.
- **Modular design.** Use only needed modules.

## Coding Conventions

- Controller: `type MainController struct { beego.Controller } func (c *MainController) Get() { c.Data["Website"] = "beego.me"; c.TplName = "index.tpl" }`.
- Model: `type User struct { Id int; Name string }; func GetUserById(id int) (User, error) { ... }`.
- Route: `beego.Router("/", &controllers.MainController{})`.
- ORM: `o := orm.NewOrm(); user := User{Id: 1}; o.Read(&user)`.

## NEVER DO THIS

1. **Never ignore the `bee` CLI.** `bee run` for hot reload.
2. **Never skip `app.conf` setup.** Required for configuration.
3. **Never mix MVC with other patterns.** Stick to Beego's MVC.
4. **Never forget `Prepare()` method.** For common controller setup.
5. **Never use raw SQL without ORM.** Beego ORM handles many cases.
6. **Never ignore module selection.** Import only needed: `github.com/beego/beego/v2/server/web`.
7. **Never skip validation.** Beego has built-in validation—use it.

## Testing

- Test controllers with `beego.TestBeegoInit`.
- Test models with test database.
- Test routes with `httptest`.


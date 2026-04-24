# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Go Service Frameworks)

### Release Discipline
- Preserve explicit request validation, timeout, and context propagation behavior.
- Keep middleware ordering intentional and security-safe.
- Maintain backward compatibility for API contracts unless explicitly versioned.

### Merge/Release Gates
- Unit/integration tests pass for modified handlers and middleware.
- Error handling and status code behavior validated for edge cases.
- Race and concurrency-sensitive paths reviewed where applicable.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

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

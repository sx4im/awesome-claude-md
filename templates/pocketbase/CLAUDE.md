# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- PocketBase 0.23+ as backend framework with embedded SQLite database
- Go 1.22+ for custom backend extensions and hooks
- Real-time subscriptions via SSE for live data updates
- PocketBase Admin UI for collection management and data browsing
- PocketBase JavaScript SDK for client integration
- S3-compatible storage for file uploads (configurable)

## Project Structure

```
pb_project/
  main.go
  hooks/
    users.go
    orders.go
    notifications.go
  services/
    email.go
    payment.go
  middleware/
    ratelimit.go
    logging.go
  migrations/
    1700000001_create_products.go
    1700000002_create_orders.go
  utils/
    validation.go
  types/
    models.go
  pb_data/
  pb_migrations/
  tests/
    users_test.go
    orders_test.go
  go.mod
  go.sum
  Dockerfile
```

## Architecture Rules

- Extend PocketBase by embedding pocketbase.PocketBase in main.go and adding hooks
- All collection schema changes done through Go migration files, never through Admin UI in production
- Business logic in hooks/ responds to record lifecycle events (OnBeforeCreate, OnAfterUpdate)
- Complex operations go in services/, hooks call services, services call the DAO layer
- Custom API endpoints registered via app.OnBeforeServe with e.Router group
- Real-time subscriptions scoped by collection-level and record-level rules

## Coding Conventions

- Use app.Dao() for database operations, never raw SQL on the SQLite file
- Access record fields through record.Get("field") and record.Set("field", value)
- API rules (collection permissions) defined in migration files, not hardcoded in hooks
- Custom endpoints return JSON via e.JSON(http.StatusOK, data) pattern
- Hook functions grouped by collection in separate files
- Error responses use apis.NewBadRequestError() and related helpers

## Library Preferences

- HTTP routing: PocketBase's embedded echo router via e.Router
- Validation: Go's built-in validation plus PocketBase's field-level validation rules
- Email: PocketBase's built-in mailer (app.NewMailClient()) with customizable templates
- Client SDK: PocketBase JavaScript SDK (pocketbase) for frontend integration
- Cron: app.OnBeforeServe with robfig/cron/v3 for scheduled tasks
- Logging: PocketBase's built-in structured logger via app.Logger()

## File Naming

- Go files use snake_case: user_hooks.go, email_service.go
- Migration files prefixed with Unix timestamp: 1700000001_description.go
- Test files use Go convention: filename_test.go colocated in same package
- Collection names are plural snake_case: users, order_items

## NEVER DO THIS

1. Never modify pb_data/data.db directly — always use the DAO or Admin API
2. Never define collection schemas in Admin UI for production — use migration files
3. Never skip API rules on collections — empty rules mean no access, "*" means public access
4. Never use app.Dao().DB() for writes without wrapping in app.Dao().RunInTransaction()
5. Never store secrets in collection records — use environment variables or app settings
6. Never rely on client-side filtering for security — enforce access control in API rules

## Testing

- Use Go's standard testing package with testify/assert for assertions
- Create test PocketBase instances with pocketbase.NewWithConfig pointing to temp directories
- Test hooks by creating records through the test app's DAO and verifying side effects
- Test custom endpoints using httptest.NewRecorder with the app's echo router
- Seed test data using app.Dao().SaveRecord() in test setup functions
- Use t.Parallel() for independent tests to speed up the test suite
- Run tests with: go test ./... -v -count=1

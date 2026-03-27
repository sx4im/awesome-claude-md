# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Directus 11.x headless CMS and data platform
- PostgreSQL as the primary database
- TypeScript for all custom extensions
- Directus SDK (@directus/sdk) for programmatic API access
- Custom extensions: endpoints, hooks, operations, interfaces, displays
- Directus Flows for no-code/low-code automation with custom operations

## Project Structure

```
extensions/
  src/
    endpoints/
      custom-reports/
        index.ts
      import-export/
        index.ts
    hooks/
      audit-log/
        index.ts
      data-sync/
        index.ts
    operations/
      send-slack-notification/
        index.ts
        api.ts
        app.ts
    interfaces/
      map-picker/
        index.ts
        interface.vue
    displays/
      status-badge/
        index.ts
        display.vue
    modules/
      analytics-dashboard/
        index.ts
        module.vue
  migrations/
    20240101A-create-custom-tables.ts
snapshots/
  production-schema.yaml
docker-compose.yml
.env
```

## Architecture Rules

- All custom logic lives in Directus extensions, never in external middleware or proxy layers
- Endpoint extensions register Express-compatible routes under /custom/ namespace
- Hook extensions react to CRUD events (items.create, items.update) and system events
- Operation extensions integrate into Directus Flows for visual workflow automation
- Schema changes tracked via Directus schema snapshots (YAML) and applied with directus schema apply
- Database migrations for data changes that schema snapshots cannot capture

## Coding Conventions

- Endpoint extensions export a default function receiving router and context: (router, context) => {}
- Hook extensions export a default function receiving filter and action event registrars
- Use context.services.ItemsService for CRUD operations within extensions, not raw SQL
- Access the database via context.database (Knex) only when ItemsService is insufficient
- Respect Directus accountability by passing the user's accountability to service constructors
- Environment variables accessed via context.env, not process.env

## Library Preferences

- Database access: Directus ItemsService for CRUD, Knex (via context.database) for complex queries
- Auth: Directus built-in auth with configurable providers (OAuth2, LDAP, SAML)
- File storage: Directus built-in storage adapters (local, S3, GCS, Azure)
- Email: Directus built-in mailer via context.services.MailService
- Schema management: Directus CLI schema snapshot and apply commands
- Client SDK: @directus/sdk with composable client (rest, graphql, realtime, auth)
- Admin UI extensions: Vue 3 with Directus's design system components

## File Naming

- Extension directories named with kebab-case describing their purpose
- Each extension has an index.ts entry point
- Operation extensions split into api.ts (server-side) and app.ts (admin UI config)
- Interface and display extensions use a .vue file for the UI component
- Migration files prefixed with date and letter sequence: 20240101A-description.ts

## NEVER DO THIS

1. Never modify Directus system tables (directus_users, directus_roles) via raw SQL
2. Never bypass Directus's permission system by using admin accountability in user-facing endpoints
3. Never store schema changes only in the database — export to schema snapshots for version control
4. Never use process.env in extensions — use context.env to access environment variables
5. Never install extensions by copying files manually — use the Directus extension SDK build system
6. Never create REST endpoints that duplicate Directus's built-in CRUD API

## Testing

- Use Vitest for testing extension logic in isolation
- Test endpoint extensions by creating a mock router and context object
- Test hook extensions by invoking registered event handlers with mock event data
- Test operation extensions by calling the handler with mock operation context
- Use @directus/sdk in integration tests to verify extensions through the Directus API
- Run a test Directus instance via Docker Compose with a separate test database
- Seed test data using ItemsService in test setup, clean up via truncation
- Run tests with: npx vitest run

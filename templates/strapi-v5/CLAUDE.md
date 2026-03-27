# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Strapi v5 headless CMS with TypeScript enabled
- PostgreSQL as the database (better-sqlite3 for local dev only)
- Strapi Document Service API for content operations (replaces Entity Service)
- Custom controllers and services for business logic beyond CRUD
- Strapi's built-in RBAC with Users & Permissions plugin
- Cloudinary or AWS S3 provider for media uploads

## Project Structure

```
src/
  api/
    article/
      content-types/article/
        schema.json
      controllers/
        article.ts
      services/
        article.ts
      routes/
        article.ts
    category/
      content-types/category/
        schema.json
      controllers/
        category.ts
      services/
        category.ts
      routes/
        category.ts
  components/
    shared/
      seo.json
      media.json
  plugins/
    custom-analytics/
      server/
        index.ts
      admin/src/
        index.tsx
  middlewares/
    rate-limiter.ts
  policies/
    is-owner.ts
config/
  database.ts
  server.ts
  middlewares.ts
  plugins.ts
```

## Architecture Rules

- Use the Document Service API (strapi.documents) for all content operations, never Entity Service
- Content types defined in schema.json files, never created exclusively through Admin UI in production
- Controllers extend core controller factories: use createCoreController and override specific actions
- Services extend core service factories: use createCoreService for data access, add custom methods
- Policies enforce authorization rules, middlewares handle cross-cutting concerns
- Lifecycle hooks defined in content-types for side effects (afterCreate, beforeUpdate)

## Coding Conventions

- Always use TypeScript for controllers, services, routes, and policies
- Access content via strapi.documents('api::article.article').findMany() pattern
- Custom controllers call this.service() to access the corresponding service
- Use Strapi's sanitizeOutput and validateQuery in custom controllers for security
- Environment-specific config uses env() helper: env('DATABASE_HOST', 'localhost')
- Draft/publish handled via document service status parameter, not custom fields

## Library Preferences

- Database: PostgreSQL for production, SQLite for local dev
- Media: @strapi/provider-upload-cloudinary or @strapi/provider-upload-aws-s3
- Email: @strapi/provider-email-sendgrid or @strapi/provider-email-nodemailer
- Search: Strapi's built-in filters, meilisearch plugin for full-text search
- i18n: @strapi/plugin-i18n for content localization (built-in)

## File Naming

- API directories are singular kebab-case: src/api/article/, src/api/blog-post/
- Content type UIDs follow api::singular.singular pattern: api::article.article
- Component categories are kebab-case folders: src/components/shared/
- Config files match Strapi conventions exactly: database.ts, server.ts, middlewares.ts

## NEVER DO THIS

1. Never use the deprecated Entity Service API (strapi.entityService) — use Document Service
2. Never modify content types through Admin UI in production — define schemas in code
3. Never bypass Strapi's sanitization by returning raw database results from controllers
4. Never hardcode API tokens or secrets in config files — use environment variables with env()
5. Never install Strapi plugins without adding them to config/plugins.ts
6. Never modify files in node_modules/@strapi — use extensions/ directory for customization

## Testing

- Use Jest with ts-jest preset for unit and integration testing
- Create a Strapi test instance using strapi().load() in global setup
- Test custom controllers via supertest against the Strapi HTTP server
- Test services through strapi.service('api::article.article')
- Mock external providers (email, upload) in test configuration
- Seed test content using the Document Service in beforeAll hooks
- Run tests with: yarn test --runInBand (Strapi requires sequential execution)

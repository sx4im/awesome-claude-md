# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- KeystoneJS 6 headless CMS and application framework
- TypeScript for all schema and custom code
- PostgreSQL as the database backend (via Prisma under the hood)
- GraphQL API auto-generated from schema definitions
- Admin UI auto-generated with React-based customization
- Node.js 20+ runtime

## Project Structure

```
keystone/
  schema.ts
  keystone.ts
  auth.ts
  lists/
    User.ts
    Post.ts
    Tag.ts
    Image.ts
  fields/
    slug.ts
    cloudinaryImage.ts
  access/
    rules.ts
    filters.ts
  hooks/
    post.hooks.ts
    user.hooks.ts
  graphql/
    extendGraphqlSchema.ts
    resolvers/
      analytics.ts
      search.ts
  seed/
    data.ts
    index.ts
  admin/
    pages/
      custom-dashboard.tsx
  migrations/
  .keystone/
```

## Architecture Rules

- All data models defined as Keystone list schemas in individual files under lists/
- Schema definitions exported and composed in schema.ts via list() function calls
- Access control defined as functions in access/rules.ts, referenced by every list and field
- Field-level and list-level access control always explicit — never rely on defaults
- Custom GraphQL resolvers extend the auto-generated schema via extendGraphqlSchema
- Hooks (beforeOperation, afterOperation) handle side effects in dedicated hook files
- Admin UI customization done through admin/ directory, never by modifying .keystone/ output

## Coding Conventions

- Define each list in its own file exporting a list() call with fields, access, hooks, and ui config
- Access control functions receive { session, context, listKey, operation } and return boolean or filter
- Use Keystone's built-in field types: text, integer, timestamp, relationship, select, image, file
- Relationship fields always specify ref with back-reference: ref: 'Post.author'
- Filter-based access returns Prisma-style where clauses for list-level read restrictions

## Library Preferences

- Database: PostgreSQL exclusively — Keystone 6 dropped SQLite for production
- GraphQL client: urql or Apollo Client on the frontend consuming Keystone's API
- Image storage: @keystone-6/cloudinary for Cloudinary, S3 via custom field
- Auth: Keystone's createAuth() with password-based authentication built-in
- Email: Resend or Nodemailer in custom hooks, not a Keystone plugin
- Migrations: Keystone's built-in Prisma migration system via keystone migrate commands

## File Naming

- List files: PascalCase matching the list name (User.ts, BlogPost.ts)
- Hook files: kebab-case with .hooks.ts suffix (post.hooks.ts)
- Access control: grouped in access/rules.ts and access/filters.ts
- Custom field files: camelCase in fields/ directory (slug.ts, cloudinaryImage.ts)
- GraphQL extensions: resolvers in graphql/resolvers/ named by domain

## NEVER DO THIS

1. Never edit files in the .keystone/ generated directory — they are overwritten on every build
2. Never use Prisma Client directly — use Keystone's context.query or context.db APIs
3. Never leave access control undefined on a list or field — Keystone defaults to public access
4. Never create circular relationship references without specifying one side as many: true
5. Never use raw SQL queries — Keystone's context.db provides type-safe Prisma operations
6. Never modify the auto-generated GraphQL schema — use extendGraphqlSchema to add custom types

## Testing

- Use Jest with ts-jest for testing hooks, access control, and custom resolvers
- Create a test Keystone context using setupTestRunner from @keystone-6/core/testing
- Test access control by calling rule functions with mock session objects
- Test hooks by creating/updating items through the test context and asserting side effects
- Test custom GraphQL resolvers using the test context's graphql.raw() method
- Seed development data using the seed/ module via a custom Keystone CLI command
- Run tests with: jest --runInBand (database tests require sequential execution)

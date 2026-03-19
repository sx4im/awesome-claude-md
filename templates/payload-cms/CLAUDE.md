# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Payload CMS 3.x (headless CMS + app framework)
- Next.js 14+ (Payload 3 is built on Next.js)
- TypeScript (strict mode)
- PostgreSQL or MongoDB
- Lexical rich text editor
- S3-compatible storage for uploads

## Project Structure

```
src/
├── app/
│   ├── (frontend)/          # Public-facing website routes
│   │   ├── page.tsx         # Home page
│   │   └── [slug]/page.tsx  # Dynamic pages from CMS
│   └── (payload)/           # Payload admin panel (auto-configured)
├── collections/
│   ├── Users.ts             # User collection (auth, roles)
│   ├── Pages.ts             # CMS-managed pages
│   ├── Posts.ts             # Blog posts
│   ├── Media.ts             # File uploads
│   └── hooks/               # Collection hooks (beforeChange, afterRead)
│       └── populateSlug.ts
├── globals/
│   ├── Header.ts            # Site header configuration
│   ├── Footer.ts            # Footer content
│   └── Settings.ts          # Global site settings
├── blocks/
│   ├── Hero.ts              # Hero section block
│   ├── ContentGrid.ts       # Grid layout block
│   └── CallToAction.ts      # CTA block
├── fields/
│   └── slug.ts              # Reusable slug field configuration
├── access/
│   ├── isAdmin.ts           # Admin-only access control
│   └── isAdminOrSelf.ts     # Admin or document owner
└── payload.config.ts        # Main Payload configuration
```

## Architecture Rules

- **Collections define content types.** Each collection (`Posts.ts`, `Pages.ts`) defines fields, hooks, access control, and admin UI config. The collection config IS the schema. Payload generates the database schema, API, and admin UI from it.
- **Blocks for flexible page layouts.** Pages use a `layout` field with block types (Hero, ContentGrid, CTA). Content editors compose pages by stacking blocks. Frontend renders each block type with a corresponding React component.
- **Globals for singleton content.** Site-wide settings (header nav, footer links, SEO defaults) are Globals, not Collections. Globals have exactly one document. no list, no IDs.
- **Access control is per-collection, per-operation.** Define `access: { read, create, update, delete }` on every collection. Use access control functions from `access/`. Never leave access wide open. the default is deny.
- **Hooks for side effects.** `beforeChange` hooks for slug generation, data validation, and computed fields. `afterChange` hooks for revalidation, webhook firing, and cache busting. Never put side effect logic in access control functions.

## Coding Conventions

- **Field reuse via factory functions.** Common fields (slug, meta description, published date) are defined once in `fields/` and imported into collections. Never copy field configs across collections.
- **Collection naming:** singular PascalCase for the file, plural for the `slug` property. `Posts.ts` → `slug: 'posts'`. API endpoints are: `GET /api/posts`, `GET /api/posts/:id`.
- **Typed access to Payload:** use generated types. Run `payload generate:types` after schema changes. Import `Post`, `Page`, `Media` types. never use `any` for document shapes.
- **Rich text with Lexical.** Payload 3 uses Lexical (not Slate). Configure custom nodes and features in the rich text field config. Render on the frontend with `@payloadcms/richtext-lexical/react`.
- **Hooks are thin.** A `beforeChange` hook validates or transforms data. Complex business logic lives in utility functions. Hooks call utilities. utilities don't know about Payload.

## Library Preferences

- **CMS:** Payload 3. runs in-process with Next.js. Not Strapi (separate process, REST-centric). Not Contentful (third-party, expensive).
- **Database:** PostgreSQL with Payload's Drizzle adapter (recommended for Payload 3). MongoDB if you need flexible schemas. Not SQLite (doesn't support Payload's concurrent query patterns).
- **Rich text:** Lexical (Payload 3 default, built by Meta). Not Slate (Payload 2 legacy).
- **Uploads:** S3-compatible storage via `@payloadcms/plugin-cloud-storage`. Not local disk in production.
- **Search:** Payload's built-in search plugin or Algolia integration. Not Elasticsearch (overkill for most CMS search).

## NEVER DO THIS

1. **Never leave access control unset.** Collections without explicit `access` config default to requiring authentication. Frontends need `read: () => true` for public content. Forgetting this means your API returns 401 for anonymous visitors.
2. **Never modify Payload's generated admin routes.** The `(payload)/` route group is managed by Payload. Customizing the admin UI goes through Payload's `admin` config, not by editing Next.js routes.
3. **Never query the database directly.** Use Payload's Local API: `payload.find({ collection: 'posts' })`. Direct database queries bypass access control, hooks, and field validation.
4. **Never store upload files on local disk in production.** Local storage doesn't work with serverless (Vercel) and doesn't scale. Use S3, Cloudflare R2, or another object store.
5. **Never hardcode field names in multiple places.** Use the field factory pattern from `fields/`. If a field name changes, it should change in one place.
6. **Never skip the `depth` parameter in queries.** `payload.find({ collection: 'posts', depth: 2 })` controls relationship population. Without `depth`, related documents return as IDs only. Too high a depth causes performance issues.
7. **Never run `payload generate:types` in CI.** Generated types are committed to git. They're dev-time artifacts, not build-time artifacts. Generating in CI means the database must be reachable during build.

## Testing

- Test access control functions directly. provide mock `req` objects and assert `true`/`false`.
- Test hooks by calling them with mock document data and verifying transformations.
- Integration test the Local API: seed data with `payload.create()`, query with `payload.find()`, assert results.
- E2E with Playwright for the admin panel. test content creation, editing, and publishing workflows.

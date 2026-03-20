# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- RedwoodJS 8+ (full-stack React framework)
- TypeScript (strict mode)
- GraphQL (with SDL-first schema)
- Prisma ORM + [PostgreSQL/SQLite]
- Storybook for component development
- Jest + @testing-library/react

## Project Structure

```
api/
├── src/
│   ├── graphql/             # SDL schema files (*.sdl.ts)
│   ├── services/            # Service functions (resolvers live here)
│   │   ├── users/
│   │   │   ├── users.ts
│   │   │   ├── users.test.ts
│   │   │   └── users.scenarios.ts
│   ├── directives/          # GraphQL directives (@requireAuth, @skipAuth)
│   ├── lib/
│   │   ├── auth.ts          # Auth decoder and getCurrentUser
│   │   ├── db.ts            # Prisma client singleton
│   │   └── logger.ts
│   └── functions/           # Serverless function handlers
├── db/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts
web/
├── src/
│   ├── components/          # Reusable UI components
│   ├── cells/               # Redwood Cells (auto-generated query components)
│   │   └── UsersCell/
│   │       ├── UsersCell.tsx
│   │       ├── UsersCell.test.tsx
│   │       └── UsersCell.mock.ts
│   ├── layouts/             # Layout components wrapping pages
│   ├── pages/               # Route-mapped page components
│   └── Routes.tsx           # All route definitions
```

## Architecture Rules

- **Cells are the data-fetching primitive.** Every component that fetches data MUST be a Cell. Cells export `QUERY`, `Loading`, `Empty`, `Failure`, and `Success` named exports. Never use raw `useQuery` or `fetch` in page components.
- **SDL defines the schema, services implement resolvers.** The SDL file declares types and queries/mutations. The corresponding service file contains the resolver functions. Never define resolver logic inline in SDL files.
- **Services are the only place for business logic.** Services call Prisma, enforce authorization, and contain domain rules. Cells and pages are presentation only.
- **Use `@requireAuth` and `@skipAuth` directives on every query/mutation.** RedwoodJS will throw a build error if a query or mutation lacks an auth directive. Never leave a resolver unprotected by accident.
- **Use Redwood's `validate` helper in services.** Import `validate` from `@redwoodjs/api` for input validation rather than writing manual checks or pulling in external validation libraries.

## Coding Conventions

- **File naming:** PascalCase for Cells (`UsersCell/UsersCell.tsx`), camelCase for services (`users.ts`), PascalCase for pages (`HomePage/HomePage.tsx`).
- **Cells must export all five states.** Always define `Loading`, `Empty`, `Failure`, `Success`, and `QUERY`. Omitting `Empty` or `Failure` causes silent rendering bugs.
- **Use Redwood's `navigate` and `routes` helpers.** Import from `@redwoodjs/router`. Never use `window.location` or raw anchor tags for internal navigation.
- **Prisma relations in services.** When resolving nested GraphQL types, add relation resolver functions in the service file (e.g., `User.posts = ...`). Never rely on Prisma `include` in the parent query to resolve nested fields.
- **Type safety with generated types.** Run `yarn rw generate types` after SDL changes. Import generated types from `types/graphql` in cells and services.

## Library Preferences

- **Auth:** Redwood's built-in auth (`@redwoodjs/auth`) with [dbAuth/Clerk/Supabase]. Never roll custom JWT logic.
- **Forms:** `@redwoodjs/forms` with `useForm`. Integrates with Cells and provides server-side error handling.
- **Styling:** [Tailwind CSS/CSS Modules]. Configured via `web/config/tailwind.config.js`.
- **Testing:** Jest + `@redwoodjs/testing/web` for Cells, `@redwoodjs/testing/api` for services.
- **Deployment:** [Vercel/Netlify/AWS Lambda] via `yarn rw deploy [TARGET]`.

## File Naming

- Cells: `web/src/cells/[Name]Cell/[Name]Cell.tsx`
- Pages: `web/src/pages/[Name]Page/[Name]Page.tsx`
- Services: `api/src/services/[name]/[name].ts`
- SDL: `api/src/graphql/[name].sdl.ts`
- Scenarios: `api/src/services/[name]/[name].scenarios.ts`

## NEVER DO THIS

1. **Never use `useEffect` + `fetch` to load data.** Use a Cell. Cells handle loading, empty, and error states automatically and integrate with Redwood's GraphQL client.
2. **Never write raw SQL in services.** Use Prisma's query builder. Raw SQL bypasses type safety and breaks Redwood's conventions.
3. **Never put auth logic in components.** Use `@requireAuth` directive on the SDL, `requireAuth()` calls in services, and `<Private>` route wrappers. Auth checks in components are bypassable.
4. **Never import from `api/` in `web/` directly.** The API and web sides are separate build targets. Share types through generated GraphQL types or the `types/` directory.
5. **Never skip scenario files for service tests.** Scenarios provide test fixtures through Prisma seeding. Writing manual `prisma.create` calls in tests is fragile and skips Redwood's test lifecycle.
6. **Never define routes outside `Routes.tsx`.** All routes must be declared in the single Routes file using `<Route>` components. Dynamic route generation elsewhere will silently fail.
7. **Never call `db` (Prisma) from a Cell or component.** Database access happens exclusively on the API side through services and resolvers.

## Testing

- **Service tests:** Use scenarios (`*.scenarios.ts`) to define test data. Test functions are called with `scenario` helper that seeds the database before each test.
- **Cell tests:** Use `render` from `@redwoodjs/testing/web`. Mock GraphQL responses with `mockGraphQLQuery` and `mockGraphQLMutation`.
- **Page tests:** Wrap with `<MemoryRouter>` and mock auth context. Test that correct Cells are rendered, not the data inside them.
- Run full test suite with `yarn rw test` (watches by default) or `yarn rw test --no-watch` in CI.

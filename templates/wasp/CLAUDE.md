# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Wasp 0.14+ (full-stack web framework with declarative DSL)
- React 18+ (client)
- Node.js + Express (server, auto-generated)
- Prisma ORM + [PostgreSQL/SQLite]
- TypeScript (strict mode)
- Vitest + @testing-library/react

## Project Structure

```
main.wasp                      # Wasp declaration file (THE source of truth)
src/
├── client/                    # React frontend code
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   └── [Feature]Page.tsx
│   ├── components/
│   ├── hooks/
│   ├── App.tsx                # Root component (referenced in main.wasp)
│   └── Main.css
├── server/                    # Node.js backend code
│   ├── actions/               # Write operations
│   │   └── [feature].ts
│   ├── queries/               # Read operations
│   │   └── [feature].ts
│   ├── workers/               # Background jobs
│   ├── webhooks/              # External API handlers
│   └── auth/
│       └── hooks.ts           # Auth lifecycle hooks
├── shared/                    # Code shared between client and server
│   └── types.ts
└── .wasproot                  # Marks project root (never delete)
migrations/                    # Prisma migrations (auto-managed)
```

## Architecture Rules

- **`main.wasp` declares everything.** Routes, pages, queries, mutations, actions, jobs, auth config, and dependencies are all declared in the `.wasp` file. Never configure these in JavaScript/TypeScript. The DSL generates the boilerplate.
- **Queries are read-only, actions are write-only.** Wasp strictly separates reads (`query`) and writes (`action`). Both are declared in `main.wasp` and implemented in `src/server/`. Never mutate data inside a query.
- **Auth is declared, not coded.** Define `auth` in `main.wasp` with the methods you need (email, Google, GitHub). Wasp generates login/signup pages, session handling, and user model. Never implement auth flows manually.
- **Entities are Prisma models.** Define data models in the `entity` block or directly in `schema.prisma`. Wasp wraps Prisma for you. Never use a different ORM or raw SQL.
- **Automatic optimistic updates.** Use `useAction` with `optimisticUpdates` config on the client. Wasp handles cache invalidation when actions complete. Never manually refetch queries after mutations.

## Coding Conventions

- **Wasp DSL syntax matters.** Declarations use specific keywords: `route`, `page`, `query`, `action`, `job`, `entity`. Follow exact syntax from Wasp docs. The DSL is not JavaScript.
- **Server function signatures.** Queries receive `(args, context)`. `context.entities` gives typed Prisma access. `context.user` gives the authenticated user. Always destructure what you need.
- **Client data fetching.** Use `useQuery(getFeature, args)` from `wasp/client/operations`. It returns `{ data, isLoading, error }`. Never use `useEffect` + `fetch`.
- **Referencing entities in operations.** In `main.wasp`, every query/action lists its `entities: [Entity]`. This gives the operation access to those Prisma models via `context.entities.Entity`. Forgetting to list an entity causes a runtime error.
- **Dependency management.** Add npm dependencies in `main.wasp` under `dependencies`, not in `package.json` (Wasp manages its own `package.json`). Never edit the generated `package.json` directly.

## Library Preferences

- **Auth:** Wasp built-in auth (email/password, OAuth). Never add Passport.js or NextAuth.
- **Email:** Wasp built-in email sending with [SendGrid/Mailgun/SMTP] configured in `.wasp`.
- **Background jobs:** Wasp `job` declaration with `pg-boss` executor. Never use Bull or external job queues.
- **Styling:** [Tailwind CSS] configured via Wasp's Tailwind integration. Add in `main.wasp` as a dependency.
- **API clients:** For external APIs, implement in server actions. Never call external APIs directly from client code.

## File Naming

- Wasp config: `main.wasp` (single file, project root)
- Pages: `src/client/pages/[Feature]Page.tsx`
- Queries: `src/server/queries/[feature].ts`
- Actions: `src/server/actions/[feature].ts`
- Shared types: `src/shared/types.ts`
- Jobs: `src/server/workers/[jobName].ts`

## NEVER DO THIS

1. **Never create Express routes manually.** Wasp generates the Express server. Define `api` declarations in `main.wasp` for custom endpoints. Hand-written Express routes won't be included in the build.
2. **Never edit generated code in `.wasp/out/`.** This directory is regenerated on every `wasp start`. All changes are lost. Customize behavior through Wasp's extension points in `src/`.
3. **Never add packages to `package.json` directly.** Use the `dependencies` field in `main.wasp`. Wasp generates its own `package.json` and your manual additions will be overwritten.
4. **Never import from `wasp/` paths that don't exist.** Wasp provides specific import paths (`wasp/client/operations`, `wasp/server`, `wasp/auth`). Guessing import paths produces confusing build errors. Always check the Wasp docs.
5. **Never skip listing entities in operation declarations.** If a query uses `context.entities.Task`, the `main.wasp` declaration must include `entities: [Task]`. Missing entity declarations cause runtime `undefined` errors with no helpful message.
6. **Never use `fetch` or `axios` in client code for app data.** All data flows through Wasp operations. Client `fetch` calls bypass auth context, CSRF protection, and cache invalidation.
7. **Never define routes in React code.** All routes are declared in `main.wasp` and mapped to page components. React Router is managed internally by Wasp.

## Testing

- **Server operation tests:** Import query/action functions directly. Mock `context` with `{ entities: { Model: prismaMock }, user: mockUser }`. Test business logic without HTTP.
- **Component tests:** Use `@testing-library/react`. Mock Wasp operations with `vi.mock('wasp/client/operations')`. Provide deterministic data for `useQuery` mocks.
- **E2E tests:** Use [Playwright/Cypress]. Run `wasp start` in test mode with a seeded database. Test full user flows including auth.
- Run tests: `wasp test` for the integrated test runner, or `npx vitest` for custom setups.

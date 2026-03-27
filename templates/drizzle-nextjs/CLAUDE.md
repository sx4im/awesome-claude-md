# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Next.js 15 with App Router and React Server Components
- Drizzle ORM with PostgreSQL (postgres.js driver)
- TypeScript 5.x in strict mode
- Tailwind CSS 4 for styling
- Zod for validation (shared between client and server)
- NextAuth.js v5 (Auth.js) for authentication
- Server Actions for mutations, Route Handlers for webhooks only

## Project Structure

```
src/
  app/
    (auth)/
      login/page.tsx
      register/page.tsx
    (dashboard)/
      dashboard/page.tsx
      settings/page.tsx
    api/
      webhooks/stripe/route.ts
    layout.tsx
    page.tsx
  components/
    ui/
      button.tsx
      input.tsx
    forms/
      user-form.tsx
  server/
    db/
      index.ts
      schema.ts
      relations.ts
    actions/
      user.actions.ts
    queries/
      user.queries.ts
  lib/
    auth.ts
    validators/
      user.validators.ts
    utils.ts
drizzle/
  migrations/
drizzle.config.ts
next.config.ts
```

## Architecture Rules

- Server Components are the default; add "use client" only when hooks or browser APIs are needed
- All database queries live in server/queries/ and are called from Server Components directly
- All mutations use Server Actions defined in server/actions/ with "use server" directive
- Drizzle schema is the single source of truth; Zod validators derive from it via drizzle-zod
- Route Handlers (route.ts) used only for webhooks and external API integrations
- Never import server-only code (db, actions) from client components

## Coding Conventions

- Define Drizzle relations in a separate relations.ts file, not inline with schema
- Server Actions must validate input with Zod, return { success, data?, error? } objects
- Prefer Drizzle's relational query API (db.query.*) over manual joins for reads
- Use SQL builder (eq, and, or, sql) for complex WHERE clauses
- Colocate loading states: page.tsx + loading.tsx + error.tsx in same directory

## Library Preferences

- ORM: Drizzle exclusively — never use Prisma, Knex, or raw pg
- Validation: Zod + drizzle-zod for schema-derived validators
- Styling: Tailwind CSS with clsx and tailwind-merge via a cn() utility
- UI components: shadcn/ui (copy-pasted, not installed as dependency)
- Forms: React Hook Form with @hookform/resolvers/zod
- Auth: NextAuth.js v5 with Drizzle adapter
- Date handling: date-fns, never moment.js or dayjs

## File Naming

- Components: kebab-case files, PascalCase exports (user-form.tsx exports UserForm)
- Server actions: kebab-case with .actions.ts suffix
- Queries: kebab-case with .queries.ts suffix
- Pages follow Next.js conventions: page.tsx, layout.tsx, loading.tsx, error.tsx

## NEVER DO THIS

1. Never use getServerSideProps or getStaticProps — this project uses App Router only
2. Never import from server/db or server/actions in a "use client" component
3. Never use Drizzle's db.execute() for queries that the query builder can express
4. Never create API routes (route.ts) for data fetching that Server Components can handle
5. Never use useEffect for data fetching — fetch in Server Components or use Server Actions
6. Never define Drizzle schema and relations in the same file — keep them separated

## Testing

- Use Vitest for unit tests and Playwright for end-to-end tests
- Test Server Actions by importing and calling them directly with mocked auth context
- Test Drizzle queries against a test database using drizzle-kit push
- Use testing-library/react for component tests with server component mocking
- Seed test data using Drizzle insert operations in test setup
- Run unit tests: npx vitest run
- Run e2e tests: npx playwright test

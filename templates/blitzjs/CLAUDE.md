# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- BlitzJS 2+ (full-stack React framework built on Next.js)
- TypeScript (strict mode)
- Prisma ORM + [PostgreSQL/SQLite]
- Blitz RPC (zero-API layer, server functions called directly from client)
- Blitz Auth (built-in session management)
- Vitest + @testing-library/react

## Project Structure

```
src/
├── app/                       # Next.js App Router pages
│   ├── layout.tsx
│   ├── page.tsx
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   └── [FEATURE]/
│       ├── page.tsx
│       └── [id]/page.tsx
├── [FEATURE]/
│   ├── mutations/             # Server mutations (create, update, delete)
│   │   ├── create[Feature].ts
│   │   └── update[Feature].ts
│   ├── queries/               # Server queries (get, list)
│   │   ├── get[Feature].ts
│   │   └── get[Features].ts
│   └── schemas.ts             # Zod schemas for validation
├── users/
│   ├── hooks/                 # Feature-specific React hooks
│   │   └── useCurrentUser.ts
│   └── queries/
│       └── getCurrentUser.ts
├── lib/
│   ├── db.ts                  # Prisma client
│   └── blitz-server.ts        # Server plugin setup
├── blitz-client.ts            # Client plugin setup
└── blitz-auth-config.ts       # Auth configuration
db/
├── schema.prisma
├── migrations/
└── seeds.ts
```

## Architecture Rules

- **RPC, not REST.** Blitz uses server functions invoked directly from client code via `invoke()` or `useQuery`/`useMutation`. Never create API route handlers for CRUD operations. The RPC layer handles serialization and transport.
- **Queries and mutations are separate files.** Each query or mutation is a single exported function in its own file. Never combine multiple operations in one file. This enables automatic code splitting.
- **Zod schemas validate all inputs.** Every mutation and query that accepts input MUST parse through a Zod schema. Define schemas in a shared `schemas.ts` per feature. Never trust client input without validation.
- **Auth context is passed automatically.** The `ctx` parameter in queries/mutations contains the session. Use `ctx.session.$authorize()` for auth checks. Never pass user IDs from the client when you can read them from `ctx.session.userId`.
- **Prisma is the only data access layer.** All database operations go through Prisma in query/mutation files. Never use raw SQL or alternative ORMs alongside Prisma.

## Coding Conventions

- **Naming:** Queries use `get[Thing]` or `get[Things]` (e.g., `getProject.ts`, `getProjects.ts`). Mutations use `create[Thing]`, `update[Thing]`, `delete[Thing]`.
- **Resolver pattern:** Every query/mutation exports a default async function that receives `(input, ctx)`. Parse `input` with Zod first, then perform the operation.
- **Use `resolver.pipe` for composition.** Chain `resolver.zod`, `resolver.authorize`, and the resolver function. This standardizes validation and auth across all resolvers.
- **Paginated queries return `{ items, nextPage, hasMore }`.** Use Blitz's `paginate` helper with Prisma's `skip`/`take`. Never return unbounded lists.
- **Collocate by feature, not by type.** Keep queries, mutations, schemas, and hooks for a feature together in one directory. Never create top-level `queries/` and `mutations/` folders.

## Library Preferences

- **Validation:** Zod (first-class Blitz integration). Never use Yup or Joi.
- **Auth:** Blitz Auth plugin with session strategy. Never implement custom JWT/cookie handling.
- **Forms:** React Hook Form + Zod resolver, or Blitz's `<Form>` with `useMutation`.
- **Styling:** [Tailwind CSS/CSS Modules].
- **State management:** React Query (built into Blitz via `useQuery`/`useMutation`). No need for Redux/Zustand for server state.
- **Email:** [Resend/Nodemailer] integrated as a Blitz plugin.

## File Naming

- Queries: `src/[feature]/queries/get[Feature].ts`
- Mutations: `src/[feature]/mutations/create[Feature].ts`
- Schemas: `src/[feature]/schemas.ts`
- Pages: `src/app/[feature]/page.tsx`
- Hooks: `src/[feature]/hooks/use[Hook].ts`

## NEVER DO THIS

1. **Never create `pages/api/` REST endpoints for data fetching.** Use Blitz RPC queries and mutations. API routes are for webhooks and third-party integrations only.
2. **Never use `useEffect` + `fetch` for data loading.** Use `useQuery(getFeature, { id })`. It handles caching, deduplication, suspense, and error boundaries automatically.
3. **Never skip `ctx.session.$authorize()` in mutations.** Every mutation that modifies data needs explicit authorization. Public mutations must still call `$authorize()` with no roles if that is intentional.
4. **Never import server-side code in client components without Blitz RPC.** Direct imports of Prisma or Node APIs in client code will crash the build. All server code must go through the RPC layer.
5. **Never store derived server state in `useState`.** Data from `useQuery` is already reactive. Copying it into local state causes stale data bugs. Use `useMutation` + `invalidateQuery` to update.
6. **Never put business logic in page components.** Pages call queries/mutations and render. Domain rules and authorization belong in the resolver functions.
7. **Never manually serialize dates or BigInts.** Blitz's RPC serializer handles `Date`, `undefined`, `Map`, `Set`, and other types that `JSON.stringify` drops. Trust the superjson layer.

## Testing

- **Query/mutation tests:** Call resolver functions directly with mock `ctx`. Seed test data with Prisma in `beforeEach` and clean up with `prisma.$transaction` rollback or database truncation.
- **Component tests:** Use `@testing-library/react`. Wrap components in Blitz test providers using `withBlitz`. Mock RPC calls with `vi.mock` on the query/mutation module.
- **Integration tests:** Use `blitz console` to interactively test queries. For automated integration, boot a test server and invoke RPC endpoints via HTTP.
- Run tests: `npx vitest` (unit/component) or `npx vitest --run` for CI.

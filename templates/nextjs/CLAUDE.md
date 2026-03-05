# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- Next.js 14+ (App Router only — no pages/ directory)
- TypeScript 5.x (strict mode enabled)
- Tailwind CSS 3.x
- Prisma ORM + PostgreSQL
- Deployed on Vercel

## Project Structure

```
src/
├── app/                  # App Router pages and layouts
│   ├── (auth)/           # Route group for authenticated pages
│   ├── (marketing)/      # Route group for public pages
│   ├── api/              # Route handlers only — no business logic here
│   └── layout.tsx        # Root layout
├── components/
│   ├── ui/               # Reusable primitives (Button, Input, Modal)
│   └── features/         # Feature-specific components (UserCard, InvoiceTable)
├── lib/                  # Shared utilities, db client, auth helpers
├── actions/              # Server actions, grouped by domain
└── types/                # Shared TypeScript types and Zod schemas
```

## Architecture Rules

- Every page in `app/` is a **server component by default**. Only add `"use client"` when you need interactivity (onClick, useState, useEffect). If a component only renders data, it stays as a server component.
- Never put business logic in `page.tsx` files. Pages are for layout composition only — they import components and pass data down.
- Use server actions in `actions/` for mutations. Each file groups actions by domain: `actions/users.ts`, `actions/invoices.ts`.
- Use route handlers (`app/api/`) only for webhooks and third-party integrations. For internal data mutations, prefer server actions.
- Data fetching happens in server components using direct Prisma calls or helper functions from `lib/`. Use TanStack Query only for client-side polling or optimistic updates.

## Coding Conventions

- Use **named exports** for all components: `export function UserCard()` — never `export default`.
- Name components in PascalCase: `UserProfile.tsx`, `InvoiceTable.tsx`.
- Name utilities and hooks in camelCase: `formatCurrency.ts`, `useDebounce.ts`.
- Prefix all custom hooks with `use`: `useAuth`, `useInvoices`, `useMediaQuery`.
- Sort imports in this order: React/Next → external packages → `@/lib` → `@/components` → relative imports → types.
- Use the `@/` path alias for all imports from `src/`. Never use relative paths that go up more than one level (`../../`).
- All environment variables used client-side **must** start with `NEXT_PUBLIC_`. Server-only secrets (database URLs, API keys) must never have this prefix.

## Library Preferences

- **Date handling:** `date-fns` — not `moment` (deprecated, not tree-shakeable) and not `dayjs` (smaller API surface causes workarounds).
- **Validation:** `zod` for both runtime validation and TypeScript type inference. Not `yup` — zod's `.infer<>` pattern eliminates type duplication.
- **Forms:** `react-hook-form` + `@hookform/resolvers/zod`. Not Formik — it re-renders the entire form on every keystroke.
- **Data fetching (client):** TanStack Query for any client-side data. Not SWR — TanStack has better devtools, mutation support, and query invalidation patterns.
- **Icons:** `lucide-react` — consistent stroke width, tree-shakeable, actively maintained.

## Image and Metadata Rules

- Always use `next/image` for images. Never use raw `<img>` tags — you lose lazy loading, automatic WebP, and responsive sizing.
- Define metadata using the `metadata` export or `generateMetadata` function in `page.tsx` or `layout.tsx`. Never use `<Head>` from `next/head` — that's Pages Router.
- Put OG images in `app/opengraph-image.tsx` using the ImageResponse API.

## File Naming

- Components: `PascalCase.tsx` → `UserCard.tsx`, `InvoiceRow.tsx`
- Hooks: `useCamelCase.ts` → `useAuth.ts`, `useDebounce.ts`
- Utilities: `camelCase.ts` → `formatCurrency.ts`, `parseDate.ts`
- Server actions: `camelCase.ts` → `users.ts`, `invoices.ts`
- Types: `camelCase.ts` → `user.ts`, `invoice.ts`
- Route handlers: `route.ts` (Next.js convention — never rename)

## NEVER DO THIS

1. **Never use `getServerSideProps`, `getStaticProps`, or `getInitialProps`.** These are Pages Router APIs. In App Router, use server components for data fetching and `generateStaticParams` for static generation.
2. **Never mix `app/` and `pages/` directories.** Pick one router. This project uses App Router exclusively.
3. **Never use `useEffect` for data fetching when a server component would work.** If the data doesn't depend on client-side state, fetch it on the server. It's faster, has no loading spinner, and doesn't expose API endpoints.
4. **Never put business logic in `page.tsx`.** Pages compose components and pass data. Extract logic into `lib/`, `actions/`, or feature components.
5. **Never use `export default` for components.** Named exports make auto-imports reliable and refactoring safe. The only exception is `page.tsx`, `layout.tsx`, and `loading.tsx` — Next.js requires default exports for those.
6. **Never hardcode environment variables.** Always use `process.env.VARIABLE_NAME` and define them in `.env.local` (gitignored). Validate required env vars at startup using `zod`.
7. **Never use `any` type.** Use `unknown` and narrow with type guards, or define proper types. If you're reaching for `any`, the type system is telling you the abstraction is wrong.

## Testing

- Use Vitest for unit and integration tests. Put tests next to the file they test: `UserCard.test.tsx` alongside `UserCard.tsx`.
- Use Playwright for E2E tests in a top-level `e2e/` directory.
- Test server actions by calling them directly — they're just async functions.
- Mock Prisma in tests using `vitest-mock-extended`. Never hit a real database in unit tests.

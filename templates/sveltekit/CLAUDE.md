# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- SvelteKit 2.x with Svelte 5 (runes mode)
- TypeScript (strict mode)
- Tailwind CSS 3.x
- Drizzle ORM or Prisma + PostgreSQL
- Deployed on Vercel, Cloudflare Pages, or Node adapter

## Project Structure

```
src/
├── routes/
│   ├── (app)/               # Authenticated route group
│   │   ├── dashboard/
│   │   │   └── +page.svelte
│   │   └── +layout.server.ts  # Auth check for all (app) routes
│   ├── (marketing)/         # Public pages
│   │   ├── +page.svelte     # Landing page
│   │   └── pricing/
│   ├── api/                 # API routes (+server.ts files)
│   │   └── webhooks/
│   └── +layout.svelte       # Root layout
├── lib/
│   ├── components/          # Reusable UI components
│   │   ├── ui/              # Primitives (Button, Input, Modal)
│   │   └── features/        # Domain (UserCard, PricingTier)
│   ├── server/              # Server-only code (db, auth, email)
│   │   ├── db.ts            # Database client
│   │   └── auth.ts          # Session helpers
│   └── utils/               # Shared utilities
├── hooks.server.ts          # Global server hooks (auth, logging)
└── app.d.ts                 # Type augmentations (Locals, PageData)
```

## Architecture Rules

- **Server-first data loading.** Use `+page.server.ts` and `+layout.server.ts` for loading data. The `load` function runs on the server, has access to the database, and sends typed data to the page. Client-side fetching is the exception, not the default.
- **Form actions for mutations.** Use SvelteKit form actions in `+page.server.ts` — not API routes — for form submissions. Actions handle progressive enhancement: forms work without JavaScript enabled.
- **`$lib/server/` is your security boundary.** Anything in `$lib/server/` is never shipped to the client. Database connections, API secrets, and auth logic must live here. SvelteKit enforces this — importing from `$lib/server/` in client code is a build error.
- **Hooks handle cross-cutting concerns.** Authentication checks, request logging, and CSRF protection go in `hooks.server.ts`. Don't duplicate auth checks in every `load` function — do it once in the hook or in a shared layout's server load.
- **Runes for all reactive state.** Use `$state()`, `$derived()`, and `$effect()`. Never use the legacy `$:` reactive syntax or Svelte stores (`writable`, `readable`) in new code.

## Coding Conventions

- Components use PascalCase: `Button.svelte`, `UserCard.svelte`. One component per file.
- Props use the `$props()` rune: `let { name, onClick } = $props<{ name: string; onClick: () => void }>()`.
- Derived values use `$derived()`: `let fullName = $derived(\`${firstName} ${lastName}\`)`. Never use `$effect()` to set derived state — that's what `$derived` is for.
- Side effects use `$effect()` sparingly. If you're doing data fetching in an effect, you should probably use a `load` function instead.
- Import aliasing: `$lib/` maps to `src/lib/`. Use it for all library imports. Never use `../../../lib/` chains.

## Library Preferences

- **ORM:** Drizzle ORM for new projects (type-safe, SQL-like API, no codegen). Prisma if you prefer schema-first with generated client. Not TypeORM — not idiomatic in the Svelte ecosystem.
- **Styling:** Tailwind CSS — Svelte handles scoped styles well, but Tailwind is faster to iterate with.
- **Auth:** Lucia (self-hosted sessions) or Auth.js adapter for SvelteKit. Not rolling your own JWT auth — session-based auth is simpler and safer for web apps.
- **Validation:** Zod + `superforms` — SvelteKit Superforms gives you progressive enhancement, client-side validation, and server validation in one API. Not handling form validation manually.
- **Email:** Resend or Postmark — not Nodemailer directly (Resend/Postmark handle deliverability).

## File Naming

- Routes: `+page.svelte`, `+page.server.ts`, `+layout.svelte` (SvelteKit convention, never rename)
- Components: `PascalCase.svelte` → `Button.svelte`, `UserCard.svelte`
- Server modules: `camelCase.ts` in `$lib/server/` → `db.ts`, `auth.ts`, `email.ts`
- Utilities: `camelCase.ts` → `formatDate.ts`, `cn.ts`
- Types: defined in `app.d.ts` for global augmentations, co-located otherwise

## NEVER DO THIS

1. **Never fetch data in `onMount` when `load` functions exist.** `load` runs on the server, avoids waterfalls, and sends data with the initial HTML. `onMount` fetching causes layout shift and loading spinners.
2. **Never import from `$lib/server/` in client-side code.** SvelteKit will throw a build error, but don't try to work around it. Server secrets belong on the server.
3. **Never use `$effect()` to synchronize state.** If value B depends on value A, use `$derived()`. Effects are for side effects (DOM manipulation, analytics, logging) — not for state derivation.
4. **Never use Svelte stores (`writable`, `readable`) in new code.** Use runes: `$state()`, `$derived()`, `$effect()`. Stores are legacy Svelte 4 API.
5. **Never use API routes for form submissions that SvelteKit form actions can handle.** Form actions give you progressive enhancement for free. API routes require JavaScript and manual `fetch` calls.
6. **Never return sensitive data from `load` functions.** Everything a `load` function returns is serialized and sent to the client. Database IDs, internal flags, and user secrets must be filtered out before returning.
7. **Never skip type augmentation in `app.d.ts`.** Define `App.Locals` for request-scoped data (user session), `App.PageData` for page data shapes. Without this, TypeScript can't help you.

## Testing

- Use Vitest for unit tests. Test utilities, helpers, and isolated logic.
- Use Playwright for E2E tests — SvelteKit has first-class Playwright integration out of the box.
- Test `load` functions by calling them directly with mock `event` objects.
- Test form actions by posting form data to the action endpoint in Playwright.

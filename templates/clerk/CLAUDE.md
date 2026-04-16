# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Clerk (complete user management)
- Next.js 14+ / React 18+
- TypeScript 5.x
- Pre-built UI components
- JWT templates

## Project Structure
```
src/
├── app/
│   ├── layout.tsx              # ClerkProvider wrapper
│   ├── page.tsx
│   └── (dashboard)/
│       └── layout.tsx          # Protected routes
├── components/
│   └── auth/
│       └── user-profile.tsx
├── middleware.ts               # authMiddleware
└── lib/
    └── clerk.ts                # Server helpers
```

## Architecture Rules

- **Complete auth solution.** User management, sessions, orgs included.
- **Pre-built components.** `<SignIn />`, `<UserButton />`, `<OrganizationSwitcher />`.
- **Server and client SDKs.** Different imports for server vs client usage.
- **JWT templates.** Custom claims for external services.

## Coding Conventions

- Provider: `<ClerkProvider>{children}</ClerkProvider>` in root layout.
- Middleware: `export default authMiddleware({ publicRoutes: ['/', '/api/webhook'] })`.
- Sign in: `<SignIn />` component or `redirectToSignIn()`.
- Get user (server): `import { auth } from '@clerk/nextjs/server'; const { userId } = auth()`.
- Get user (client): `import { useUser } from '@clerk/nextjs'; const { user } = useUser()`.
- Protect API: `if (!userId) return new Response('Unauthorized', { status: 401 })`.

## NEVER DO THIS

1. **Never expose Clerk secret keys client-side.** Only use `NEXT_PUBLIC` keys for public config.
2. **Never ignore the middleware matcher.** Protect routes appropriately—don't over or under protect.
3. **Never use client hooks in server components.** `useUser` is client-only; use `auth()` on server.
4. **Never forget to configure JWT templates.** Needed for external API authentication.
5. **Never skip webhook handling.** Handle user.created, user.updated for your database sync.
6. **Never test in production.** Use Clerk's development instance for testing.
7. **Never ignore rate limits.** Clerk has API rate limits—cache where possible.

## Testing

- Test with Clerk's testing tokens for E2E tests.
- Test webhook handlers with Clerk's webhook testing.
- Test JWT templates with jwt.io.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Better Auth (framework-agnostic auth library)
- TypeScript 5.x
- Database adapters (Prisma, Drizzle, Kysely)
- Framework adapters (Next.js, Nuxt, SvelteKit, etc.)
- Plugins for OAuth, passwordless, etc.

## Project Structure
```
src/
├── lib/
│   └── auth.ts                 # Auth configuration
├── server/
│   └── auth.ts                 # Server-side auth setup
├── app/
│   └── api/
│       └── auth/
│           └── [...all]/
│               └── route.ts    # Next.js API handler
└── components/
    └── auth/
        └── sign-in.tsx
```

## Architecture Rules

- **Framework-agnostic core.** Better Auth works with any framework via adapters.
- **Database-first approach.** User data in your database, not external service.
- **Plugin architecture.** Extend with OAuth, passwordless, organization plugins.
- **Type-safe sessions.** Session data typed from configuration.

## Coding Conventions

- Initialize: `export const auth = betterAuth({ database: prismaAdapter(prisma), plugins: [googleOAuth()] })`.
- API route (Next.js): `import { auth } from '@/lib/auth'; export const { GET, POST } = auth.handler`.
- Client: `import { createAuthClient } from 'better-auth/client'; const client = createAuthClient({ baseURL: 'http://localhost:3000' })`.
- Sign in: `const result = await client.signIn.email({ email, password })`.
- Get session: `const session = await client.getSession()`.
- Server session: `await auth.api.getSession({ headers: request.headers })`.

## NEVER DO THIS

1. **Never skip the database adapter.** Better Auth requires database integration.
2. **Never expose secret keys client-side.** Only public config in client initialization.
3. **Never forget to configure cookie options.** Domain, secure, sameSite for production.
4. **Never ignore the session expiration.** Configure appropriate session lifetimes.
5. **Never use without rate limiting.** Implement rate limiting on auth endpoints.
6. **Never forget CSRF protection.** Enabled by default, don't disable without reason.
7. **Never ignore the trustHost option.** Configure for serverless/edge environments.

## Testing

- Test sign up flow with test database.
- Test session management (creation, validation, expiration).
- Test OAuth flows with mock providers.


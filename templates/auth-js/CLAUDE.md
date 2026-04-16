# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Auth.js v5 (NextAuth.js successor)
- Next.js 14+ App Router
- TypeScript 5.x
- OAuth providers (GitHub, Google, etc.)
- Credentials provider for password auth

## Project Structure
```
src/
├── auth.ts                     # Auth configuration
├── middleware.ts               # Auth middleware
├── app/
│   ├── api/
│   │   └── auth/
│   │       └── [...nextauth]/
│   │           └── route.ts    # API route
│   └── (protected)/
│       └── layout.tsx          # Protected layout
├── components/
│   └── auth/
│       └── sign-in-button.tsx
└── lib/
    └── auth-actions.ts         # Server actions
```

## Architecture Rules

- **Edge-compatible.** Auth.js runs on Edge Runtime.
- **Database optional.** Use JWT sessions or database sessions.
- **Multiple providers.** Combine OAuth, email, credentials.
- **Middleware for protection.** Protect routes at the edge.

## Coding Conventions

- Config: `export const { handlers, auth, signIn, signOut } = NextAuth({ providers: [GitHub], adapter: PrismaAdapter(prisma) })`.
- API route: `export const { GET, POST } = handlers`.
- Middleware: `export { auth as middleware } from '@/auth'` with `export const config = { matcher: ['/dashboard/:path*'] }`.
- Server component: `const session = await auth(); if (!session) redirect('/login')`.
- Client sign in: `import { signIn } from 'next-auth/react'; <button onClick={() => signIn('github')}>`.
- Server action: `await signIn('credentials', { redirectTo: '/dashboard' })`.

## NEVER DO THIS

1. **Never expose the secret.** `NEXTAUTH_SECRET` is server-only.
2. **Never use JWT for sensitive data.** Database sessions for sensitive applications.
3. **Never ignore the `trustHost` option.** Required for serverless/edge deployments.
4. **Never forget to configure callbacks.** `session`, `jwt`, `signIn` callbacks control behavior.
5. **Never skip CSRF protection.** Enabled by default, keep it on.
6. **Never use `signIn` without checking result.** Handle errors appropriately.
7. **Never ignore the adapter choice.** Prisma adapter needs specific schema.

## Testing

- Test OAuth flow with test providers.
- Test middleware protection.
- Test session expiration and refresh.


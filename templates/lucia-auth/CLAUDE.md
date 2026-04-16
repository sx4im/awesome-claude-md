# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Lucia v3 (auth library for serverless)
- TypeScript 5.x
- Database adapters (Prisma, Drizzle, Kysely)
- Framework agnostic
- Serverless/edge optimized

## Project Structure
```
src/
├── lib/
│   ├── auth.ts                 # Lucia configuration
│   ├── session.ts              # Session helpers
│   └── password.ts             # Password hashing
├── db/
│   └── schema.ts               # User/session schema
└── app/
    └── (auth)/
        ├── login/
        │   └── page.tsx
        └── signup/
            └── page.tsx
```

## Architecture Rules

- **Bring your own database.** Lucia provides the auth layer, you manage data.
- **Serverless native.** Designed for Edge/Serverless runtimes.
- **Session management core.** Lucia focuses on secure session handling.
- **Type-safe.** Session and user types inferred from config.

## Coding Conventions

- Initialize: `const lucia = new Lucia(adapter, { sessionCookie: { attributes: { secure: process.env.NODE_ENV === 'production' } } })`.
- Database adapter: `const adapter = new PrismaAdapter(prisma.session, prisma.user)`.
- Create session: `const session = await lucia.createSession(userId, {}); const sessionCookie = lucia.createSessionCookie(session.id)`.
- Validate: `const sessionId = cookies().get(lucia.sessionCookieName)?.value ?? null; const { user, session } = await lucia.validateSession(sessionId)`.
- Delete: `await lucia.invalidateSession(sessionId)`.

## NEVER DO THIS

1. **Never use the default session duration blindly.** Configure based on security needs.
2. **Never skip the database setup.** Users and sessions need proper schema.
3. **Never forget to handle session cookie in responses.** `cookies().set(sessionCookie.name, sessionCookie.value, sessionCookie.attributes)`.
4. **Never ignore session rotation.** Lucia rotates sessions automatically—handle it.
5. **Never use without proper CORS configuration.** For cross-domain scenarios.
6. **Never skip password hashing.** Use `argon2`, `bcrypt`, or `scrypt`.
7. **Never expose session tokens in logs or errors.** Keep them confidential.

## Testing

- Test session creation and validation.
- Test session expiration and rotation.
- Test concurrent session handling.


# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Full-Stack)

### Release Discipline
- Maintain contract consistency across UI, API, DB schema, and background jobs.
- Ship schema changes with backward-compatible rollout and rollback notes.
- Guard critical business flows with idempotency and retry safety.

### Merge/Release Gates
- API contract checks, migration checks, and e2e smoke tests pass.
- Auth and billing-critical paths validated explicitly.
- No breaking change without migration path and versioning note.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Next.js 14+ with App Router (not Pages Router)
- TypeScript 5.4+ with strict mode
- Clerk v5 for authentication, session management, and organizations
- Tailwind CSS 3.4 for styling
- Drizzle ORM with PostgreSQL for application data
- Vercel for deployment with Edge Runtime support
- Zod for runtime validation of Clerk webhook payloads

## Project Structure

```
app/
  (auth)/
    sign-in/[[...sign-in]]/page.tsx    # Clerk SignIn component
    sign-up/[[...sign-up]]/page.tsx    # Clerk SignUp component
    layout.tsx                          # Centered auth layout
  (dashboard)/
    layout.tsx                          # Authenticated layout with UserButton
    settings/
      [[...settings]]/page.tsx         # Clerk UserProfile component
    org/
      [[...org]]/page.tsx              # OrganizationProfile component
  api/
    webhooks/
      clerk/route.ts                   # Clerk webhook handler (user.created, org events)
    trpc/[trpc]/route.ts               # tRPC API handler
middleware.ts                           # Clerk authMiddleware at project root
lib/
  clerk/
    server.ts                          # currentUser(), auth() wrappers
    webhooks.ts                        # Webhook event type handlers and Svix verification
    organizations.ts                   # Org membership checks, role utilities
  db/
    schema.ts                          # Drizzle schema with clerkUserId foreign keys
    queries.ts                         # Data access layer, always filtered by userId/orgId
components/
  auth/
    AuthGuard.tsx                      # Client-side auth state wrapper
    RoleGate.tsx                       # Role-based UI rendering (admin, member)
    OrgSwitcher.tsx                    # Organization switcher with CreateOrganization
env.ts                                 # Zod-validated environment variables
```

## Architecture Rules

- Use `auth()` from `@clerk/nextjs/server` in Server Components and Route Handlers; never import Clerk client utilities in server code
- Use `useAuth()`, `useUser()`, `useOrganization()` hooks only in Client Components marked with `"use client"`
- Middleware in `middleware.ts` uses `clerkMiddleware()` with `createRouteMatcher()` for public/protected route definitions
- Every database table that stores user data must have a `clerk_user_id` column; every query must filter by the authenticated user
- Organization-scoped data uses `clerk_org_id`; enforce org context via `auth().orgId` in every org-scoped query
- Clerk webhooks are verified using Svix; extract the `svix-id`, `svix-timestamp`, `svix-signature` headers
- Use Clerk's `metadata` (publicMetadata, privateMetadata, unsafeMetadata) for user-specific feature flags and preferences

## Coding Conventions

- Protect routes in middleware, not in individual page components; pages assume authenticated context
- Use `currentUser()` for displaying user info, `auth()` for lightweight auth checks (userId, orgId, orgRole)
- Organization roles follow Clerk's built-in `org:admin` and `org:member`; define custom permissions in Clerk Dashboard
- Webhook handlers must be idempotent; use `clerk_user_id` as the upsert key for `user.created` and `user.updated`
- Client-side auth loading states use `<SignedIn>`, `<SignedOut>`, `<ClerkLoading>` components, not manual `isLoaded` checks
- Environment variables: `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`, `CLERK_WEBHOOK_SECRET`
- Redirect URLs configured via `NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in` and `NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard`

## Library Preferences

- @clerk/nextjs over next-auth or iron-session for authentication
- Drizzle ORM over Prisma for type-safe database access with better edge compatibility
- Zod for webhook payload validation and environment variable parsing
- svix for webhook signature verification (Clerk uses Svix under the hood)
- @clerk/themes for pre-built dark/light theme customization of Clerk components
- nuqs for URL search params state management in authenticated pages

## File Naming

- Route files: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx` per Next.js conventions
- Clerk catch-all routes: `[[...slug]]/page.tsx` pattern for sign-in, sign-up, user-profile, org-profile
- Components: PascalCase `.tsx` files grouped by feature
- Server utilities: camelCase `.ts` files in `lib/`
- Webhook handlers: `route.ts` in `app/api/webhooks/clerk/`

## NEVER DO THIS

1. Never call `auth()` or `currentUser()` in Client Components; these are server-only functions that will throw at runtime
2. Never store Clerk user data by copying email/name into your database as source of truth; always read from Clerk, store only `clerkUserId` as the foreign key
3. Never skip Svix webhook verification in production; replay attacks and spoofed payloads are real threats
4. Never use `useAuth().getToken()` and pass it manually to API routes; Clerk automatically sends the session cookie
5. Never put sensitive logic behind client-side `<SignedIn>` guards alone; always verify auth server-side in Route Handlers and Server Components
6. Never hardcode organization IDs or role strings; use `auth().orgRole` and Clerk Dashboard permissions

## Testing

- Mock Clerk in tests with `@clerk/testing` package; use `setupClerkTestingToken()` for Playwright/Cypress E2E
- Unit test webhook handlers by constructing Svix-signed payloads with test secrets
- Test middleware route matching with different path patterns in isolation using `createRouteMatcher`
- Verify org-scoped queries return empty results when `orgId` is missing or mismatched
- Test role-based UI rendering by mocking `useOrganization()` with different `membership.role` values
- E2E tests use Clerk test mode users created via Clerk Backend API `clerkClient.users.createUser()`
- Seed test org with known members and roles via `clerkClient.organizations.createOrganization()`

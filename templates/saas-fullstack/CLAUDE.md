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

- Next.js 14+ (App Router)
- TypeScript 5.x (strict mode)
- Prisma ORM + PostgreSQL
- Stripe (payments and subscriptions)
- Clerk or Auth.js for authentication
- Resend for transactional email
- Tailwind CSS 3.x
- Deployed on Vercel

## Project Structure

```
src/
├── app/
│   ├── (app)/              # Authenticated app routes
│   │   ├── dashboard/
│   │   ├── settings/
│   │   └── billing/
│   ├── (marketing)/        # Public pages (landing, pricing, blog)
│   ├── api/
│   │   ├── webhooks/       # Stripe, Clerk, and third-party webhooks
│   │   └── trpc/           # tRPC handler (if used)
│   └── layout.tsx
├── components/
│   ├── ui/                 # Design system primitives
│   └── features/           # Feature components (PricingCard, BillingPortal)
├── lib/
│   ├── db.ts               # Prisma client singleton
│   ├── stripe.ts           # Stripe client + helper functions
│   ├── auth.ts             # Auth helpers (getCurrentUser, requireAuth)
│   ├── email.ts            # Resend client + send helpers
│   └── constants.ts        # Plan limits, feature flags, config objects
├── actions/                # Server actions by domain
├── emails/                 # React Email templates
└── types/
```

## Architecture Rules

- **Multi-tenant by default.** Every database table that stores user data includes a `userId` or `organizationId` column. Every query filters by the authenticated user's tenant. No exceptions.
- **Auth middleware protects all `(app)/` routes.** Use Clerk's middleware or Auth.js session checks. Public routes live under `(marketing)/`. Never rely on client-side checks alone.
- **Billing logic is isolated.** All Stripe-related code lives in `lib/stripe.ts` and `actions/billing.ts`. Feature code never calls Stripe directly. it calls billing service functions that abstract the plan check.
- **Plan limits live in a config object.** Never hardcode `if (plan === 'pro' && items < 100)`. Define plan limits in `lib/constants.ts` as a typed object and reference it everywhere.
- **Email templates are React components.** Use React Email (`@react-email/components`) in the `emails/` directory. Each template is a named export with typed props.

## Database Conventions

- All tables include: `id` (cuid2), `createdAt` (DateTime), `updatedAt` (DateTime), and `deletedAt` (DateTime, nullable) for soft deletes.
- Use cuid2 for all IDs. not UUID (harder to debug), not auto-increment (exposes count). Generate with `@default(cuid())` in Prisma schema.
- Foreign keys use the pattern `{entity}Id`: `userId`, `organizationId`, `subscriptionId`.
- Indexes on every foreign key column used in `WHERE` clauses. Prisma doesn't add these automatically.
- Soft delete by default. Set `deletedAt` timestamp instead of deleting rows. All queries must filter `WHERE deletedAt IS NULL`. create a Prisma middleware or extension to enforce this.

## Coding Conventions

- **Named exports everywhere.** `export function PricingCard()`. never `export default`. Exception: Next.js page/layout files.
- **Server components by default.** Only add `"use client"` when the component needs interactivity.
- **Environment variables:** Stripe keys, database URLs, and auth secrets never start with `NEXT_PUBLIC_`. Only marketing-safe values get the prefix.
- Always use `getCurrentUser()` from `lib/auth.ts` to get the authenticated user in server components and actions. Never trust a `userId` sent from the client.

## Library Preferences

- **Auth:** Clerk for fastest setup with organizations and SSO. Auth.js if you need database-backed sessions.
- **Payments:** Stripe only. Use the `stripe` npm package, not raw `fetch` to Stripe APIs.
- **Email:** Resend + React Email. not SendGrid (Resend has a better developer API) and not Nodemailer (Resend handles deliverability).
- **Validation:** Zod for all input validation. forms, server actions, webhook payloads.
- **IDs:** `@paralleldrive/cuid2`. not `uuid` (cuid2 is shorter, sortable, and collision-resistant).

## Stripe Webhook Handling

- Webhook handler lives at `app/api/webhooks/stripe/route.ts`.
- Always verify the webhook signature using `stripe.webhooks.constructEvent()`. Never skip verification, even in development.
- Handle these events at minimum: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`.
- Webhook handlers update the database. they call service functions, not Prisma directly.
- Return `200` immediately after processing. Stripe retries on non-2xx responses.

## NEVER DO THIS

1. **Never expose the Stripe secret key to the client.** `STRIPE_SECRET_KEY` must never start with `NEXT_PUBLIC_`. Use `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` for client-side Stripe.js.
2. **Never trust a client-sent `userId`.** Always derive the user from the server session. A request body with `{ userId: "..." }` is an attack vector.
3. **Never put billing logic in API routes.** Billing checks, plan upgrades, and invoice logic go in `lib/stripe.ts` and `actions/billing.ts`. Route handlers are glue code only.
4. **Never hardcode plan limits.** Define them in `lib/constants.ts` as a `PLAN_LIMITS` object keyed by plan ID. Feature code reads from this object, never inlines magic numbers.
5. **Never skip webhook signature verification.** Even in dev, always pass the webhook secret. Without it, anyone can fake a Stripe event and give themselves a paid plan.
6. **Never store card details in your database.** Stripe handles PCI compliance. You store `stripeCustomerId` and `stripeSubscriptionId`. nothing else.
7. **Never send emails without a template.** All emails use React Email components from `emails/`. No inline HTML strings, no string concatenation.

## Testing

- Use Vitest for unit tests. Mock Stripe calls using `vi.mock('./lib/stripe')`.
- Use Stripe CLI for local webhook testing: `stripe listen --forward-to localhost:3000/api/webhooks/stripe`.
- Test auth flows with Clerk's test mode or Auth.js test helpers.
- E2E billing flows use Stripe test cards: `4242 4242 4242 4242` for success, `4000 0000 0000 0002` for decline.

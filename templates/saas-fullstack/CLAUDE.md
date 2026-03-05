# [PROJECT NAME] — [ONE LINE DESCRIPTION]

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
- **Billing logic is isolated.** All Stripe-related code lives in `lib/stripe.ts` and `actions/billing.ts`. Feature code never calls Stripe directly — it calls billing service functions that abstract the plan check.
- **Plan limits live in a config object.** Never hardcode `if (plan === 'pro' && items < 100)`. Define plan limits in `lib/constants.ts` as a typed object and reference it everywhere.
- **Email templates are React components.** Use React Email (`@react-email/components`) in the `emails/` directory. Each template is a named export with typed props.

## Database Conventions

- All tables include: `id` (cuid2), `createdAt` (DateTime), `updatedAt` (DateTime), and `deletedAt` (DateTime, nullable) for soft deletes.
- Use cuid2 for all IDs — not UUID (harder to debug), not auto-increment (exposes count). Generate with `@default(cuid())` in Prisma schema.
- Foreign keys use the pattern `{entity}Id`: `userId`, `organizationId`, `subscriptionId`.
- Indexes on every foreign key column used in `WHERE` clauses. Prisma doesn't add these automatically.
- Soft delete by default. Set `deletedAt` timestamp instead of deleting rows. All queries must filter `WHERE deletedAt IS NULL` — create a Prisma middleware or extension to enforce this.

## Coding Conventions

- **Named exports everywhere.** `export function PricingCard()` — never `export default`. Exception: Next.js page/layout files.
- **Server components by default.** Only add `"use client"` when the component needs interactivity.
- **Environment variables:** Stripe keys, database URLs, and auth secrets never start with `NEXT_PUBLIC_`. Only marketing-safe values get the prefix.
- Always use `getCurrentUser()` from `lib/auth.ts` to get the authenticated user in server components and actions. Never trust a `userId` sent from the client.

## Library Preferences

- **Auth:** Clerk for fastest setup with organizations and SSO. Auth.js if you need database-backed sessions.
- **Payments:** Stripe only. Use the `stripe` npm package, not raw `fetch` to Stripe APIs.
- **Email:** Resend + React Email — not SendGrid (Resend has a better developer API) and not Nodemailer (Resend handles deliverability).
- **Validation:** Zod for all input validation — forms, server actions, webhook payloads.
- **IDs:** `@paralleldrive/cuid2` — not `uuid` (cuid2 is shorter, sortable, and collision-resistant).

## Stripe Webhook Handling

- Webhook handler lives at `app/api/webhooks/stripe/route.ts`.
- Always verify the webhook signature using `stripe.webhooks.constructEvent()`. Never skip verification, even in development.
- Handle these events at minimum: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`.
- Webhook handlers update the database — they call service functions, not Prisma directly.
- Return `200` immediately after processing. Stripe retries on non-2xx responses.

## NEVER DO THIS

1. **Never expose the Stripe secret key to the client.** `STRIPE_SECRET_KEY` must never start with `NEXT_PUBLIC_`. Use `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` for client-side Stripe.js.
2. **Never trust a client-sent `userId`.** Always derive the user from the server session. A request body with `{ userId: "..." }` is an attack vector.
3. **Never put billing logic in API routes.** Billing checks, plan upgrades, and invoice logic go in `lib/stripe.ts` and `actions/billing.ts`. Route handlers are glue code only.
4. **Never hardcode plan limits.** Define them in `lib/constants.ts` as a `PLAN_LIMITS` object keyed by plan ID. Feature code reads from this object—never inlines magic numbers.
5. **Never skip webhook signature verification.** Even in dev, always pass the webhook secret. Without it, anyone can fake a Stripe event and give themselves a paid plan.
6. **Never store card details in your database.** Stripe handles PCI compliance. You store `stripeCustomerId` and `stripeSubscriptionId` — nothing else.
7. **Never send emails without a template.** All emails use React Email components from `emails/`. No inline HTML strings, no string concatenation.

## Testing

- Use Vitest for unit tests. Mock Stripe calls using `vi.mock('./lib/stripe')`.
- Use Stripe CLI for local webhook testing: `stripe listen --forward-to localhost:3000/api/webhooks/stripe`.
- Test auth flows with Clerk's test mode or Auth.js test helpers.
- E2E billing flows use Stripe test cards: `4242 4242 4242 4242` for success, `4000 0000 0000 0002` for decline.

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

## Production Delivery Playbook (Category: Payments & Billing)

### Release Discipline
- Treat payment flows as high-risk: idempotency, reconciliation, and fraud controls first.
- Never trust client-side payment state without server verification.
- Preserve auditability for charge/refund/subscription transitions.

### Merge/Release Gates
- Webhook signature validation and replay protection verified.
- Successful and failed payment lifecycle paths tested.
- Financial side effects are idempotent and recoverable.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- [NODE/PYTHON/GO] backend with TypeScript
- Stripe SDK (`stripe` npm package) pinned to a specific API version
- Stripe Webhooks with signature verification
- Stripe Checkout Sessions for payment flows
- Stripe Billing for subscriptions (if applicable)
- {database} for syncing Stripe state locally
- {framework} for HTTP endpoints

## Project Structure

```
src/
├── stripe/
│   ├── client.ts              # Stripe SDK initialization (singleton)
│   ├── checkout.ts            # Create checkout sessions, build line items
│   ├── subscriptions.ts       # Subscription CRUD, plan changes, cancellation
│   ├── webhooks.ts            # Webhook endpoint + event routing
│   ├── handlers/              # One handler per webhook event type
│   │   ├── checkout-completed.ts
│   │   ├── invoice-paid.ts
│   │   ├── invoice-failed.ts
│   │   ├── subscription-updated.ts
│   │   └── subscription-deleted.ts
│   ├── sync.ts                # Reconcile Stripe state with local DB
│   └── types.ts               # Stripe-related type extensions
├── models/
│   ├── user.ts                # User model with stripeCustomerId field
│   └── subscription.ts        # Local subscription mirror table
└── config/
    └── stripe.config.ts       # API keys, webhook secrets, price IDs
```

## Architecture Rules

- **Stripe is the source of truth for payment state.** Your database stores a mirror for fast reads, but Stripe's records are canonical. When in doubt, fetch from Stripe API. The local mirror is updated exclusively via webhooks, not by optimistically writing after API calls.
- **Webhook-driven state updates.** After calling `stripe.checkout.sessions.create()`, do NOT update the user's subscription status. Wait for the `checkout.session.completed` webhook. The checkout might fail, the user might close the tab, or the payment might require 3D Secure. Only the webhook confirms success.
- **One handler per event type.** `handlers/checkout-completed.ts` exports a single function that processes `checkout.session.completed`. The webhook endpoint in `webhooks.ts` routes events to the correct handler via a switch/map. Never put all event logic in one giant function.
- **Idempotent webhook handlers.** Stripe retries failed webhooks. Every handler must check if the event has already been processed (by storing `event.id` or checking resulting state). Processing the same event twice must produce the same outcome.
- **Customer-centric design.** Create a Stripe Customer when a user signs up (or on first purchase). Store `stripeCustomerId` on the user record. All subsequent Stripe calls use this customer ID. Never create anonymous checkout sessions for registered users.

## Coding Conventions

- Pin the Stripe API version in the SDK initialization: `new Stripe(key, { apiVersion: '2024-06-20' })`. Never use the dashboard default -- it changes and breaks your integration silently.
- Price IDs and product IDs are config values, not hardcoded strings. Store them in `stripe.config.ts` or environment variables: `STRIPE_PRICE_PRO_MONTHLY=price_xxxxx`.
- All Stripe API calls go through the `stripe/` directory. No other part of the codebase imports `stripe` directly. Controllers call service functions like `createCheckoutSession(userId, priceId)`.
- Amounts are in cents (or smallest currency unit). Never pass dollar amounts to Stripe. Always convert: `amount: Math.round(dollars * 100)`. Display conversion happens in the frontend only.
- Use Stripe's `metadata` field to attach your internal IDs: `metadata: { userId, planId }`. This links Stripe objects back to your domain without extra lookups.

## Library Preferences

- **SDK:** Official `stripe` npm package. Not raw HTTP calls to the Stripe API -- the SDK handles pagination, retries, idempotency keys, and type safety.
- **Webhook verification:** `stripe.webhooks.constructEvent(body, sig, secret)`. Not manual HMAC calculation. The SDK method handles timestamp tolerance.
- **Checkout flow:** Stripe Checkout (hosted page). Not Stripe Elements (embedded form) unless you need full UI control. Checkout handles SCA, localization, and tax automatically.
- **Subscription management:** Stripe Customer Portal for self-service plan changes. Not a custom UI that calls the Subscriptions API directly -- the Portal handles proration, cancellation, and payment method updates.
- **Testing:** Stripe CLI (`stripe listen --forward-to`) for local webhook testing. Not ngrok -- the Stripe CLI provides event triggering and log tailing.

## File Naming

- Handlers: `kebab-case.ts` -> `checkout-completed.ts`, `invoice-paid.ts`
- Services: `kebab-case.ts` -> `checkout.ts`, `subscriptions.ts`
- Config: `kebab-case.config.ts` -> `stripe.config.ts`
- Types: `kebab-case.ts` -> `types.ts`
- Models: `kebab-case.ts` -> `subscription.ts`, `user.ts`

## NEVER DO THIS

1. **Never trust client-side price data.** The checkout session must build line items from server-side price IDs. If the client sends `{ price: 9.99 }`, a user can change it to `0.01`. Always use `price: 'price_xxx'` from your config.
2. **Never skip webhook signature verification.** Without `stripe.webhooks.constructEvent()`, anyone can POST fake events to your webhook endpoint. This is a payment bypass vulnerability.
3. **Never parse the webhook body as JSON before verification.** Signature verification requires the raw request body (Buffer/string). If your framework parses JSON automatically (Express with `express.json()`), exclude the webhook route or use `express.raw({ type: 'application/json' })`.
4. **Never update subscription status from the API response.** `stripe.subscriptions.update()` returns the updated subscription, but your local DB should only change when the webhook arrives. The API response is for logging, not for state transitions.
5. **Never store full card numbers or sensitive payment data.** Use Stripe's tokenization. Your server never sees card details. If you're receiving raw card numbers, your integration is wrong and you're in PCI scope.
6. **Never retry failed payments manually.** Stripe has Smart Retries for invoices. Configure dunning in the Stripe Dashboard. Custom retry logic creates duplicate charges.
7. **Never hardcode Stripe keys in source.** Use environment variables: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`. The publishable key can be in frontend config but the secret key must never appear in client bundles or version control.

## Testing

- Use Stripe's test mode keys (`sk_test_*`) in development. Never use live keys locally.
- Trigger webhook events locally: `stripe listen --forward-to localhost:3000/api/webhooks/stripe` then `stripe trigger checkout.session.completed`.
- Write integration tests that create real test-mode Stripe objects (customers, sessions, subscriptions) and verify your handlers process the resulting webhooks correctly. Clean up with `stripe.customers.del()` in teardown.
- Test idempotency: send the same webhook event twice and verify the handler produces the same result without duplicate database records or side effects.
- Test failure paths: declined cards (`tok_chargeDeclined`), incomplete 3DS (`tok_threeDSecure2Required`), and expired sessions. Your UI and backend must handle each gracefully.

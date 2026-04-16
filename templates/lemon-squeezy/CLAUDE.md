# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Lemon Squeezy (merchant of record for SaaS)
- Next.js/React/Any framework
- TypeScript 5.x
- Webhooks for events
- Subscription management

## Project Structure
```
src/
├── lib/
│   ├── lemon-squeezy.ts        # API client setup
│   └── webhooks.ts             # Webhook handlers
├── app/
│   └── api/
│       └── webhooks/
│           └── lemon/
│               └── route.ts    # Webhook endpoint
├── components/
│   └── billing/
│       └── pricing.tsx
└── lib/
    └── subscriptions.ts        # Subscription logic
```

## Architecture Rules

- **Merchant of record.** Lemon Squeezy handles taxes, compliance.
- **Webhooks for state sync.** Listen to subscription events.
- **Checkout links.** Redirect to Lemon Squeezy checkout.
- **Customer portal.** Users manage subscriptions via hosted pages.

## Coding Conventions

- API key: `const lemonSqueezy = new LemonSqueezyClient(LEMON_SQUEEZY_API_KEY)`.
- Create checkout: `await lemonSqueezy.checkout.create({ product_options: { name, description }, checkout_options: { embed: false } })`.
- Webhook handling: Verify signature with `webhookSecret`.
- Signature: `import { createHmac } from 'crypto'; const signature = createHmac('sha256', secret).update(payload).digest('hex')`.
- Events: Handle `subscription_created`, `subscription_updated`, `subscription_cancelled`.
- Update user: Sync subscription status to your database on webhook events.

## NEVER DO THIS

1. **Never trust webhook without signature verification.** Verify `X-Signature` header.
2. **Never expose API keys client-side.** Only use in server-side code.
3. **Never forget to handle webhook retries.** Return 200 only after successful processing.
4. **Never skip idempotency for webhooks.** Same event may be sent multiple times.
5. **Never use test mode in production.** Separate test and live API keys.
6. **Never ignore tax implications.** Lemon Squeezy handles it, but understand your obligations.
7. **Never forget to handle checkout errors.** Users may cancel or encounter payment issues.

## Testing

- Test webhooks with Lemon Squeezy's test events.
- Test subscription lifecycle (create, update, cancel).
- Test signature verification with known payloads.


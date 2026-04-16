# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Paddle (payments infrastructure)
- Next.js/React/Any framework
- TypeScript 5.x
- Paddle.js for checkout
- Webhooks for events

## Project Structure
```
src/
├── lib/
│   ├── paddle.ts               # Paddle client setup
│   └── webhooks.ts             # Webhook handling
├── app/
│   ├── api/
│   │   └── webhooks/
│   │       └── paddle/
│   │           └── route.ts    # Webhook endpoint
│   └── checkout/
│       └── page.tsx            # Checkout page
└── components/
    └── pricing/
        └── pricing-table.tsx
```

## Architecture Rules

- **Paddle.js for frontend.** Checkout overlay or inline checkout.
- **Price entities define billing.** Products, prices, subscriptions.
- **Webhooks for backend sync.** Listen for subscription lifecycle events.
- **Customer portal hosted.** Users manage subscriptions via Paddle.

## Coding Conventions

- Initialize: `Paddle.Setup({ vendor: 123456, environment: 'sandbox' })`.
- Checkout: `Paddle.Checkout.open({ product: 123, email: 'user@example.com' })`.
- Webhook verification: `const signature = headers['paddle-signature']; verify with public key`.
- API (server): `fetch('https://sandbox-api.paddle.com/prices', { headers: { Authorization: `Bearer ${apiKey}` } })`.
- Subscription status: Update user record on `subscription.activated`, `subscription.updated`, etc.

## NEVER DO THIS

1. **Never use production vendor ID in development.** Use sandbox.
2. **Never skip webhook signature verification.** Essential for security.
3. **Never ignore idempotency keys for API calls.** Prevent duplicate operations.
4. **Never forget to handle subscription past_due.** Graceful handling of failed payments.
5. **Never expose API keys in frontend.** Use Paddle.js, not raw API calls.
6. **Never ignore proration settings.** Understand how upgrades/downgrades bill.
7. **Never skip testing with Paddle's webhooks simulator.** Test all event types.

## Testing

- Test checkout flow with sandbox.
- Test webhook handling with test events.
- Test subscription lifecycle transitions.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Razorpay (payments for India)
- Next.js/React/Any framework
- Node.js SDK
- Webhooks for events
- Razorpay Checkout.js

## Project Structure
```
src/
├── lib/
│   ├── razorpay.ts             # SDK setup
│   └── webhooks.ts             # Webhook handlers
├── app/
│   ├── api/
│   │   ├── payment/
│   │   │   └── route.ts        # Create order
│   │   └── webhooks/
│   │       └── razorpay/
│   │           └── route.ts    # Webhook handler
│   └── payment/
│       └── page.tsx            # Payment page
└── components/
    └── payment/
        └── razorpay-button.tsx
```

## Architecture Rules

- **Orders first, then payment.** Create Razorpay order on server, complete on client.
- **Checkout.js for frontend.** Razorpay's checkout handles payment UI.
- **Webhooks for confirmation.** Verify payment status via webhooks, not just callback.
- **Signature verification essential.** Verify payment signatures to prevent tampering.

## Coding Conventions

- Initialize: `const razorpay = new Razorpay({ key_id: RAZORPAY_KEY_ID, key_secret: RAZORPAY_KEY_SECRET })`.
- Create order: `const order = await razorpay.orders.create({ amount: 50000, currency: 'INR', receipt: 'order_receipt' })`.
- Checkout options: `{ key: RAZORPAY_KEY_ID, amount: order.amount, order_id: order.id, handler: function(response) { /* verify */ } }`.
- Verify signature: `crypto.createHmac('sha256', secret).update(orderId + '|' + paymentId).digest('hex') === signature`.
- Webhook: Verify `X-Razorpay-Signature` header with webhook secret.

## NEVER DO THIS

1. **Never create order amount on client.** Always server-side to prevent tampering.
2. **Never trust client-side payment success alone.** Always verify via webhooks.
3. **Never skip signature verification.** Prevents payment fraud.
4. **Never use test mode keys in production.** Separate environments strictly.
5. **Never ignore webhook retries.** Handle idempotently—may receive same event multiple times.
6. **Never forget to handle payment failures.** Not all payments succeed.
7. **Never skip 3D Secure handling.** Razorpay handles it, but understand the flow.

## Testing

- Test with Razorpay test cards.
- Test webhook handling with test payloads.
- Test signature verification with known data.


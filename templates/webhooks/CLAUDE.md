# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Webhooks (event delivery mechanism)
- TypeScript/Python/Go
- HMAC signature verification
- Idempotency handling
- Retry with backoff

## Project Structure
```
src/
├── webhooks/
│   ├── handlers/
│   │   ├── stripe.ts
│   │   └── github.ts
│   ├── middleware/
│   │   └── verify-signature.ts
│   └── lib/
│       ├── idempotency.ts
│       └── retries.ts
└── routes/
    └── webhooks.ts             // Webhook endpoints
```

## Architecture Rules

- **Signature verification mandatory.** Verify HMAC to ensure authenticity.
- **Idempotency for safety.** Same event delivered twice shouldn't duplicate work.
- **Ack quickly, process async.** Return 2xx immediately, queue for processing.
- **Retry with exponential backoff.** When calling outbound webhooks.

## Coding Conventions

- Verify: `const signature = req.headers['x-signature']; const expected = hmac(payload, secret); if (!timingSafeEqual(signature, expected)) throw 401`.
- Idempotency: `const exists = await db.webhookEvents.findUnique(eventId); if (exists) return 200`.
- Queue: `await queue.add('process-webhook', { payload })`; return 202.
- Retry: `fetchWithRetry(url, { retries: 3, backoff: 'exponential' })`.

## NEVER DO THIS

1. **Never trust webhook without signature.** Always verify HMAC or JWT.
2. **Never process synchronously.** Timeout risk—acknowledge and queue.
3. **Never skip idempotency handling.** Networks retry—expect duplicates.
4. **Never expose webhook secrets in logs.** Log event ID, not payload with secrets.
5. **Never use predictable webhook IDs.** Include timestamp, random component.
6. **Never forget to handle old events.** Ignore events older than threshold.
7. **Never use HTTP for webhooks in production.** HTTPS only.

## Testing

- Test signature verification with valid/invalid signatures.
- Test idempotency with duplicate event IDs.
- Test retry behavior with failing endpoints.


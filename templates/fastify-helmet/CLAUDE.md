# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fastify security middleware
- @fastify/helmet
- @fastify/cors
- @fastify/rate-limit
- Security headers

## Project Structure
```
src/
├── plugins/
│   ├── security.ts             // Security plugin registration
│   └── cors.ts
├── routes/
└── app.ts                      // Fastify instance
```

## Architecture Rules

- **Helmet for headers.** `contentSecurityPolicy`, `hsts`, etc.
- **CORS configuration.** Origin validation, credentials.
- **Rate limiting.** Prevent brute force.
- **Register early.** Security plugins first.

## Coding Conventions

- Helmet: `app.register(helmet, { contentSecurityPolicy: { directives: { defaultSrc: ["'self'"], styleSrc: ["'self'", "'unsafe-inline'"] } } })`.
- CORS: `app.register(cors, { origin: ['https://example.com'], credentials: true })`.
- Rate limit: `app.register(rateLimit, { max: 100, timeWindow: '1 minute' })`.
- JWT: `app.register(jwt, { secret: process.env.JWT_SECRET })`.

## NEVER DO THIS

1. **Never use `unsafe-inline` without need.** Weakens CSP.
2. **Never allow all origins in production.** `origin: true` is dangerous.
3. **Never skip rate limiting on auth endpoints.** Protect against brute force.
4. **Never expose version info.** Disable `x-powered-by`.
5. **Never use weak JWT secrets.** Minimum 256-bit entropy.
6. **Never ignore security plugin order.** Register before routes.
7. **Never skip HTTPS in production.** HSTS, secure cookies require HTTPS.

## Testing

- Test security headers with `curl -I`.
- Test CORS preflight requests.
- Test rate limit enforcement.


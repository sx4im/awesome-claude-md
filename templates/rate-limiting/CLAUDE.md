# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Rate Limiting (Redis-based)
- TypeScript/Python/Go
- Token bucket or sliding window
- Middleware implementation
- Distributed rate limiting

## Project Structure
```
src/
├── middleware/
│   └── rate-limit.ts           // Rate limiting middleware
├── lib/
│   ├── stores/
│   │   └── redis.ts            // Redis client
│   └── algorithms/
│       ├── token-bucket.ts
│       └── sliding-window.ts
└── config/
    └── rate-limits.ts          // Limit configurations
```

## Architecture Rules

- **Client identification.** By IP, user ID, or API key.
- **Redis for distribution.** Shared state across multiple servers.
- **Headers for transparency.** Return `X-RateLimit-Limit`, `X-RateLimit-Remaining`.
- **429 status when exceeded.** Too Many Requests response.

## Coding Conventions

- Middleware: `app.use('/api/', rateLimit({ windowMs: 60000, max: 100, store: redisStore }))`.
- Key generation: `key: (req) => req.ip` or `key: (req) => req.user.id`.
- Handler: `(req, res, next) => { if (await limiter.check(req)) next(); else res.status(429).send() }`.
- Algorithm: Token bucket for burst allowance, sliding window for strict limits.

## NEVER DO THIS

1. **Never rate limit without identification.** Every request needs a key to limit by.
2. **Never use in-memory stores in production.** Single-server only—use Redis.
3. **Never forget to handle Redis failures.** Fail open (allow) or closed (deny) explicitly.
4. **Never apply blanket limits.** Different endpoints need different limits.
5. **Never ignore client feedback.** Always send rate limit headers.
6. **Never block legitimate users.** Implement whitelisting for trusted sources.
7. **Never skip burst handling.** Allow short bursts for better UX.

## Testing

- Test limit enforcement at boundary.
- Test Redis failure scenarios.
- Test distributed rate limiting across instances.


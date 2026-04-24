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

## Production Delivery Playbook (Category: Architecture & Domain Patterns)

### Release Discipline
- Preserve domain invariants and explicit command/query/event boundaries.
- Maintain idempotency and ordering guarantees in event-driven paths.
- Avoid coupling domain rules to transport/framework details.

### Merge/Release Gates
- Critical business invariants tested across happy and failure paths.
- Replay/rebuild behavior validated where events are source of truth.
- Backward compatibility verified for contracts and event schemas.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

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

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

## Production Delivery Playbook (Category: Backend)

### Release Discipline
- Fail closed on authz/authn checks and input validation.
- Use explicit timeouts/retries/circuit-breaking for external dependencies.
- Preserve API compatibility unless breaking change is approved and documented.

### Merge/Release Gates
- Unit + integration tests and contract tests pass.
- Static checks pass and critical endpoint latency regressions reviewed.
- Structured error handling verified for all modified endpoints.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Firebase Cloud Functions (2nd gen, Node.js 20)
- TypeScript (strict mode)
- Firestore as primary database
- Firebase Auth for authentication
- Firebase Storage for files
- Firebase Emulator Suite for local development

## Project Structure

```
functions/
├── src/
│   ├── index.ts             # Function exports (single entry point)
│   ├── http/                # HTTP-triggered functions (Express or directly)
│   │   ├── api.ts           # Express app for REST endpoints
│   │   └── webhooks.ts      # Webhook handlers
│   ├── triggers/            # Firestore/Auth/Storage triggers
│   │   ├── onUserCreate.ts  # auth.user().onCreate
│   │   ├── onOrderWrite.ts  # firestore.document().onWrite
│   │   └── onFileUpload.ts  # storage.object().onFinalize
│   ├── scheduled/           # Cron-triggered functions
│   │   └── dailyCleanup.ts  # Scheduled cleanup tasks
│   ├── services/            # Business logic (called by triggers and HTTP)
│   │   ├── user.service.ts
│   │   └── notification.service.ts
│   ├── lib/
│   │   ├── firestore.ts     # Firestore client, typed collection helpers
│   │   ├── auth.ts          # Auth verification middleware
│   │   └── config.ts        # Environment config
│   └── types/               # Shared TypeScript types
├── .env                     # Local emulator config
└── package.json
```

## Architecture Rules

- **One function per file, all exported from `index.ts`.** Each function file exports a single Cloud Function. `index.ts` re-exports them all: `export { onUserCreate } from './triggers/onUserCreate'`. Firebase deploys functions based on these exports.
- **Functions are thin.** A trigger function extracts the event data, calls a service function, and handles errors. Business logic lives in `services/`. Never put Firestore queries or complex logic in trigger handlers.
- **Typed Firestore collections.** Create typed helper functions: `const usersCollection = () => db.collection('users') as CollectionReference<User>`. Never use untyped `db.collection('users').doc(id).get()`. the `data()` return type is `DocumentData` (useless).
- **Idempotent triggers.** Firestore `onWrite` and `onChange` triggers can fire multiple times. Every trigger must be idempotent. running it twice with the same data produces the same result. Use document fields to track processed state.
- **2nd gen functions for everything new.** Use `onRequest`, `onDocumentCreated`, `onCall` from `firebase-functions/v2`. 1st gen functions are legacy. 2nd gen gives you concurrency control, higher memory, and min instances.

## Coding Conventions

- **Function naming:** descriptive verb + noun: `onUserCreate`, `onOrderStatusChange`, `sendDailyReport`. Functions are named exports matching the file name.
- **Firestore document paths:** `users/{userId}`, `users/{userId}/orders/{orderId}`. Always reference paths as template strings. Never hardcode collection names in service code. define them as constants.
- **Transaction for multi-document writes.** If you update user balance AND create a transaction record, use `runTransaction()`. Never do sequential writes that could leave data inconsistent if one fails.
- **Error handling:** Cloud Functions that handle HTTP requests must always return a response. Trigger functions must catch errors. an unhandled exception causes the function to retry indefinitely.
- **Environment config:** use `defineSecret()` and `defineString()` from Functions v2 config. Not `functions.config()` (legacy). Not hardcoded values.

## Library Preferences

- **HTTP framework:** Express inside `onRequest` for REST APIs with multiple routes. Not Hono or Fastify (Express has the best Firebase Functions integration).
- **Validation:** Zod. validate request bodies and Firestore document shapes. Not Joi.
- **Email:** Firebase Extensions (Trigger Email) for simple cases. Resend or SendGrid for custom templates.
- **Scheduling:** `onSchedule` from Functions v2 with cron syntax. Not external cron services.
- **Local dev:** Firebase Emulator Suite. non-negotiable. Never test against production Firestore during development.

## NEVER DO THIS

1. **Never test against production Firebase.** Use the Firebase Emulator Suite for all local development. Create, read, update, delete operations against production during development will corrupt real user data.
2. **Never write non-idempotent triggers.** Triggers can execute multiple times for the same event. If `onUserCreate` sends a welcome email, check a `welcomeEmailSent` field before sending. Never assume a trigger runs exactly once.
3. **Never return without a response in HTTP functions.** An HTTP function that doesn't call `res.send()` or `res.json()` will timeout after 60 seconds, wasting resources and leaving the client hanging.
4. **Never use `any` for Firestore document data.** Type your collections with `CollectionReference<T>`. Without typing, every `.data()` call returns `DocumentData` and you lose all type safety.
5. **Never deploy all functions when only one changed.** Use `firebase deploy --only functions:functionName`. Deploying all functions is slow and risks deploying untested changes.
6. **Never store secrets in code or `.env` files committed to git.** Use `defineSecret()` for API keys and credentials. They're stored in Secret Manager and injected at runtime.
7. **Never create Firestore indexes manually.** Generate them from failing queries (Firebase logs the index creation URL) or define them in `firestore.indexes.json`. Manual console indexes aren't version-controlled.

## Testing

- Use the Firebase Emulator Suite for integration tests. Start emulators, seed data, trigger functions, assert results.
- Unit test services by mocking Firestore with `firebase-admin/testing` or plain mocks.
- Test HTTP functions with `supertest` against the Express app directly (no emulator needed for unit tests).
- Test trigger idempotency: fire the same event twice and assert the side effect only happens once.

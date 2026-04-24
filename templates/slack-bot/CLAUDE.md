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

## Production Delivery Playbook (Category: Bots & Plugins)

### Release Discipline
- Constrain event handlers to explicit allowlists and permission scopes.
- Validate all external payloads and signatures where supported.
- Prevent runaway automation loops and duplicate side effects.

### Merge/Release Gates
- Webhook/event contract tests pass.
- Rate-limit and retry behavior validated.
- Security-sensitive commands reviewed for abuse paths.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Slack Bolt.js 3.x (TypeScript)
- Node.js 20+ with TypeScript 5.x (strict mode)
- Block Kit for all message rendering
- Slack Events API + Socket Mode for development
- [DATABASE: PostgreSQL/Redis/DynamoDB] for persistence

## Project Structure

```
src/
├── app.ts                    # Bolt app initialization, middleware registration
├── listeners/
│   ├── actions/              # Block Kit interactive handlers (button clicks, menus)
│   ├── commands/             # Slash command handlers (/{command-name})
│   ├── events/               # Event handlers (message, app_mention, member_joined)
│   ├── shortcuts/            # Global and message shortcuts
│   └── views/                # Modal submission and view_closed handlers
├── blocks/
│   ├── home-tab.ts           # App Home tab Block Kit layout
│   ├── modals/               # Modal view definitions (Block Kit JSON builders)
│   └── messages/             # Message attachment and Block Kit builders
├── services/
│   ├── slack.ts              # Slack Web API wrapper (chat.postMessage, users.info)
│   └── {domain}.ts           # Business logic, separated from Slack plumbing
├── middleware/
│   ├── auth.ts               # Custom middleware (team validation, feature flags)
│   └── logging.ts            # Request logging middleware
├── types/
│   └── slack.ts              # Extended Slack types, action payloads, view state
└── utils/
    ├── blocks.ts             # Block Kit builder helpers
    └── parse.ts              # Slash command argument parsing
```

## Architecture Rules

- **Listeners are thin.** Every handler in `listeners/` extracts data from the Slack payload, calls a service, and responds. Business logic never lives in a listener. Listeners are the controller layer.
- **Block Kit is built in `blocks/`, never inline.** Never construct Block Kit JSON inside a listener. Create builder functions that accept data and return block arrays. This makes blocks testable and reusable.
- **Always `ack()` within 3 seconds.** Slack requires acknowledgment within 3 seconds for all interactions. For slow operations, `ack()` immediately, then use `respond()` or `client.chat.postMessage()` to send results asynchronously.
- **Socket Mode for development, HTTP for production.** Socket Mode requires no public URL and simplifies local dev. Production deployments use HTTP mode behind a load balancer with the `/slack/events` endpoint.
- **All user-facing text goes through Block Kit.** Never send plain text messages with `chat.postMessage({ text })` alone. Always include `blocks` for rich formatting. The `text` field is the fallback for notifications only.

## Coding Conventions

- **Typed action IDs.** Every `action_id` and `block_id` is a string constant defined in a central `constants.ts`. Never use inline string literals like `action_id: 'approve_btn'` in both the block builder and the listener. Mismatched strings are silent failures.
- **Listener registration is declarative.** Register listeners in `app.ts` by importing from `listeners/` index files. Each listener file exports a function that takes `(app: App)` and registers itself. Never nest registrations inside callbacks.
- **Modal state is parsed with a helper.** Slack modal view state is deeply nested (`view.state.values[block_id][action_id].value`). Write a typed `parseViewState(view)` utility. Never traverse the raw state object inline in handlers.
- **Use `respond()` for ephemeral replies to commands.** For slash commands and actions, `respond()` uses the `response_url`. Use `client.chat.postMessage()` only when you need to post to a different channel or as a visible message.

## Library Preferences

- **Framework:** `@slack/bolt` (not raw `@slack/web-api` with express). Bolt handles verification, routing, and middleware.
- **Block Kit:** Hand-written builder functions returning typed block arrays. Not `slack-block-builder` (adds indirection, falls behind API updates).
- **Database:** [PREFERENCE: Prisma for SQL / ioredis for Redis]. Not raw `pg` (Prisma handles migrations and type safety).
- **Scheduling:** `node-cron` for recurring tasks. Not `setTimeout` loops. For distributed jobs, use a proper queue like BullMQ.

## File Naming

- Listeners: `kebab-case.ts` matching the Slack event or action → `app-mention.ts`, `approve-request.ts`
- Block builders: `kebab-case.ts` describing the view → `home-tab.ts`, `approval-modal.ts`
- Services: `kebab-case.ts` → `user-service.ts`, `notification-service.ts`
- Types: `kebab-case.ts` → `slack-types.ts`, `domain-types.ts`

## NEVER DO THIS

1. **Never forget to `ack()`.** Every action, command, shortcut, and view submission must call `ack()` or Slack shows an error to the user. Even if your handler throws, `ack()` must happen first. Put it on the first line.
2. **Never use `app.message()` with a broad regex.** A pattern like `/hello/` fires on every message containing "hello" in every channel the bot is in. Be specific: match exact commands or use mentions.
3. **Never store tokens in code.** `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET` come from environment variables. Never commit the `xoxb-` token. Use `.env` for local dev.
4. **Never build modals by mutating a shared object.** Block Kit JSON objects are plain objects. If you reuse a reference, pushing to `blocks` in one modal mutates the shared array. Always return fresh arrays from builder functions.
5. **Never ignore `app_uninstalled` events.** When a workspace uninstalls your app, clean up stored tokens and data. Continuing to call APIs with revoked tokens causes errors and violates Slack policy.
6. **Never send a wall of text in a single message.** Break long content into Block Kit sections with dividers. Slack truncates messages over 3000 characters. Use `chat.postMessage` with file uploads for large content.
7. **Never assume `user.id` is unique across workspaces.** In multi-workspace bots, always key data by `(team_id, user_id)`.

## Testing

- Use Vitest for unit testing services and block builders independently from Slack.
- Mock `client`, `ack`, `respond`, and `say` as jest functions. Pass them to listener handlers directly.
- Test Block Kit output by snapshotting the JSON structure. Catches accidental layout changes.
- Integration test slash commands by posting to `/slack/events` with signed test payloads using `@slack/bolt`'s test helpers.
- Test modal flows end-to-end: trigger → `ack({ response_action: 'update' })` → `view_submission` handler → final message.

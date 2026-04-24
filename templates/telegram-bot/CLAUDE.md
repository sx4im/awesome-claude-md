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

- Python 3.11+
- python-telegram-bot v20+ (async, native `asyncio`)
- PostgreSQL + SQLAlchemy 2.0 (or SQLite for simple bots)
- Redis for caching and rate limiting (optional)
- Docker for deployment

## Project Structure

```
src/
├── bot.py                   # Application entry point (build app, register handlers)
├── handlers/
│   ├── start.py             # /start, /help command handlers
│   ├── menu.py              # Inline keyboard and callback handlers
│   ├── conversation.py      # Multi-step conversation handlers
│   └── errors.py            # Global error handler
├── services/
│   ├── user.py              # User account logic (create, update, check subscription)
│   └── content.py           # Content generation, API calls, data processing
├── keyboards/
│   ├── inline.py            # InlineKeyboardMarkup builders
│   └── reply.py             # ReplyKeyboardMarkup builders
├── db/
│   ├── models.py            # SQLAlchemy models (User, Subscription, etc.)
│   ├── session.py           # Database session factory
│   └── crud.py              # Database operations
├── middleware/
│   ├── auth.py              # Check user permissions/subscription
│   └── rate_limit.py        # Rate limiting per user
├── utils/
│   ├── formatting.py        # Message formatting (HTML/Markdown)
│   └── constants.py         # Bot messages, error strings, config
└── config.py                # Environment variable loading
```

## Architecture Rules

- **Handlers are thin.** They parse the update, call a service function, and send a response. Business logic lives in `services/`. Never do database queries or API calls directly in handlers.
- **`ConversationHandler` for multi-step flows.** Sign-up, onboarding, and form submission use `ConversationHandler` with explicit state constants. Never manage conversation state with global variables.
- **Keyboards are built in `keyboards/`.** Every inline keyboard and reply keyboard is a function in `keyboards/inline.py` or `keyboards/reply.py`. Never construct `InlineKeyboardMarkup` inline in handlers. it clutters the code.
- **All bot messages are constants.** Define every user-facing string in `utils/constants.py`. Never hardcode messages in handlers. This makes the bot translatable and message changes don't require handler edits.
- **Error handler catches everything.** Register a global error handler that logs the error with context (user ID, update type, traceback) and sends a user-friendly apology message. Unhandled errors should never crash the bot.

## Coding Conventions

- **Async everything.** `python-telegram-bot` v20+ is fully async. All handlers are `async def`. All database and API calls use `await`. Never use synchronous blocking calls inside handlers.
- **Callback data is structured.** Use a prefix pattern: `callback_data="menu:main"`, `callback_data="order:confirm:123"`. Parse by splitting on `:`. Never use unstructured strings or UUIDs as callback data.
- **One handler per command.** `/start` → `handlers/start.py`. `/settings` → `handlers/settings.py`. Don't put multiple unrelated commands in one file.
- **Group related callback queries.** All callback queries from a menu's inline keyboards are handled in the same file as the menu handler. `handlers/menu.py` handles both the `/menu` command and all `menu:*` callbacks.
- **Type hints everywhere.** `async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None`. Never use untyped handlers.

## Library Preferences

- **Bot framework:** `python-telegram-bot` v20+. not `aiogram` (smaller English community), not `telethon` (more for userbot/scraping). PTB has the best documentation and async support.
- **Database:** SQLAlchemy 2.0 async with `asyncpg` for PostgreSQL. SQLite with `aiosqlite` for simple bots. Not raw SQL queries.
- **HTTP client:** `httpx` (async). for external API calls. Not `requests` (synchronous, will block the event loop).
- **Scheduling:** `APScheduler` (comes with PTB's `JobQueue`). for scheduled messages, reminders, and periodic tasks.
- **Config:** `pydantic-settings` for typed environment variable loading with validation.

## NEVER DO THIS

1. **Never use synchronous libraries in async handlers.** `requests.get()` blocks the entire event loop. all users wait while one request completes. Use `httpx.AsyncClient()` or `aiohttp`.
2. **Never store bot tokens in code.** Load from environment variables via `config.py`. Never commit tokens. a leaked bot token gives full control of the bot.
3. **Never hardcode chat/user IDs.** Admin IDs, group IDs, and channel IDs come from config. Hardcoded IDs break when moving between test and production bots.
4. **Never handle errors silently.** If a handler fails, the user should get a meaningful response ("Something went wrong, please try again"). Silent failures make users think the bot is broken.
5. **Never use `time.sleep()`.** It blocks the async loop. Use `await asyncio.sleep()`. `time.sleep(5)` in a handler freezes the entire bot for 5 seconds.
6. **Never send unbounded messages.** Telegram has rate limits (30 messages/second to different chats, 1 message/second to same chat). Batch broadcasts and add delays. Hitting rate limits gets the bot temporarily banned.
7. **Never skip input sanitization.** User messages can contain anything. HTML injection, extremely long strings, special characters. Sanitize before storing or displaying. Use Telegram's HTML parse mode with proper escaping.

## Testing

- Test handlers by creating mock `Update` and `Context` objects. Verify the handler calls the right service functions with the right arguments.
- Test services independently with mocked database sessions.
- Test conversation flows by simulating the full state machine: entry → step 1 → step 2 → completion.
- Use a test bot token and a private test group for integration testing. Never test on production.

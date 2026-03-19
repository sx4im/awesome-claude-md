# [PROJECT NAME] — [ONE LINE DESCRIPTION]

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
- **Keyboards are built in `keyboards/`.** Every inline keyboard and reply keyboard is a function in `keyboards/inline.py` or `keyboards/reply.py`. Never construct `InlineKeyboardMarkup` inline in handlers — it clutters the code.
- **All bot messages are constants.** Define every user-facing string in `utils/constants.py`. Never hardcode messages in handlers. This makes the bot translatable and message changes don't require handler edits.
- **Error handler catches everything.** Register a global error handler that logs the error with context (user ID, update type, traceback) and sends a user-friendly apology message. Unhandled errors should never crash the bot.

## Coding Conventions

- **Async everything.** `python-telegram-bot` v20+ is fully async. All handlers are `async def`. All database and API calls use `await`. Never use synchronous blocking calls inside handlers.
- **Callback data is structured.** Use a prefix pattern: `callback_data="menu:main"`, `callback_data="order:confirm:123"`. Parse by splitting on `:`. Never use unstructured strings or UUIDs as callback data.
- **One handler per command.** `/start` → `handlers/start.py`. `/settings` → `handlers/settings.py`. Don't put multiple unrelated commands in one file.
- **Group related callback queries.** All callback queries from a menu's inline keyboards are handled in the same file as the menu handler. `handlers/menu.py` handles both the `/menu` command and all `menu:*` callbacks.
- **Type hints everywhere.** `async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None`. Never use untyped handlers.

## Library Preferences

- **Bot framework:** `python-telegram-bot` v20+ — not `aiogram` (smaller English community), not `telethon` (more for userbot/scraping). PTB has the best documentation and async support.
- **Database:** SQLAlchemy 2.0 async with `asyncpg` for PostgreSQL. SQLite with `aiosqlite` for simple bots. Not raw SQL queries.
- **HTTP client:** `httpx` (async) — for external API calls. Not `requests` (synchronous, will block the event loop).
- **Scheduling:** `APScheduler` (comes with PTB's `JobQueue`) — for scheduled messages, reminders, and periodic tasks.
- **Config:** `pydantic-settings` for typed environment variable loading with validation.

## NEVER DO THIS

1. **Never use synchronous libraries in async handlers.** `requests.get()` blocks the entire event loop — all users wait while one request completes. Use `httpx.AsyncClient()` or `aiohttp`.
2. **Never store bot tokens in code.** Load from environment variables via `config.py`. Never commit tokens — a leaked bot token gives full control of the bot.
3. **Never hardcode chat/user IDs.** Admin IDs, group IDs, and channel IDs come from config. Hardcoded IDs break when moving between test and production bots.
4. **Never handle errors silently.** If a handler fails, the user should get a meaningful response ("Something went wrong, please try again"). Silent failures make users think the bot is broken.
5. **Never use `time.sleep()`.** It blocks the async loop. Use `await asyncio.sleep()`. `time.sleep(5)` in a handler freezes the entire bot for 5 seconds.
6. **Never send unbounded messages.** Telegram has rate limits (30 messages/second to different chats, 1 message/second to same chat). Batch broadcasts and add delays. Hitting rate limits gets the bot temporarily banned.
7. **Never skip input sanitization.** User messages can contain anything — HTML injection, extremely long strings, special characters. Sanitize before storing or displaying. Use Telegram's HTML parse mode with proper escaping.

## Testing

- Test handlers by creating mock `Update` and `Context` objects. Verify the handler calls the right service functions with the right arguments.
- Test services independently with mocked database sessions.
- Test conversation flows by simulating the full state machine: entry → step 1 → step 2 → completion.
- Use a test bot token and a private test group for integration testing. Never test on production.

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Tornado v6.4 (async Python web framework)
- Python 3.11+
- AsyncHTTPClient for HTTP requests
- WebSocket support
- High-concurrency design

## Project Structure

```
app/
├── __init__.py
├── main.py                     # Tornado app
├── handlers/                   # Request handlers
│   ├── __init__.py
│   ├── base.py                 # Base handler
│   ├── users.py
│   └── websocket.py
├── models/
│   └── user.py
└── lib/
    └── database.py
```

## Architecture Rules

- **RequestHandler classes.** Subclass `RequestHandler` for route handlers.
- **Async by design.** Tornado was async before asyncio existed. Uses own event loop.
- **Non-blocking I/O everywhere.** Database, HTTP calls must be non-blocking.
- **WebSocket support built-in.** `WebSocketHandler` for real-time communication.

## Coding Conventions

- Create handler: `class MainHandler(tornado.web.RequestHandler): async def get(self): self.write('Hello')`.
- Route mapping: `[(r'/users', UsersHandler), (r'/ws', WebSocketHandler)]`.
- Async HTTP: `http_client = AsyncHTTPClient(); response = await http_client.fetch(url)`.
- WebSocket: `async def open(self): ...`, `async def on_message(self, message): ...`.
- Template: `self.render('template.html', **kwargs)`.

## NEVER DO THIS

1. **Never use blocking I/O in handlers.** Tornado's performance relies on non-blocking I/O.
2. **Never forget to call `self.finish()`.** Or use `async def` and Tornado handles it.
3. **Never mix Tornado with asyncio carelessly.** Tornado has its own event loop integration.
4. **Never use sync database drivers.** Use asyncpg, Motor (async MongoDB), etc.
5. **Never ignore Tornado's security features.** XS RF protection, secure cookies built-in.
6. **Never use `time.sleep` in handlers.** Use `await tornado.gen.sleep()` instead.
7. **Never deploy with single process for high traffic.** Use multiple processes behind proxy.

## Testing

- Use `tornado.testing.AsyncHTTPTestCase`.
- Test handlers by creating `Application` with test handlers.
- Test WebSockets with `websocket_connect` test helper.


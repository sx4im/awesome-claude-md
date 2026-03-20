# [PROJECT NAME] - WebSocket Server

## Tech Stack

- Node.js 20+ with TypeScript (strict mode)
- Socket.IO 4.x (or `ws` for raw WebSockets)
- [EXPRESS/FASTIFY] HTTP server for REST endpoints and upgrade handling
- Redis adapter for horizontal scaling (`@socket.io/redis-adapter`)
- Zod for message payload validation
- JWT for connection authentication
- {database} for persistent state

## Project Structure

```
src/
├── server.ts                  # HTTP server + Socket.IO initialization
├── config/                    # Environment config, Redis, JWT secrets
├── middleware/
│   ├── auth.middleware.ts     # Socket authentication (handshake JWT verify)
│   └── rate-limit.ts         # Per-socket message rate limiting
├── handlers/                  # Event handler modules (one per domain)
│   ├── chat.handler.ts        # message:send, message:edit, typing events
│   ├── room.handler.ts        # room:join, room:leave, room:create
│   └── presence.handler.ts   # user:online, user:offline, heartbeat
├── schemas/                   # Zod schemas for every inbound event payload
│   ├── chat.schema.ts
│   └── room.schema.ts
├── services/                  # Business logic (DB queries, notifications)
├── types/                     # Shared types: event maps, socket data
│   └── events.ts              # Typed event map for server and client
└── utils/
    ├── broadcast.ts           # Room-aware broadcast helpers
    └── reconnect.ts           # Server-side reconnection state tracking
```

## Architecture Rules

- **Typed event maps.** Define a `ServerToClientEvents` and `ClientToServerEvents` interface in `types/events.ts`. Pass them to `Server<ClientToServerEvents, ServerToClientEvents>`. Every `socket.emit()` and `socket.on()` is then type-checked at compile time.
- **Handler registration pattern.** Each handler file exports a function `(io: Server, socket: Socket) => void` that registers event listeners. `server.ts` calls `registerChatHandlers(io, socket)` inside `io.on('connection')`. Never pile all event handlers into a single connection callback.
- **Validate every inbound payload.** Every `socket.on('event', data)` callback runs `data` through a Zod schema before processing. Clients send arbitrary JSON. Treat every message as untrusted input.
- **Room-based broadcasting.** Use Socket.IO rooms for scoped messaging. `socket.join(roomId)` on subscription, `io.to(roomId).emit()` for broadcast. Never iterate over all connected sockets to find recipients manually.
- **Authentication at handshake.** Verify JWT in `io.use()` middleware during the handshake, not after connection. Attach the decoded user to `socket.data`. Reject unauthenticated connections before they can send events.

## Coding Conventions

- Event names use colon-separated namespacing: `chat:message:send`, `room:join`, `presence:heartbeat`. Never use camelCase event names -- colons create a visual hierarchy.
- Acknowledgment callbacks: use Socket.IO's `callback` argument for request-response patterns. `socket.emit('room:join', { roomId }, (response) => ...)`. Not a separate `room:join:response` event.
- Error responses use a consistent shape: `{ success: false, error: { code: string, message: string } }`. Never throw exceptions in socket handlers -- they crash the connection silently.
- All handler functions are `async`. Wrap each in a try-catch that emits a structured error event to the sender.
- Log connection ID + user ID on every event for traceability. Use structured logging (pino) with `socket.id` and `socket.data.userId`.

## Library Preferences

- **WebSocket engine:** Socket.IO. not raw `ws` (unless you need zero abstraction overhead). Socket.IO provides rooms, namespaces, auto-reconnection, and binary support out of the box.
- **Scaling:** `@socket.io/redis-adapter` for multi-instance deployments. Not sticky sessions alone -- they fail on rolling deploys.
- **Validation:** Zod. not Joi or class-validator. Zod infers TypeScript types from schemas, eliminating duplicate type definitions.
- **Auth:** `jsonwebtoken` for JWT verification in handshake middleware. Not Passport -- it's designed for HTTP request/response, not persistent connections.
- **Rate limiting:** Custom per-socket counter with sliding window in Redis. Not express-rate-limit -- it works on HTTP requests, not socket events.

## File Naming

- Handlers: `kebab-case.handler.ts` -> `chat.handler.ts`, `presence.handler.ts`
- Schemas: `kebab-case.schema.ts` -> `chat.schema.ts`, `room.schema.ts`
- Middleware: `kebab-case.ts` -> `auth.middleware.ts`, `rate-limit.ts`
- Services: `kebab-case.service.ts` -> `message.service.ts`, `room.service.ts`
- Types: `kebab-case.ts` -> `events.ts`, `socket-data.ts`

## NEVER DO THIS

1. **Never skip payload validation.** A malicious client can send `{ roomId: { $gt: "" } }` as a room join payload. Without Zod validation, this hits your database query directly. Validate shape and types on every event.
2. **Never store session state only in socket memory.** Sockets disconnect. If user presence, typing status, or cursor position lives only in `socket.data`, it vanishes on reconnect. Persist ephemeral state in Redis with TTL.
3. **Never broadcast to all sockets when you mean a room.** `io.emit()` sends to every connected client. Use `io.to(roomId).emit()` for room-scoped messages. Broadcasting everything wastes bandwidth and leaks data between unrelated users.
4. **Never use `setTimeout` for heartbeat/keepalive.** Socket.IO has built-in `pingInterval` and `pingTimeout` configuration. Configure them in the server options. Manual heartbeat timers drift and duplicate.
5. **Never expose internal error stack traces to clients.** Catch errors in handlers and return `{ code: 'INTERNAL_ERROR', message: 'Something went wrong' }`. The full stack trace is for server logs only.
6. **Never forget to handle `disconnect`.** Clean up room memberships, update presence, and release locks in the `disconnect` handler. Orphaned state from unhandled disconnects causes ghost users and stale data.
7. **Never use namespaces as a substitute for rooms.** Namespaces are for separating concerns (e.g., `/chat` vs `/notifications`). Rooms are for dynamic grouping within a namespace. Using namespaces for per-conversation isolation creates hundreds of namespace instances.

## Testing

- Unit test handlers by mocking `socket` and `io` objects. Pass a fake socket with `emit` and `on` spies. Verify the handler calls `io.to(room).emit()` with the correct payload.
- Integration test with `socket.io-client`: spin up the server, connect a test client, emit events, and assert on received messages. Use `done()` callbacks or promisified `once()` for async assertions.
- Test authentication by connecting with invalid/expired/missing JWT and asserting the connection is rejected with a `connect_error` event.
- Test reconnection by forcibly disconnecting a client and verifying it re-authenticates and rejoins its rooms automatically.
- Load test with `artillery` or `k6` WebSocket support to verify the server handles the expected number of concurrent connections without degradation.

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- NestJS WebSockets
- @nestjs/platform-socket.io
- Socket.io
- Gateway pattern
- Rooms and namespaces

## Project Structure
```
src/
├── chat/
│   ├── chat.gateway.ts         // WebSocket gateway
│   ├── chat.module.ts
│   └── chat.service.ts
├── events/
│   └── events.gateway.ts
└── app.module.ts
```

## Architecture Rules

- **Gateway pattern.** `@WebSocketGateway()` for socket handling.
- **SubscribeMessage.** Handle incoming socket events.
- **Emitting events.** Server-to-client communication.
- **Rooms and namespaces.** Organize socket connections.

## Coding Conventions

- Gateway: `@WebSocketGateway({ cors: { origin: '*' } }) export class ChatGateway { @WebSocketServer() server: Server; @SubscribeMessage('message') handleMessage(@MessageBody() data: string, @ConnectedSocket() client: Socket): void { this.server.emit('message', data); } }`.
- Connection: `@SubscribeMessage('join') handleJoin(@MessageBody() room: string, @ConnectedSocket() client: Socket) { client.join(room); }`.
- Broadcast: `this.server.to(room).emit('message', data)`.
- Lifecycle: `handleConnection(client: Socket) { ... } handleDisconnect(client: Socket) { ... }`.

## NEVER DO THIS

1. **Never broadcast to all clients always.** Use rooms for targeted emits.
2. **Never skip authentication.** Use guards for WebSocket connections.
3. **Never forget error handling.** Socket errors can crash the server.
4. **Never store state only in memory.** Redis adapter for scaling.
5. **Never ignore the `ConnectedSocket` decorator.** Access socket instance.
6. **Never skip CORS configuration.** Required for cross-origin connections.
7. **Never use `server.emit` for private messages.** Target specific clients.

## Testing

- Test with `socket.io-client` in tests.
- Test room joining/leaving.
- Test reconnection handling.


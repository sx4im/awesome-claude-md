# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- NestJS Microservices
- @nestjs/microservices
- Transport: Redis/NATS/Kafka/RabbitMQ
- gRPC support
- Event-driven

## Project Structure
```
├── apps/
│   ├── api-gateway/
│   │   └── src/
│   │       └── main.ts         // HTTP entry
│   └── users-service/
│       └── src/
│           ├── main.ts         // Microservice entry
│           └── users.controller.ts
├── libs/
│   └── shared/
│       └── src/
│           └── events/
└── nest-cli.json
```

## Architecture Rules

- **Hybrid application.** HTTP + microservice in one app.
- **Message patterns.** `@MessagePattern` for request-response.
- **Event patterns.** `@EventPattern` for fire-and-forget.
- **Client proxy.** Communicate between services.

## Coding Conventions

- Microservice main: `const app = await NestFactory.createMicroservice<Transport>(AppModule, { transport: Transport.REDIS, options: { host: 'localhost', port: 6379 } }); await app.listen();`.
- Controller: `@Controller() export class UsersController { @MessagePattern({ cmd: 'get_user' }) async getUser(@Payload() id: number): Promise<User> { ... } }`.
- Client: `@Inject('USERS_SERVICE') private client: ClientProxy; this.client.send({ cmd: 'get_user' }, id)`.
- Event: `@EventPattern('user_created') async handleUserCreated(@Payload() data: UserCreatedEvent) { ... }`.

## NEVER DO THIS

1. **Never skip error handling in message handlers.** Use exception filters.
2. **Never use sync calls for everything.** Events for async operations.
3. **Never forget timeout configuration.** `send()` takes `timeout` option.
4. **Never ignore the `Payload()` decorator.** Extracts message payload.
5. **Never mix HTTP and microservice controllers carelessly.** Separate concerns.
6. **Never skip service discovery.** Use Consul, Kubernetes DNS, etc.
7. **Never forget circuit breakers.** Prevent cascade failures.

## Testing

- Test with in-memory transport for unit tests.
- Test message patterns end-to-end.
- Test with actual message broker in integration tests.


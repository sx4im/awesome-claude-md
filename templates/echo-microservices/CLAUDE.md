# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Echo microservices
- NATS/Redis/RabbitMQ
- Service discovery
- Load balancing
- Health checks

## Project Structure
```
services/
├── api-gateway/
│   └── main.go                 // HTTP gateway
├── user-service/
│   └── main.go                 // User service
└── order-service/
    └── main.go                 // Order service
├── docker-compose.yml
└── k8s/
```

## Architecture Rules

- **API Gateway pattern.** Single entry point for clients.
- **Service mesh or message bus.** Communication between services.
- **Health endpoints.** `/health` for orchestration.
- **Circuit breakers.** Prevent cascade failures.

## Coding Conventions

- Gateway: `e.GET("/users/:id", func(c echo.Context) error { resp, _ := http.Get(userServiceURL + "/" + c.Param("id")); return c.JSON(200, resp) })`.
- Service: `e.GET("/health", func(c echo.Context) error { return c.JSON(200, map[string]string{"status": "up"}) })`.
- Discovery: Use Consul, etcd, or Kubernetes DNS.
- Message bus: NATS for pub/sub between services.

## NEVER DO THIS

1. **Never hardcode service URLs.** Use service discovery.
2. **Never skip health checks.** Required for orchestration.
3. **Never ignore timeout configuration.** Prevent hanging requests.
4. **Never skip circuit breaker pattern.** Fail fast when service down.
5. **Never share databases between services.** Each service owns its data.
6. **Never forget distributed tracing.** Track requests across services.
7. **Never use sync calls for everything.** Async events for decoupling.

## Testing

- Test with Docker Compose locally.
- Test service discovery works.
- Test circuit breaker triggers.


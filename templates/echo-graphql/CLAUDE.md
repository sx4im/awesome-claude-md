# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Echo with GraphQL
- graphql-go/graphql
- gqlgen or graph-gophers
- GraphQL Playground
- Subscription support

## Project Structure
```
├── graphql/
│   ├── schema.graphql          // Schema definition
│   ├── resolver.go             // Resolvers
│   ├── generated.go            // Generated code
│   └── model/
│       └── models_gen.go
├── server.go                   // Echo server setup
└── gqlgen.yml                  // Config
```

## Architecture Rules

- **Schema-first.** Define GraphQL SDL first.
- **Code generation.** `gqlgen` generates Go code from schema.
- **Resolver implementation.** Implement generated resolver interface.
- **Echo integration.** HTTP handlers for GraphQL.

## Coding Conventions

- Schema: `type Query { users: [User!]! } type User { id: ID! name: String! }`.
- Generate: `go run github.com/99designs/gqlgen generate`.
- Resolver: `type Resolver struct{ db *sql.DB } func (r *Resolver) Users(ctx context.Context) ([]*model.User, error) { ... }`.
- Handler: `h := handler.NewDefaultServer(generated.NewExecutableSchema(generated.Config{Resolvers: &Resolver{db: db}})); e.POST("/graphql", echo.WrapHandler(h))`.

## NEVER DO THIS

1. **Never edit generated files.** They'll be overwritten.
2. **Never skip schema validation.** Check schema before generating.
3. **Never forget DataLoader.** Essential for N+1 problem.
4. **Never ignore resolver context.** Use for auth, tracing.
5. **Never use resolvers for business logic.** Delegate to services.
6. **Never skip playground in dev.** GraphQL Playground for testing.
7. **Never forget to regenerate after schema changes.** `gqlgen generate`.

## Testing

- Test with GraphQL Playground.
- Test resolvers with mock database.
- Test subscriptions with WebSocket client.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Echo with gRPC
- google.golang.org/grpc
- Protocol Buffers
- grpc-gateway (optional)
- Evans CLI

## Project Structure
```
├── proto/
│   └── service.proto           // Proto definitions
├── pb/
│   └── service.pb.go           // Generated Go code
├── server/
│   └── grpc.go                 // gRPC server
├── gateway/
│   └── http.go                 // HTTP gateway
└── main.go                     // Entry point
```

## Architecture Rules

- **Proto definitions.** Define services and messages in `.proto`.
- **Code generation.** `protoc` generates Go interfaces.
- **Service implementation.** Implement generated interfaces.
- **HTTP gateway optional.** REST API via grpc-gateway.

## Coding Conventions

- Proto: `service UserService { rpc GetUser(GetUserRequest) returns (User); } message User { int64 id = 1; string name = 2; }`.
- Generate: `protoc --go_out=. --go-grpc_out=. proto/service.proto`.
- Server: `type server struct { pb.UnimplementedUserServiceServer } func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) { ... }`.
- Start: `s := grpc.NewServer(); pb.RegisterUserServiceServer(s, &server{}); listener, _ := net.Listen("tcp", ":50051"); s.Serve(listener)`.

## NEVER DO THIS

1. **Never edit generated protobuf code.** Always regenerate.
2. **Never break proto compatibility.** Follow versioning rules.
3. **Never skip context handling.** gRPC is context-driven.
4. **Never ignore deadlines/cancellation.** Check `ctx.Done()`.
5. **Never use without TLS in production.** `credentials.NewServerTLSFromFile`.
6. **Never forget to handle gRPC errors properly.** Status codes matter.
7. **Never skip health checks.** `grpc_health_v1` for load balancers.

## Testing

- Test with Evans CLI.
- Test with generated Go client.
- Test with grpcurl.


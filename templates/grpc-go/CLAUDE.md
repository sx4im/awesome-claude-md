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

## Production Delivery Playbook (Category: Backend)

### Release Discipline
- Fail closed on authz/authn checks and input validation.
- Use explicit timeouts/retries/circuit-breaking for external dependencies.
- Preserve API compatibility unless breaking change is approved and documented.

### Merge/Release Gates
- Unit + integration tests and contract tests pass.
- Static checks pass and critical endpoint latency regressions reviewed.
- Structured error handling verified for all modified endpoints.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Go 1.22+
- gRPC + Protocol Buffers (protobuf v3)
- Connect RPC (buildkite/connect-go) or grpc-go
- PostgreSQL (sqlc for structured typing)
- Zap (Structured JSON logging)
- Docker (deployments)

## Project Structure

```
.
├── proto/                   # Protobuf definitions (.proto files)
│   ├── api/
│   │   └── v1/
│   │       ├── user.proto
│   │       └── auth.proto
│   └── buf.yaml             # Buf configuration
├── gen/                     # Auto-generated code (DO NOT EDIT)
│   └── api/
│       └── v1/
│           ├── user.pb.go
│           └── user_connect.go
├── cmd/
│   └── server/              # Application entrypoint
│       └── main.go
├── internal/
│   ├── server/              # gRPC service implementations
│   │   └── user_server.go
│   ├── database/            # sqlc generated queries
│   └── config/              # Env loading / settings
├── Makefile                 # Generate protobufs, build
├── docker-compose.yml       
└── go.mod
```

## Architecture Rules

- **Schema-first API design.** You define the `.proto` files first. Protobuf determines the strict boundary, input limits, and return types. The Go backend only implements the interface defined by the generated protobuf code.
- **Service encapsulation.** Implement business logic within the GRPC server struct endpoints (`CreateUser`, `GetUser`). If it's a massive application, extract a specific domain layer underlying the server. For most standard APIs, the Server struct acts as your controller.
- **Connect RPC vs vanilla gRPC.** Use `Connect RPC` (https://connectrpc.com/). It automatically supports standard gRPC, gRPC-Web, and regular HTTP/JSON across a single port using the standard `net/http` package. It removes the necessity for Envoy proxies when bridging web/gRPC.
- **Dependency Injection.** Thread dependencies (DB connections, auth clients, loggers) into the Server struct on initialization. Do not use global variables (`var DB *sql.DB`).
- **Context is king.** Accept `context.Context` seamlessly through interceptors (auth token tracking, request IDs, span tracing). Pass context straight down into SQL queries and external client calls to ensure proper timeout and cancellation propagation.

## Coding Conventions

- **Buf for Protobufs.** Manage, format, and lint protobufs with `buf` (https://buf.build/). Never run raw `protoc` strings with massive plugin flags manually. Describe instructions in `buf.gen.yaml`.
- **Structured Logging.** Use `go.uber.org/zap`. Inject a logger on initialization and attach request-specific fields. (e.g., `logger.With(zap.String("trace_id", reqID))`). JSON output for prod, Human output for console.
- **Error mapping.** Return correct gRPC status codes (`codes.NotFound`, `codes.Unauthenticated`, `codes.InvalidArgument`). Never just return a generic `err` string formatted from the standard library. Wrap DB errors correctly.
- **Makefile automation.** Put the code generation inside the Makefile: `make gen` runs `buf generate` and `sqlc generate`.

## Library Preferences

- **gRPC Framework:** `Connect RPC` (buildkite) is preferred to standard `google.golang.org/grpc` due to seamless HTTP/1.1 REST integration and stdlib net/http compliance.
- **Database:** `database/sql` + `sqlc`. Raw queries compiled into type-safe methods. No heavy reflection-bound ORMs.
- **Protobuf tooling:** `buf`. Standardizing the compiler chain removes immense pain point of `protoc` versions across machines.
- **Configuration:** `envconfig` or `viper`. 

## NEVER DO THIS

1. **Never make breaking changes to `.proto` files in production boundaries.** Standard rules: don't alter the types of fields or re-use field tags (e.g. `string user_id = 1` -> `int64 user_id = 1`). Delete the field or deprecate it, and append a new field. `buf breaking` checks this automatically.
2. **Never expose database types via Protobuf endpoints.** If you have a generated sqlc struct `User`, DO NOT force the Protobuf representation to perfectly map it. Define separate clean Protobuf messages, and map the SQL data manually in Go code. Boundaries must remain separate.
3. **Never write gRPC APIs without proper interceptors.** Logging, panic recovery, and metric tracking must be interceptors wrapper functions applied universally to the RPC handler. Without a panic interceptor, a panic in one handler brings down the entire server.
4. **Never swallow upstream cancellation context.** If your frontend abandons a request midway, the incoming `ctx` is canceled. When running `db.QueryRowContext(ctx...)`, it prevents exhausting connection pools on useless queries. Do not replace it with `context.Background()`.
5. **Never write non-deterministic tests.** gRPC requests are easily mimicked. Mock out the SQL interfaces. Use `httptest` servers or generic in-memory mocks to test endpoint validity without spawning full Docker databases unless performing robust E2E testing.
6. **Never leave input un-validated.** Relying purely on Protobufs typed nature is insufficient. Even if it's a `string`, it could be 1GB long. Use `@bufbuild/protovalidate` inside your `.proto` definitions to limit regex boundaries, string lengths, and numeric sizing.

## Testing

- **Unit test endpoints.** Spin up a quick `httptest.Server` (if using Connect) spanning the RPC implementation, use an HTTP client configured as a gRPC client, and send messages natively testing validation paths.
- **E2E with database.** Use `testcontainers-go` to spool a real Postgres container, run your sqlc scripts, execute an endpoint against it, confirm side effects, and cleanly tear it down.

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

## Production Delivery Playbook (Category: DevOps & Infra)

### Release Discipline
- Infrastructure changes must be reviewable, reproducible, and auditable.
- Never bypass policy checks for convenience in CI/CD.
- Protect secret handling and artifact integrity at every stage.

### Merge/Release Gates
- Plan/apply (or equivalent) reviewed with no unknown drift.
- Pipeline security checks pass (SAST/dep/vuln scans as configured).
- Disaster recovery and rollback notes updated for impactful changes.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- OpenTelemetry JS SDK v1.20+ for traces, metrics, and logs
- @opentelemetry/auto-instrumentations-node for automatic instrumentation
- OTLP exporter (gRPC) to OpenTelemetry Collector
- OpenTelemetry Collector v0.95+ with processors and exporters
- Jaeger for trace visualization and analysis
- Prometheus for metrics backend via OTLP receiver
- Node.js 20 LTS with TypeScript 5.3+
- Express.js or Fastify for HTTP framework instrumentation

## Project Structure

```
.
├── src/
│   ├── instrumentation/
│   │   ├── tracing.ts
│   │   ├── metrics.ts
│   │   ├── logging.ts
│   │   ├── setup.ts
│   │   └── custom-spans.ts
│   ├── middleware/
│   │   ├── trace-context.ts
│   │   └── request-metrics.ts
│   ├── lib/
│   │   ├── db-instrumentation.ts
│   │   ├── http-client-instrumentation.ts
│   │   └── queue-instrumentation.ts
│   └── app.ts
├── collector/
│   ├── otel-collector-config.yaml
│   ├── pipeline-traces.yaml
│   ├── pipeline-metrics.yaml
│   └── pipeline-logs.yaml
├── dashboards/
│   ├── service-overview.json
│   └── trace-analysis.json
├── docker-compose.yaml
└── tsconfig.json
```

## Architecture Rules

- Instrumentation must be initialized before any other imports; tracing.ts must be loaded via --require or --import flag in Node.js startup
- Use the NodeSDK class from @opentelemetry/sdk-node as the single entry point for all signal configuration
- Propagation must use W3C TraceContext and Baggage propagators; B3 only if integrating with legacy Zipkin services
- All outgoing HTTP calls must propagate trace context headers automatically via HttpInstrumentation
- Custom spans must be created through the global tracer provider, never by instantiating TracerProvider directly
- Metrics must use the OTLP exporter with delta temporality for Prometheus compatibility via the Collector
- Resource attributes must include service.name, service.version, deployment.environment, and host.name
- Batch span processor with maxExportBatchSize of 512 and scheduledDelayMillis of 5000 in production

## Coding Conventions

- Import the OpenTelemetry API package (@opentelemetry/api) for creating spans, not the SDK package
- Custom span names follow the format: {component}.{operation} (e.g., user-service.getUserById)
- Span attributes use semantic conventions from @opentelemetry/semantic-conventions
- Metrics instrument names use dots as separators: http.server.request.duration, db.query.count
- Always set span status to SpanStatusCode.ERROR and record the exception with span.recordException() on failures
- Use context.with() for explicit context propagation in async callbacks and event emitters
- Log correlation: attach trace_id and span_id to every structured log entry via the Logs Bridge API

## Library Preferences

- Use @opentelemetry/instrumentation-http over manual HTTP span creation
- Use @opentelemetry/instrumentation-express or @opentelemetry/instrumentation-fastify for route-level spans
- Use @opentelemetry/instrumentation-pg for PostgreSQL, @opentelemetry/instrumentation-redis for Redis
- Use @opentelemetry/instrumentation-aws-sdk for AWS service calls
- Use pino as the logger with pino-opentelemetry-transport for log correlation
- Use @opentelemetry/exporter-trace-otlp-grpc over HTTP for lower overhead in production

## File Naming

- Instrumentation files: {concern}.ts in src/instrumentation/ (tracing.ts, metrics.ts)
- Custom instrumentations: {service-name}-instrumentation.ts in src/lib/
- Collector configs: otel-collector-{purpose}.yaml
- Middleware: kebab-case matching the concern (trace-context.ts, request-metrics.ts)

## NEVER DO THIS

1. Never import from @opentelemetry/sdk-trace-base in application code; use @opentelemetry/api for span creation and reserve SDK imports for the setup file only
2. Never create a new TracerProvider per request; use the globally registered provider via trace.getTracer()
3. Never disable batching in production (use BatchSpanProcessor, not SimpleSpanProcessor) as it will cause severe latency
4. Never log full span objects; they contain circular references and will crash JSON.stringify
5. Never set attribute values to undefined or null; skip the attribute entirely or use a sentinel string
6. Never use synchronous exporters in the hot path; all exporters must be async and non-blocking

## Testing

- Use @opentelemetry/sdk-trace-base InMemorySpanExporter in tests to capture and assert on emitted spans
- Assert that critical code paths produce spans with the correct name, attributes, and parent-child relationships
- Test context propagation across async boundaries with explicit context assertions
- Validate collector configuration with otelcol validate --config before deployment
- Integration tests must verify end-to-end trace propagation from HTTP request to database query
- Use the OpenTelemetry Collector's debug exporter in test environments to inspect the full telemetry pipeline
- Metrics tests must verify histogram bucket boundaries and counter monotonicity

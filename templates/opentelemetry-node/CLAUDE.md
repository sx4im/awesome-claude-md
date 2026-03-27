# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

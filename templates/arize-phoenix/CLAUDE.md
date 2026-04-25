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

## Production Delivery Playbook

### Release Discipline
- Validate all critical paths work before merging.
- Maintain security and performance baselines.
- Ensure error handling covers edge cases.

### Merge/Release Gates
- All tests passing (unit, integration, e2e).
- Security scan clean.
- Performance benchmarks met.
- Code review approved.

### Incident Handling Standard
- On incident: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause and follow-up hardening.

## Tech Stack

- **Phoenix**: ML observability (v2.0+)\n- **Python 3.9+**: Instrumentation language\n- **OpenInference**: ML telemetry standard\n- **OpenTelemetry**: Distributed tracing\n- **FastAPI**: Phoenix collector service\n- **PostgreSQL/SQLite**: Metadata storage

## Project Structure

```
phoenix-observability/\n├── app/                        # Phoenix server\n├── tracing/                    # OTel instrumentation\n├── evaluations/                # LLM evaluation suites\n├── embeddings/                 # Vector drift detection\n└── dashboards/                 # Custom views
```

## Architecture Rules

- **Trace all LLM calls.** Every model invocation emits spans.\n- **Embedding drift detection.** Monitor distributions over time.\n- **RAG evaluation.** Trace retriever accuracy, hit rate.\n- **A/B test framework.** Compare model versions with experiments.\n- **Cost attribution.** Tag spans with team/project IDs.

## Coding Conventions

- **Tracer configuration.** `TracerProvider` with `OpenInferenceSpanExporter`.\n- **Span attributes.** Set `openinference.span.kind` as LLM, retriever, chain.\n- **Session tracking.** Use `session_id` for multi-turn conversations.\n- **Evaluation datasets.** Upload with `px.Client().log_evaluations()`.

## NEVER DO THIS

1. **Never sample traces in production.** Capture 100% initially.\n2. **Never log raw PII in spans.** Use `mask_pii=True`.\n3. **Never ignore retrieval failures.** Log errors and empty results.\n4. **Never separate prompt/response.** Log both together.\n5. **Never skip embedding projections.** Visualize regularly.\n6. **Never use Phoenix only for metrics.** Use LLM-as-a-judge.\n7. **Never silo observability data.** Export to Datadog/New Relic.

## Testing

- **Evaluation drift detection.** Run nightly on production samples.\n- **Trace completeness.** Verify all spans have required attributes.\n- **Dashboard usability.** Ensure Phoenix UI loads in < 3s.\n- **Export validation.** Test OTel export. No span drops.\n- **Synthetic monitoring.** Generate queries every 5 minutes.
## Claude Code Integration

- Use `@` mentions to reference specific documentation sections
- Leverage context for framework-specific code generation
- Apply conventions when scaffolding new features
- Validate against NEVER DO THIS rules before accepting changes

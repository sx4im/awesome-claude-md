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

## Production Delivery Playbook (Category: Testing)

### Release Discipline
- Prefer deterministic, isolated tests over brittle timing-dependent flows.
- Quarantine flaky tests and provide root-cause notes before merge.
- Keep test intent explicit and tied to user/business risk.

### Merge/Release Gates
- No new flaky tests introduced in CI.
- Coverage is meaningful on modified critical paths.
- Test runtime impact remains acceptable for pipeline SLAs.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- k6 v0.50+ (Grafana k6) as the load testing framework
- JavaScript ES6 modules for test scripts (k6 uses a Go-based JS runtime, not Node.js)
- k6/http for HTTP requests, k6/ws for WebSocket testing
- k6/browser for browser-based protocol testing
- Grafana + InfluxDB for results visualization (k6 run --out influxdb=http://localhost:8086/k6)
- k6-operator for Kubernetes-distributed execution

## Project Structure

```
tests/
  smoke/            # Quick validation, 1-2 VUs, 30s duration
  load/             # Normal load, ramp to expected traffic
  stress/           # Beyond normal, find breaking points
  spike/            # Sudden surges
  soak/             # Extended duration, memory leak detection
lib/
  helpers.js        # Shared utility functions (randomItem, buildPayload)
  auth.js           # Token generation, login flows
  checks.js         # Reusable check sets (assertStatus, assertBody)
  thresholds.js     # Standard threshold configurations
config/
  environments.js   # Base URLs and env-specific settings per stage
  scenarios.js      # Reusable executor configurations
data/
  users.csv         # Test user pools (use SharedArray for memory efficiency)
  payloads/         # JSON request body templates
scripts/
  run-suite.sh      # Orchestrates multi-script test runs
  compare.sh        # Compares results across runs
```

## Architecture Rules

- Always use `SharedArray` for CSV/JSON test data to avoid duplicating data per VU
- Define thresholds in the `options` export, never rely on manual result inspection
- Use `group()` to logically organize related requests within a test script
- Use `scenarios` with executors (ramping-vus, constant-arrival-rate, externally-controlled) instead of simple vus/duration
- Tag requests with `tags: { name: 'login' }` for per-endpoint threshold filtering
- Use `handleSummary()` export to produce JSON and HTML reports simultaneously
- Sleep between iterations using `sleep(Math.random() * 3 + 1)` to simulate real user pacing

## Coding Conventions

- One test scenario per file; compose via shell scripts or k6-operator
- Export `options` at the top of every test file with thresholds and scenarios
- Use `check()` after every HTTP call; never ignore response validation
- Name checks descriptively: `check(res, { 'POST /api/orders returns 201': (r) => r.status === 201 })`
- Use `Trend`, `Counter`, `Rate`, `Gauge` custom metrics for business-level tracking
- Prefer `http.batch()` for parallel requests that simulate real page loads
- Set `discardResponseBodies: true` in options unless you need body parsing

## Library Preferences

- k6/http over k6/experimental/grpc unless testing gRPC services
- k6/encoding for base64/crypto operations (not external npm packages)
- k6 extensions via xk6 for Kafka (xk6-kafka), SQL (xk6-sql), Redis (xk6-redis)
- Papa Parse via bundled JS for CSV handling inside init context
- k6-summary for custom HTML report generation in handleSummary

## File Naming

- Test files: `<type>-<feature>.test.js` (e.g., `load-checkout.test.js`)
- Helper modules: camelCase `.js` files in `lib/`
- Data files: lowercase-kebab with extensions `.csv` or `.json`
- Config files: lowercase with `.js` extension in `config/`

## NEVER DO THIS

1. Never use `open()` inside the default function; it runs in init context only and will fail at scale
2. Never create objects or parse JSON inside the VU loop that could be done in init context
3. Never hardcode base URLs; always pull from `__ENV.BASE_URL` or environment config
4. Never omit thresholds; every test must have at least `http_req_duration` and `http_req_failed` thresholds
5. Never use `console.log` for metrics tracking; use custom metrics (Trend, Counter, Rate) instead
6. Never run stress tests against production without explicit approval and circuit breakers in place
7. Never share mutable state between VUs; k6 VUs are isolated, use `exec.vu.idInTest` for partitioning

## Testing

- Run smoke tests before every load test to validate script correctness: `k6 run --vus 1 --duration 10s`
- Validate thresholds pass in CI with `k6 run --quiet` and check exit code (non-zero means threshold breach)
- Use `k6 inspect` to validate script syntax without executing
- Test data files must have at least 100 entries to avoid predictable caching during load runs
- Record baseline metrics on a known-good build; compare subsequent runs against baseline
- Use `--out json=results.json` in CI for programmatic result comparison between builds
- Run distributed tests with k6-operator: split by scenario, aggregate with Grafana dashboards

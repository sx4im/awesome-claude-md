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

- **Cohere API**: Managed embedding service (v2.0+)\n- **Python/Node.js SDKs**: Official client libraries\n- **embed-english-v3**: High-quality English model\n- **embed-multilingual-v3**: Multilingual support\n- **AWS/GCP Marketplace**: PrivateLink deployment\n- **NumPy/PyTorch**: Vector manipulation

## Project Structure

```
cohere-embeddings/\n├── client/                     # API client wrapper\n├── models/                     # Model selection logic\n├── batching/                   # Large-scale processing\n├── evaluation/                 # Quality metrics\n└── caching/                    # Embedding cache
```

## Architecture Rules

- **Model selection by domain.** Use `embed-english-v3` for English, `embed-multilingual-v3` for mixed.\n- **Batch API usage.** Maximize batch size (96 texts per call).\n- **Rate limit handling.** Implement exponential backoff.\n- **Input truncation.** Cohere auto-truncates at 512 tokens.\n- **Embed vs Classify.** Classification endpoint for < 100 classes.

## Coding Conventions

- **Async batch processing.** Use `cohere.AsyncClient()` with `asyncio.gather()`.\n- **Connection pooling.** Reuse `cohere.Client()` instances.\n- **Embedding normalization.** Cohere v3 embeddings already normalized.\n- **Request tracing.** Tag with `x-client-name` for analytics.\n- **Fallback strategy.** Implement model fallback on rate limits.

## NEVER DO THIS

1. **Never embed one text at a time.** Batch aggressively. Single-text calls have 10x overhead.\n2. **Never ignore 429 errors.** Respect rate limits.\n3. **Never use embed-v2 for new projects.** v3 has better quality.\n4. **Never store API keys in code.** Use environment variables.\n5. **Never skip input validation.** Validate text length and encoding.\n6. **Never block on embedding calls.** Use async or background queues.\n7. **Never forget cost monitoring.** v3 costs $0.1/1M tokens.

## Testing

- **Embedding quality benchmarks.** Run MTEB retrieval tasks.\n- **API latency tests.** p99 < 500ms for 96-text batch.\n- **Rate limit resilience.** Simulate 429 responses.\n- **Cost per query.** Calculate for typical RAG query.\n- **Multilingual coverage.** Test 10+ languages.
## Claude Code Integration

- Use `@` mentions to reference specific documentation sections
- Leverage context for framework-specific code generation
- Apply conventions when scaffolding new features
- Validate against NEVER DO THIS rules before accepting changes

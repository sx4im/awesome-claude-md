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

- **Dask**: Parallel computing library (v2024.1+)\n- **Python 3.9+**: Primary language\n- **Pandas/NumPy**: Data structures\n- **Distributed scheduler**: Cluster coordination\n- **Kubernetes/Helm**: Container orchestration\n- **Jupyter**: Interactive development

## Project Structure

```
dask-pipeline/\n├── client/                     # Client configuration\n├── delayed/                    # Lazy computation graphs\n├── dataframe/                  # Parallel pandas\n├── bag/                        # Semi-structured data\n└── scheduler/                  # Cluster deployment
```

## Architecture Rules

- **Lazy evaluation first.** Build graph with `delayed`, `dask.dataframe`.\n- **Partition sizing.** Target 100MB-1GB partitions.\n- **Worker memory management.** Set `memory_limit` per worker.\n- **Graph optimization.** Let Dask optimize task graph.\n- **Avoid data movement.** Structure tasks to minimize shuffles.

## Coding Conventions

- **Delayed decorator.** Use `@dask.delayed` for custom functions.\n- **Dataframe partitions.** Specify `npartitions` or `chunksize`.\n- **Persist strategically.** Use `.persist()` for intermediate results.\n- **Progress bars.** Install `dask-labextension` for monitoring.\n- **Debug with sample.** Test on small subset first.

## NEVER DO THIS

1. **Never call `.compute()` in loops.** Build full graph, compute once.\n2. **Never ignore worker memory.** Workers dying from OOM kills entire job.\n3. **Never use `.apply()` row-wise.** It's slow. Use `map_partitions`.\n4. **Never partition too finely.** 10KB partitions kill scheduler.\n5. **Never skip error handling.** Dask hides tracebacks.\n6. **Never mix schedulers.** Don't use `distributed` with `threaded`.\n7. **Never forget cluster shutdown.** Call `client.close()` and `cluster.close()`.

## Testing

- **Unit tests with synchronous scheduler.** `scheduler='synchronous'`.\n- **Integration tests on real cluster.** 3-worker cluster.\n- **Scale testing.** 10x data increase.\n- **Memory profiling.** `memory_profiler` with Dask.\n- **Fault tolerance.** Kill worker mid-computation. Verify recovery.
## Claude Code Integration

- Use `@` mentions to reference specific documentation sections
- Leverage context for framework-specific code generation
- Apply conventions when scaffolding new features
- Validate against NEVER DO THIS rules before accepting changes

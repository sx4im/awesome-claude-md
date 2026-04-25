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

- **AutoGPT Core**: Agent framework (v0.5+)\n- **Python 3.11+**: Orchestration language\n- **OpenAI GPT-4**: Primary LLM\n- **LangChain/LlamaIndex**: Agent memory, retrieval\n- **Redis/PostgreSQL**: Memory backend\n- **Playwright/Selenium**: Browser automation

## Project Structure

```
autogpt-agent/\n├── agent/                      # Core agent logic\n│   ├── memory/                 # Short/long-term memory\n│   └── abilities/              # Agent capabilities\n├── planning/                   # Task decomposition\n├── workspace/                  # Working directory\n└── benchmarks/                 # Evaluation tasks
```

## Architecture Rules

- **Sandboxed execution.** Run abilities in isolated containers.\n- **Human-in-the-loop.** Require approval for destructive operations.\n- **Token budget management.** Track cumulative usage. Halt if exceeded.\n- **Goal constraint validation.** Validate against allowlist.\n- **Memory context windows.** Summarize old memories. Keep recent verbatim.

## Coding Conventions

- **Ability registration.** `@ability` decorator with JSON schema.\n- **Agent loop control.** `max_iterations` limit. Stuck detection.\n- **Error recovery.** Catch ability failures. Return structured errors.\n- **Logging chain-of-thought.** Log all reasoning steps.

## NEVER DO THIS

1. **Never give unrestricted code execution.** Use restricted environments.\n2. **Never allow credential access.** No production secrets access.\n3. **Never skip output validation.** Validate all generated code.\n4. **Never ignore loop detection.** Force pause after repeated actions.\n5. **Never grant network egress freely.** Whitelist allowed domains.\n6. **Never store plaintext secrets.** Memory occasionally logged.\n7. **Never deploy without kill switch.** Emergency stop mechanism.

## Testing

- **Task completion rate.** %% of benchmark tasks completed.\n- **Cost per task.** Average token spend per goal.\n- **Loop detection rate.** How often loop detection triggers.\n- **Sandbox escape attempts.** Monitor for breakouts.\n- **Latency breakdown.** Time in planning vs execution vs API.
## Claude Code Integration

- Use `@` mentions to reference specific documentation sections
- Leverage context for framework-specific code generation
- Apply conventions when scaffolding new features
- Validate against NEVER DO THIS rules before accepting changes

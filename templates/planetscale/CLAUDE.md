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

## Production Delivery Playbook (Category: Database & Messaging)

### Release Discipline
- Protect data correctness with transactional boundaries and idempotent consumers.
- Preserve migration safety (forward + rollback) for schema/index changes.
- Handle poison messages and dead-letter routing explicitly.

### Merge/Release Gates
- Migration dry-run reviewed; no destructive change without backup plan.
- Consumer/producer contract tests pass.
- Data integrity checks and replay strategy documented.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- PlanetScale (serverless MySQL platform)
- Vitess-based (YouTube's scaling solution)
- Git-like branching for databases
- Deploy requests for schema changes
- Edge replication

## Project Structure
```
src/
├── db/
│   ├── connection.ts           # Connection setup (mysql2)
│   ├── schema.prisma           # ORM schema (optional)
│   └── migrations/
└── scripts/
    └── db-push.ts
```

## Architecture Rules

- **Branch-based workflows.** Create database branches like git branches for development.
- **Deploy requests for schema changes.** Review and approve schema changes before production.
- **Vitess-backed scaling.** Automatic sharding and connection pooling.
- **Edge for global distribution.** Replicate read regions globally.

## Coding Conventions

- Connection: Use `mysql2` or `planetscale` database-js driver.
- `database-js`: `import { connect } from '@planetscale/database'; const conn = connect({ host, username, password })`.
- Branching: `pscale branch create mydb dev-branch`.
- Deploy request: `pscale deploy-request create mydb dev-branch main`.
- ORM: Prisma, Drizzle work normally. Configure connection string.

## NEVER DO THIS

1. **Never connect to main branch directly for development.** Always use branches.
2. **Never make schema changes without deploy requests.** Bypassing loses audit trail.
3. **Never ignore the connection limits.** Monitor and configure connection pooling.
4. **Never use foreign key constraints.** PlanetScale recommends avoiding FKs (Vitess limitation).
5. **Never skip the edge regions if global.** Use for read replicas near users.
6. **Never commit credentials.** Use environment variables for connection strings.
7. **Never forget pscale CLI.** `pscale` CLI is essential for branch management.

## Testing

- Test branch-based development workflow.
- Test deploy request review process.
- Test connection pooling under load.

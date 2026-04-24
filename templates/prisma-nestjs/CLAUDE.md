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

- Prisma with NestJS
- @nestjs/prisma
- Prisma Client
- Prisma Service pattern
- TypeScript

## Project Structure
```
src/
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── src/
│   ├── prisma/
│   │   ├── prisma.module.ts
│   │   └── prisma.service.ts   // PrismaClient wrapper
│   ├── users/
│   │   └── users.service.ts
│   └── app.module.ts
```

## Architecture Rules

- **Prisma Service.** Wrapper around PrismaClient for NestJS DI.
- **Module pattern.** `PrismaModule` exports `PrismaService`.
- **Service injection.** Use `PrismaService` in other services.
- **Lifecycle hooks.** Connect/disconnect with `onModuleInit`/`onModuleDestroy`.

## Coding Conventions

- Service: `@Injectable() export class PrismaService extends PrismaClient implements OnModuleInit { async onModuleInit() { await this.$connect(); } async enableShutdownHooks(app: INestApplication) { this.$on('beforeExit', async () => { await app.close(); }); } }`.
- Module: `@Module({ providers: [PrismaService], exports: [PrismaService] }) export class PrismaModule {}`.
- Usage: `@Injectable() export class UsersService { constructor(private prisma: PrismaService) {} async findAll() { return this.prisma.user.findMany(); } }`.

## NEVER DO THIS

1. **Never instantiate PrismaClient directly.** Always use PrismaService.
2. **Never skip `onModuleInit`.** Connection should be explicit.
3. **Never forget `enableShutdownHooks`.** Graceful shutdown.
4. **Never create multiple PrismaClient instances.** Use singleton pattern.
5. **Never ignore transaction handling.** Use `$transaction` for atomic ops.
6. **Never skip migration running.** Database must match schema.
7. **Never use raw queries without escaping.** Risk of SQL injection.

## Testing

- Test with test database or `prisma.$transaction` rollback.
- Test PrismaService lifecycle.
- Mock PrismaService for unit tests.

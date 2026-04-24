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

- Symfony 7 (PHP framework)
- PHP 8.3+
- Doctrine ORM
- Twig templates
- Flex for project management

## Project Structure
```
├── config/
├── src/
│   ├── Controller/
│   │   └── UserController.php
│   ├── Entity/
│   │   └── User.php
│   ├── Repository/
│   └── Form/
│       └── UserType.php
├── templates/
│   └── user/
│       └── index.html.twig
└── tests/
```

## Architecture Rules

- **Bundle-based organization.** Controllers, entities, templates grouped by domain.
- **Dependency injection container.** Services configured in `services.yaml`.
- **Doctrine for ORM.** Entities, repositories, migrations.
- **Twig for templates.** Template inheritance and components.

## Coding Conventions

- Controller: `class UserController extends AbstractController { public function index(UserRepository $repo): Response { ... } }`.
- Route: `#[Route('/users', name: 'user_index')]` attribute.
- Entity: `#[ORM\Entity] class User { #[ORM\Id, ORM\GeneratedValue, ORM\Column] private ?int $id = null; }`.
- Form: `class UserType extends AbstractType { public function buildForm(FormBuilderInterface $builder, array $options): void { $builder->add('name', TextType::class); } }`.
- Template: `{{ user.name }}`, `{% for user in users %}`, `{% extends 'base.html.twig' %}`.

## NEVER DO THIS

1. **Never put business logic in controllers.** Use services.
2. **Never ignore dependency injection.** Don't use `new Service()`, use injection.
3. **Never skip form validation.** Symfony forms handle validation—use it.
4. **Never forget to clear cache after config changes.** `php bin/console cache:clear`.
5. **Never use raw SQL without parameter binding.** SQL injection risk.
6. **Never ignore security.yaml configuration.** Firewalls, access control matter.
7. **Never commit `.env.local` with secrets.** Use `.env.local` for local secrets—gitignore it.

## Testing

- Test with PHPUnit.
- Test controllers with `WebTestCase`.
- Test forms with `FormTestCase`.

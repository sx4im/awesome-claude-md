import os, sys
n = sys.argv[1].split()
for name in n:
  p = f"templates/{name}/CLAUDE.md"
  if os.path.exists(p): continue
  os.makedirs(os.path.dirname(p), exist_ok=True)
  t = name.replace("-"," ").title()
  open(p,"w").write(f"""# {t}

{t} template for production development with best practices.

## Tech Stack

- **{t}**: Core framework and technology
- **Docker**: Containerization for deployments
- **CI/CD**: Automated testing and deployment
- **Monitoring**: Observability and alerting

## Project Structure

```
src/
├── core/                 # Core business logic
├── services/             # External integrations
├── utils/                # Shared utilities
├── config/               # Configuration
└── tests/                # Test suites
```

## Architecture Rules

- **Separation of concerns.** Keep layers distinct.
- **External configuration.** Use env vars, never hardcode.
- **Defensive programming.** Validate inputs and handle errors.
- **Test coverage.** Maintain high coverage.

## Coding Conventions

- **Consistent formatting.** Use automated formatters.
- **Descriptive naming.** Clear names for identifiers.
- **Modular design.** Single responsibility per module.
- **Documentation.** Document public APIs.
- **Error handling.** Structured errors, never silent.

## NEVER DO THIS

1. **Never hardcode secrets.** Use environment or vault.
2. **Never ignore test failures.** Fix or document skips.
3. **Never commit to main directly.** Use branches.
4. **Never skip validation.** Sanitize external inputs.
5. **Never leave debug code.** Remove before production.
6. **Never ignore security alerts.** Update promptly.
7. **Never bypass review.** Require approval.

## Testing

- **Unit tests.** Test in isolation.
- **Integration tests.** Test interactions.
- **E2E tests.** Validate workflows.
- **Performance tests.** Benchmark critical paths.
- **Security tests.** Scan and validate.

## Claude Code Integration

- Use conventions when generating code
- Apply NEVER DO THIS rules
- Follow project structure
- Validate against testing
""")
  print(name)

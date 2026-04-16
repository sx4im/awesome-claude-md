# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Codecov
- Coverage reporting
- PR coverage checks
- Coverage diff
- Badge generation

## Project Structure
```
.github/
└── workflows/
    └── test.yml                // Uploads coverage
codecov.yml                     // Optional configuration
src/
```

## Architecture Rules

- **Coverage tracking.** Track coverage over time.
- **PR comments.** Coverage diff on PRs.
- **Coverage gates.** Fail PRs that drop coverage.
- **Monorepo support.** Multiple coverage reports.

## Coding Conventions

- Config: `coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 2%
    patch:
      default:
        target: 80%`.
- Upload: `- uses: codecov/codecov-action@v4
  with:
    file: ./coverage/lcov.info
    fail_ci_if_error: true`.
- Badge: `![Coverage](https://codecov.io/gh/owner/repo/branch/main/graph/badge.svg)`.

## NEVER DO THIS

1. **Never chase 100% coverage blindly.** Quality over quantity.
2. **Never ignore coverage drops.** Investigate significant drops.
3. **Never skip configuring `target`.** Set realistic thresholds.
4. **Never use without `fail_ci_if_error`.** Silent failures hide issues.
5. **Never forget to ignore generated code.** `ignore` in config.
6. **Never upload multiple times per build.** Dedupe uploads.
7. **Never ignore flaky coverage.** Investigate inconsistent reports.

## Testing

- Test coverage uploads successfully.
- Test PR comments appear.
- Test coverage badge updates.


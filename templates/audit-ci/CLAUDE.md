# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- audit-ci
- NPM audit in CI
- Vulnerability checking
- Severity filtering
- Allowlist support

## Project Structure
```
audit-ci.json                   // or .audit-ci.json
package.json
.github/
└── workflows/
    └── security.yml            // Security audit
```

## Architecture Rules

- **Automated auditing.** Check vulnerabilities in CI.
- **Severity filtering.** Block on high/critical only.
- **Allowlist management.** Known acceptable vulnerabilities.
- **Fail fast.** Prevent shipping known vulnerabilities.

## Coding Conventions

- Config: `{ "moderate": true, "high": true, "critical": true, "allowlist": ["axios|0.21.0", "lodash|4.17.20"] }`.
- Run: `npx audit-ci`.
- NPM script: `"audit:ci": "audit-ci --moderate"`.
- Allowlist: Document why each is acceptable with expiry date.

## NEVER DO THIS

1. **Never ignore all audit failures blindly.** Review each vulnerability.
2. **Never use without allowlist documentation.** Explain why allowed.
3. **Never skip critical vulnerabilities.** Always fix criticals.
4. **Never forget to update allowlist regularly.** Review periodically.
5. **Never use in place of `npm audit fix`.** Try fixing first.
6. **Never ignore transitive vulnerabilities.** `npm audit --prod`.
7. **Never skip the `--report-type` option.** Summary vs full.

## Testing

- Test audit-ci catches known vulnerabilities.
- Test allowlist permits expected packages.
- Test CI fails on new critical vulnerabilities.


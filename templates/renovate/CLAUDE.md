# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Renovate (dependency updates)
- GitHub/GitLab/Bitbucket
- Automated PRs
- Configurable rules
- Scheduling

## Project Structure
```
.github/
└── renovate.json               // Renovate configuration
package.json
```

## Architecture Rules

- **Automated dependency updates.** Creates PRs for new versions.
- **Smart grouping.** Group related updates.
- **Scheduling.** Control when PRs are created.
- **Auto-merge.** Merge safe updates automatically.

## Coding Conventions

- Config: `{ "extends": ["config:base"], "schedule": ["before 9am on monday"], "automerge": true, "automergeType": "pr", "requiredStatusChecks": null }`.
- Grouping: `{ "packageRules": [{ "matchPackagePatterns": ["*"], "groupName": "all dependencies" }] }`.
- Pinning: `"extends": ["config:base", ":pinAllExceptPeerDependencies"]`.
- Ignore: `{ "ignoreDeps": ["some-package"] }`.

## NEVER DO THIS

1. **Never enable auto-merge without tests.** CI must pass.
2. **Never skip reviewing major version updates.** Breaking changes likely.
3. **Never ignore lockfile maintenance.** `lockFileMaintenance` enabled.
4. **Never use without pinning dependencies.** Exact versions for reproducibility.
5. **Never forget to configure `schedule`.** Too many PRs interrupt workflow.
6. **Never ignore security updates.** `extends: ["github>whitesource/merge-confidence:beta"]`.
7. **Never skip the onboarding PR.** Review Renovate's initial configuration.

## Testing

- Test PRs pass CI before merging.
- Test grouped updates work correctly.
- Test scheduling respects time windows.
- Test with private packages.
- Test with private packages.

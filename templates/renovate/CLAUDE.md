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

## File Naming

- Config: `renovate.json`, `.github/renovate.json`, or `renovate.json5` at project root
- Presets: shared configs via `extends` from npm packages or GitHub repos

## Testing

- Test that PRs pass CI before auto-merge triggers.
- Test grouped updates bundle related packages into a single PR.
- Test scheduling respects configured time windows and timezone.
- Test private package updates resolve through configured registries.
- Test major version updates are never auto-merged without review.

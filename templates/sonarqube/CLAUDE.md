# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- SonarQube / SonarCloud
- Code quality analysis
- Security hotspots
- Technical debt tracking
- CI integration

## Project Structure
```
.github/
└── workflows/
    └── sonar.yml               // SonarQube scan
sonar-project.properties        // Project configuration
src/
```

## Architecture Rules

- **Static analysis.** Bugs, vulnerabilities, code smells.
- **Quality gates.** Block PRs that don't meet standards.
- **Security scanning.** Detect vulnerabilities.
- **Debt tracking.** Estimate time to fix issues.

## Coding Conventions

- Config: `sonar.projectKey=my-project
sonar.organization=my-org
sonar.sources=src
sonar.tests=tests
sonar.javascript.lcov.reportPaths=coverage/lcov.info`.
- CI: `- name: SonarQube Scan
  uses: sonarsource/sonarcloud-github-action@master
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}`.
- Ignore: `// NOSONAR` comment to suppress false positives.

## NEVER DO THIS

1. **Never ignore quality gate failures.** Fix or adjust threshold.
2. **Never commit secrets.** SonarQube detects them.
3. **Never skip test coverage reporting.** Configure `lcov`.
4. **Never use default quality profile without review.** Customize for project.
5. **Never ignore security hotspots.** Review each one.
6. **Never forget to configure exclusions.** `node_modules/`, `dist/`.
7. **Never skip branch analysis.** Analyze PRs, not just main.

## Testing

- Test quality gate passes before merging.
- Test coverage reports upload correctly.
- Test security hotspots are reviewed.


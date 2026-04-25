# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Tech Stack

- **Gitea**: Self-hosted Git service (v1.21+)
- **Gitea Actions**: Built-in CI/CD
- **Act**: Local runner testing
- **Docker**: Containerized execution
- **YAML**: Workflow definition
- **Self-hosted runners**: Custom runners

## Project Structure

```
gitea-project/
├── .gitea/
│   └── workflows/              # Gitea workflows
│       ├── ci.yml
│       └── release.yml
├── .github/workflows/           # Compatibility
│   └── ci.yml
├── Dockerfile                  # Runner environment
└── scripts/
    └── build.sh
```

## Architecture Rules

- **GitHub compatible.** Use GitHub Actions syntax. `jobs`, `steps`, `uses`, `run`.
- **Self-hosted runners.** Configure runners for specific needs. GPU, ARM, more resources.
- **Secret management.** Repository and organization secrets. Encrypted storage.
- **Artifact storage.** Local artifact server. S3 compatible.
- **Matrix builds.** Test multiple versions. Node 18, 20. Python 3.10, 3.11.

## Coding Conventions

- **Workflow syntax.** `on: push`, `jobs:`, `steps:`. GitHub Actions compatible.
- **Actions marketplace.** Use `uses: actions/checkout@v4`. Most GitHub actions work.
- **Local actions.** `uses: ./.gitea/actions/local-action`. Repository-local actions.
- **Environment variables.** `env:` at workflow, job, or step level.
- **Secret access.** `${{ secrets.MY_SECRET }}`. Automatic masking in logs.

## NEVER DO THIS

1. **Never commit secrets.** Use Gitea secrets. Never in YAML.
2. **Never use latest tags.** Pin to SHA or specific version. Reproducible builds.
3. **Never skip runner security.** Self-hosted runners execute arbitrary code. Isolate them.
4. **Never ignore logs.** Build logs contain debugging info. Check failures.
5. **Never use infinite loops.** Workflow with bad condition runs forever. Timeout workflows.
6. **Never forget artifact retention.** Artifacts consume storage. Set retention policies.
7. **Never use privileged containers.** Breaks security. Use rootless containers.

## Testing

- **Workflow validation.** Gitea validates YAML syntax. Check before push.
- **Local testing.** Use `act` for local testing. Test workflows before pushing.
- **Runner testing.** Verify runners pick up jobs. Labels match correctly.
- **Secret testing.** Secrets available in workflow. Masked in logs.
- **Matrix testing.** All matrix combinations pass. No version-specific failures.

## Claude Code Integration

- Use `@.gitea/workflows/` for Gitea Actions workflow patterns
- Reference `@.github/workflows/` for GitHub compatibility
- Apply Gitea CI/CD from architecture rules
- Validate against Gitea Actions best practices in NEVER DO THIS

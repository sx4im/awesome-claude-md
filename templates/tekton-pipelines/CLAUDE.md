# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Tech Stack

- **Tekton**: K8s-native CI/CD (v0.56+)
- **Tasks**: Reusable building blocks
- **Pipelines**: DAG of tasks
- **Triggers**: Event-based pipeline runs
- **Workspaces**: Shared storage between tasks
- **Chains**: Supply chain security

## Project Structure

```
tekton-pipelines/
├── tasks/                      # Reusable tasks
│   ├── buildah-build.yaml
│   ├── run-tests.yaml
│   └── deploy-kustomize.yaml
├── pipelines/                  # Pipeline definitions
│   ├── ci-pipeline.yaml
│   └── cd-pipeline.yaml
├── triggers/                   # Event triggers
│   ├── github-trigger.yaml
│   └── gitlab-trigger.yaml
└── chains/                     # Supply chain configs
    └── signing-secrets.yaml
```

## Architecture Rules

- **Task reusability.** One task per concept. Build, test, deploy as separate tasks.
- **Workspace sharing.** Use workspaces for artifacts between tasks. PVC or emptyDir.
- **Parameter passing.** Pass config via parameters. Secrets via workspace or secret volume.
- **Service accounts.** Each pipeline run uses specific SA. Least privilege for pipeline tasks.
- **Results.** Use results for lightweight outputs. URLs, versions, not large artifacts.

## Coding Conventions

- **Task definition.** `steps` with containers. `script` for shell commands.
- **Workspace binding.** Define in Task, bind in Pipeline. Name matching for connectivity.
- **Sidecars.** Use for test dependencies. Databases, caches. Terminate when steps complete.
- **Finally tasks.** `finally` for cleanup. Always run even if pipeline fails.
- **When expressions.** Conditional task execution. `when: input: "$(params.skip)" operator: notin values: ["true"]`.

## NEVER DO THIS

1. **Never hardcode credentials.** Use Kubernetes secrets. Mount as env or volume.
2. **Never use latest image tags.** Pin digests for reproducibility. `image@sha256:...`.
3. **Never skip resource limits.** Tasks without limits can exhaust cluster. Set CPU/memory.
4. **Never ignore pipeline results.** Failed pipelines must block deployment. Don't override.
5. **Never use privileged containers.** Breaks multi-tenancy. Use buildah unprivileged mode.
6. **Never forget about logs.** Tekton logs to CloudWatch/Stackdriver. Configure retention.
7. **Never skip supply chain security.** Use Tekton Chains. Sign images and artifacts.

## Testing

- **Task testing.** Run individual tasks in isolation. Verify step outputs.
- **Pipeline testing.** Run full pipeline on test repo. Verify DAG execution order.
- **Trigger testing.** Send test webhook. Verify pipeline triggered with correct params.
- **Workspace testing.** Verify data persists between tasks. Check volume binding.
- **Resource testing.** Monitor pod resource usage. Right-size requests/limits.

## Claude Code Integration

- Use `@tasks/` for reusable task definitions
- Reference `@pipelines/` for pipeline orchestration patterns
- Apply cloud-native CI/CD from architecture rules
- Validate against Tekton best practices in NEVER DO THIS

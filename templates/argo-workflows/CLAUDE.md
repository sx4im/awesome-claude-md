# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Tech Stack

- **Argo Workflows**: Kubernetes workflow engine (v3.5+)
- **Kubernetes**: Container orchestration platform (v1.27+)
- **YAML**: Workflow definition language
- **Docker**: Container image format for workflow steps
- **MinIO/S3**: Artifact repository for intermediate data
- **Prometheus/Grafana**: Workflow metrics and monitoring

## Project Structure

```
argo-workflows/
├── workflows/                  # Workflow definitions
│   ├── data-pipeline.yaml
│   ├── ml-training.yaml
│   └── ci-cd.yaml
├── templates/                  # Reusable templates
│   ├── steps/
│   │   └── docker-build.yaml
│   └── dag/
│       └── etl-dag.yaml
├── config/                     # Argo configuration
│   ├── configmap.yaml
│   └── rbac.yaml
└── scripts/                    # Helper scripts
    └── submit-workflow.sh
```

## Architecture Rules

- **Template reusability.** Define `WorkflowTemplates` for common steps. Reference with `templateRef`.
- **Artifact passing.** Use S3/MinIO for large data between steps. Don't use container filesystem for big data.
- **Resource requests.** Set CPU/memory requests and limits. Prevents cluster starvation and OOM kills.
- **Retry strategy.** Configure `retryStrategy` for transient failures. Don't fail entire workflow on flaky step.
- **Workflow TTL.** Set `ttlStrategy` to auto-delete old workflows. Prevents etcd bloat.

## Coding Conventions

- **Workflow spec structure.** `entrypoint`, `templates` array. Each template has `container`, `script`, or `dag`.
- **Parameter passing.** Use `inputs.parameters` and `outputs.parameters`. Pass between steps in DAG.
- **Conditionals.** Use `when: "{{inputs.parameters.should-run}} == true"` for conditional step execution.
- **Loops.** Use `withItems` or `withParam` for parallel iteration over lists or JSON arrays.
- **Secrets.** Mount Kubernetes secrets as volumes or env vars. Never hardcode credentials.

## NEVER DO THIS

1. **Never skip resource limits.** Unbounded workflows can crash nodes. Always set CPU/memory limits.
2. **Never use `:latest` tags.** Pin specific image digests for reproducible workflows.
3. **Never ignore artifact GC.** Configure retention policies. Artifact storage grows indefinitely.
4. **Never expose Argo UI publicly.** Use authentication proxy or VPN. Argo has powerful cluster access.
5. **Never forget workflow RBAC.** Service accounts need minimal permissions. Don't use default SA.
6. **Never use `hostPath` volumes.** Security risk and node coupling. Use PVCs or object storage.
7. **Never skip monitoring.** Workflows can hang silently. Prometheus alerts on duration and failures.

## Testing

- **Workflow validation.** Use `argo lint` or `argo template lint` before submission.
- **Local testing.** Use `argo submit --dry-run` to validate. Test individual containers separately.
- **Resource testing.** Monitor pod resource usage. Right-size requests/limits.
- **Failure scenario testing.** Kill pods mid-execution. Verify retry and resume behavior.
- **Artifact testing.** Verify artifacts are correctly uploaded/downloaded between steps.

## Claude Code Integration

- Use `@workflows/` for Argo workflow definition patterns
- Reference `@templates/` for reusable step and DAG templates
- Apply workflow orchestration patterns from architecture rules
- Validate against Kubernetes workflow best practices in NEVER DO THIS

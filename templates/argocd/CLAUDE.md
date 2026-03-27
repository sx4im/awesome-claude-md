# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- ArgoCD v2.10+ for GitOps continuous delivery
- Kustomize for manifest templating and overlays
- ApplicationSets for multi-cluster and multi-tenant deployments
- Sealed Secrets for encrypted secret management
- External Secrets Operator for Vault/AWS Secrets Manager integration
- GitHub Actions for CI (image build + push), ArgoCD for CD

## Project Structure

```
.
├── apps/
│   ├── base/
│   │   ├── kustomization.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── hpa.yaml
│   ├── overlays/
│   │   ├── dev/
│   │   │   ├── kustomization.yaml
│   │   │   └── patches/
│   │   ├── staging/
│   │   │   ├── kustomization.yaml
│   │   │   └── patches/
│   │   └── production/
│   │       ├── kustomization.yaml
│   │       └── patches/
│   └── components/
│       ├── monitoring/
│       └── ingress/
├── applicationsets/
│   ├── cluster-addons.yaml
│   ├── tenant-apps.yaml
│   └── generators/
├── argocd/
│   ├── argocd-cm.yaml
│   ├── argocd-rbac-cm.yaml
│   ├── projects/
│   └── notifications/
├── clusters/
│   ├── dev/
│   ├── staging/
│   └── production/
└── scripts/
    └── validate.sh
```

## Architecture Rules

- Every Application must belong to an AppProject with restricted sourceRepos and destinations
- Use sync waves via argocd.argoproj.io/sync-wave annotations: CRDs (wave -5), namespaces (wave -3), configs (wave -1), apps (wave 0), post-deploy jobs (wave 5)
- ApplicationSets must use the git generator for directory-based discovery or the matrix generator for cluster x app combinations
- All secrets must go through Sealed Secrets or External Secrets Operator; never commit plaintext secrets
- Health checks must be defined for custom resources using argocd-cm resource.customizations.health
- Sync policies: automated sync with selfHeal enabled for dev/staging, manual sync required for production
- Prune must be enabled with ServerSideApply for all environments

## Coding Conventions

- Kustomize bases must be deployable standalone without any overlay for local testing
- Use strategic merge patches over JSON patches; JSON patches only for array operations
- Resource names follow the pattern: {app}-{component}-{resource-type}
- All resources must have labels: app.kubernetes.io/name, app.kubernetes.io/part-of, app.kubernetes.io/managed-by: argocd
- Annotations for sync waves must always include a comment explaining the ordering rationale
- ConfigMap and Secret names must use the namePrefix or nameSuffix generators for rolling updates

## Library Preferences

- Use Kustomize built-in transformers over custom plugins
- Prefer kustomize components for reusable cross-cutting features (monitoring sidecars, network policies)
- Use ApplicationSet template patches over per-app Application manifests
- Notifications via argocd-notifications with Slack and PagerDuty integrations

## File Naming

- Kubernetes manifests: lowercase-kebab-case matching the resource kind (deployment.yaml, service.yaml)
- Patches: patches/{target-resource}-{description}.yaml
- ApplicationSets: {scope}-{generator-type}.yaml (e.g., tenant-apps-git.yaml)
- Sealed secrets: sealed-{secret-name}.yaml

## NEVER DO THIS

1. Never use Helm charts directly in ArgoCD when Kustomize overlays can achieve the same result; wrap Helm with Kustomize helmCharts if Helm is needed
2. Never set retry.limit higher than 5 or retry.backoff.duration lower than 10s to avoid API server overload
3. Never grant ArgoCD cluster-admin; use fine-grained RBAC per AppProject with deny-by-default namespace restrictions
4. Never use spec.source.targetRevision: HEAD in production; always pin to a Git tag or commit SHA
5. Never put environment-specific values in base kustomization; all env differences must live in overlays
6. Never skip the PreSync hook for database migrations; always run migrations as a pre-sync Job with a backoffLimit of 1
7. Never disable pruning to work around drift; fix the drift source or add the argocd.argoproj.io/compare-options: IgnoreExtraneous annotation

## Testing

- Run `kustomize build` on every overlay in CI to catch rendering errors before merge
- Validate all rendered manifests with kubeconform using strict mode and the latest Kubernetes schema
- Use argocd app diff --local against each overlay to preview changes before merging
- ApplicationSet templates must be tested with argocd appset generate --dry-run
- Sync wave ordering must be validated with a script that parses annotations and checks dependency order
- Run kubeval or kubeconform with --kubernetes-version matching each target cluster version

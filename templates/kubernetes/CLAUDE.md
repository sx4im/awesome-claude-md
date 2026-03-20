# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Kubernetes 1.28+ (EKS, GKE, AKS, or self-managed)
- Kustomize for environment-specific overlays
- Helm 3 for third-party chart dependencies
- kubectl for cluster interaction
- [ArgoCD / Flux] for GitOps continuous delivery

## Project Structure

```
[PROJECT_ROOT]/
├── base/                             # Shared base manifests
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml                     # HorizontalPodAutoscaler
│   ├── pdb.yaml                     # PodDisruptionBudget
│   └── configmap.yaml
├── overlays/
│   ├── dev/
│   │   ├── kustomization.yaml       # Patches for dev
│   │   ├── replica-patch.yaml
│   │   └── env-config.yaml
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   └── resource-patch.yaml
│   └── prod/
│       ├── kustomization.yaml
│       ├── replica-patch.yaml
│       ├── resource-patch.yaml
│       └── ingress-patch.yaml
├── components/                       # Reusable Kustomize components
│   ├── monitoring/                  # Prometheus annotations, ServiceMonitor
│   └── istio/                       # Istio sidecar configuration
├── charts/                          # Helm charts for third-party deps
│   └── values-[env].yaml
├── scripts/
│   └── validate.sh                  # Pre-commit manifest validation
└── docs/
    └── runbook.md                   # Operational procedures
```

## Architecture Rules

- **Base + overlays, always.** All resource definitions live in `base/`. Environment differences are expressed as Kustomize patches in `overlays/`. Never duplicate a full Deployment manifest across environments. If environments differ by 3 fields, patch those 3 fields.
- **One namespace per service per environment.** `[SERVICE]-[ENV]` naming (e.g., `api-prod`, `api-dev`). Never deploy dev and prod workloads in the same namespace. Namespace-scoped RBAC and NetworkPolicies depend on this boundary.
- **Resource requests and limits on every container.** No exceptions. A container without resource limits can consume an entire node's memory and OOMKill neighboring pods. Set requests to typical usage, limits to 2x requests for burst headroom.
- **Health checks are non-negotiable.** Every Deployment has `readinessProbe`, `livenessProbe`, and `startupProbe` (for slow-starting apps). Readiness gates traffic. Liveness restarts. Startup prevents liveness from killing pods that are still initializing. Never use the same endpoint for all three unless you understand the consequences.
- **PodDisruptionBudgets on everything in production.** `minAvailable: 1` at minimum. Without a PDB, a node drain during cluster upgrade can take down all replicas simultaneously.

## Coding Conventions

- **Labels are structured.** Every resource has: `app.kubernetes.io/name`, `app.kubernetes.io/instance`, `app.kubernetes.io/version`, `app.kubernetes.io/component`, `app.kubernetes.io/managed-by`. These labels power service discovery, monitoring queries, and `kubectl` filtering.
- **Use `kustomization.yaml` commonLabels sparingly.** `commonLabels` are injected into selectors, which are immutable after creation. If you change a common label, you must delete and recreate the Deployment. Use `commonAnnotations` for metadata that changes.
- **Strategic merge patches over JSON patches.** Use strategic merge patches (`patchesStrategicMerge`) for most overrides. JSON patches (`patchesJson6902`) only when you need to modify array elements by index. Strategic merge is readable; JSON patches are cryptic.
- **Secrets via external operators.** Use External Secrets Operator or Sealed Secrets to sync secrets from Vault/AWS Secrets Manager. Never commit base64-encoded `Secret` manifests to git — base64 is encoding, not encryption.
- **Image tags are immutable.** Use digest-pinned images (`image: app@sha256:abc123`) or semantic version tags (`image: app:v1.2.3`). Never use `:latest` in production. `:latest` means "whatever was pushed last," which is non-deterministic across nodes.

## Library Preferences

- **Overlay engine:** Kustomize (built into kubectl). Not Jsonnet (steep learning curve, poor tooling). Helm for third-party charts only, not for your own application manifests unless chart distribution is required.
- **GitOps:** ArgoCD or Flux. Not manual `kubectl apply` in production. Not CI-triggered `kubectl apply` (no drift detection, no rollback tracking).
- **Secrets management:** External Secrets Operator syncing from AWS Secrets Manager / HashiCorp Vault. Not Sealed Secrets (encryption key management overhead). Not raw Kubernetes Secrets committed to git.
- **Ingress:** Ingress-NGINX or Istio Gateway. Not multiple ingress controllers fighting over the same IngressClass.
- **Monitoring:** Prometheus + Grafana via kube-prometheus-stack Helm chart. ServiceMonitor CRDs for per-service metrics scraping.

## File Naming

- Manifests: `resource-type.yaml` (e.g., `deployment.yaml`, `service.yaml`, `hpa.yaml`)
- Patches: `descriptive-patch.yaml` (e.g., `replica-patch.yaml`, `resource-patch.yaml`)
- Environment values: `values-[env].yaml` for Helm overrides
- Never combine multiple resource types in one file unless they are tightly coupled (e.g., Deployment + Service for a single microservice in a simple setup)

## NEVER DO THIS

1. **Never run `kubectl apply` against production without `--dry-run=server` first.** Server-side dry run validates against the actual cluster state, admission webhooks, and resource quotas. Client-side dry run catches only syntax errors.
2. **Never use `kubectl edit` in production.** Edits bypass git history, drift from the source of truth, and get overwritten on the next GitOps sync. All changes go through git, review, and merge.
3. **Never set `replicas` in a Deployment that has an HPA.** The HPA manages replica count. Setting `replicas` in the manifest fights the autoscaler. On every deploy, you reset the HPA's scaling decisions. Remove the `replicas` field entirely and let HPA control it.
4. **Never mount ServiceAccount tokens when not needed.** Set `automountServiceAccountToken: false` on pods that do not call the Kubernetes API. A compromised pod with a mounted token can enumerate and attack cluster resources.
5. **Never use `hostNetwork: true` or `hostPID: true` unless you are deploying infrastructure daemons.** These break network isolation and let the pod see all host processes. Application workloads never need this.
6. **Never create CronJobs without `concurrencyPolicy` and `activeDeadlineSeconds`.** Without these, a stuck job spawns infinite overlapping instances. Set `concurrencyPolicy: Forbid` and a reasonable deadline.
7. **Never skip NetworkPolicies.** By default, every pod can talk to every other pod. Create a default-deny ingress policy per namespace and explicitly allow only required traffic paths. Zero-trust networking starts here.

## Testing

- Validate all manifests with `kubectl apply --dry-run=server` or `kubeconform` in CI. Catch schema violations, invalid API versions, and typos before merge.
- Use `kustomize build overlays/dev | kubeconform` to validate the fully-rendered output of each overlay, not just the base templates.
- Use `kubeval` or OPA/Gatekeeper policies to enforce conventions (resource limits present, labels present, no `latest` tags) as CI gates.
- Test Helm chart upgrades with `helm upgrade --dry-run --debug` against a staging cluster to catch value mismatches and hook failures before production.
- Maintain a `kind` or `k3d` cluster config in the repo for local integration testing. Developers should be able to deploy the full overlay locally with one command.

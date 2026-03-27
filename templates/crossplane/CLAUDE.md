# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Crossplane v1.15+ for control plane infrastructure management
- Provider AWS v0.47+ (upbound/provider-aws family providers) for AWS resources
- Provider Kubernetes for in-cluster resource management
- Composite Resource Definitions (XRDs) and Compositions for platform abstractions
- Functions (composition functions) for advanced templating via function-patch-and-transform
- External Secrets Operator for provider credential injection
- Argo CD for GitOps delivery of Crossplane manifests

## Project Structure

```
.
├── apis/
│   ├── database/
│   │   ├── definition.yaml
│   │   ├── composition-aws.yaml
│   │   └── composition-gcp.yaml
│   ├── network/
│   │   ├── definition.yaml
│   │   └── composition-aws.yaml
│   ├── cluster/
│   │   ├── definition.yaml
│   │   └── composition-eks.yaml
│   └── storage/
│       ├── definition.yaml
│       └── composition-s3.yaml
├── providers/
│   ├── provider-aws.yaml
│   ├── provider-kubernetes.yaml
│   └── provider-configs/
│       ├── aws-dev.yaml
│       ├── aws-staging.yaml
│       └── aws-production.yaml
├── functions/
│   ├── function-patch-and-transform.yaml
│   └── function-auto-ready.yaml
├── claims/
│   ├── dev/
│   ├── staging/
│   └── production/
├── packages/
│   ├── configuration/
│   │   ├── crossplane.yaml
│   │   └── Makefile
│   └── provider/
└── tests/
    └── compositions/
```

## Architecture Rules

- Every managed resource must be part of a Composition; never create bare managed resources directly
- XRDs define the platform API; spec fields must be minimal and expose only what application teams need
- Compositions must use function-patch-and-transform for all patching; legacy inline patches are deprecated
- Provider configs must use InjectedIdentity or Secret reference; never embed credentials in ProviderConfig
- Use composition-revision-policy: Manual to control rollout of Composition changes to existing resources
- All Compositions must include a function-auto-ready step as the last pipeline function to set readiness
- Claims (XRCs) must be namespace-scoped; Composite Resources (XRs) are cluster-scoped and managed by the platform team
- Resource naming: use spec.resourceRef naming with a deterministic suffix derived from claim metadata

## Coding Conventions

- XRD group must follow the pattern: {domain}.platform.{org}.io (e.g., databases.platform.acme.io)
- XRD version must start at v1alpha1 and follow Kubernetes API versioning conventions
- Composition names: {provider}-{resource-type} (e.g., aws-postgresql, gcp-gke-cluster)
- All managed resources in a Composition must have explicit providerConfigRef patches from the XR
- Status conditions must be patched back to the XR for observability: connectionDetails, readiness
- Connection details must use connectionSecretKeys to expose only required fields (host, port, username, password)
- Every XRD spec must include a required parameters.region field and an optional parameters.tags map

## Library Preferences

- Use upbound/provider-aws family providers over monolithic provider-aws for faster reconciliation
- Use function-patch-and-transform over legacy patch-and-transform engine
- Use function-go-templating for complex conditional logic that patch-and-transform cannot express
- Use crossplane-contrib/provider-helm only when no native provider support exists
- Package compositions as Crossplane Configurations using crossplane.yaml and OCI images

## File Naming

- XRD definitions: definition.yaml in the resource-type directory
- Compositions: composition-{provider}.yaml alongside the definition
- Provider configs: {provider}-{environment}.yaml
- Claims: {resource-name}.yaml in the environment directory
- Functions: function-{name}.yaml in the functions directory
- Packages: crossplane.yaml as the Configuration metadata file

## NEVER DO THIS

1. Never use spec.publishConnectionDetailsTo without a SecretStoreConfig; connection secrets must go to an external store in production
2. Never set deletionPolicy: Orphan unless explicitly required for migration; it leaves dangling cloud resources
3. Never create Compositions with more than 20 managed resources; break them into nested XRs for composability
4. Never use spec.writeConnectionSecretToRef in the Composition for multiple resources writing to the same secret; use connectionDetailKeys merging
5. Never skip readinessChecks on managed resources; unchecked resources will report Ready prematurely
6. Never use wildcards in ProviderConfig IRSA trust policies; scope to specific service accounts

## Testing

- Validate all XRDs and Compositions with crossplane beta validate before merge
- Use crossplane beta render to dry-run Compositions locally with sample XR inputs
- Write render tests for every Composition with expected output YAML checked into the tests directory
- End-to-end tests must provision real resources in a sandbox AWS account and assert readiness within timeout
- Test claim creation and deletion in a kind cluster with Crossplane installed using the CI pipeline
- Verify that connection secrets contain all expected keys after successful provisioning
- Run crossplane beta diff to compare rendered output between Composition revisions before promoting

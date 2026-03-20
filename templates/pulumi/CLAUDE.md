# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Pulumi 3+ with TypeScript
- [AWS / GCP / Azure] provider
- Pulumi ESC for environment and secrets management
- Node.js 20+ runtime
- Jest for infrastructure testing

## Project Structure

```
[PROJECT_ROOT]/
├── index.ts                          # Main entrypoint, composes stacks
├── components/
│   ├── networking.ts                 # VPC, subnets, security groups
│   ├── database.ts                   # RDS, DynamoDB, Cloud SQL
│   ├── compute.ts                    # ECS, Lambda, GKE, Cloud Run
│   ├── storage.ts                    # S3, GCS buckets
│   └── monitoring.ts                 # CloudWatch, alerts, dashboards
├── config/
│   ├── types.ts                      # Shared config interfaces
│   └── defaults.ts                   # Default values per environment
├── utils/
│   ├── naming.ts                     # Resource naming conventions
│   └── tags.ts                       # Common tag generation
├── stacks/
│   ├── network-stack.ts              # Network layer composition
│   ├── data-stack.ts                 # Data layer composition
│   └── app-stack.ts                  # Application layer composition
├── tests/
│   ├── components/
│   │   └── networking.test.ts
│   └── utils/
│       └── naming.test.ts
├── Pulumi.yaml                       # Project definition
├── Pulumi.dev.yaml                   # Dev stack config
├── Pulumi.staging.yaml               # Staging stack config
├── Pulumi.prod.yaml                  # Prod stack config
├── tsconfig.json
└── package.json
```

## Architecture Rules

- **ComponentResources for everything.** Group related resources into classes extending `pulumi.ComponentResource`. A VPC component encapsulates the VPC, subnets, route tables, and NAT gateways. Never create loose resources in `index.ts`. Components are the unit of reuse, testing, and reasoning.
- **Stack references for cross-stack dependencies.** The app stack reads VPC ID from the network stack via `StackReference`. Never hardcode resource IDs across stacks. Never pass resources between stacks by importing them in the same program — use explicit `StackReference` outputs.
- **Configuration drives everything.** Use `pulumi.Config` and typed config objects for environment-specific values (instance sizes, replica counts, feature flags). Never use `if (pulumi.getStack() === "prod")` conditionals. Stacks should be structurally identical, differing only in config values.
- **Outputs are the API contract.** Every ComponentResource exports outputs that downstream consumers need (IDs, ARNs, endpoints, connection strings). Define output types explicitly. Never force consumers to reach into component internals.
- **Protect stateful resources.** Databases, S3 buckets with data, and encryption keys get `{ protect: true }` in resource options. This prevents accidental deletion via `pulumi destroy` or resource replacement. Removing protection is a deliberate, reviewed action.

## Coding Conventions

- **Type everything.** Define interfaces for component args: `interface NetworkArgs { cidrBlock: string; azCount: number; enableNat: boolean; }`. Never use anonymous objects or `any` for resource inputs. Pulumi's TypeScript types are your safety net.
- **Naming convention function.** Create a `naming.ts` utility: `const name = (resource: string) => \`\${project}-\${stack}-\${resource}\``. Every resource uses this function. Never concatenate names inline. Consistent naming enables filtering in the cloud console and cost allocation.
- **Apply and transform, don't await.** Use `pulumi.interpolate\`\${vpc.id}-subnet\`` and `.apply(v => ...)` for computed values. Never use `await` on Pulumi Outputs — they are not Promises. `Output.apply()` is the monadic bind; treat it like `.then()` but for infrastructure values.
- **Tags as a utility.** Define common tags once: `const baseTags = { Project: project, Stack: stack, ManagedBy: "pulumi" }`. Spread into every resource: `tags: { ...baseTags, Name: name("api") }`. Never tag resources individually with different key conventions.
- **Explicit dependencies with `dependsOn`.** When Pulumi cannot infer the dependency graph (e.g., IAM policies that must exist before a Lambda), use `{ dependsOn: [policy] }`. Never rely on implicit ordering from code execution sequence.

## Library Preferences

- **Language:** TypeScript. Not Python or Go for Pulumi unless the team is already fluent. TypeScript gives the best type inference, IDE support, and access to the largest Pulumi component ecosystem.
- **State backend:** Pulumi Cloud (managed state, secrets, RBAC, drift detection). Self-hosted S3 backend only if compliance requires it. Not local state files.
- **Secrets:** Pulumi's built-in secrets management (`pulumi config set --secret`). Secrets are encrypted in state. Not plaintext config values for passwords, API keys, or certificates.
- **Provider packages:** First-party Pulumi providers (`@pulumi/aws`, `@pulumi/gcp`). Not Terraform bridge providers unless the native Pulumi provider is missing a resource.
- **Multi-cloud:** Avoid unless genuinely required. Each cloud has different resource models. Write cloud-specific components, not leaky abstractions.

## File Naming

- Components: `PascalCase.ts` or `kebab-case.ts` matching the component class name
- Stack configs: `Pulumi.[stack-name].yaml`
- Tests: `component-name.test.ts` mirroring the source file
- Utilities: `kebab-case.ts` (e.g., `naming.ts`, `tags.ts`)
- Index: `index.ts` is the only file that instantiates components and exports stack outputs

## NEVER DO THIS

1. **Never use `pulumi up --yes` in production without reviewing the preview.** The preview shows creates, updates, and deletes. Skipping review in production means you deploy blind. CI/CD should require manual approval for prod stacks.
2. **Never store secrets as plaintext config.** `pulumi config set dbPassword hunter2` stores it in plaintext in `Pulumi.dev.yaml` which is committed to git. Always use `pulumi config set --secret dbPassword`. Pulumi encrypts secrets in the stack file.
3. **Never use `Output.get()` or cast Outputs to strings.** `Output<string>` is not a string. Calling `.get()` only works during `pulumi up`, not during previews or tests. Use `.apply()` to transform outputs. If you need a value synchronously, your architecture is wrong.
4. **Never create resources in loops without stable keys.** `for (let i = 0; i < count; i++)` creates resources named `resource-0`, `resource-1`. Removing an item renumbers everything. Use `for...of` with a meaningful key: `for (const az of azs) { new Subnet(\`subnet-\${az}\`, ...) }`.
5. **Never ignore replacement warnings in previews.** If the preview shows `+-` (replace), the resource will be deleted and recreated. For databases and stateful resources, this means data loss. Investigate why and use `aliases` or `import` to prevent unintended replacements.
6. **Never put secrets in `index.ts` or any source file.** Use `pulumi.Config` to read secrets at runtime. Source files are committed to git. Config secrets are encrypted in state.
7. **Never skip `pulumi preview` in CI for pull requests.** Every PR that changes infrastructure should show a preview comment with the planned changes. Reviewers must see what will be created, updated, or destroyed before approving.

## Testing

- **Unit tests with mocks.** Use `pulumi.runtime.setMocks()` to mock resource creation. Assert that components create expected resources with correct properties: verify security groups have correct ingress rules, S3 buckets have encryption enabled.
- **Property tests.** Assert that all resources have required tags, that no security group allows `0.0.0.0/0` ingress on port 22, and that all S3 buckets block public access. Run these in CI against every PR.
- **Integration tests.** For critical infrastructure, deploy to an ephemeral stack (`pulumi up --stack test-pr-123`), run validation (HTTP health checks, connectivity tests), then destroy. Budget for the cloud cost.
- **Policy as code.** Use Pulumi CrossGuard or OPA policies to enforce compliance rules (no public S3 buckets, no unencrypted databases) as automated gates in the deployment pipeline.

# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: DevOps & Infra)

### Release Discipline
- Infrastructure changes must be reviewable, reproducible, and auditable.
- Never bypass policy checks for convenience in CI/CD.
- Protect secret handling and artifact integrity at every stage.

### Merge/Release Gates
- Plan/apply (or equivalent) reviewed with no unknown drift.
- Pipeline security checks pass (SAST/dep/vuln scans as configured).
- Disaster recovery and rollback notes updated for impactful changes.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Terraform 1.6+ (HCL)
- AWS, GCP, or Azure provider
- Remote state in S3/GCS with DynamoDB/GCS locking
- Modules for reusable infrastructure components
- Terragrunt (optional) for multi-environment orchestration

## Project Structure

```
infra/
├── environments/
│   ├── dev/
│   │   ├── main.tf          # Root module for dev
│   │   ├── variables.tf     # Dev-specific variable values
│   │   ├── terraform.tfvars # Variable overrides
│   │   └── backend.tf       # Remote state config for dev
│   ├── staging/
│   └── prod/
├── modules/
│   ├── networking/          # VPC, subnets, security groups
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── database/            # RDS, Cloud SQL instances
│   ├── compute/             # ECS, GKE, EC2 instances
│   └── monitoring/          # CloudWatch, alerts, dashboards
└── global/                  # Resources shared across environments
    ├── iam/                 # IAM roles and policies
    └── dns/                 # Route53 hosted zones
```

## Architecture Rules

- **Modules for everything reusable.** If you create a resource in more than one environment, it belongs in `modules/`. Environments consume modules with different variables. Never copy-paste resource blocks across environment directories.
- **One backend per environment.** Each environment has its own remote state file. Dev state is separate from prod state. A `terraform apply` in dev can never accidentally destroy prod resources.
- **Variables have types, descriptions, and validation.** Every variable block includes `type`, `description`, and `validation` where applicable. Never use untyped `variable "name" {}`.
- **Outputs expose what downstream modules need.** Every module outputs IDs, ARNs, and connection strings that other modules consume. Don't make consumers use data sources to look up resources created by another module.
- **Lifecycle rules are explicit.** Resources that should never be destroyed use `lifecycle { prevent_destroy = true }`. Resources that should be recreated before the old one is destroyed use `create_before_destroy = true`.

## Coding Conventions

- **Resource naming:** `resource "aws_instance" "api_server"`. descriptive, snake_case. The resource name describes what it IS, not what module it's in. Never use `main`, `this`, or `default` as resource names.
- **Tag everything.** Every resource has at minimum: `Name`, `Environment`, `Project`, `ManagedBy = "terraform"`. Define common tags as a local and merge with resource-specific tags.
- **Use `locals` for computed values.** `locals { api_name = "${var.project}-${var.environment}-api" }`. Never concatenate strings inline in resource arguments repeatedly.
- **Data sources for external references.** Looking up an existing VPC? Use `data "aws_vpc"`. Never hardcode IDs like `vpc-0abc123`. Data sources are self-documenting and environment-agnostic.
- **No inline provisioners.** Don't use `provisioner "local-exec"` or `remote-exec` in resource blocks. Use dedicated tools (Ansible, user_data scripts, cloud-init) for configuration management.

## Library Preferences

- **State backend:** S3 + DynamoDB (AWS), GCS (GCP). not local state (team members overwrite each other). Not Terraform Cloud unless the team is already paying for it.
- **Module source:** internal modules via relative paths (`source = "../../modules/networking"`). Public registry modules for battle-tested infra (vpc, eks). Pin module versions.
- **Secrets:** AWS Secrets Manager or GCP Secret Manager. not Terraform variables for secrets (they end up in state files). Reference secrets at runtime, not at plan time.
- **Linting:** `tflint`. catches deprecated syntax, invalid resource types, and provider-specific issues. Not just `terraform validate` (it only checks syntax).

## NEVER DO THIS

1. **Never store state locally.** Local state can't be shared, locks don't work, and losing the file means Terraform forgets everything it created. Use remote state with locking from day one.
2. **Never hardcode resource IDs.** `subnet_id = "subnet-0abc123"` breaks in every other environment. Use variables, data sources, or module outputs.
3. **Never use `terraform destroy` in production without a plan review.** Always run `terraform plan -destroy` first and review every resource being destroyed. Automation should require approval gates.
4. **Never commit `.tfvars` files with secrets.** Use environment variables (`TF_VAR_db_password`) or a secrets manager. `.tfvars` files in git mean secrets in git history forever.
5. **Never use `count` for resources that need stable identifiers.** Use `for_each` with a map. `count` breaks when you remove an item from the middle of a list. Terraform renumbers everything and recreates all subsequent resources.
6. **Never modify state manually with `terraform state mv` unless you understand the consequences.** State surgery is dangerous. Document what you're doing, create a backup, and have a rollback plan.
7. **Never skip `terraform fmt`.** Run it before every commit. Inconsistent formatting in HCL creates noisy diffs and hides real changes.

## Workflow

```bash
# Initialize backend
terraform init

# Preview changes
terraform plan -out=plan.tfplan

# Apply the reviewed plan
terraform apply plan.tfplan

# Format all HCL files
terraform fmt -recursive

# Validate configuration
terraform validate
```

## Testing

- Use `terraform plan` in CI for every PR. verify the plan shows expected changes and no unexpected destroys.
- Use `terraform validate` and `tflint` in CI to catch syntax and provider issues.
- Use Terratest (Go) for integration tests that create real infrastructure, verify it, and destroy it.
- Every module has an `examples/` directory with a minimal working configuration for testing.

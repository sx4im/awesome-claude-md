# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Tech Stack

- **Terraform**: IaC tool (v1.7+)
- **HCL**: HashiCorp Configuration Language
- **AWS/Azure/GCP**: Cloud providers
- **Terraform Cloud/Enterprise**: Remote state and collaboration
- **Terragrunt**: DRY configuration wrapper
- **Atlantis**: Terraform pull request automation

## Project Structure

```
terraform-infra/
├── modules/                    # Reusable modules
│   ├── vpc/
│   ├── eks/
│   └── rds/
├── environments/
│   ├── dev/
│   │   └── main.tf
│   ├── staging/
│   └── prod/
├── backend.tf                  # State configuration
├── providers.tf                # Provider versions
└── versions.tf                 # Terraform version
```

## Architecture Rules

- **Module granularity.** One module per logical component: VPC, cluster, database. Reusable across envs.
- **State isolation.** Separate state per environment. `dev/terraform.tfstate` ≠ `prod/terraform.tfstate`.
- **Variable validation.** Use `validation` blocks in variables. Fail fast on invalid inputs.
- **Remote state.** Use S3/GCS with locking (DynamoDB/Cloud Storage). Never local state in team settings.
- **Immutable infrastructure.** Replace rather than modify. `terraform taint` or `create_before_destroy`.

## Coding Conventions

- **Resource addressing.** Reference with `module.vpc.private_subnets[0]`. Explicit dependencies.
- **Dynamic blocks.** Use for conditional nested blocks. `dynamic "ingress" { for_each = var.ingress_rules }`.
- **Locals.** Compute derived values in `locals`. Keep variables simple. Use locals for transformation.
- **Data sources.** Query existing resources with `data`. Don't manage what you don't own.
- **Workspaces.** Use for environment separation only. `terraform workspace select prod`.

## NEVER DO THIS

1. **Never modify state manually.** `terraform state rm` and `import` are safe. Editing JSON is dangerous.
2. **Never use `-auto-approve` in production.** Review plan output. Approve only after review.
3. **Never hardcode credentials.** Use `~/.aws/credentials`, env vars, or IAM roles. Never in `.tf` files.
4. **Never ignore `terraform plan` drift.** Drift indicates manual changes or bugs. Reconcile immediately.
5. **Never skip backend locking.** Concurrent applies corrupt state. Use DynamoDB or native locking.
6. **Never use `count` for conditional.** Use `for_each` with map, or `count = var.enabled ? 1 : 0` carefully.
7. **Never forget about `terraform destroy` testing.** Regularly test destruction. Catches dependency issues.

## Testing

- **Plan testing.** Run `terraform plan -detailed-exitcode` in CI. Non-zero on changes = drift detected.
- **Validate testing.** `terraform validate` catches syntax errors. Fast feedback loop.
- **Lint testing.** Use `tflint` for best practices. Enforce naming conventions, unused vars.
- **Security testing.** Use `tfsec` or `checkov`. Static analysis for security misconfigurations.
- **Cost testing.** Use `infracost`. Break build if cost increases > threshold.

## Claude Code Integration

- Use `@modules/` for reusable Terraform module patterns
- Reference `@environments/` for environment-specific configurations
- Apply IaC best practices from architecture rules
- Validate against Terraform security in NEVER DO THIS

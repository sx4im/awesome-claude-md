# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Ansible 2.15+ (ansible-core) with Python 3.10+
- Jinja2 templating for configuration files
- Ansible Galaxy collections for cloud and service modules
- Molecule for role testing
- ansible-vault for secrets encryption
- [Dynamic inventory from AWS/GCP/Azure or static inventory]

## Project Structure

```
[PROJECT_ROOT]/
├── inventories/
│   ├── dev/
│   │   ├── hosts.yml                 # Dev inventory (static or plugin)
│   │   └── group_vars/
│   │       ├── all.yml               # Variables for all dev hosts
│   │       └── webservers.yml        # Variables for dev webservers
│   ├── staging/                      # Same structure as dev
│   └── prod/                         # Same structure, vault.yml for secrets
├── roles/
│   ├── common/                       # Base OS configuration
│   │   ├── tasks/main.yml
│   │   ├── handlers/main.yml
│   │   ├── templates/               # Jinja2 templates
│   │   ├── files/                   # Static files
│   │   ├── vars/main.yml            # Role-internal variables
│   │   ├── defaults/main.yml        # Overridable default values
│   │   └── meta/main.yml            # Role metadata and dependencies
│   ├── nginx/
│   ├── postgresql/
│   └── app_deploy/
├── playbooks/
│   ├── site.yml                     # Master playbook (imports all)
│   ├── webservers.yml               # Web tier playbook
│   ├── databases.yml                # Database tier playbook
│   └── deploy.yml                   # Application deployment
├── collections/
│   └── requirements.yml             # Galaxy collection dependencies
├── ansible.cfg                      # Project-level Ansible configuration
├── Makefile                         # Shortcut commands
└── molecule/                        # Integration test scenarios
```

## Architecture Rules

- **Roles for configuration, playbooks for orchestration.** Roles encapsulate the "how" (install nginx, configure PostgreSQL). Playbooks define the "what and where" (apply nginx role to webservers group). Never put 200 tasks in a playbook file. If a playbook has more than 10 direct tasks, extract a role.
- **Variables cascade predictably.** `defaults/main.yml` (lowest) -> `group_vars/all.yml` -> `group_vars/group.yml` -> `host_vars/host.yml` -> playbook vars -> extra vars (highest). Put sane defaults in `defaults/main.yml`. Override per-environment in `group_vars`. Never set the same variable in 4 places.
- **Idempotency is non-negotiable.** Every task must be safe to run repeatedly. Running the playbook twice produces zero changes on the second run. If a task shows "changed" on every run, it is broken. Use `creates:`, `when:`, and proper module arguments to ensure idempotency.
- **Handlers for service restarts.** Configuration changes notify handlers: `notify: restart nginx`. Handlers run once at the end, even if notified multiple times. Never put `service: name=nginx state=restarted` as a regular task — it restarts nginx on every run regardless of whether config changed.
- **Inventory per environment, no branching logic.** Don't use `when: env == "prod"` in tasks. Instead, set different variable values in `inventories/prod/group_vars/` vs `inventories/dev/group_vars/`. The same role code runs everywhere; only the data changes.

## Coding Conventions

- **YAML formatting.** Use 2-space indentation. Use `true`/`false` for booleans, never `yes`/`no` (YAML spec allows both, but `yes` is ambiguous and easily confused with string values). Quote strings that could be misinterpreted: `version: "1.10"` (not `1.10` which YAML parses as float `1.1`).
- **Task naming.** Every task has a `name:` that describes the desired state, not the action: `name: Ensure nginx is installed` not `name: Install nginx`. Names appear in output and should read as assertions.
- **Fully qualified collection names (FQCN).** Use `ansible.builtin.copy:` not `copy:`. Use `community.general.ufw:` not `ufw:`. FQCN prevents ambiguity when multiple collections provide modules with the same short name. Required since Ansible 2.10+.
- **No bare variables in `when:`.** Write `when: enable_ssl | bool` not `when: enable_ssl`. A string `"false"` is truthy. The `| bool` filter handles string-to-boolean conversion correctly.
- **Tags for selective execution.** Tag every role invocation and significant task blocks: `tags: [nginx, webserver]`. Run subsets with `--tags nginx`. Never have untagged tasks that only run during full playbook execution — they become invisible.

## Library Preferences

- **Collections:** `ansible.builtin` for core modules. `community.general` for extras. Cloud-specific: `amazon.aws`, `google.cloud`, `azure.azcollection`. Pin versions in `requirements.yml`.
- **Secret management:** `ansible-vault` for encrypting variable files. Not plaintext passwords in `group_vars`. Not external vault lookup plugins unless integrating with HashiCorp Vault or AWS Secrets Manager.
- **Template engine:** Jinja2 with `trim_blocks` and `lstrip_blocks` enabled in `ansible.cfg`. Produces clean config files.
- **Testing:** Molecule with Docker driver for role testing. Not manual SSH testing against staging.
- **Linting:** `ansible-lint` in CI. Catches deprecated syntax, missing names, bare variables, and FQCN violations.

## File Naming

- Playbooks: `purpose.yml` (e.g., `site.yml`, `deploy.yml`, `webservers.yml`)
- Roles: `snake_case` directory names matching the service or function (e.g., `nginx`, `app_deploy`, `common`)
- Templates: `filename.conf.j2` matching the target filename with `.j2` suffix
- Variable files: `all.yml`, `group_name.yml` matching inventory group names
- Vault files: `vault.yml` inside `group_vars/group_name/` directory (separate from unencrypted vars)

## NEVER DO THIS

1. **Never use `shell:` or `command:` when a module exists.** `shell: apt-get install nginx` is not idempotent and ignores Ansible's change tracking. Use `ansible.builtin.apt: name=nginx state=present`. Modules handle idempotency, error reporting, and platform differences. Use `shell:` only when no module exists, and always add `changed_when:` and `creates:` or `removes:`.
2. **Never commit unencrypted secrets.** Passwords, API keys, and certificates in plaintext `group_vars` files end up in git history forever. Use `ansible-vault encrypt_string` for individual values or encrypt entire files with `ansible-vault encrypt`.
3. **Never use `ignore_errors: true` as a crutch.** It silently swallows failures and makes playbooks unreliable. If a task can legitimately fail, use `failed_when:` with a specific condition or `rescue:` blocks. `ignore_errors` means "I don't care if this breaks," which is never true in production.
4. **Never hardcode IPs in playbooks or roles.** IPs belong in inventory. Roles reference group names and variables. A role that contains `192.168.1.50` is useless in any other environment.
5. **Never run playbooks without `--diff --check` first in production.** Check mode simulates the run without making changes. Diff mode shows what would change. Skipping this is deploying blind. Make it a habit: `ansible-playbook site.yml -i inventories/prod --diff --check` before every `--limit` or full run.
6. **Never use `lineinfile` for complex config files.** It manages a single line and is fragile if the file format changes. Use `ansible.builtin.template` with a full Jinja2 template. Templates are version-controlled, diffable, and handle the complete file structure.
7. **Never set `become: true` at the playbook level.** Set `become:` on the specific tasks or roles that need root. Running the entire playbook as root when only 3 tasks out of 40 need privilege escalation violates least privilege and masks permission issues.

## Testing

- Use Molecule to test roles in isolated Docker containers. Each role has a `molecule/default/` scenario with a `converge.yml` playbook and `verify.yml` assertions.
- Molecule test lifecycle: `create` (spin up container) -> `converge` (run role) -> `idempotence` (run again, assert zero changes) -> `verify` (assert desired state) -> `destroy`.
- Use `ansible-lint` in CI as a required check. It enforces FQCN, task naming, proper module usage, and dozens of best practices. Fix violations, never add `# noqa` without a documented reason.
- Test Jinja2 templates by rendering with `ansible.builtin.debug: msg="{{ lookup('template', 'nginx.conf.j2') }}"` and validating output.
- Run playbooks against a staging inventory before production. Staging must mirror production's OS, packages, and network topology.

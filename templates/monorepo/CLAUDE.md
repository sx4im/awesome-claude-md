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

## Production Delivery Playbook (Category: Monorepo & Package Management)

### Release Discipline
- Keep workspace dependency graph stable and deterministic.
- Prevent cross-package breaking changes without coordinated versioning.
- Optimize for incremental builds/tests and cache correctness.

### Merge/Release Gates
- Workspace install, build, and test orchestration pass end-to-end.
- Changed packages and dependents validated via affected graph checks.
- Version/publish strategy verified for modified packages.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Turborepo for build orchestration
- pnpm workspaces for package management
- TypeScript 5.x (strict mode across all packages)
- Shared packages under `packages/`
- Applications under `apps/`

## Project Structure

```
.
├── apps/
│   ├── web/               # Next.js web application
│   ├── api/               # Express/Fastify API server
│   └── docs/              # Documentation site (Nextra, Astro, etc.)
├── packages/
│   ├── ui/                # @repo/ui: shared React component library
│   ├── utils/             # @repo/utils: shared utility functions
│   ├── types/             # @repo/types: shared TypeScript types
│   ├── config/            # @repo/config: shared ESLint, Prettier, TS configs
│   └── db/                # @repo/db: Prisma client and schema (if shared)
├── turbo.json             # Pipeline configuration
├── pnpm-workspace.yaml    # Workspace definition
├── package.json           # Root package.json (scripts, devDeps only)
└── tsconfig.json          # Base TS config (extended by all packages)
```

## Architecture Rules

- **Apps consume packages. Packages never import from apps.** Dependency flow is always: `apps/ → packages/`. If two apps need the same code, it belongs in a package.
- **Every shared package uses the `@repo/` scope.** Name packages `@repo/ui`, `@repo/utils`, `@repo/types`. Never use unscoped names or a different scope.
- **One concern per package.** `@repo/ui` contains React components. `@repo/utils` contains framework-agnostic utilities. Don't dump everything into a single `@repo/shared` package.
- **TypeScript configs inherit from root.** The root `tsconfig.json` defines base `compilerOptions`. Each package's `tsconfig.json` uses `"extends": "../../tsconfig.json"` and only overrides what's specific to that package.
- **Turborepo manages all builds.** Never run `tsc` or `next build` directly in an app. always use `turbo run build`. This ensures the dependency graph is respected and caching works.

## Package Decision Tree

When adding new code, follow this logic:

1. **Used in only one app?** → Put it in that app's directory. Do not create a package.
2. **Used in two or more apps?** → Create a shared package under `packages/`.
3. **Is it a React component?** → `@repo/ui`
4. **Is it a utility function with no React dependency?** → `@repo/utils`
5. **Is it a TypeScript type or interface?** → `@repo/types`
6. **Is it configuration (ESLint, Prettier, tsconfig)?** → `@repo/config`
7. **Is it database-related (Prisma schema, client)?** → `@repo/db`

## Coding Conventions

- **Root `package.json` has no runtime dependencies.** Only `devDependencies` (Turborepo, TypeScript, linters). Runtime deps live in the specific app or package that needs them.
- **Unified TypeScript version.** All packages use the same TypeScript version, installed at the root. Individual packages do not pin their own version.
- **Import from package names, not relative paths.** Inside `apps/web`, import `{ Button } from '@repo/ui'`. never `from '../../packages/ui/src/Button'`.
- **Every package has its own `package.json`.** Define `name`, `main`, `types`, `scripts`, and `dependencies`. Use `"main": "./src/index.ts"` for internal packages that don't need a separate build step.
- **Use `internal` flag for packages that shouldn't be published.** Set `"private": true` in `package.json` for all packages that are only used within the monorepo.

## turbo.json Conventions

```jsonc
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],      // Build deps first
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,               // Never cache dev servers
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"]       // Lint after deps build (for types)
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
```

- `dependsOn: ["^build"]` means "build my dependencies before running this task." Always use this for `build`, `lint`, and `test`.
- Never cache `dev` tasks. Set `"cache": false` and `"persistent": true`.
- Outputs must list every directory the task writes to. Missing an output directory breaks remote caching.

## File Naming

- Packages: `packages/{name}/` → `packages/ui/`, `packages/utils/`
- Package names: `@repo/{name}` → `@repo/ui`, `@repo/types`
- Apps: `apps/{name}/` → `apps/web/`, `apps/api/`
- Configs: descriptive names → `eslint.config.js`, `tsconfig.json`
- All source: follow the conventions of the specific framework (Next.js, Express, etc.)

## NEVER DO THIS

1. **Never import between apps directly.** `apps/web` must never import from `apps/api`. If they need shared code, extract it to a `packages/` package.
2. **Never put secrets in `turbo.json`.** Environment variables referenced in `turbo.json`'s `env` or `globalEnv` are used for cache key hashing, not for storing values. Actual secrets go in `.env` files (gitignored).
3. **Never duplicate types across packages.** If `apps/web` and `apps/api` both need a `User` type, it goes in `@repo/types`. Type duplication causes drift and bugs.
4. **Never run builds without Turborepo.** Direct `npm run build` inside an app skips dependency building and cache. Always use `turbo run build --filter=apps/web` if you want to target a specific app.
5. **Never install the same dependency at different versions.** Use `pnpm dedupe` to check. Two versions of React in a monorepo causes "hooks called in wrong order" errors. Pin exact versions in the root `pnpm-workspace.yaml` catalog or use `pnpm.overrides`.
6. **Never create circular dependencies between packages.** If `@repo/ui` imports from `@repo/utils` AND `@repo/utils` imports from `@repo/ui`, extract the shared code into a third package. Run `turbo run build` to catch cycles. it will error.
7. **Never skip `turbo.json` output declarations.** Every `build` task must declare its `outputs`. Without them, Turborepo's cache replays don't restore build artifacts, and CI will have mysterious failures.

## Testing

- Each package has its own test setup. Run all tests via `turbo run test`.
- Use Vitest for all TypeScript packages. Configure in each package's `vitest.config.ts`.
- Shared test utilities go in a `@repo/test-utils` package if needed.
- CI runs `turbo run lint test build` in that order. lint catches issues fast, tests verify logic, build confirms production output.

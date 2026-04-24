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

## Production Delivery Playbook (Category: Frontend)

### Release Discipline
- Enforce performance budgets (bundle size, LCP, CLS) before merge.
- Preserve accessibility baselines (semantic HTML, keyboard nav, ARIA correctness).
- Block hydration/runtime errors with production build verification.

### Merge/Release Gates
- Typecheck + lint + unit tests + production build pass.
- Critical route smoke tests for navigation, auth, and error boundaries.
- No new console errors/warnings in key user flows.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Svelte 5 with runes reactivity ($state, $derived, $effect)
- SvelteKit 2 with Vite 5
- TypeScript 5.4+ in strict mode
- Tailwind CSS 4 with @tailwindcss/vite plugin
- Superforms + Zod for form handling and validation
- Drizzle ORM with PostgreSQL for persistence
- Lucia Auth v3 for authentication
- Paraglide JS for i18n

## Project Structure

```
src/
  lib/
    components/    # Reusable Svelte 5 components
    server/        # Server-only modules (db, auth)
    stores/        # Shared $state runes wrapped in modules
    utils/         # Pure utility functions
    types/         # TypeScript type definitions
  routes/
    (app)/         # Authenticated route group
    (auth)/        # Login/register route group
    api/           # API route handlers (+server.ts)
  params/          # SvelteKit param matchers
  hooks.server.ts  # Server hooks (auth, logging)
  hooks.client.ts  # Client hooks (error tracking)
static/            # Static assets served at root
tests/             # Playwright e2e tests
drizzle/           # Database migrations
```

## Architecture Rules

- Use runes exclusively. Never use legacy `let` reactivity, `$:` reactive statements, or Svelte stores from `svelte/store`.
- Declare component state with `$state()`. Use `$derived()` for computed values. Reserve `$effect()` for DOM side effects and cleanup only.
- All data loading happens in `+page.server.ts` or `+layout.server.ts` load functions. Components never fetch data directly.
- Form mutations use SvelteKit form actions in `+page.server.ts` with Superforms for progressive enhancement.
- Server-only code lives in `$lib/server/` and imports are enforced by SvelteKit's server-only module boundary.
- Use snippet blocks (`{#snippet}`) instead of slots for component composition.
- Shared reactive state across components uses module-level `$state` in `$lib/stores/`.

## Coding Conventions

- Components use PascalCase filenames: `UserProfile.svelte`, `DataTable.svelte`.
- Props are declared with `let { prop1, prop2 }: Props = $props()` destructuring pattern.
- Event handlers use the `onclick` attribute syntax, not `on:click` directive.
- CSS scoping is handled by Svelte component styles. Use Tailwind utility classes for layout, custom `<style>` blocks for complex animations.
- Type all component props with an exported `Props` interface in the `<script>` block.
- Prefer `{#each items as item (item.id)}` with keyed blocks for lists.
- Use `$effect()` with explicit return for cleanup functions. Never use `$effect()` for state derivation.

## Library Preferences

- Forms: @superforms/sveltekit with Zod schemas (never hand-roll form validation)
- Tables: @tanstack/svelte-table for complex data grids
- Toasts: svelte-sonner for notifications
- Icons: unplugin-icons with Iconify collections
- Date handling: date-fns (never moment.js)
- HTTP client: built-in SvelteKit fetch (never axios)
- Animation: svelte/transition and svelte/animate built-ins

## File Naming

- Components: `PascalCase.svelte`
- Routes: SvelteKit conventions (`+page.svelte`, `+page.server.ts`, `+layout.svelte`)
- Utilities: `camelCase.ts`
- Types: `camelCase.ts` with PascalCase exports
- Tests: `componentName.test.ts` for unit, `featureName.spec.ts` for e2e

## NEVER DO THIS

1. Never use `$:` reactive declarations or `svelte/store` writable/readable/derived. Use `$state`, `$derived`, and `$effect` runes instead.
2. Never fetch data inside `onMount` or `$effect`. Use SvelteKit load functions for all data fetching.
3. Never mutate `$derived()` values. They are read-only computed properties.
4. Never use `<slot>` elements. Use `{#snippet}` and `{@render}` for content projection in Svelte 5.
5. Never write `on:click` or `on:submit` directives. Use `onclick` and `onsubmit` attribute syntax.
6. Never import from `svelte/internal`. These are private APIs that break between versions.
7. Never disable TypeScript strict mode or use `@ts-ignore` without a linked issue explaining why.

## Testing

- Unit tests: Vitest with @testing-library/svelte for component testing.
- Run component tests with `pnpm test:unit` which executes `vitest run`.
- E2E tests: Playwright targeting Chrome and Firefox.
- Run e2e tests with `pnpm test:e2e` which executes `playwright test`.
- Test files live next to source files for unit tests, in `tests/` for e2e.
- Mock server dependencies using `vi.mock()` for `$lib/server/` imports.
- All form actions must have both happy-path and validation-error test cases.

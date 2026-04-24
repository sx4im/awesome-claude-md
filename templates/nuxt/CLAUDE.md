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

- Nuxt 3.x with Vue 3 (Composition API only)
- TypeScript (strict mode)
- Tailwind CSS 3.x or UnoCSS
- Pinia for state management
- Nitro server engine for API routes
- Auto-imported composables and components

## Project Structure

```
.
├── app.vue                  # Root component
├── pages/
│   ├── index.vue            # / route
│   ├── dashboard.vue        # /dashboard route
│   └── users/
│       └── [id].vue         # /users/:id dynamic route
├── components/
│   ├── ui/                  # Primitives auto-imported: UiButton, UiModal
│   └── features/            # Domain: FeatureUserCard, FeatureOrderList
├── composables/             # Auto-imported composables (useAuth, useFetch wrapper)
├── server/
│   ├── api/                 # API routes (auto-registered)
│   │   ├── users/
│   │   │   ├── index.get.ts # GET /api/users
│   │   │   └── index.post.ts# POST /api/users
│   │   └── auth/
│   ├── middleware/           # Server middleware (auth, logging)
│   └── utils/               # Server-only utilities (db, email)
├── stores/                  # Pinia stores
│   ├── auth.ts
│   └── ui.ts
├── types/                   # Shared TypeScript types
├── utils/                   # Auto-imported utility functions
└── nuxt.config.ts
```

## Architecture Rules

- **Composition API only.** Every component uses `<script setup lang="ts">`. Never use the Options API (`data()`, `methods`, `computed`). Never use the raw `setup()` function. `<script setup>` is the standard.
- **Auto-imports are the convention.** Nuxt auto-imports composables from `composables/`, utilities from `utils/`, and components from `components/`. Don't add manual `import` statements for auto-imported items. Do be explicit about third-party imports.
- **Server routes handle all backend logic.** API routes live in `server/api/` and are automatically registered by Nitro. Name files with HTTP method suffixes: `index.get.ts`, `index.post.ts`, `[id].put.ts`.
- **Pinia is the only state store.** One store per domain: `stores/auth.ts`, `stores/cart.ts`. Use the Setup Store syntax (function that returns reactive state). not the Options Store syntax.
- **`useFetch` and `useAsyncData` for all data loading.** These integrate with Nuxt's SSR hydration. Never use raw `$fetch` in component setup. it runs on both server and client, causing double requests.

## Coding Conventions

- **Components:** `<script setup lang="ts">` first, then `<template>`, then `<style scoped>`. Always include `lang="ts"`.
- **Props:** `defineProps<{ title: string; count?: number }>()`. Never use the runtime declaration (`defineProps({ title: String })`).
- **Emits:** `defineEmits<{ (e: 'update', value: string): void }>()`. Always type them.
- **Composable naming:** always `use` prefix. `useAuth()`, `useProducts()`, `useMediaQuery()`. Return objects, not arrays.
- **Computed over watchers.** If value B depends on value A, use `computed()`. Use `watch()` only for side effects (API calls, logging, DOM mutations). Never use `watch` to set another ref. that's what `computed` is for.

## Library Preferences

- **State:** Pinia. not Vuex (Pinia is the official recommendation, Vuex is legacy). Use Setup Stores (composable-style) over Options Stores.
- **Styling:** Tailwind CSS or UnoCSS (UnoCSS if you want faster builds and `@apply`-free workflow). Not Vuetify for custom apps (too opinionated, hard to customize deeply).
- **Validation:** Zod for both client and server validation. Use `zod` in server routes to validate request bodies. Use VeeValidate + Zod on the client for form validation.
- **Date/time:** `date-fns`. not `moment` (deprecated, not tree-shakeable).
- **HTTP (server-side):** `$fetch` from Nitro's `ofetch`. not `axios`. `$fetch` is already available everywhere in Nuxt.

## File Naming

- Pages: `kebab-case.vue` → `user-profile.vue`, `order-details.vue`
- Components: `PascalCase.vue` → subdirectory prefix auto-applied: `ui/Button.vue` → `<UiButton />`
- Composables: `useCamelCase.ts` → `useAuth.ts`, `useProducts.ts`
- Server routes: `method.ts` suffix → `index.get.ts`, `[id].delete.ts`
- Stores: `camelCase.ts` → `auth.ts`, `cart.ts`
- Middleware: `camelCase.ts` → `auth.ts` (in `middleware/` for route middleware, `server/middleware/` for server)

## NEVER DO THIS

1. **Never use the Options API.** No `data()`, `methods`, `computed`, `watch` objects. Composition API with `<script setup>` is the only pattern in this project.
2. **Never use `ref()` when `reactive()` is cleaner for objects.** But also never use `reactive()` for primitives. use `ref()`. Rule: primitives → `ref()`, complex objects you destructure → `ref()`, objects you pass whole → `reactive()`.
3. **Never use raw `$fetch` in `<script setup>`.** Use `useFetch()` or `useAsyncData()`. they prevent double-fetching during SSR hydration. Raw `$fetch` is for event handlers and server routes only.
4. **Never use `watch` to derive state.** `watch(a, () => { b.value = a.value * 2 })` should be `const b = computed(() => a.value * 2)`. Watchers are for side effects, not state derivation.
5. **Never register components manually when auto-import works.** Components in `components/` are auto-imported. Adding manual `import` statements clutters the code and conflicts with Nuxt's resolution.
6. **Never put database connections in `composables/`.** Database clients, API secrets, and server-only logic go in `server/utils/`. Composables run on both client and server. server secrets would leak to the browser.
7. **Never skip TypeScript in `<script setup>`.** Always use `lang="ts"`. Never use `any` for props, emits, or composable return types. The Nuxt type system is excellent. use it.

## Testing

- Use Vitest for unit tests. Test composables, utilities, and Pinia stores.
- Use `@nuxt/test-utils` for component and integration tests with Nuxt context.
- Use Playwright for E2E tests.
- Test server routes by calling them with `$fetch` from `@nuxt/test-utils`. they're just H3 event handlers.
- Test Pinia stores by creating a test Pinia instance with `createTestingPinia()`.

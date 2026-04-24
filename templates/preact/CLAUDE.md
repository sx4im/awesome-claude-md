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

- Preact 10.x with TypeScript (strict mode)
- Preact Signals for reactive state management
- Vite 5.x as build tool and dev server
- preact-router or wouter for routing
- CSS Modules or Tailwind CSS 3.x
- Target bundle size: < [30]kb gzipped total

## Project Structure

```
src/
├── components/
│   ├── ui/               # Primitives: Button, Input, Modal
│   └── features/         # Domain components: UserCard, OrderList
├── signals/               # Shared signal definitions and computed state
│   ├── auth.ts            # Auth state signals
│   └── ui.ts              # UI state signals (sidebar, theme)
├── hooks/                 # Custom hooks (useClickOutside, useMediaQuery)
├── pages/                 # Route-level components, one per route
├── services/              # API call functions (typed fetch wrappers)
├── types/                 # Shared TypeScript interfaces
├── utils/                 # Pure utility functions
└── main.tsx               # App entry point: router and providers
```

## Architecture Rules

- **Preact is not React.** It is a 3kb alternative with the same API surface but different internals. Do not import from `react`. Import from `preact`, `preact/hooks`, and `preact/compat` only when a third-party library demands React compatibility.
- **Signals are the primary state model.** Use `@preact/signals` for all shared and component-local state. Signals provide fine-grained reactivity without re-rendering the component tree. A signal update only re-renders the exact DOM node that reads it.
- **Bundle size is a feature.** Every dependency is a cost decision. Before adding a library, check its bundle size on bundlephobia. If a library adds more than 5kb gzipped, justify it explicitly or find a lighter alternative.
- **No React compatibility layer unless required.** `preact/compat` adds ~2kb and exists only for third-party React libraries that reference `react` internals. If you control the code, import from `preact` directly.
- **Services encapsulate all network calls.** Components and signals never call `fetch` directly. Services return typed data and handle errors consistently.

## Coding Conventions

- Components use the `function` keyword: `export function UserCard()`. Not `const UserCard = () => {}`. Arrow functions are for inline callbacks and signal computations.
- Import from `preact` and `preact/hooks`, never from `react`. JSX pragma is `h` from `preact`, configured in `tsconfig.json` with `"jsxImportSource": "preact"`.
- Signals in components: use `signal()` for local state, import shared signals from `signals/`. Access signal values with `.value` in logic and directly in JSX (Preact auto-subscribes).
- Computed values use `computed()` from `@preact/signals`: `const fullName = computed(() => firstName.value + ' ' + lastName.value)`. Not `useMemo`.
- Side effects on signal changes use `effect()` from `@preact/signals`. Not `useEffect` with signal values in deps arrays. `effect()` auto-tracks signal dependencies.
- Explicit return types on all exported functions. Internal helpers can rely on inference.
- Use the `@/` path alias mapped to `src/`. Never use `../../../` chains.

## Library Preferences

- **State management:** `@preact/signals`. Not Redux, not Zustand, not Jotai. Signals are built for Preact's rendering model and provide surgical DOM updates without VDOM diffing overhead.
- **Routing:** `preact-router` for simple SPAs, `wouter` for a lighter option. Not `react-router` (too heavy, requires `preact/compat`).
- **Styling:** CSS Modules for scoped styles with zero runtime cost. Or Tailwind CSS if the project already uses it. Not styled-components or Emotion (runtime CSS-in-JS defeats the purpose of choosing Preact for size).
- **Forms:** Signals-based form state. Bind inputs directly to signals: `<input value={name} onInput={(e) => name.value = e.currentTarget.value} />`. Not `react-hook-form` (React dependency, compat overhead).
- **HTTP client:** Plain `fetch` with a typed wrapper in services. Not `axios` (too large for a Preact project).
- **Dates:** `dayjs` (2kb) or vanilla `Intl.DateTimeFormat`. Not `date-fns` (tree-shaking helps but it's still heavier than necessary).

## File Naming

- Components: `PascalCase.tsx` → `UserCard.tsx`, `OrderList.tsx`
- Signals: `camelCase.ts` → `auth.ts`, `ui.ts`, `cart.ts`
- Hooks: `useCamelCase.ts` → `useClickOutside.ts`, `useMediaQuery.ts`
- Pages: `PascalCase.tsx` → `HomePage.tsx`, `Settings.tsx`
- Services: `camelCase.ts` → `users.ts`, `orders.ts`
- Utils: `camelCase.ts` → `formatDate.ts`, `cn.ts`
- Test files: co-located as `ComponentName.test.tsx`

## NEVER DO THIS

1. **Never import from `react`.** Import from `preact`, `preact/hooks`, or `preact/compat`. Writing `import { useState } from 'react'` will either fail or silently bundle React alongside Preact, doubling your framework size.
2. **Never use `useState`/`useEffect` when signals work.** `useState` triggers full component re-renders. `signal()` updates only the DOM nodes that read the signal. For shared state, signals avoid prop drilling entirely. Reserve hooks for third-party library interop.
3. **Never use `React.memo` or `shouldComponentUpdate`.** Preact's VDOM diffing is already fast, and signals bypass it entirely. Manual memoization adds complexity with no measurable benefit in a Preact app.
4. **Never add runtime CSS-in-JS.** styled-components, Emotion, and similar libraries add 8-15kb of runtime JavaScript. That can exceed Preact itself. Use CSS Modules or Tailwind for zero-runtime styling.
5. **Never access signal values with `.value` in JSX.** In JSX, pass the signal directly: `<span>{count}</span>`, not `<span>{count.value}</span>`. Preact auto-subscribes to signals in JSX. Using `.value` breaks fine-grained updates and causes full component re-renders.
6. **Never add dependencies without checking bundle size.** Run `npx bundlephobia [package]` before `npm install`. A 50kb charting library in a Preact app is a red flag. Find a lighter alternative or lazy-load it.
7. **Never use `preact/compat` for code you control.** `preact/compat` is a shim for third-party React libraries. Your own components should import from `preact` directly. The compat layer adds overhead and masks Preact-specific APIs like signals.

## Testing

- Use Vitest + Preact Testing Library (`@testing-library/preact`). Not React Testing Library.
- Test signal-driven components by updating signals directly in tests and asserting DOM changes. No need to simulate user events for pure signal state.
- Mock services at the module level with `vi.mock('./services/users')`.
- For integration tests, use `@preact/signals` `batch()` to group signal updates and assert final DOM state.
- Bundle size tests: assert total bundle size in CI with `bundlesize` or Vite's `rollup-plugin-visualizer`. Regressions in bundle size are test failures.

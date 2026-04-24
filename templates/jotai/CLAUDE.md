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

- Jotai v2 (atomic state management)
- React 18+
- TypeScript 5.x
- Immer (optional)
- jotai/utils for advanced patterns

## Project Structure

```
src/
├── atoms/
│   ├── index.ts                # Atom exports
│   ├── auth.ts                 # Auth-related atoms
│   ├── ui.ts                   # UI state atoms
│   └── derived.ts              // Computed/derived atoms
├── hooks/
│   └── useAtoms.ts             # Custom atom hooks
└── lib/
    └── atom-utils.ts           // Atom utilities
```

## Architecture Rules

- **Atoms are minimal state units.** Create small, focused atoms: `countAtom`, `userAtom`, `themeAtom`.
- **Derived atoms for computed state.** Use `atom((get) => ...)` for values computed from other atoms.
- **Writeable derived atoms for actions.** Use `atom(null, (get, set, update) => ...)` for action atoms.
- **Family atoms for collections.** `atomFamily` for creating atoms per entity (e.g., per todo item).

## Coding Conventions

- Define atoms: `const countAtom = atom(0)` for primitive state.
- Derived atoms: `const doubledAtom = atom((get) => get(countAtom) * 2)`.
- Use atoms: `const [count, setCount] = useAtom(countAtom)` or `const count = useAtomValue(countAtom)`.
- Async atoms: `const userAtom = atom(async (get) => fetchUser(get(userIdAtom)))`.
- Resettable atoms: `const countAtom = atomWithReset(0)` + `useResetAtom(countAtom)`.

## Library Preferences

- **Utils:** `jotai/utils` for `atomWithStorage`, `atomWithReset`, `selectAtom`.
- **Immer:** `jotai/immer` for mutable updates in atoms.
- **Query:** `jotai-tanstack-query` for integrating with TanStack Query.
- **DevTools:** Jotai DevTools for debugging atom dependencies.

## File Naming

- Atom files: `[domain].ts` → `auth.ts`, `ui.ts`
- Barrel export: `atoms/index.ts`

## NEVER DO THIS

1. **Never create atoms inside components.** Atoms are static definitions. Define them at module level.
2. **Never use `useAtom` when `useAtomValue` suffices.** `useAtom` subscribes and provides setter. If you only read, use `useAtomValue`.
3. **Never ignore atom dependencies.** Jotai tracks dependencies automatically in derived atoms. Don't manually recreate this.
4. **Never create giant atoms.** Split state into focused atoms. `appStateAtom` with everything is an anti-pattern.
5. **Never forget async atom loading states.** Async atoms return Promises. Handle `Suspense` or use `useAtomValue` carefully.
6. **Never use Jotai for server state.** Use TanStack Query for API data. Jotai is for client state.
7. **Never mutate atom values directly.** `const [count] = useAtom(countAtom); count++` doesn't work. Use the setter.

## Testing

- Test atoms in isolation. They're pure functions.
- Use `Provider` from `jotai` to scope atoms in tests.
- Test derived atoms by setting dependencies and checking outputs.
- Test async atoms by awaiting in tests.

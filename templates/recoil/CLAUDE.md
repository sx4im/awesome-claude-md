# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Recoil (Facebook's state management)
- React 18+
- TypeScript 5.x
- React 18+ Concurrent Features (experimental integration)

## Project Structure

```
src/
├── atoms/
│   ├── index.ts                // Atom exports
│   ├── auth.ts                 // Auth atoms
│   └── ui.ts                   // UI atoms
├── selectors/
│   ├── index.ts                // Selector exports
│   └── derived.ts              // Computed values
├── hooks/
│   └── useRecoil.ts            // Custom Recoil hooks
└── lib/
    └── recoil-effects.ts       // Atom effects
```

## Architecture Rules

- **Atoms are units of state.** Create small, focused atoms: `textState`, `currentUserState`.
- **Selectors for derived state.** Pure functions that compute from atoms or other selectors.
- **Atom effects for side effects.** Persistence, logging, or synchronization using `effects_UNSTABLE`.
- **Family atoms for dynamic state.** `atomFamily` for parameterized state (per-item selection).

## Coding Conventions

- Create atom: `const textState = atom({ key: 'textState', default: '' })`.
- Create selector: `const charCountState = selector({ key: 'charCountState', get: ({get}) => get(textState).length })`.
- Use hooks: `const [text, setText] = useRecoilState(textState)`.
- Read-only: `const count = useRecoilValue(charCountState)`.
- Setter only: `const setText = useSetRecoilState(textState)`.

## Library Preferences

- **Recoil DevTools:** Use Recoilize or similar for debugging.
- **Persistence:** Atom effects for localStorage sync.
- **Async queries:** Use selectors or `useRecoilValueLoadable` with Suspense.
- **URL sync:** Custom effects for query parameter synchronization.

## File Naming

- Atom files: `[domain].ts` → `auth.ts`, `settings.ts`
- Selector files: `[purpose].ts` or co-located with atoms.
- Effects file: `effects.ts` or `recoil-effects.ts`.

## NEVER DO THIS

1. **Never duplicate atom keys.** Keys must be globally unique. Collisions cause silent failures.
2. **Never create atoms inside components.** Define at module level like hooks.
3. **Never ignore `key` prop requirements.** Every atom and selector needs a unique string key.
4. **Never use Recoil for server state.** Selectors can fetch, but TanStack Query is better for caching.
5. **Never forget to wrap with `RecoilRoot`.** All Recoil usage requires this provider at the root.
6. **Never ignore circular dependencies.** Selectors depending on each other in cycles cause infinite loops.
7. **Never use Recoil in production without considering alternatives.** Meta doesn't heavily invest in Recoil. Consider Jotai or Zustand for new projects.

## Testing

- Wrap tests with `RecoilRoot`. Provide `initializeState` for initial values.
- Test selectors by checking computed values with mock atoms.
- Test effects by verifying side effects (localStorage, etc.).
- Use `act()` for state updates in tests.


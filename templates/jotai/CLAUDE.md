# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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


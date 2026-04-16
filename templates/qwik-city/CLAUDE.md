# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Qwik City (Qwik meta-framework)
- Qwik 1.5+
- Resumability over hydration
- File-based routing
- Server$ functions

## Project Structure
```
src/
├── routes/
│   ├── index.tsx               // Route component
│   ├── layout.tsx              // Root layout
│   └── api/
│       └── hello/index.ts      // API endpoint
├── components/
│   └── Counter.tsx
└── entry.ssr.tsx
```

## Architecture Rules

- **Resumability.** App resumes from where server left off—no hydration.
- **$ suffix for lazy loading.** `component$`, `useSignal$`, `server$`.
- **Server$ for server code.** Automatically server-side only.
- **Optimistic UI.** `routeAction$` for form submissions.

## Coding Conventions

- Component: `export default component$(() => { const count = useSignal(0); return <button onClick$={() => count.value++}>{count.value}</button> })`.
- Layout: `export default component$(() => { return <Slot /> })` with `<Slot />` for children.
- Server: `export const useGetData = routeLoader$(async () => { return await db.get() })`.
- Action: `export const useAddUser = routeAction$(async (data) => { await db.add(data) })`.

## NEVER DO THIS

1. **Never forget $ suffix.** Required for Qwik optimizer to work.
2. **Never capture state in closures directly.** Use `useSignal`, `useStore`.
3. **Never use `useEffect` pattern.** Qwik has `useVisibleTask$`, `useTask$`.
4. **Never ignore the `Slot` component.** For layout composition.
5. **Never mix client-only code without $.** Must be explicit.
6. **Never skip the `entry.ssr.tsx` setup.** Required entry point.
7. **Never forget about `useClientEffect$`.** For browser-only code.

## Testing

- Test with `@builder.io/qwik-testing`.
- Test resumability (no hydration errors).
- Test server functions execute server-side.


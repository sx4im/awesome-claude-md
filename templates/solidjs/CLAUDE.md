# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- SolidJS (or SolidStart for SSR/Full-stack)
- TypeScript (strict mode)
- Vite (or Nitro with SolidStart)
- Tailwind CSS
- TanStack Query (or Solid's native resources)

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Button.tsx
│   └── Modal.tsx
├── features/            # Feature-scoped logic and components
│   ├── auth/
│   │   ├── AuthForm.tsx
│   │   └── auth.store.ts # Global state (createSignal/createStore)
│   └── dashboard/
├── hooks/               # Custom composable utilities
│   └── useClickOutside.ts
├── routes/              # File-based routing (SolidStart or Solid Router)
│   ├── index.tsx        # Homepage
│   ├── login.tsx
│   └── api/             # API endpoints (SolidStart)
│       └── auth.ts
├── lib/                 # Shared utilities, API clients
│   └── api.ts
├── global.css           # Tailwind styles
└── entry-client.tsx     # Browser entry point
```

## Architecture Rules

- **Components run ONCE.** Unlike React, Solid components are just setup functions for the reactive graph. They execute exactly once. Never put `console.log` in the body of a component expecting to see it on every update. It won't run.
- **Signals are the source of truth.** Use `createSignal()` for simple state and `createStore()` for deep objects. Pass getter functions (`count()`) not the raw values down the tree.
- **JSX compilation is fine-grained.** Solid compiles JSX directly into DOM updates. It does not use a Virtual DOM (VDOM). When a signal updates, only the specific DOM node bound to that signal updates.
- **SolidStart for SSR.** If you need Server-Side Rendering (SSR), Server Actions, and API routes, use SolidStart. Treat it like Next.js or Nuxt, where server functions are collocated with components.
- **Control Flow components are mandatory.** Never use `array.map()` or `items.length > 0 && <div>` in your JSX. Use Solid's native `<For>`, `<Index>`, and `<Show>` components. They are highly optimized to minimize DOM operations.

## Coding Conventions

- **Never destructure props.** Destructuring breaking reactivity. `const { name } = props` evaluates `name` immediately (losing the getter). Access props as `props.name`. If you must destructure or apply defaults, use Solid's `mergeProps` and `splitProps`.
- **Derived state is just a function.** You don't need `useMemo`. Just write a function: `const doubleCount = () => count() * 2`. The reactive system will only re-evaluate it when the underlying signal changes.
- **Lifecycle hooks.** Use `onMount` and `onCleanup`. `createEffect` should primarily be used for side-effects (like modifying the DOM directly or triggering a non-reactive API), not for synchronizing state changes.
- **Server functions (SolidStart).** Use `cache()` for GET requests (data loading) and `action()` for POST/PUT/DELETE mutations. These naturally integrate into Solid's reactive tree.

## Library Preferences

- **Routing:** `@solidjs/router` (Built-in for SolidStart, standard for Solid SPAs).
- **State Management:** Native `createSignal` / `createStore`. If you need global state, export a created signal from a regular `.ts` file or provide via Context. Don't pull in heavy state libraries unless strictly required.
- **Data fetching:** `@tanstack/solid-query` or Solid's native `createResource` combined with `cache()`.
- **Styling:** Tailwind CSS or plain CSS. Avoid heavy CSS-in-JS libraries which carry large runtime penalties that combat Solid's lightweight philosophy.

## NEVER DO THIS

1. **Never destructure component props.** `function UserCard({ name, age })` immediately breaks reactivity. The values are static. Use `function UserCard(props)` and reference `props.name`.
2. **Never spread props onto DOM elements arbitrarily.** Using `<div {...props}>` can override essential attributes or create unexpected DOM updates. Use `splitProps` to separate known attributes from generic attributes.
3. **Never use standard array map for rendering.** `items.map(Item)` will re-render the entire list every time the array updates. Use `<For each={items}>{(item) => <Item data={item} />}</For>` to only render added/removed nodes.
4. **Never treat `createEffect` like React's `useEffect`.** Solid's effects automatically track dependencies—no dependency array `. `createEffect` runs synchronously. If you update a signal inside `createEffect`, it may cause an infinite loop. Better to compute state via functions (`() => ...`) than explicitly setting signals inside an effect.
5. **Never mutate an array/object inside `createSignal` directly.** Reactivity triggers on identity tracking. If you use `items().push(newItem)`, the reference doesn't change and the UI won't update. Standard rule: `setItems([...items(), newItem])` or use `createStore`.
6. **Never use `memo` by default.** Solid's tracking is fine-grained. Wrapping components in some imaginary `React.memo` equivalent is unnecessary and actively harmful as components only run once anyway.
7. **Never call an API directly on mount if data is required for rendering.** Use `createResource()`. It integrates with Suspense, handles loading states properly, and supports SSR hydration without double-fetching.

## Testing

- Unit components with **Vitest** + **Solid Testing Library**.
- Solid Testing Library works exactly like React Testing Library but correctly manages Solid's reactive boundaries during test executions.
- Server Actions (SolidStart) can be unit-tested seamlessly without the DOM.

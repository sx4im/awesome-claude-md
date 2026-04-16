# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- SolidStart (SolidJS meta-framework)
- SolidJS 1.8+
- File-based routing
- Server functions
- Vite-based

## Project Structure
```
src/
├── routes/
│   ├── index.tsx               // Home route
│   ├── about.tsx
│   └── api/
│       └── hello.ts            // API routes
├── components/
│   └── Counter.tsx
├── entry-client.tsx
├── entry-server.tsx
└── app.tsx
```

## Architecture Rules

- **File-based routing.** `routes/` directory becomes URL structure.
- **Server functions.** `createServerFunction` for server-side code.
- **Solid primitives.** Signals, memos, effects for reactivity.
- **Islands optional.** Partial hydration with `client:only`.

## Coding Conventions

- Route: Export default component from `routes/*.tsx`.
- Layout: `routes/__layout.tsx` wraps child routes.
- API: `export async function GET(event) { return json(data) }` in `routes/api/`.
- Server function: `const getData = createServerFunction(async () => { return db.query() })`.
- Component: `function Counter() { const [count, setCount] = createSignal(0); return <button onClick={() => setCount(c => c + 1)}>{count()}</button> }`.

## NEVER DO THIS

1. **Never forget signal calls are functions.** `count()` not `count`.
2. **Never use server functions in client-only code.** Only in server contexts.
3. **Never ignore the `client:only` directive.** For client-side only components.
4. **Never mix Solid reactivity with React patterns.** Different mental model.
5. **Never skip the `entry-client` and `entry-server` files.** Required for setup.
6. **Never forget `createEffect` for side effects.** Solid's useEffect equivalent.
7. **Never use SolidStart without knowing SolidJS.** Learn Solid first.

## Testing

- Test with `solid-testing-library`.
- Test server functions separately.
- Test routes with integration tests.


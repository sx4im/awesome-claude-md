# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Fresh (Deno web framework)
- Deno 2+
- Preact
- Islands architecture
- File-based routing

## Project Structure
```
routes/
├── index.tsx                   // Home page
├── about.tsx
├── api/
│   └── hello.ts                // API routes
├── _layout.tsx                 // Root layout
└── _app.tsx                    // App wrapper
components/
└── *.tsx                       // Preact components
```

## Architecture Rules

- **Islands architecture.** Static HTML with interactive islands.
- **File-based routing.** `routes/` becomes URL structure.
- **Zero build step.** Deno runs TypeScript directly.
- **Preact by default.** Lightweight React alternative.

## Coding Conventions

- Page: `export default function HomePage() { return <div>Hello</div> }`.
- Handler: `export const handler: Handlers = { async GET(req, ctx) { return await ctx.render({ data }) } }`.
- Island: `export default function Counter() { const [count, setCount] = useState(0); return <button onClick={() => setCount(c => c + 1)}>{count}</button> }` with `// islands/Counter.tsx`.
- Layout: `export default function Layout({ Component, state }) { return <html><body><Component /></body></html> }`.

## NEVER DO THIS

1. **Never put islands in routes.** Islands must be in `islands/` directory.
2. **Never use Node.js modules.** Fresh is Deno-only.
3. **Never forget the `handler` export.** For server-side data.
4. **Never use `useState` outside islands.** Server components don't hydrate.
5. **Never ignore the `ctx.render` data flow.** Pass data from handler to page.
6. **Never skip `import_map.json`.** Required for dependencies.
7. **Never use `npm:` specifiers without need.** Prefer `esm.sh` or `jsr`.

## Testing

- Test with Deno's test runner.
- Test islands hydrate correctly.
- Test with `deno task start`.


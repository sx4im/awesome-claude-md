# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Kitajs (fastify + JSX)
- Fastify v5
- TypeScript JSX
- Type-safe HTML
- Server-first

## Project Structure
```
src/
├── components/
│   └── Button.tsx              // JSX components
├── pages/
│   ├── home.tsx                // Page routes
│   └── about.tsx
├── app.tsx                     // Fastify app setup
└── server.ts                   // Entry point
```

## Architecture Rules

- **JSX for HTML.** Type-safe server-side rendering.
- **Fastify foundation.** High-performance Node.js framework.
- **File-based routing.** `pages/` directory structure.
- **No client JS required.** Progressive enhancement optional.

## Coding Conventions

- Page: `export function get() { return <div>Hello</div> }`.
- Component: `function Button({ children }: { children: JSX.Element }) { return <button>{children}</button> }`.
- Handler: `export function post(req: FastifyRequest) { return <div>Posted</div> }`.
- Layout: Create `layout.tsx` in pages directory.

## NEVER DO THIS

1. **Never use client-side hooks.** Server-rendered JSX—no useState/useEffect.
2. **Never forget the function export.** Pages export `get`, `post`, etc.
3. **Never mix with React components.** Kitajs JSX != React JSX.
4. **Never skip Fastify plugin system.** Use for extending functionality.
5. **Never ignore the `jsx` pragma.** Different from React.
6. **Never use without understanding Fastify.** Learn Fastify basics first.
7. **Never forget to type requests.** Fastify's typed request/response.

## Testing

- Test with Fastify's inject method.
- Test JSX renders valid HTML.
- Test with `tsx` or `ts-node`.


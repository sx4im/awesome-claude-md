# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Deno 1.40+ (or Deno 2.x)
- Fresh 2.x (Preact-based web framework)
- TypeScript (strict, no build step)
- Preact for interactive islands
- Tailwind CSS (via Fresh plugin)
- Deployed on Deno Deploy (edge)

## Project Structure

```
├── routes/
│   ├── index.tsx            # Home page (/)
│   ├── about.tsx            # Static page
│   ├── blog/
│   │   ├── index.tsx        # Blog listing
│   │   └── [slug].tsx       # Dynamic blog post page
│   └── api/
│       ├── users.ts         # API route (GET, POST handlers)
│       └── webhook.ts       # Webhook handler
├── islands/
│   ├── Counter.tsx          # Interactive Preact component (hydrated)
│   ├── SearchDialog.tsx     # Client-side search
│   └── ThemeToggle.tsx      # Dark/light mode toggle
├── components/
│   ├── Header.tsx           # Static component (no JS shipped)
│   ├── Footer.tsx
│   └── BlogCard.tsx
├── lib/
│   ├── db.ts               # Database connection (Deno KV or PostgreSQL)
│   └── utils.ts            # Shared utilities
├── static/                  # Static assets (favicon, images)
├── fresh.config.ts          # Fresh configuration
├── deno.json                # Deno configuration, import map
└── dev.ts                   # Development entry point
```

## Architecture Rules

- **Islands architecture.** Pages render to static HTML by default. Only components in `islands/` ship JavaScript to the browser. A page with zero islands sends zero JS. This is Fresh's core principle. don't fight it.
- **Routes are the pages and APIs.** File-based routing in `routes/`. `.tsx` files export a Preact component (page) or handler functions (`GET`, `POST`). Both can coexist in the same file.
- **Components are static, islands are interactive.** `components/Header.tsx` renders on the server and ships zero JS. `islands/Counter.tsx` hydrates on the client with Preact. Never put event handlers in `components/`. they won't work.
- **No build step.** Deno runs TypeScript directly. Fresh compiles islands on-demand. There is no `npm run build`. `deno task start` serves the app.
- **Import maps in `deno.json`.** All dependencies are URLs or mapped in `deno.json`. No `node_modules`, no `package.json`. Use `deno.json` imports for aliasing: `"$lib/": "./lib/"`.

## Coding Conventions

- **Route handlers are named exports.** `export const handler: Handlers<Data> = { GET(req, ctx) { .. }, POST(req, ctx) { .. } }`. The component is the default export: `export default function Page({ data }: PageProps<Data>)`.
- **Islands receive serializable props only.** Props passed to island components must be JSON-serializable (no functions, no classes, no Dates). Fresh serializes props for hydration. non-serializable values cause runtime errors.
- **Use Deno APIs directly.** `Deno.readTextFile()`, `Deno.env.get()`, `Deno.KV`. No need for Node.js polyfills. Deno has built-in support for Web APIs (`fetch`, `Response`, `Request`).
- **Preact hooks in islands only.** `useState`, `useEffect`, `useCallback` work in `islands/` components. They don't work in `components/` (those are server-rendered only).
- **Permissions are explicit.** Deno runs with `--allow-net`, `--allow-read`, etc. Request only the permissions needed. Fresh's dev task sets appropriate permissions.

## Library Preferences

- **Framework:** Fresh. the official Deno web framework. Not Oak (lower-level, no SSR). Not Hono (works on Deno but Fresh has better Deno Deploy integration).
- **Database:** Deno KV (built-in key-value store, free on Deno Deploy) for simple data. `deno-postgres` for PostgreSQL. Not ORMs. Deno's ecosystem is leaner.
- **Styling:** Tailwind CSS via Fresh's Tailwind plugin. Not CSS-in-JS (Fresh strips JS from non-island components).
- **UI components:** Preact. not React (Fresh is built on Preact, they're API-compatible but Preact is 3KB).
- **Testing:** Deno's built-in test runner (`deno test`). Not Jest, not Vitest.

## NEVER DO THIS

1. **Never put event handlers in `components/`.** Components in `components/` are server-rendered only. `onClick`, `onChange`, and other event handlers are silently ignored. Move interactive elements to `islands/`.
2. **Never pass non-serializable props to islands.** Functions, class instances, and Dates can't be serialized for hydration. Pass primitive values or plain objects. Transform data in the island, not before passing it.
3. **Never use `node_modules` or `npm install`.** Deno uses URL imports or `deno.json` import maps. If you need an npm package, use `npm:` specifier: `import express from "npm:express"`. but prefer Deno-native libraries.
4. **Never use `require()`.** Deno uses ES modules exclusively. `import` and `export` only. CommonJS is not supported.
5. **Never ignore Deno permission flags.** Running with `--allow-all` in production defeats Deno's security model. Specify exactly which permissions the app needs: `--allow-net=0.0.0.0:8000 --allow-env`.
6. **Never create heavy islands for static content.** If a component just renders text and images, it belongs in `components/`. Every island adds Preact runtime + component JS to the page.
7. **Never use `window` or `document` in route handlers or components.** Server-side rendering has no `window`. Guard with `typeof document !== 'undefined'` or move to an island with `useEffect`.

## Testing

- Use `deno test` with the built-in test runner. No test framework needed.
- Test route handlers by constructing `Request` objects and asserting `Response` status/body.
- Test islands with Preact Testing Library (works with Deno's test runner).
- Use `deno lint` and `deno fmt` in CI. They're built-in and enforced project-wide.

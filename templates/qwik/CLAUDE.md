# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Qwik (Resumable framework)
- Qwik City (Meta-framework, routing)
- TypeScript (strict mode)
- Tailwind CSS
- Vite

## Project Structure

```
src/
├── components/          # Reusable Qwik UI components
│   ├── ui/              # Buttons, inputs, generic UI
│   └── router-head/     # Document head, injected globally
├── routes/              # Qwik City file-based routing
│   ├── index.tsx        # Homepage
│   ├── layout.tsx       # Root layout
│   ├── plugin@auth.ts   # Middleware (runs before all routes)
│   ├── blog/
│   │   ├── index.tsx
│   │   └── [slug]/
│   │       └── index.tsx # Dynamic route handler
│   └── api/             # API Endpoints
├── global.css           # Global Tailwind imports
└── entry.ssr.tsx        # Server-side rendering entry
```

## Architecture Rules

- **Resumability is core.** Qwik apps serialize the application state and framework state into HTML. There is no traditional "hydration." JavaScript is only downloaded when the user interacts (clicks, scrolls).
- **`$` represents lazy loading.** Any function ending in `$` (like `component$`, `onClick$`, `useTask$`) tells the Qwik optimizer to extract that function into its own JavaScript chunk, which will be lazy-loaded on demand. Respect the `$` rules.
- **Qwik City defines routing.** `src/routes/` maps automatically to URLs. `layout.tsx` files wrap sub-routes.
- **Signals for state.** Use `useSignal()` for primitives and `useStore()` for reactive objects. Never mutate an object without assigning to `.value` (for signals) or directly on the store.
- **Actions and Loaders for data flow.** Use `routeLoader$` to load data on the server during SSR. Use `routeAction$` to handle form submissions and mutations linearly. This functions like Remix/SvelteKit.

## Coding Conventions

- **Component declaration.** Always wrap components in `component$`. `export const MyComponent = component$(() => { .. })`.
- **Event handlers.** Must end in `$`. `<button onClick$={() => ...}>`. Never write `<button onClick={() => ...}>`.
- **Inline components.** Helper components within the same file shouldn't use `component$` if they are purely presentational and only called as functions `{MyInlineComponent()}` instead of standard JSX `<MyInlineComponent />`.
- **Props are serializable.** Props passed to `component$` must be serializable (no class instances, no un-serializable maps).
- **Use `useTask$` and `useVisibleTask$`.** Use `useTask$` for logic that must run on the server AND client. Use `useVisibleTask$` strictly for logic that relies on browser APIs (like DOM measurements or initializing third-party JS).

## Library Preferences

- **Routing / Meta-framework:** Qwik City (Built-in).
- **Styling:** Tailwind CSS or Vanilla Extract. (Tailwind is native via Qwik CLI plugins).
- **State Management:** Qwik's built-in `useSignal`/`useStore`/`useContext`. Do not use Redux or Zustand.
- **Icons:** `@qwikest/icons` or direct SVG components.
- **Form validation:** Modular forms (`@modular-forms/qwik`) or Qwik City's native `zod` validation inside actions.

## NEVER DO THIS

1. **Never forget the `$` suffix on closures passed to Qwik APIs.** `useTask$(() => {})`, not `useTask(() => {})`. The framework will error out or fail to lazy-load if you break the optimizer boundaries.
2. **Never overuse `useVisibleTask$`.** It forces executing JS on the client, essentially creating a hydration boundary. Only use it when absolutely necessary (e.g., using `window`, checking container sizes, or mounting a heavy WebGL canvas). Use bounds correctly.
3. **Never capture non-serializable data in a `$` closure.** Because `$` creates a network boundary where JS is downloaded later, any variables captured from the parent scope must be serializable to JSON. You cannot capture a class instance or a DOM element reference inside an `onClick$`.
4. **Never fetch data in components incorrectly.** Don't use standard `useEffect` + `fetch` patterns. Use Qwik City's `routeLoader$` to fetch data on the server securely and pass it predictably to components.
5. **Never import Heavy libraries globally.** Because Qwik is designed to slice chunks, importing massive libraries linearly at the top of a file might break the lazy-loading paradigm. Rely on `$` bounds to isolate library payloads.
6. **Never mutate `server$` functions from the client.** `server$` functions are backend APIs disguised as functions. Treat them securely. Don't trust input parameters implicitly.
7. **Never use standard React hooks.** Although Qwik uses JSX, `useState` and `useEffect` do not exist. You must use `useSignal` and `useTask$`.

## Testing

- Unit tests with **Vitest**. (Setup via `npm run qwik add vitest`).
- E2E tests with **Playwright**.
- Because Qwik handles async boundaries organically, testing complex interaction states often requires testing the compiled client output via Playwright.

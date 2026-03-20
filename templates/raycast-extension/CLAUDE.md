# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Raycast Extensions API
- TypeScript 5.x (strict mode)
- React 18 (Raycast's built-in renderer)
- Raycast UI components (List, Form, Detail, Action, ActionPanel)
- Node.js 20+ runtime (Raycast bundles its own)

## Project Structure

```
src/
├── [COMMAND_NAME].tsx        # Each command is a separate entry file
├── [COMMAND_NAME_2].tsx      # Raycast discovers commands from package.json
├── components/
│   ├── [ENTITY]ListItem.tsx  # List.Item wrappers for domain entities
│   └── [ENTITY]Detail.tsx    # Detail view components
├── hooks/
│   ├── use[Entity].ts        # Data fetching hooks (useFetch, useCachedPromise)
│   └── usePreferences.ts     # Typed preferences access
├── services/
│   ├── api.ts                # External API client
│   └── [DOMAIN].ts           # Business logic
├── utils/
│   ├── icons.ts              # Icon helpers and mappings
│   └── format.ts             # Display formatting helpers
├── types/
│   └── [DOMAIN].ts           # Domain type definitions
└── assets/
    └── [ICON].png            # Custom command icons (512x512, 1024x1024)
package.json                  # Commands, preferences, and extension metadata
```

## Architecture Rules

- **Each command is a top-level file in `src/`.** Raycast discovers commands from `package.json`'s `commands` array, where each entry points to a file in `src/`. There is no router. Each command is an independent entry point with its own React tree.
- **Raycast re-renders on every keystroke.** The search bar triggers `onSearchTextChange` on every character. Use `useCachedPromise` or `useFetch` with debouncing for API calls. Never fire a network request on every keystroke without throttling.
- **Preferences are declared in `package.json`.** User-configurable values (API keys, defaults) are defined in the `preferences` array in `package.json`, not in a custom settings UI. Access them via `getPreferenceValues<Preferences>()`.
- **All UI uses Raycast components.** You cannot use HTML, CSS, or custom DOM elements. Raycast provides `List`, `Grid`, `Form`, `Detail`, `ActionPanel`, and `Action`. Detail views support Markdown for rich content.
- **Cache aggressively with `LocalStorage` and `Cache`.** Raycast extensions should feel instant. Use `Cache` for ephemeral data (survives extension reloads) and `LocalStorage` for persistent data. Show cached data immediately while fetching fresh data.

## Coding Conventions

- **Commands export a default React component.** `export default function Command() { ... }`. This is the entry point Raycast calls. Never export a named component as the command root.
- **Use `useCachedPromise` for data fetching.** It handles loading states, caching, revalidation, and error display. Never use raw `useEffect` + `useState` for API calls; you lose Raycast's built-in loading indicators and error handling.
- **Actions go in `ActionPanel`.** Every interactive element is an `Action` inside `ActionPanel`. Copy to clipboard, open in browser, delete, refresh — all are Actions. Never try to handle clicks on List.Item directly.
- **Show loading and empty states.** Use `List`'s `isLoading` prop during fetches. Provide `List.EmptyView` for zero-result states. Never render an empty list without explanation.
- **Toast for async feedback.** Use `showToast({ style: Toast.Style.Success })` for operation feedback. Use `Toast.Style.Animated` during operations and update to `Success` or `Failure` on completion.

## Library Preferences

- **HTTP client:** `@raycast/utils`'s `useFetch` hook for GET requests inside components. `node-fetch` or built-in `fetch` for service-layer API calls. Not axios (unnecessary dependency).
- **Data fetching:** `useCachedPromise` from `@raycast/utils`. Not SWR or React Query (Raycast's utilities integrate with Raycast's cache and loading UI natively).
- **Date formatting:** `date-fns` if needed. Not `moment` (too large, deprecated).
- **Markdown:** Native string templates for Detail markdown. Not `marked` or `remark` (Detail views render markdown natively).

## File Naming

- Commands: `kebab-case.tsx` matching the command name → `search-issues.tsx`, `create-task.tsx`
- Components: `PascalCase.tsx` → `IssueListItem.tsx`, `ProjectDetail.tsx`
- Hooks: `camelCase.ts` → `useIssues.ts`, `useProjects.ts`
- Services: `kebab-case.ts` → `api-client.ts`, `auth-service.ts`
- Types: `kebab-case.ts` → `issue-types.ts`

## NEVER DO THIS

1. **Never use `useEffect` + `fetch` for data loading.** Use `useCachedPromise` or `useFetch` from `@raycast/utils`. Raw `useEffect` gives you no loading spinner, no error toast, no caching, and no revalidation. This is the most common Raycast extension mistake.
2. **Never fire API calls on every keystroke.** `onSearchTextChange` fires per character. Wrap API calls in `useCachedPromise` with a debounced key, or implement client-side filtering with `List`'s built-in `filtering={true}`.
3. **Never use `console.log` for user feedback.** Users cannot see the console. Use `showToast()` for operation results and `showHUD()` for quick confirmations that close the window.
4. **Never hardcode API keys.** Declare them as `preferences` in `package.json` with `type: "password"`. Raycast secures them in the system keychain and prompts users on first run.
5. **Never render HTML in Detail views.** `Detail` accepts Markdown only, via the `markdown` prop. HTML tags are not rendered. Use Markdown syntax for formatting, images, and links.
6. **Never block the main render with heavy computation.** Raycast expects renders in milliseconds. Offload heavy work to async functions and show `isLoading={true}` while processing.
7. **Never forget `ActionPanel` on list items.** Items without actions feel broken. At minimum, provide a "Copy to Clipboard" and "Open in Browser" action. Users expect `Cmd+Enter` to do something.

## Testing

- Use Vitest for unit testing services, API clients, and utility functions.
- Test hooks with `@testing-library/react-hooks` and mock `@raycast/api` modules.
- Mock `getPreferenceValues()` to return test preferences. Mock `LocalStorage` and `Cache` for storage tests.
- Raycast provides `ray lint` and `ray build` — run both in CI. `ray lint` catches common API misuse.
- Manual test in Raycast itself: check loading states, empty states, error toasts, keyboard navigation, and action shortcuts.

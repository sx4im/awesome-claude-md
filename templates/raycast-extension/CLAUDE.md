# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Bots & Plugins)

### Release Discipline
- Constrain event handlers to explicit allowlists and permission scopes.
- Validate all external payloads and signatures where supported.
- Prevent runaway automation loops and duplicate side effects.

### Merge/Release Gates
- Webhook/event contract tests pass.
- Rate-limit and retry behavior validated.
- Security-sensitive commands reviewed for abuse paths.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Raycast Extensions API
- TypeScript 5.x (strict mode)
- React 18 (Raycast's built-in renderer)
- Raycast UI components (List, Form, Detail, Action, ActionPanel)
- Node.js 20+ runtime (Raycast bundles its own)

## Project Structure

```
src/
├── {command-name}.tsx        # Each command is a separate entry file
├── {command-name-2}.tsx      # Raycast discovers commands from package.json
├── components/
│   ├── {Entity}ListItem.tsx  # List.Item wrappers for domain entities
│   └── {Entity}Detail.tsx    # Detail view components
├── hooks/
│   ├── use{Entity}.ts        # Data fetching hooks (useFetch, useCachedPromise)
│   └── usePreferences.ts     # Typed preferences access
├── services/
│   ├── api.ts                # External API client
│   └── {domain}.ts           # Business logic
├── utils/
│   ├── icons.ts              # Icon helpers and mappings
│   └── format.ts             # Display formatting helpers
├── types/
│   └── {domain}.ts           # Domain type definitions
└── assets/
    └── {icon}.png            # Custom command icons (512x512, 1024x1024)
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

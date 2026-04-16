# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- HTMX v2.0 (advanced patterns)
- Hyperscript or Alpine.js for interactions
- Server-side framework (Go/Rust/Python)
- JSON-HTML dual endpoints
- Out-of-band swaps

## Project Structure
```
src/
├── handlers/
│   ├── html_handlers.go        // HTMX fragment endpoints
│   ├── api_handlers.go         // JSON API endpoints
│   └── partials/
│       └── table-rows.html
├── middleware/
│   └── htmx.go                 // HX-* header handling
├── static/
│   └── htmx.min.js
└── templates/
    ├── layouts/
    └── fragments/
```

## Architecture Rules

- **Dual endpoints.** Same routes return HTML for HTMX, JSON for API clients.
- **HX-Request detection.** Check request headers to determine response format.
- **Out-of-band swaps.** Use `hx-swap-oob` for updating multiple elements.
- **View transitions.** Use `hx-swap="transition:true"` for smooth updates.

## Coding Conventions

- Handler: `if r.Header.Get("HX-Request") != "" { renderTemplate(w, "fragment", data) } else { renderJSON(w, data) }`.
- OOB swap: `template.Execute(w, map[string]any{"items": items, "count": count})` with `{{range .items}}...{{end}}<div id="count" hx-swap-oob="true">{{.count}}</div>`.
- Boosting: Add `hx-boost="true"` to links for SPA-like navigation.
- Indicators: Use `hx-indicator="#spinner"` with CSS opacity transitions.

## NEVER DO THIS

1. **Never mix HTMX with heavy JS frameworks.** HTMX replaces React/Vue for server-rendered apps.
2. **Never ignore the `HX-Trigger` header.** Use for client-side events after swaps.
3. **Never skip CSRF tokens.** HTMX requests need CSRF protection.
4. **Never use `innerHTML` manually.** Let HTMX handle DOM updates.
5. **Never ignore `HX-Target` validation.** Ensure targets exist to prevent errors.
6. **Never poll excessively.** Use WebSockets or SSE for real-time, not polling.
7. **Never forget history management.** Use `hx-push-url="true"` for bookmarkable states.

## Testing

- Test fragment endpoints return valid HTML.
- Test OOB swaps update multiple elements.
- Test boosted navigation works correctly.


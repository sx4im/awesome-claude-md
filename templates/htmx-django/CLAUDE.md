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

## Production Delivery Playbook (Category: Frontend)

### Release Discipline
- Enforce performance budgets (bundle size, LCP, CLS) before merge.
- Preserve accessibility baselines (semantic HTML, keyboard nav, ARIA correctness).
- Block hydration/runtime errors with production build verification.

### Merge/Release Gates
- Typecheck + lint + unit tests + production build pass.
- Critical route smoke tests for navigation, auth, and error boundaries.
- No new console errors/warnings in key user flows.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Python 3.12+ with type hints on all function signatures
- Django 5.1+ with server-side rendering as the primary architecture
- htmx 2.0 for dynamic interactions without writing JavaScript
- django-htmx middleware for server-side htmx request detection
- Alpine.js 3.x for minimal client-side state when htmx alone is insufficient
- django-template-partials for reusable partial template rendering
- Tailwind CSS 3.4 via django-tailwind for utility-first styling
- WhiteNoise for static file serving in production

## Project Structure

```
project/
  settings/
    base.py             # Shared settings, INSTALLED_APPS includes django_htmx
    development.py      # DEBUG=True, django-debug-toolbar
    production.py       # WhiteNoise, CSRF settings, SECURE_* flags
  urls.py               # Root URL configuration
apps/
  core/
    templates/
      base.html         # Base template with htmx script, Alpine.js, Tailwind
      partials/         # Shared partial templates (pagination, modals, toasts)
    templatetags/
      htmx_tags.py      # Custom tags for htmx attributes and URL generation
    middleware.py        # Custom middleware for htmx-specific response handling
  tasks/
    models.py
    views.py            # Full page views + htmx partial views in same module
    urls.py             # URL patterns including htmx endpoints
    forms.py            # Django forms used for both full and htmx submissions
    templates/
      tasks/
        list.html       # Full page: extends base.html
        _list.html      # Partial: just the task list, swapped by htmx
        _row.html       # Partial: single task row for inline updates
        _form.html      # Partial: form rendered for hx-get modal loading
        _search.html    # Partial: search results for hx-trigger="input changed"
static/
  css/
    input.css           # Tailwind input file
  js/
    app.js              # Alpine.js components, htmx event listeners
templates/
  components/           # Project-wide reusable template components
    _modal.html         # Generic modal wrapper with hx-target
    _toast.html         # Toast notification partial
    _pagination.html    # Cursor pagination controls with hx-get
```

## Architecture Rules

- Every htmx endpoint returns an HTML partial, not JSON; use `django-template-partials` or prefix partials with `_`
- Views detect htmx requests using `request.htmx` (from django-htmx middleware) and return partial vs full page accordingly
- Pattern: `if request.htmx: return render(request, "tasks/_list.html", ctx)` else `return render(request, "tasks/list.html", ctx)`
- All htmx attributes go in templates, never generated in Python views; views only return HTML
- Use `hx-target` and `hx-swap` explicitly on every htmx element; avoid relying on inheritance for clarity
- Forms use standard Django form classes; htmx submits them via `hx-post` with `hx-target` for inline error display
- Use `HX-Trigger` response header to fire client-side events for toasts, modal closes, and list refreshes

## Coding Conventions

- Partial templates are prefixed with underscore: `_list.html`, `_row.html`, `_form.html`
- URL names for htmx endpoints use the suffix `_partial`: `task_list_partial`, `task_form_partial`
- Views that handle both htmx and full requests are single functions, not separate view classes
- Use `django.contrib.messages` with a `_toast.html` partial that listens to `HX-Trigger: showMessage`
- Pagination uses cursor-based `hx-get` on a "Load More" button with `hx-swap="afterend"` and `hx-target="this"`
- Search uses `hx-get` with `hx-trigger="input changed delay:300ms"` for debounced server-side search
- Inline editing uses `hx-get` to swap a display row with a form row, `hx-put` to save, re-render the display row

## Library Preferences

- django-htmx for middleware and `request.htmx` attribute access
- django-template-partials over django-render-block for partial template reuse
- Alpine.js over jQuery or vanilla JS for client-side state (dropdowns, toggles, modals)
- django-widget-tweaks for adding htmx attributes to form field widgets in templates
- heroicons via django-heroicons for consistent SVG icons in templates
- django-debug-toolbar with htmx panel for debugging htmx requests during development

## File Naming

- Full page templates: descriptive name without prefix, e.g., `list.html`, `detail.html`
- Partial templates: underscore prefix, e.g., `_list.html`, `_row.html`, `_form.html`
- Component templates: underscore prefix in `components/` directory
- Views: `views.py` per app, not split into `views/` package unless exceeding 300 lines
- URL configs: `urls.py` per app with `app_name` set for namespacing

## NEVER DO THIS

1. Never return JSON from htmx endpoints; always return rendered HTML partials
2. Never use `hx-swap="innerHTML"` as a default everywhere; choose the appropriate swap strategy per interaction
3. Never put htmx attributes in Python view code; all `hx-*` attributes belong in Django templates
4. Never skip CSRF tokens on htmx POST requests; include `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` or use the django-htmx CSRF helper
5. Never disable Django's template auto-escaping for htmx responses; XSS is still a risk with server-rendered HTML
6. Never create a separate API app returning JSON just for htmx; htmx endpoints live alongside their full-page views
7. Never use `hx-boost="true"` on the body tag globally; apply it selectively to navigation links only

## Testing

- Test htmx views by setting `HTTP_HX_REQUEST=true` header in Django test client requests
- Assert partial responses do not contain `<html>` or `<body>` tags; they should be bare HTML fragments
- Test that non-htmx requests to the same URL return full page responses with base template
- Verify `HX-Trigger` headers are set correctly in responses using `response["HX-Trigger"]`
- Use Playwright for E2E tests that exercise htmx interactions (swap, OOB updates, triggers)
- Test form validation by posting invalid data via htmx and asserting error messages in the partial response
- Use django-debug-toolbar's htmx panel to profile query counts on partial endpoints

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

- Eleventy (11ty) 3.x as static site generator
- Nunjucks as primary template language (`.njk`)
- WebC for interactive component islands
- CSS (no preprocessor; CSS custom properties and nesting)
- JavaScript data files for dynamic content
- Deployed on [Netlify / Cloudflare Pages / Vercel]

## Project Structure

```
src/
├── _includes/
│   ├── layouts/
│   │   ├── base.njk            # HTML shell: <html>, <head>, <body>
│   │   ├── page.njk            # Standard page layout (extends base)
│   │   └── post.njk            # Blog post layout with metadata
│   ├── components/
│   │   ├── header.njk          # Site header partial
│   │   ├── footer.njk          # Site footer partial
│   │   ├── nav.njk             # Navigation partial
│   │   └── post-card.njk       # Reusable post card partial
│   └── webc/
│       └── search-dialog.webc  # Interactive WebC component
├── pages/
│   ├── index.njk               # Home page
│   └── pages.json              # Directory data file (layout, permalink)
├── blog/
│   ├── posts/                  # Blog posts as Markdown
│   ├── posts.json              # Directory data file for all posts
│   └── index.njk               # Blog listing page
├── _data/
│   ├── site.json               # Global site metadata (title, url, author)
│   ├── navigation.json         # Nav menu items
│   └── helpers.js              # Computed global data (fetch external APIs)
├── assets/
│   ├── css/
│   │   └── main.css            # Global stylesheet
│   ├── js/
│   │   └── main.js             # Minimal client-side JS (no bundler)
│   └── img/                    # Static images
├── feed.njk                    # RSS/Atom feed template
└── sitemap.njk                 # XML sitemap template
eleventy.config.js              # Eleventy configuration (filters, collections, plugins)
```

## Architecture Rules

- **Eleventy is a static site generator, not a framework.** It transforms templates and data into HTML files. There is no client-side runtime, no hydration, no virtual DOM. Every page is a static HTML file at build time.
- **Data cascade is the content model.** Data flows from global (`_data/`), to directory data files (`posts.json`), to template frontmatter. Lower levels override higher levels. Understand the cascade before adding data anywhere.
- **Layouts chain, not nest.** `post.njk` extends `base.njk` via `layout: layouts/base.njk` in its frontmatter. Never use Nunjucks `{% include %}` for layout wrapping. Includes are for partials (header, footer, card), not page structure.
- **Collections organize content.** Use tags in frontmatter to create collections: `tags: posts`. Access them in templates as `collections.posts`. Custom collections are defined in `eleventy.config.js` with `addCollection()`.
- **No JavaScript bundler.** Client-side JS is vanilla, minimal, and loaded directly. If you need interactivity, use WebC components with `<script>` blocks or progressive enhancement. Do not add Webpack, Rollup, or Vite.

## Coding Conventions

- Templates use Nunjucks (`.njk`). Content uses Markdown (`.md`) with YAML frontmatter. Never mix template logic into Markdown files beyond frontmatter.
- Filters handle data transformation in templates. Add custom filters in `eleventy.config.js`: `eleventyConfig.addFilter("readableDate", (date) => ...)`. Never put complex logic in Nunjucks templates.
- Shortcodes generate reusable HTML snippets. Use paired shortcodes for wrappers: `{% callout "warning" %}Content{% endcallout %}`. Define them in `eleventy.config.js`.
- Directory data files (`posts.json`) set defaults for all files in a directory. Use them to set `layout`, `tags`, and `permalink` patterns instead of repeating frontmatter in every file.
- Permalinks control output paths. Set them in frontmatter or directory data: `permalink: /blog/{{ page.fileSlug }}/`. Always include trailing slash for directory-style URLs.

## Library Preferences

- **Templating:** Nunjucks for layouts and pages. It has the best filter and macro support. Not Liquid (weaker logic). Not Pug (unfamiliar syntax for content authors).
- **Components:** WebC for anything interactive. It outputs standards-based HTML with scoped CSS and JS. Not a full framework like React or Vue.
- **CSS:** Plain CSS with custom properties and native nesting. Not Sass (unnecessary complexity for static sites). Not Tailwind (adds build tooling Eleventy doesn't need).
- **Images:** `@11ty/eleventy-img` plugin. It generates responsive `<picture>` elements with multiple formats (WebP, AVIF) at build time. Not manual `<img>` tags.
- **RSS:** Template-based using `@11ty/eleventy-plugin-rss`. Generates Atom/RSS from collections.
- **Syntax highlighting:** `@11ty/eleventy-plugin-syntaxhighlight` using Prism. Applied at build time, zero client JS.

## File Naming

- Templates: `kebab-case.njk` → `about-us.njk`, `contact.njk`
- Layouts: `kebab-case.njk` → `base.njk`, `post.njk` (in `_includes/layouts/`)
- Partials: `kebab-case.njk` → `post-card.njk`, `site-header.njk`
- Content: `kebab-case.md` → `first-post.md`, `getting-started.md`
- Data files: `camelCase.js` or `kebab-case.json` → `site.json`, `helpers.js`
- WebC: `kebab-case.webc` → `search-dialog.webc`, `theme-toggle.webc`
- Config: `eleventy.config.js` (not `.eleventy.js`, the old convention)

## NEVER DO THIS

1. **Never use `{% include %}` for layout wrapping.** Includes are for partials (a header, a card). Layouts use the `layout` frontmatter key and Eleventy's layout chaining. Using includes for page structure breaks the data cascade and pagination.
2. **Never put logic in Markdown files.** Markdown files contain frontmatter and prose. If you need conditional rendering or loops, create a Nunjucks template that consumes the Markdown content. Template logic in `.md` files is fragile and confusing.
3. **Never hardcode site metadata in templates.** Put site title, URL, author, and description in `_data/site.json`. Reference them as `{{ site.title }}`. Hardcoded values become stale and inconsistent across pages.
4. **Never use `console.log` for debugging data in templates.** Use the `log` filter: `{{ myData | log }}`. It outputs to the terminal during build. Or use `{% set debug = myData | dump %}` to render data as JSON in the HTML.
5. **Never skip directory data files.** If every post in `blog/posts/` has `layout: layouts/post.njk` and `tags: posts` in its frontmatter, move those to `blog/posts/posts.json`. Repeating frontmatter across files is a maintenance burden.
6. **Never add a JavaScript bundler.** Eleventy's strength is simplicity. If you need React or Vue components, you picked the wrong tool. Use WebC for interactive islands. Vanilla JS with progressive enhancement handles the rest.
7. **Never use the old `.eleventy.js` config filename.** Eleventy 3.x uses `eleventy.config.js` (or `.cjs`/`.mjs`). The old dotfile name still works but is deprecated. Use the new convention.

## Testing

- Use Eleventy's `--dryrun` flag to validate builds without writing output. Catches template errors, missing data, and broken permalinks.
- Test HTML output with `html-validate` or `pa11y` for accessibility. Run against the `_site/` build output.
- Broken links: use `hyperlink` or `broken-link-checker` against the built site. Internal links break when permalinks change.
- Lighthouse CI for performance. Eleventy sites with no JS should score 100 on performance. If they don't, you added unnecessary client-side code.

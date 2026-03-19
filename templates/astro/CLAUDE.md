# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Astro 4.x
- TypeScript (strict mode)
- Content Collections for structured content
- MDX for rich content pages
- Tailwind CSS 3.x
- Deployed on Vercel, Netlify, or Cloudflare Pages

## Project Structure

```
src/
├── pages/
│   ├── index.astro          # Home page
│   ├── blog/
│   │   ├── index.astro      # Blog listing
│   │   └── [slug].astro     # Dynamic blog post page
│   ├── docs/
│   │   └── [...slug].astro  # Catch-all for docs (from content collection)
│   └── rss.xml.ts           # RSS feed endpoint
├── layouts/
│   ├── BaseLayout.astro     # HTML shell, meta, global styles
│   ├── BlogLayout.astro     # Blog post wrapper
│   └── DocsLayout.astro     # Documentation wrapper with sidebar
├── components/
│   ├── Header.astro         # Static components as .astro
│   ├── Footer.astro
│   ├── BlogCard.astro
│   └── interactive/         # Client-side components (React, Svelte, etc.)
│       └── SearchDialog.tsx  # Uses client:load or client:visible
├── content/
│   ├── config.ts            # Content collection schemas (Zod)
│   ├── blog/                # Blog posts as .md or .mdx
│   │   └── my-first-post.mdx
│   └── docs/                # Documentation as .md or .mdx
│       └── getting-started.md
├── styles/
│   └── global.css           # Global styles and Tailwind imports
└── lib/
    └── utils.ts             # Shared utility functions
```

## Architecture Rules

- **Static by default.** Every page is server-rendered to static HTML at build time. Use `export const prerender = true` (the default) for all pages. Only add `export const prerender = false` for truly dynamic pages (search, dashboards with auth).
- **`.astro` components for static content.** If a component doesn't need client-side JavaScript (no clicks, no state), use `.astro`. It ships zero JavaScript. This is the default for headers, footers, cards, layouts.
- **Framework components for interactivity only.** Use React/Svelte/Vue components only when you need client-side state or event handlers. Place them in `components/interactive/` with explicit `client:` directives.
- **Content Collections are the CMS.** All structured content (blog posts, docs, changelogs) lives in `content/` with Zod schemas in `content/config.ts`. Query with `getCollection()` and `getEntry()`. never read `.md` files with `fs`.
- **Island architecture.** Interactive components are loaded with `client:load` (immediately), `client:visible` (when scrolled into view), or `client:idle` (on browser idle). Choose the laziest option that works. Default to `client:visible`.

## Coding Conventions

- Astro components use `.astro` extension. Frontmatter (TypeScript) goes in `---` fences at the top. Template HTML goes below.
- Props in Astro components: `interface Props { title: string; date: Date }` in the frontmatter, destructured with `const { title, date } = Astro.props`.
- Content collection schemas are strict: every field is validated with Zod. Frontmatter without a matching schema is a build error.
- All image assets go through `astro:assets` with the `<Image />` component. automatic optimization, WebP, lazy loading. Never use raw `<img>` tags for local images.
- MDX components are passed via the `components` prop in layouts. Custom heading anchors, code blocks, and callouts are defined once and applied globally.

## Library Preferences

- **Content:** Astro Content Collections. not a headless CMS (for content that lives in the repo). For external content, use Astro's fetch in `getStaticPaths`.
- **Styling:** Tailwind CSS. not CSS-in-JS (Astro strips JS, so CSS-in-JS is the wrong abstraction). Scoped `<style>` blocks for component-specific overrides.
- **Search:** Pagefind. not Algolia (Pagefind is static, free, and runs at build time). Works perfectly with Astro's static output.
- **MDX plugins:** `rehype-pretty-code` for syntax highlighting (uses Shiki), `remark-gfm` for GitHub-flavored Markdown. Not `prismjs`. Shiki is more accurate.
- **RSS:** `@astrojs/rss`. built-in, works with content collections.

## File Naming

- Pages: `kebab-case.astro` → `about-us.astro`, `contact.astro`
- Layouts: `PascalCase.astro` → `BaseLayout.astro`, `BlogLayout.astro`
- Astro components: `PascalCase.astro` → `BlogCard.astro`, `Header.astro`
- Interactive components: `PascalCase.tsx` → `SearchDialog.tsx`
- Content: `kebab-case.mdx` → `getting-started.mdx`, `my-first-post.mdx`
- Utilities: `camelCase.ts` → `formatDate.ts`, `readingTime.ts`

## NEVER DO THIS

1. **Never ship JavaScript when Astro components work.** If a component doesn't need interactivity, write it as `.astro`. A React component that only renders HTML still ships React's runtime. An `.astro` component ships nothing.
2. **Never use `client:load` when `client:visible` works.** Loading a comment section immediately when it's below the fold wastes bandwidth. Use `client:visible`. it loads when the user scrolls to it.
3. **Never read content files with `fs.readFileSync`.** Use Astro's `getCollection()` and `getEntry()`. They validate frontmatter, parse MDX, and integrate with Astro's type system.
4. **Never use `<img>` tags for local images.** Use `<Image />` from `astro:assets`. It handles responsive sizing, format conversion, and lazy loading. Raw `<img>` tags bypass all of this.
5. **Never put interactive logic in `.astro` components.** Astro frontmatter runs at build time (or server-side). Client-side state, event handlers, and DOM manipulation need a framework component with a `client:` directive.
6. **Never create pages outside `src/pages/`.** Astro uses file-based routing. A file in `src/components/MyPage.astro` is a component, not a route. Routes must be in `src/pages/`.
7. **Never skip content collection schemas.** Untyped frontmatter is a ticking timebomb. Define Zod schemas for every collection in `content/config.ts`. Build-time validation catches errors before they reach production.

## Testing

- Use Vitest for unit tests on utilities and helper functions.
- Use Playwright for E2E tests. test the built site, not the dev server.
- Content validation is handled at build time by content collection schemas. a build failure is a test failure.
- Test accessibility with `@axe-core/playwright` in E2E tests.
- Lighthouse CI for performance scoring. Astro sites should score 95+ on performance consistently.

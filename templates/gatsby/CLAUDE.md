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

- Gatsby 5.x with React 18
- TypeScript (strict mode)
- GraphQL data layer for all content queries
- MDX 2 for rich content pages
- Tailwind CSS 3.x
- Deployed on [Gatsby Cloud / Netlify / Vercel]

## Project Structure

```
src/
├── pages/
│   ├── index.tsx              # Home page (auto-routed)
│   ├── 404.tsx                # Custom 404 page
│   └── about.tsx              # Static pages as .tsx files
├── templates/
│   ├── BlogPost.tsx           # Template for programmatic page creation
│   └── TagArchive.tsx         # Template for tag listing pages
├── components/
│   ├── ui/                    # Primitives: Button, Card, SEO
│   ├── layout/                # Layout components: Header, Footer, Sidebar
│   │   └── Layout.tsx         # Main layout wrapper
│   └── features/              # Domain components: PostCard, AuthorBio
├── hooks/                     # Custom hooks wrapping useStaticQuery
│   ├── useSiteMetadata.ts     # Site-wide metadata query
│   └── useAllPosts.ts         # Blog post listing query
├── content/
│   ├── blog/                  # MDX blog posts
│   │   └── my-first-post.mdx
│   └── pages/                 # MDX content pages
├── styles/
│   └── global.css             # Global styles and Tailwind imports
└── lib/
    └── utils.ts               # Shared utility functions

gatsby-config.ts               # Plugin configuration and site metadata
gatsby-node.ts                 # Programmatic page creation (createPages)
gatsby-browser.tsx             # Client-side wrappers (providers, layout)
gatsby-ssr.tsx                 # Server-side wrappers (must mirror gatsby-browser)
```

## Architecture Rules

- **GraphQL is the only data access layer.** All content, metadata, images, and file data flow through Gatsby's GraphQL layer. Never use `fs.readFileSync` or direct file imports for content. Use `useStaticQuery` in components and page queries in pages/templates.
- **Page queries vs. static queries.** Page queries (exported `graphql` tag) are for pages and templates only. They receive variables from `createPages` context. Components use `useStaticQuery` which cannot accept variables.
- **Templates are not pages.** Files in `src/templates/` are used by `gatsby-node.ts` `createPages` to generate pages programmatically. They are never auto-routed. Pages in `src/pages/` are auto-routed by filename.
- **gatsby-browser and gatsby-ssr must match.** Any wrapper component (providers, layout) exported from `gatsby-browser.tsx` must be identically exported from `gatsby-ssr.tsx`. Mismatches cause hydration errors.
- **Images go through gatsby-plugin-image.** All images use `<GatsbyImage>` (for dynamic queries) or `<StaticImage>` (for hardcoded paths). These handle responsive sizing, lazy loading, and format conversion automatically.

## Coding Conventions

- All function components use the `function` keyword: `export function PostCard()`. Not `const PostCard = () => {}`. Arrow functions are for inline callbacks only.
- Page components receive `pageContext` and `data` as props. Type them explicitly: `const BlogPost: React.FC<PageProps<Queries.BlogPostQuery>> = ({ data })`.
- Use Gatsby's generated TypeScript types. Run `gatsby develop` to generate types in `src/gatsby-types.d.ts`. Query result types follow the pattern `Queries.YourQueryNameQuery`.
- GraphQL queries must have unique names. `query SiteMetadata { ... }` and `query AllBlogPosts { ... }`. Anonymous queries cause build failures.
- Wrap `useStaticQuery` calls in custom hooks. Never call `useStaticQuery` directly in a component. Create `hooks/useSiteMetadata.ts` that returns typed data.

## Library Preferences

- **Content:** MDX 2 via `gatsby-plugin-mdx`. Not plain Markdown. MDX allows embedding React components in content. Frontmatter is the metadata layer.
- **Styling:** Tailwind CSS. Not styled-components or CSS modules. Gatsby's build pipeline works best with utility-first CSS that doesn't depend on runtime injection.
- **Images:** `gatsby-plugin-image` + `gatsby-plugin-sharp`. Always. Not raw `<img>` tags, not next/image, not external image CDNs for local assets.
- **SEO:** Custom `<SEO>` component using `useStaticQuery` for defaults + prop overrides. Not `react-helmet` directly in every page.
- **Data sources:** `gatsby-source-filesystem` for local files, `gatsby-source-contentful` or `gatsby-source-sanity` for CMS. All sources feed into the GraphQL layer.
- **Search:** Pagefind or Algolia via `gatsby-plugin-algolia`. Not client-side filtering of all posts. Pre-built search indices are mandatory for content sites.

## File Naming

- Pages: `camelCase.tsx` → `index.tsx`, `about.tsx`, `contact.tsx`
- Templates: `PascalCase.tsx` → `BlogPost.tsx`, `TagArchive.tsx`
- Components: `PascalCase.tsx` → `PostCard.tsx`, `AuthorBio.tsx`
- Hooks: `useCamelCase.ts` → `useSiteMetadata.ts`, `useAllPosts.ts`
- Content: `kebab-case.mdx` → `my-first-post.mdx`, `getting-started.mdx`
- Config files: `gatsby-*.ts` → `gatsby-config.ts`, `gatsby-node.ts`

## NEVER DO THIS

1. **Never import data without GraphQL.** `import posts from '../content/blog'` bypasses Gatsby's data layer. Use a GraphQL query. Gatsby transforms, optimizes, and types all data through GraphQL.
2. **Never use `<img>` for local images.** Use `<StaticImage>` for hardcoded paths and `<GatsbyImage>` for dynamic query results. Raw `<img>` tags skip responsive sizing, lazy loading, and WebP conversion.
3. **Never put variable-dependent queries in components.** `useStaticQuery` does not accept variables. If you need filtered or parameterized data, use a page query in a template and pass the variable from `gatsby-node.ts` via `createPages` context.
4. **Never skip naming GraphQL queries.** `export const query = graphql`{ ... }`` without a query name causes build failures and type generation issues. Always name them: `query BlogPostBySlug($slug: String!) { ... }`.
5. **Never create pages manually in `src/pages/` when they need dynamic data.** Blog posts from MDX should be created programmatically in `gatsby-node.ts` using `createPages`. The `src/pages/` directory is for static, non-parameterized routes only.
6. **Never mismatch gatsby-browser and gatsby-ssr exports.** If `wrapRootElement` is exported from `gatsby-browser.tsx`, the identical function must be exported from `gatsby-ssr.tsx`. Mismatches cause React hydration errors that are extremely hard to debug.
7. **Never use `navigate()` for external URLs.** Gatsby's `navigate()` is for internal routing only. For external links, use `<a href="...">`. Using `navigate('https://...')` will try to route internally and fail silently.

## Testing

- Use Jest + React Testing Library. Gatsby ships with Jest config support via `gatsby-plugin-testing`.
- Mock Gatsby's modules in `__mocks__/gatsby.ts`: mock `useStaticQuery`, `graphql`, `Link`, and `navigate`.
- Test components with mocked GraphQL data. Create fixtures matching your query shapes in `__fixtures__/`.
- Use Playwright for E2E tests against `gatsby build && gatsby serve`. Never test against the dev server.
- Content validation happens at build time. A failing build is a failing test. Run `gatsby build` in CI before deploy.

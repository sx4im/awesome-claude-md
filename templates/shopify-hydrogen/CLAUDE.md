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

## Production Delivery Playbook (Category: Full-Stack)

### Release Discipline
- Maintain contract consistency across UI, API, DB schema, and background jobs.
- Ship schema changes with backward-compatible rollout and rollback notes.
- Guard critical business flows with idempotency and retry safety.

### Merge/Release Gates
- API contract checks, migration checks, and e2e smoke tests pass.
- Auth and billing-critical paths validated explicitly.
- No breaking change without migration path and versioning note.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Hydrogen (Shopify's React framework for headless commerce)
- Remix (Hydrogen is built on Remix)
- TypeScript (strict mode)
- Tailwind CSS 3.x
- Shopify Storefront API (GraphQL)
- Deployed on Oxygen (Shopify's hosting) or any Node.js host

## Project Structure

```
app/
├── routes/
│   ├── ($locale)._index.tsx      # Home page with locale prefix
│   ├── ($locale).products.$handle.tsx  # Product detail page
│   ├── ($locale).collections.$handle.tsx
│   ├── ($locale).cart.tsx        # Cart page
│   ├── ($locale).account.tsx     # Customer account
│   ├── api.predictive-search.tsx # API resource route for search
│   └── [sitemap.xml].tsx         # Dynamic sitemap
├── components/
│   ├── Layout.tsx               # Header, footer, cart drawer
│   ├── ProductCard.tsx
│   ├── ProductForm.tsx          # Variant selector, add to cart
│   └── CartLineItem.tsx
├── lib/
│   ├── fragments.ts             # GraphQL fragments (reusable query pieces)
│   ├── queries.ts               # Storefront API queries
│   ├── mutations.ts             # Cart mutations, customer mutations
│   └── utils.ts                 # Price formatting, image sizing
├── styles/
│   └── app.css                  # Tailwind imports + custom styles
└── root.tsx                     # Root layout, cart provider, analytics
```

## Architecture Rules

- **Storefront API for all data.** Every product, collection, and customer query goes through Shopify's Storefront API via GraphQL. Never use the Admin API from the frontend. it has different auth and rate limits.
- **Hydrogen provides commerce primitives.** Use `<Money>`, `<Image>`, `<CartForm>`, `<VariantSelector>` from `@shopify/hydrogen`. They handle currency formatting, responsive images, and cart mutations correctly. Never reimplement these.
- **GraphQL fragments for reusable selections.** Define fragments once: `PRODUCT_CARD_FRAGMENT`, `PRODUCT_VARIANT_FRAGMENT`. Import them in queries. Never duplicate field selections across queries.
- **This is Remix under the hood.** All Remix architecture rules apply: `loader` for reads, `action` for writes (cart mutations), nested routes for layouts, progressive enhancement.
- **Locale-prefixed routes.** Use `($locale)` optional segment for multi-market support. All routes are locale-aware. The locale determines currency, language, and pricing context.

## Coding Conventions

- **Named fragments in separate files.** `lib/fragments.ts` exports every fragment. Queries in `lib/queries.ts` import and compose them. Never write inline fragments in route files.
- **Use Hydrogen's analytics.** `<Analytics.PageView>` and `sendShopifyAnalytics()` for conversion tracking. Not custom analytics that bypass Shopify's attribution.
- **Cart mutations through `<CartForm>`.** Never call the Storefront API directly for cart operations. `<CartForm action={CartForm.ACTIONS.LinesAdd}>` handles optimistic UI, error recovery, and session management.
- **Image sizing:** use `<Image>` from `@shopify/hydrogen` with `aspectRatio` and `sizes` props. It generates responsive `srcset` and uses Shopify's CDN transforms. Never use raw `<img>` tags for product images.
- **Price rendering:** use `<Money data={price}>` component. It handles currency formatting, locale-aware decimal separators, and compare-at-price display. Never format prices with `toFixed(2)`.

## NEVER DO THIS

1. **Never query the Admin API from the storefront.** The Admin API requires different credentials, has lower rate limits, and exposes data customers shouldn't see. Use the Storefront API exclusively.
2. **Never hardcode prices or currency.** Use `<Money>` component. Hardcoded `$` symbols break for EUR, GBP, and any multi-currency store.
3. **Never build a custom cart.** Hydrogen's `<CartForm>` and cart utilities handle cart cookies, Storefront API cart mutations, buyer identity, and discount codes. Custom carts miss edge cases.
4. **Never skip SEO meta.** Every product and collection page must return `seo` data from the `loader`. Hydrogen's `<Seo>` component renders proper meta tags. Missing meta = invisible to search engines.
5. **Never duplicate GraphQL fragment fields.** If you're selecting `title`, `handle`, `images` in multiple queries, extract it to a fragment. Duplicate selections drift apart and cause inconsistent data across pages.
6. **Never ignore Shopify's rate limits.** The Storefront API has a calculated cost-based rate limit. Use `storefront.query()` (Hydrogen's client). it handles retries. Raw `fetch` to the API doesn't.
7. **Never use `getProductById` when `getProductByHandle` works.** Handles are human-readable URL slugs. IDs are opaque GIDs. Routes use handles (`/products/cool-shirt`). Use handle-based queries in loaders.

## Testing

- Use Vitest for unit tests on utilities, price formatting, and helper functions.
- Use Playwright for E2E tests against a dev store. test add to cart, checkout flow, collection browsing.
- Test with multiple locales to verify currency and language switching.
- Test against Shopify's API with the Hydrogen dev server (`shopify hydrogen dev`).

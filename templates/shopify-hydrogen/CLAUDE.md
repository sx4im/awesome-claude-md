# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

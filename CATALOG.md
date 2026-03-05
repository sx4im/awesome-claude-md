# Template Catalog

A quick reference for every CLAUDE.md template in this repo. Pick the one that matches your stack, copy it to your project root, and replace the `[PLACEHOLDERS]`.

| Template | Stack | Key Libraries | Lines | Last Updated |
|----------|-------|---------------|-------|--------------|
| [nextjs](templates/nextjs/CLAUDE.md) | Next.js 14+ App Router, TypeScript | Tailwind, Prisma, Zod, date-fns, TanStack Query | ~84 | 2026-03-05 |
| [react-vite](templates/react-vite/CLAUDE.md) | React 18, TypeScript, Vite | TanStack Query, Zustand, Tailwind, react-hook-form | ~82 | 2026-03-05 |
| [python-fastapi](templates/python-fastapi/CLAUDE.md) | Python 3.11+, FastAPI | SQLAlchemy 2.0, Pydantic v2, Alembic, passlib | ~88 | 2026-03-05 |
| [flutter](templates/flutter/CLAUDE.md) | Flutter 3.x, Dart 3.x | Riverpod, GoRouter, Freezed, Dio, mocktail | ~91 | 2026-03-05 |
| [saas-fullstack](templates/saas-fullstack/CLAUDE.md) | Next.js 14, TypeScript, Full-stack SaaS | Prisma, Stripe, Clerk/Auth.js, Resend, React Email | ~96 | 2026-03-05 |
| [monorepo](templates/monorepo/CLAUDE.md) | Turborepo, pnpm workspaces | TypeScript, shared packages, Vitest | ~109 | 2026-03-05 |
| [ml-python](templates/ml-python/CLAUDE.md) | Python 3.11+, ML/Data Science | PyTorch, scikit-learn, MLflow, polars, FastAPI | ~113 | 2026-03-05 |
| [open-source-lib](templates/open-source-lib/CLAUDE.md) | TypeScript library | Vitest, tsup, Changesets, GitHub Actions | ~119 | 2026-03-05 |
| [django](templates/django/CLAUDE.md) | Python 3.11+, Django 5.x | Django REST Framework, PostgreSQL, Celery, Redis | ~98 | 2026-03-05 |
| [express-typescript](templates/express-typescript/CLAUDE.md) | Node.js 20+, Express, TypeScript | Prisma, Zod, JWT, Vitest | ~91 | 2026-03-05 |
| [go-api](templates/go-api/CLAUDE.md) | Go 1.22+, API Server | Chi, PostgreSQL, sqlc, slog | ~89 | 2026-03-05 |
| [react-native-expo](templates/react-native-expo/CLAUDE.md) | React Native 0.73+, Expo SDK 50+ | Expo Router, TanStack Query, Zustand, SecureStore | ~86 | 2026-03-05 |
| [sveltekit](templates/sveltekit/CLAUDE.md) | SvelteKit 2.x, Svelte 5 (Runes) | TypeScript, Tailwind, Drizzle ORM | ~85 | 2026-03-05 |
| [nuxt](templates/nuxt/CLAUDE.md) | Nuxt 3.x, Vue 3 (Composition API) | TypeScript, Pinia, Tailwind/UnoCSS, Nitro | ~91 | 2026-03-05 |
| [chrome-extension](templates/chrome-extension/CLAUDE.md) | Chrome Extension Manifest V3 | TypeScript, Vite, CRXJS, React | ~84 | 2026-03-05 |
| [cli-node](templates/cli-node/CLAUDE.md) | Node.js CLI Tool | TypeScript, Commander, Chalk, Inquirer, tsup | ~83 | 2026-03-05 |
| [astro](templates/astro/CLAUDE.md) | Astro 4.x, Static Content Site | TypeScript, Content Collections, MDX, Tailwind | ~95 | 2026-03-05 |
| [rust-axum](templates/rust-axum/CLAUDE.md) | Rust 2024, Web API | Axum 0.7+, SQLx, Tokio, Tower | ~85 | 2026-03-05 |
| [electron](templates/electron/CLAUDE.md) | Electron 28+, Desktop App | React 18, TypeScript, Vite, IPC, Zustand | ~87 | 2026-03-05 |
| [laravel](templates/laravel/CLAUDE.md) | PHP 8.2+, Laravel 11.x | Eloquent, Redis Queues, Sanctum, Pint | ~94 | 2026-03-05 |

---

## Community Templates

*No community templates yet.* Want to add one?

1. Read the [Contributing Guide](CONTRIBUTING.md)
2. Create a new directory under `templates/` with your stack name
3. Write a `CLAUDE.md` following the template structure requirements (80–150 lines, opinionated, stack-specific)
4. Run `python scripts/validate.py` to make sure it passes
5. Open a PR — community templates will be listed in this section

<!-- COMMUNITY_TEMPLATES_START -->
<!-- Add community templates here via PR. Format: -->
<!-- | [template-name](templates/template-name/CLAUDE.md) | Stack description | Key Libraries | ~lines | YYYY-MM-DD | -->
<!-- COMMUNITY_TEMPLATES_END -->

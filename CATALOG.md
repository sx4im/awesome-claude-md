# Template Catalog

A quick reference for every CLAUDE.md template in this repo. Pick the one that matches your stack, copy it to your project root, and replace the `[PLACEHOLDERS]`.

## Frontend

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [nextjs](templates/nextjs/CLAUDE.md) | Next.js 14+ App Router, TypeScript | Tailwind, Prisma, Zod, TanStack Query | 84 |
| [react-vite](templates/react-vite/CLAUDE.md) | React 18, TypeScript, Vite | TanStack Query, Zustand, Tailwind | 82 |
| [sveltekit](templates/sveltekit/CLAUDE.md) | SvelteKit 2.x, Svelte 5 (runes) | Tailwind, Drizzle ORM, Lucia, superforms | 85 |
| [nuxt](templates/nuxt/CLAUDE.md) | Nuxt 3.x, Vue 3, Composition API | Pinia, Tailwind, Zod, VeeValidate | 91 |
| [remix](templates/remix/CLAUDE.md) | Remix 2.x, React 18 | Prisma, conform, remix-auth | 73 |
| [astro](templates/astro/CLAUDE.md) | Astro 4.x, TypeScript | Content Collections, MDX, Pagefind | 95 |
| [angular](templates/angular/CLAUDE.md) | Angular 17+, Signals | NgRx Signal Store, Angular Material | 78 |
| [qwik](templates/qwik/CLAUDE.md) | Qwik, Qwik City, TypeScript | Resumable, $ optimizer, routeLoader$ | 69 |
| [solidjs](templates/solidjs/CLAUDE.md) | SolidJS, SolidStart | Fine-grained signals, createResource | 72 |
| [threejs-r3f](templates/threejs-r3f/CLAUDE.md) | React Three Fiber, Drei | Rapier physics, Zustand, GSAP | 80 |
| [htmx-go](templates/htmx-go/CLAUDE.md) | Go, HTMX, Templ | Tailwind, sqlc, Air hot-reload | 78 |

## Full-Stack

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [t3-stack](templates/t3-stack/CLAUDE.md) | tRPC, Next.js, Prisma | NextAuth, Zod, @t3-oss/env-nextjs | 82 |
| [saas-fullstack](templates/saas-fullstack/CLAUDE.md) | Next.js 14, TypeScript | Stripe, Clerk, Resend, Prisma | 96 |
| [supabase-nextjs](templates/supabase-nextjs/CLAUDE.md) | Next.js, Supabase | Supabase Auth, RLS, Realtime, Storage | 79 |
| [shopify-hydrogen](templates/shopify-hydrogen/CLAUDE.md) | Hydrogen, Remix | Storefront API, Tailwind | 70 |
| [payload-cms](templates/payload-cms/CLAUDE.md) | Payload CMS 3.x, Next.js | Lexical rich text, Drizzle | 83 |

## Backend

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [python-fastapi](templates/python-fastapi/CLAUDE.md) | Python 3.11+, FastAPI | SQLAlchemy 2.0, Pydantic v2, Alembic | 88 |
| [django](templates/django/CLAUDE.md) | Django 5.x, DRF | Celery, Redis, django-allauth, pytest | 98 |
| [express-typescript](templates/express-typescript/CLAUDE.md) | Express 4.x, TypeScript | Prisma, Zod, Pino, jose | 91 |
| [go-api](templates/go-api/CLAUDE.md) | Go 1.22+, Chi | sqlc, pgx, slog, testcontainers | 89 |
| [rust-axum](templates/rust-axum/CLAUDE.md) | Rust, Axum 0.7+ | SQLx, Tokio, Tower, serde, tracing | 85 |
| [spring-boot](templates/spring-boot/CLAUDE.md) | Java 21+, Spring Boot 3.2 | JPA, MapStruct, Flyway, Testcontainers | 83 |
| [dotnet-api](templates/dotnet-api/CLAUDE.md) | .NET 8, C# 12 | EF Core, MediatR, FluentValidation | 81 |
| [laravel](templates/laravel/CLAUDE.md) | PHP 8.2+, Laravel 11 | Eloquent, Sanctum, Filament, Pest | 94 |
| [graphql-api](templates/graphql-api/CLAUDE.md) | Apollo/Yoga, TypeScript | Pothos, Prisma, DataLoader | 75 |
| [firebase-functions](templates/firebase-functions/CLAUDE.md) | Cloud Functions v2, TypeScript | Firestore, Firebase Auth, Zod | 78 |
| [nestjs](templates/nestjs/CLAUDE.md) | NestJS 10+, TypeScript | Prisma, class-validator, Passport | 78 |
| [elixir-phoenix](templates/elixir-phoenix/CLAUDE.md) | Elixir, Phoenix 1.7+, Ecto | LiveView, PubSub, Oban | 80 |
| [ruby-on-rails](templates/ruby-on-rails/CLAUDE.md) | Ruby 3.2+, Rails 7.1+ | Hotwire, Sidekiq, RSpec, Pagy | 79 |
| [grpc-go](templates/grpc-go/CLAUDE.md) | Go, gRPC, Connect RPC | Protobuf, Buf, sqlc, Zap | 74 |

## Mobile

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [flutter](templates/flutter/CLAUDE.md) | Flutter 3.x, Dart 3.x | Riverpod, GoRouter, Freezed, Dio | 91 |
| [react-native-expo](templates/react-native-expo/CLAUDE.md) | Expo SDK 50+, TypeScript | Expo Router, TanStack Query, SecureStore | 86 |
| [swift-ios](templates/swift-ios/CLAUDE.md) | SwiftUI, Swift 5.9+ | Swift Concurrency, SwiftData, Keychain | 76 |
| [kotlin-android](templates/kotlin-android/CLAUDE.md) | Jetpack Compose, Kotlin | Hilt, Room, Retrofit, Coil | 86 |

## Desktop

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [electron](templates/electron/CLAUDE.md) | Electron 28+, React, TypeScript | Vite, electron-builder, Zustand | 87 |
| [tauri](templates/tauri/CLAUDE.md) | Tauri 2.x, Rust + React | rusqlite, contextBridge, tauri plugins | 76 |

## CLI & Tools

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [cli-node](templates/cli-node/CLAUDE.md) | Node.js 20+, TypeScript | Commander, Chalk, Ora, Inquirer | 83 |
| [rust-cli](templates/rust-cli/CLAUDE.md) | Rust (stable) | clap, thiserror, anyhow, indicatif | 77 |
| [chrome-extension](templates/chrome-extension/CLAUDE.md) | Chrome MV3, TypeScript | Vite, CRXJS, contextBridge | 84 |
| [telegram-bot](templates/telegram-bot/CLAUDE.md) | Python 3.11+ | python-telegram-bot v20+, SQLAlchemy | 79 |

## DevOps & Infra

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [docker-compose](templates/docker-compose/CLAUDE.md) | Docker, Compose v2 | Multi-stage builds, health checks | 96 |
| [terraform](templates/terraform/CLAUDE.md) | Terraform 1.6+, HCL | AWS/GCP/Azure providers, tflint | 93 |
| [aws-cdk](templates/aws-cdk/CLAUDE.md) | AWS CDK v2, TypeScript | CloudFormation, L3 constructs, esbuild | 74 |

## Specialized

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [monorepo](templates/monorepo/CLAUDE.md) | Turborepo, pnpm workspaces | TypeScript, shared packages | 109 |
| [ml-python](templates/ml-python/CLAUDE.md) | Python 3.11+, ML/Data Science | PyTorch, MLflow, polars, FastAPI | 113 |
| [open-source-lib](templates/open-source-lib/CLAUDE.md) | TypeScript library | Vitest, tsup, Changesets | 119 |
| [unity-csharp](templates/unity-csharp/CLAUDE.md) | Unity 2022+, C# | URP, DOTween, Input System | 76 |
| [deno-fresh](templates/deno-fresh/CLAUDE.md) | Deno, Fresh 2.x, Preact | Deno KV, Tailwind, deno test | 80 |
| [solidity-hardhat](templates/solidity-hardhat/CLAUDE.md) | Solidity 0.8+, Hardhat | Ethers.js v6, OpenZeppelin, TypeChain | 70 |
| [wordpress-theme](templates/wordpress-theme/CLAUDE.md) | WordPress 6.x, PHP 8.1+ | Gutenberg, ACF, @wordpress/scripts | 75 |

---

## Community Templates

*No community templates yet.* Want to add one?

1. Read the [Contributing Guide](CONTRIBUTING.md)
2. Create a new directory under `templates/` with your stack name
3. Write a `CLAUDE.md` following the template structure requirements (50+ lines, opinionated, stack-specific)
4. Run `python scripts/validate.py` to make sure it passes
5. Open a PR

<!-- COMMUNITY_TEMPLATES_START -->
<!-- COMMUNITY_TEMPLATES_END -->

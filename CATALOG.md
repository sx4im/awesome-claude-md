# Template Catalog

A quick reference for every CLAUDE.md template in this repo. Pick the one that matches your stack, copy it to your project root, and replace the `[PLACEHOLDERS]`.

## Frontend

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [nextjs](templates/nextjs/CLAUDE.md) | Next.js 14+ App Router, TypeScript | Tailwind, Prisma, Zod, TanStack Query | 84 |
| [react-vite](templates/react-vite/CLAUDE.md) | React 18, TypeScript, Vite | TanStack Query, Zustand, Tailwind | 82 |
| [vue-vite](templates/vue-vite/CLAUDE.md) | Vue 3, Vite, Composition API | Pinia, Vue Router, Tailwind, VueUse | 87 |
| [sveltekit](templates/sveltekit/CLAUDE.md) | SvelteKit 2.x, Svelte 5 (runes) | Tailwind, Drizzle ORM, Lucia, superforms | 85 |
| [nuxt](templates/nuxt/CLAUDE.md) | Nuxt 3.x, Vue 3, Composition API | Pinia, Tailwind, Zod, VeeValidate | 91 |
| [remix](templates/remix/CLAUDE.md) | Remix 2.x, React 18 | Prisma, conform, remix-auth | 73 |
| [astro](templates/astro/CLAUDE.md) | Astro 4.x, TypeScript | Content Collections, MDX, Pagefind | 95 |
| [angular](templates/angular/CLAUDE.md) | Angular 17+, Signals | NgRx Signal Store, Angular Material | 78 |
| [gatsby](templates/gatsby/CLAUDE.md) | Gatsby 5, GraphQL, TypeScript | MDX, gatsby-image, Tailwind | 96 |
| [qwik](templates/qwik/CLAUDE.md) | Qwik, Qwik City, TypeScript | Resumable, $ optimizer, routeLoader$ | 69 |
| [solidjs](templates/solidjs/CLAUDE.md) | SolidJS, SolidStart | Fine-grained signals, createResource | 72 |
| [preact](templates/preact/CLAUDE.md) | Preact, Signals, Vite | preact/compat, @preact/signals | 83 |
| [lit-components](templates/lit-components/CLAUDE.md) | Lit 3.x, Web Components | @lit/reactive-element, Shadow DOM | 93 |
| [eleventy](templates/eleventy/CLAUDE.md) | Eleventy 3.x, Nunjucks, WebC | Markdown, data cascade, collections | 100 |
| [threejs-r3f](templates/threejs-r3f/CLAUDE.md) | React Three Fiber, Drei | Rapier physics, Zustand, GSAP | 80 |
| [htmx-go](templates/htmx-go/CLAUDE.md) | Go, HTMX, Templ | Tailwind, sqlc, Air hot-reload | 78 |

## Full-Stack

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [t3-stack](templates/t3-stack/CLAUDE.md) | tRPC, Next.js, Prisma | NextAuth, Zod, @t3-oss/env-nextjs | 82 |
| [saas-fullstack](templates/saas-fullstack/CLAUDE.md) | Next.js 14, TypeScript | Stripe, Clerk, Resend, Prisma | 96 |
| [supabase-nextjs](templates/supabase-nextjs/CLAUDE.md) | Next.js, Supabase | Supabase Auth, RLS, Realtime, Storage | 79 |
| [convex-nextjs](templates/convex-nextjs/CLAUDE.md) | Convex, Next.js, TypeScript | Reactive queries, mutations, actions | 89 |
| [redwoodjs](templates/redwoodjs/CLAUDE.md) | RedwoodJS, GraphQL, Prisma | Cells, services, SDL-first schema | 93 |
| [blitzjs](templates/blitzjs/CLAUDE.md) | BlitzJS, Prisma, TypeScript | RPC mutations/queries, sessions | 97 |
| [wasp](templates/wasp/CLAUDE.md) | Wasp DSL, React, Node.js | Declarative auth, jobs, CRUD | 88 |
| [meteor](templates/meteor/CLAUDE.md) | Meteor, React, MongoDB | DDP, pub/sub, methods, Tracker | 90 |
| [shopify-hydrogen](templates/shopify-hydrogen/CLAUDE.md) | Hydrogen, Remix | Storefront API, Tailwind | 70 |
| [payload-cms](templates/payload-cms/CLAUDE.md) | Payload CMS 3.x, Next.js | Lexical rich text, Drizzle | 83 |

## Backend

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [python-fastapi](templates/python-fastapi/CLAUDE.md) | Python 3.11+, FastAPI | SQLAlchemy 2.0, Pydantic v2, Alembic | 88 |
| [django](templates/django/CLAUDE.md) | Django 5.x, DRF | Celery, Redis, django-allauth, pytest | 98 |
| [flask](templates/flask/CLAUDE.md) | Flask, Python 3.11+ | SQLAlchemy, Marshmallow, Celery, Blueprint | 86 |
| [express-typescript](templates/express-typescript/CLAUDE.md) | Express 4.x, TypeScript | Prisma, Zod, Pino, jose | 91 |
| [nestjs](templates/nestjs/CLAUDE.md) | NestJS 10+, TypeScript | Prisma, class-validator, Passport | 78 |
| [fastify](templates/fastify/CLAUDE.md) | Fastify, TypeScript | JSON Schema, Prisma, Pino | 90 |
| [hono](templates/hono/CLAUDE.md) | Hono, TypeScript | Zod OpenAPI, Cloudflare Workers/Bun | 92 |
| [adonisjs](templates/adonisjs/CLAUDE.md) | AdonisJS 6, TypeScript | Lucid ORM, Edge, Vine validation | 90 |
| [koa-typescript](templates/koa-typescript/CLAUDE.md) | Koa, TypeScript | TypeORM, middleware, Joi | 99 |
| [trpc-standalone](templates/trpc-standalone/CLAUDE.md) | tRPC, TypeScript, Zod | Standalone server, subscriptions | 88 |
| [go-api](templates/go-api/CLAUDE.md) | Go 1.22+, Chi | sqlc, pgx, slog, testcontainers | 89 |
| [gin-go](templates/gin-go/CLAUDE.md) | Go, Gin | GORM, Swagger, structured logging | 93 |
| [fiber-go](templates/fiber-go/CLAUDE.md) | Go, Fiber v2 | GORM/sqlc, JWT, rate limiting | 93 |
| [grpc-go](templates/grpc-go/CLAUDE.md) | Go, gRPC, Connect RPC | Protobuf, Buf, sqlc, Zap | 74 |
| [rust-axum](templates/rust-axum/CLAUDE.md) | Rust, Axum 0.7+ | SQLx, Tokio, Tower, serde, tracing | 85 |
| [actix-web](templates/actix-web/CLAUDE.md) | Rust, Actix-web 4 | SQLx, Tokio, serde, middleware | 91 |
| [spring-boot](templates/spring-boot/CLAUDE.md) | Java 21+, Spring Boot 3.2 | JPA, MapStruct, Flyway, Testcontainers | 83 |
| [ktor](templates/ktor/CLAUDE.md) | Kotlin, Ktor | Exposed ORM, Koin, kotlinx.serialization | 100 |
| [scala-play](templates/scala-play/CLAUDE.md) | Scala 3, Play Framework | Slick, Akka/Pekko, sbt | 95 |
| [dotnet-api](templates/dotnet-api/CLAUDE.md) | .NET 8, C# 12 | EF Core, MediatR, FluentValidation | 81 |
| [laravel](templates/laravel/CLAUDE.md) | PHP 8.2+, Laravel 11 | Eloquent, Sanctum, Filament, Pest | 94 |
| [ruby-on-rails](templates/ruby-on-rails/CLAUDE.md) | Ruby 3.2+, Rails 7.1+ | Hotwire, Sidekiq, RSpec, Pagy | 79 |
| [elixir-phoenix](templates/elixir-phoenix/CLAUDE.md) | Elixir, Phoenix 1.7+, Ecto | LiveView, PubSub, Oban | 80 |
| [graphql-api](templates/graphql-api/CLAUDE.md) | Apollo/Yoga, TypeScript | Pothos, Prisma, DataLoader | 75 |
| [firebase-functions](templates/firebase-functions/CLAUDE.md) | Cloud Functions v2, TypeScript | Firestore, Firebase Auth, Zod | 78 |

## AI & ML

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [langchain-python](templates/langchain-python/CLAUDE.md) | LangChain, Python 3.11+ | LCEL, vector stores, structured output | 94 |
| [rag-pipeline](templates/rag-pipeline/CLAUDE.md) | Python, embeddings, vector DB | Pinecone/Chroma/Qdrant, chunking, eval | 99 |
| [llm-api](templates/llm-api/CLAUDE.md) | OpenAI/Anthropic SDK, TypeScript | Streaming, function calling, rate limiting | 94 |
| [huggingface](templates/huggingface/CLAUDE.md) | Transformers, Python | PEFT/LoRA, Datasets, Trainer | 100 |
| [ml-python](templates/ml-python/CLAUDE.md) | Python 3.11+, ML/Data Science | PyTorch, MLflow, polars, FastAPI | 113 |
| [jupyter-data-science](templates/jupyter-data-science/CLAUDE.md) | Jupyter, Python | pandas/polars, scikit-learn, plotly | 91 |
| [data-pipeline](templates/data-pipeline/CLAUDE.md) | Airflow/Dagster, Python | dbt, data transforms, scheduling | 101 |

## Mobile

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [flutter](templates/flutter/CLAUDE.md) | Flutter 3.x, Dart 3.x | Riverpod, GoRouter, Freezed, Dio | 91 |
| [react-native-expo](templates/react-native-expo/CLAUDE.md) | Expo SDK 50+, TypeScript | Expo Router, TanStack Query, SecureStore | 86 |
| [ionic-capacitor](templates/ionic-capacitor/CLAUDE.md) | Ionic 7+, Capacitor | Angular/React, native plugins | 84 |
| [swift-ios](templates/swift-ios/CLAUDE.md) | SwiftUI, Swift 5.9+ | Swift Concurrency, SwiftData, Keychain | 76 |
| [kotlin-android](templates/kotlin-android/CLAUDE.md) | Jetpack Compose, Kotlin | Hilt, Room, Retrofit, Coil | 86 |
| [dotnet-maui](templates/dotnet-maui/CLAUDE.md) | .NET MAUI, C# | CommunityToolkit, MVVM | 97 |

## Desktop

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [electron](templates/electron/CLAUDE.md) | Electron 28+, React, TypeScript | Vite, electron-builder, Zustand | 87 |
| [tauri](templates/tauri/CLAUDE.md) | Tauri 2.x, Rust + React | rusqlite, contextBridge, tauri plugins | 76 |

## CLI & Tools

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [cli-node](templates/cli-node/CLAUDE.md) | Node.js 20+, TypeScript | Commander, Chalk, Ora, Inquirer | 83 |
| [cli-python](templates/cli-python/CLAUDE.md) | Python 3.11+, Typer | Rich, Click, pyproject.toml | 96 |
| [cli-go](templates/cli-go/CLAUDE.md) | Go, Cobra | Viper, Bubble Tea, GoReleaser | 89 |
| [rust-cli](templates/rust-cli/CLAUDE.md) | Rust (stable) | clap, thiserror, anyhow, indicatif | 77 |
| [vscode-extension](templates/vscode-extension/CLAUDE.md) | VS Code API, TypeScript | Extension API, webview, LSP | 97 |
| [chrome-extension](templates/chrome-extension/CLAUDE.md) | Chrome MV3, TypeScript | Vite, CRXJS, contextBridge | 84 |

## Testing

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [playwright](templates/playwright/CLAUDE.md) | Playwright, TypeScript | Page Object Model, fixtures, traces | 79 |
| [cypress](templates/cypress/CLAUDE.md) | Cypress, TypeScript | Custom commands, intercepts, fixtures | 85 |

## DevOps & Infra

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [docker-compose](templates/docker-compose/CLAUDE.md) | Docker, Compose v2 | Multi-stage builds, health checks | 96 |
| [kubernetes](templates/kubernetes/CLAUDE.md) | Kubernetes, Kustomize | kubectl, manifests, ConfigMaps | 94 |
| [helm-chart](templates/helm-chart/CLAUDE.md) | Helm 3, Go templates | Values, dependencies, hooks | 88 |
| [terraform](templates/terraform/CLAUDE.md) | Terraform 1.6+, HCL | AWS/GCP/Azure providers, tflint | 93 |
| [pulumi](templates/pulumi/CLAUDE.md) | Pulumi, TypeScript | Component resources, stacks, secrets | 92 |
| [aws-cdk](templates/aws-cdk/CLAUDE.md) | AWS CDK v2, TypeScript | CloudFormation, L3 constructs, esbuild | 74 |
| [github-actions](templates/github-actions/CLAUDE.md) | GitHub Actions, YAML | Reusable workflows, matrix, composite | 80 |
| [ansible](templates/ansible/CLAUDE.md) | Ansible, Jinja2, YAML | Roles, inventory, Galaxy collections | 96 |

## Bots & Plugins

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [discord-bot](templates/discord-bot/CLAUDE.md) | discord.js v14, TypeScript | Slash commands, embeds, components | 99 |
| [slack-bot](templates/slack-bot/CLAUDE.md) | Bolt.js, TypeScript | Block Kit, events API, slash commands | 84 |
| [telegram-bot](templates/telegram-bot/CLAUDE.md) | Python 3.11+ | python-telegram-bot v20+, SQLAlchemy | 79 |
| [obsidian-plugin](templates/obsidian-plugin/CLAUDE.md) | Obsidian API, TypeScript | Plugin API, settings, views, modals | 81 |
| [figma-plugin](templates/figma-plugin/CLAUDE.md) | Figma Plugin API, TypeScript | UI messaging, node traversal | 82 |
| [raycast-extension](templates/raycast-extension/CLAUDE.md) | Raycast API, React | Preferences, commands, actions | 83 |

## Game Dev

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [unity-csharp](templates/unity-csharp/CLAUDE.md) | Unity 2022+, C# | URP, DOTween, Input System | 76 |
| [godot-gdscript](templates/godot-gdscript/CLAUDE.md) | Godot 4.x, GDScript | Scene tree, signals, resources | 86 |
| [unreal-cpp](templates/unreal-cpp/CLAUDE.md) | Unreal Engine 5, C++ | Gameplay framework, UObject, Blueprints | 94 |

## Specialized

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [monorepo](templates/monorepo/CLAUDE.md) | Turborepo, pnpm workspaces | TypeScript, shared packages | 109 |
| [open-source-lib](templates/open-source-lib/CLAUDE.md) | TypeScript library | Vitest, tsup, Changesets | 119 |
| [stripe-integration](templates/stripe-integration/CLAUDE.md) | Stripe SDK, TypeScript | Webhooks, checkout, subscriptions | 85 |
| [websocket-node](templates/websocket-node/CLAUDE.md) | ws/Socket.IO, TypeScript | Rooms, auth, reconnection | 85 |
| [wasm-rust](templates/wasm-rust/CLAUDE.md) | Rust, wasm-bindgen | wasm-pack, js-sys, web-sys | 83 |
| [embedded-rust](templates/embedded-rust/CLAUDE.md) | Rust no_std, embassy | HAL, RTIC, probe-rs | 87 |
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

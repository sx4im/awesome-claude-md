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
| [alpine-js](templates/alpine-js/CLAUDE.md) | Alpine.js 3.14, Tailwind CSS 4 | HTMX 2, Alpine Plugins, Vite 5 | 97 |
| [analog-angular](templates/analog-angular/CLAUDE.md) | Analog.js 1.x, Angular 18, Vite 5 | Angular Material, TanStack Query, Zod | 105 |
| [ember-js](templates/ember-js/CLAUDE.md) | Ember.js 5.x, TypeScript | Ember Data, Embroider, Ember Concurrency | 121 |
| [fresh-preact](templates/fresh-preact/CLAUDE.md) | Deno Fresh 2.x, Preact 10 | Preact Signals, Deno KV, Tailwind | 111 |
| [docusaurus](templates/docusaurus/CLAUDE.md) | Docusaurus 3.6, React 18, MDX 3 | Algolia DocSearch, Mermaid, Prism | 98 |
| [svelte5-runes](templates/svelte5-runes/CLAUDE.md) | Svelte 5, SvelteKit 2, Vite 5 | Superforms, Zod, Drizzle ORM, Lucia Auth | 92 |
| [storybook-react](templates/storybook-react/CLAUDE.md) | Storybook 8, React 18, Vite 5 | Chromatic, MSW 2, Tailwind CSS 4 | 96 |
| [htmx-django](templates/htmx-django/CLAUDE.md) | Django 5.1+, htmx 2.0, Python | Alpine.js, django-htmx, Tailwind CSS | 110 |
| [htmx-flask](templates/htmx-flask/CLAUDE.md) | Flask 3.1, HTMX 2.0, Jinja2 | SQLAlchemy 2.0, WTForms, Tailwind CSS 4 | 119 |
| [web-components](templates/web-components/CLAUDE.md) | Native Web Components, Shadow DOM | TypeScript, Vite 5, Web Test Runner | 113 |
| [tanstack-start](templates/tanstack-start/CLAUDE.md) | TanStack Start 1.x, React 19 | TanStack Router, TanStack Query, Vinxi | 98 |
| [pixi-js](templates/pixi-js/CLAUDE.md) | PixiJS 8.x, TypeScript | @pixi/sound, @pixi/spine, gsap | 103 |
| [babylon-js](templates/babylon-js/CLAUDE.md) | Babylon.js 7.x, TypeScript | Havok physics, GUI, Inspector, Loaders | 110 |
| [webgpu-wgsl](templates/webgpu-wgsl/CLAUDE.md) | WebGPU API, WGSL, TypeScript | Vite 5, wgpu-matrix, lil-gui | 114 |

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
| [clerk-nextjs](templates/clerk-nextjs/CLAUDE.md) | Next.js 14+, Clerk v5, TypeScript | Drizzle ORM, Tailwind CSS, Zod | 102 |
| [drizzle-nextjs](templates/drizzle-nextjs/CLAUDE.md) | Next.js 15, Drizzle ORM, PostgreSQL | Tailwind CSS 4, Zod, NextAuth.js v5 | 105 |
| [directus](templates/directus/CLAUDE.md) | Directus 11.x, PostgreSQL | Directus SDK, Flows, custom extensions | 106 |
| [keystone-js](templates/keystone-js/CLAUDE.md) | KeystoneJS 6, TypeScript, PostgreSQL | GraphQL, Prisma, Admin UI | 100 |
| [medusa-js](templates/medusa-js/CLAUDE.md) | Medusa.js 2.x, TypeScript | MikroORM, Redis, Medusa Workflows | 111 |
| [strapi-v5](templates/strapi-v5/CLAUDE.md) | Strapi v5, TypeScript, PostgreSQL | Document Service API, RBAC, Cloudinary | 106 |
| [supabase-realtime](templates/supabase-realtime/CLAUDE.md) | Supabase, Next.js 14, React 18+ | Realtime, RLS, Edge Functions | 110 |
| [pocketbase](templates/pocketbase/CLAUDE.md) | PocketBase 0.23+, Go 1.22+ | SSE realtime, SQLite, PocketBase SDK | 95 |
| [vercel-ai](templates/vercel-ai/CLAUDE.md) | Next.js 15, Vercel AI SDK 4.x | OpenAI, Anthropic, Drizzle ORM, shadcn/ui | 109 |

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
| [bun-elysia](templates/bun-elysia/CLAUDE.md) | Bun 1.1+, Elysia.js 1.x | TypeBox, Eden Treaty, Drizzle ORM | 93 |
| [deno-deploy](templates/deno-deploy/CLAUDE.md) | Deno 2.x, Hono v4 | Deno KV, Deno Deploy, import maps | 96 |
| [deno-oak](templates/deno-oak/CLAUDE.md) | Deno 2.x, Oak 16+ | Deno KV, Zod, djwt | 94 |
| [swift-vapor](templates/swift-vapor/CLAUDE.md) | Swift 5.9+, Vapor 4 | Fluent ORM, PostgreSQL, Redis, JWT | 93 |
| [clojure-ring](templates/clojure-ring/CLAUDE.md) | Clojure 1.12, Ring 1.12, JVM 21 | Compojure, next.jdbc, HoneySQL, nREPL | 95 |
| [haskell-servant](templates/haskell-servant/CLAUDE.md) | Haskell GHC 9.6+, Servant 0.20 | Persistent, Esqueleto, Aeson, Katip | 97 |
| [crystal-kemal](templates/crystal-kemal/CLAUDE.md) | Crystal 1.12+, Kemal 1.4 | Granite ORM, crystal-pg, ECR templates | 113 |
| [php-symfony](templates/php-symfony/CLAUDE.md) | PHP 8.3+, Symfony 7.1+ | Doctrine ORM 3, Messenger, Twig, PHPStan | 116 |
| [prisma-express](templates/prisma-express/CLAUDE.md) | Express.js 4.x, Prisma 5.x, TypeScript | Zod, Passport.js, Winston, Bull | 101 |
| [mongodb-express](templates/mongodb-express/CLAUDE.md) | Express 4.x, MongoDB 7.x, Mongoose 8.x | Zod, mongodb-memory-server, Jest | 101 |
| [cloudflare-workers](templates/cloudflare-workers/CLAUDE.md) | Cloudflare Workers, Hono v4 | D1, R2, KV, Queues, Wrangler v3 | 94 |
| [nim-web](templates/nim-web/CLAUDE.md) | Nim 2.x, Jester 0.6 | Karax, norm ORM, nimja templates | 102 |
| [ocaml-dream](templates/ocaml-dream/CLAUDE.md) | OCaml 5.x, Dream 1.0 | Dune 3, Caqti, Yojson, Tyxml | 98 |

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
| [gradio-ml](templates/gradio-ml/CLAUDE.md) | Gradio 4.x, Python 3.11+ | Transformers, Hugging Face Hub, torch 2.x | 93 |
| [pytorch-lightning](templates/pytorch-lightning/CLAUDE.md) | PyTorch 2.x, Lightning 2.x, Python | torchmetrics, Hydra, Weights & Biases | 100 |
| [mlflow](templates/mlflow/CLAUDE.md) | MLflow 2.x, Python 3.11+ | scikit-learn, Optuna, PostgreSQL, S3 | 103 |
| [streamlit](templates/streamlit/CLAUDE.md) | Streamlit 1.38+, Python 3.11+ | pandas, Plotly, st-aggrid, SQLAlchemy | 92 |

## Mobile

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [flutter](templates/flutter/CLAUDE.md) | Flutter 3.x, Dart 3.x | Riverpod, GoRouter, Freezed, Dio | 91 |
| [react-native-expo](templates/react-native-expo/CLAUDE.md) | Expo SDK 50+, TypeScript | Expo Router, TanStack Query, SecureStore | 86 |
| [ionic-capacitor](templates/ionic-capacitor/CLAUDE.md) | Ionic 7+, Capacitor | Angular/React, native plugins | 84 |
| [swift-ios](templates/swift-ios/CLAUDE.md) | SwiftUI, Swift 5.9+ | Swift Concurrency, SwiftData, Keychain | 76 |
| [kotlin-android](templates/kotlin-android/CLAUDE.md) | Jetpack Compose, Kotlin | Hilt, Room, Retrofit, Coil | 86 |
| [dotnet-maui](templates/dotnet-maui/CLAUDE.md) | .NET MAUI, C# | CommunityToolkit, MVVM | 97 |
| [expo-router](templates/expo-router/CLAUDE.md) | Expo SDK 52+, Expo Router v4 | NativeWind 4, Zustand 5, TanStack Query 5 | 117 |
| [capacitor-vue](templates/capacitor-vue/CLAUDE.md) | Vue 3.5+, Capacitor 6, Ionic 8 | Pinia, Vue Router, Vitest, Cypress | 108 |
| [jetpack-compose](templates/jetpack-compose/CLAUDE.md) | Kotlin 2.0+, Jetpack Compose, Material 3 | Hilt, Room, Retrofit, Coil 3 | 92 |
| [nativescript-angular](templates/nativescript-angular/CLAUDE.md) | NativeScript 8, Angular 17+ | NgRx Signal Store, NativeScript CLI | 117 |
| [kotlin-multiplatform](templates/kotlin-multiplatform/CLAUDE.md) | Kotlin 2.0+, Compose Multiplatform | Ktor 3, SQLDelight 2, Koin, Decompose | 103 |
| [maui-blazor](templates/maui-blazor/CLAUDE.md) | .NET 9 MAUI Blazor Hybrid, C# 12 | Fluxor, EF Core 9, Refit, Bootstrap 5 | 137 |

## Desktop

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [electron](templates/electron/CLAUDE.md) | Electron 28+, React, TypeScript | Vite, electron-builder, Zustand | 87 |
| [tauri](templates/tauri/CLAUDE.md) | Tauri 2.x, Rust + React | rusqlite, contextBridge, tauri plugins | 76 |
| [avalonia-dotnet](templates/avalonia-dotnet/CLAUDE.md) | Avalonia UI 11+, C# 12, .NET 9 | CommunityToolkit.Mvvm, EF Core 9, SQLite | 120 |
| [compose-desktop](templates/compose-desktop/CLAUDE.md) | Compose for Desktop, Kotlin 2.0+ | Decompose 3, Koin 4, Exposed ORM, Ktor 3 | 119 |
| [wails-go](templates/wails-go/CLAUDE.md) | Wails v2, Go 1.22+, Svelte 5 | SQLite, Tailwind CSS 4, Wails bindings | 112 |
| [swiftui-macos](templates/swiftui-macos/CLAUDE.md) | SwiftUI, Swift 5.10+, macOS 14 | SwiftData, CloudKit, Combine, MVVM | 99 |

## CLI & Tools

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [cli-node](templates/cli-node/CLAUDE.md) | Node.js 20+, TypeScript | Commander, Chalk, Ora, Inquirer | 83 |
| [cli-python](templates/cli-python/CLAUDE.md) | Python 3.11+, Typer | Rich, Click, pyproject.toml | 96 |
| [cli-go](templates/cli-go/CLAUDE.md) | Go, Cobra | Viper, Bubble Tea, GoReleaser | 89 |
| [rust-cli](templates/rust-cli/CLAUDE.md) | Rust (stable) | clap, thiserror, anyhow, indicatif | 77 |
| [vscode-extension](templates/vscode-extension/CLAUDE.md) | VS Code API, TypeScript | Extension API, webview, LSP | 97 |
| [chrome-extension](templates/chrome-extension/CLAUDE.md) | Chrome MV3, TypeScript | Vite, CRXJS, contextBridge | 84 |
| [mcp-server-typescript](templates/mcp-server-typescript/CLAUDE.md) | MCP SDK v1.x, TypeScript 5.4+ | Zod, stdio/SSE transport, tsup, Vitest | 102 |
| [openapi-codegen](templates/openapi-codegen/CLAUDE.md) | OpenAPI 3.1, TypeScript 5.4+ | openapi-typescript, openapi-fetch, Redocly | 104 |
| [puppeteer-node](templates/puppeteer-node/CLAUDE.md) | Puppeteer 22+, TypeScript | Jest, pixelmatch, Page Object Model | 98 |

## Testing

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [playwright](templates/playwright/CLAUDE.md) | Playwright, TypeScript | Page Object Model, fixtures, traces | 79 |
| [cypress](templates/cypress/CLAUDE.md) | Cypress, TypeScript | Custom commands, intercepts, fixtures | 85 |
| [k6-load-testing](templates/k6-load-testing/CLAUDE.md) | Grafana k6 v0.50+, JavaScript ES6 | k6/http, k6/browser, Grafana, InfluxDB | 90 |
| [locust-python](templates/locust-python/CLAUDE.md) | Locust 2.29+, Python 3.12+ | gevent, Faker, pandas, Docker Compose | 100 |

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
| [argocd](templates/argocd/CLAUDE.md) | ArgoCD v2.10+, Kustomize | ApplicationSets, Sealed Secrets, External Secrets | 102 |
| [crossplane](templates/crossplane/CLAUDE.md) | Crossplane v1.15+, Provider AWS | XRDs, Compositions, Functions, Argo CD | 109 |
| [skaffold](templates/skaffold/CLAUDE.md) | Skaffold v2.10+, Kubernetes | Docker, Helm, kustomize, Cloud Code | 114 |
| [tilt-dev](templates/tilt-dev/CLAUDE.md) | Tilt v0.33+, Starlark | kind/k3d, ctlptl, Helm, Tilt Cloud | 116 |
| [dagger-ci](templates/dagger-ci/CLAUDE.md) | Dagger v0.14+, Go SDK | BuildKit, Dagger Cloud, Dagger modules | 103 |
| [earthly-ci](templates/earthly-ci/CLAUDE.md) | Earthly v0.8+, Earthfile | Earthly Satellites, BuildKit, multi-platform | 107 |
| [nix-flake](templates/nix-flake/CLAUDE.md) | Nix v2.20+, Nixpkgs | flake-utils, devenv, home-manager, cachix | 111 |
| [bazel-java](templates/bazel-java/CLAUDE.md) | Bazel 7.x, Java 21, Kotlin 1.9+ | bzlmod, rules_jvm_external, JUnit 5 | 112 |
| [aws-lambda-node](templates/aws-lambda-node/CLAUDE.md) | AWS Lambda Node.js 20, SAM | DynamoDB, esbuild, Powertools, Jest | 96 |
| [aws-step-functions](templates/aws-step-functions/CLAUDE.md) | AWS Step Functions, CDK v2 | Lambda, DynamoDB, SQS, X-Ray | 106 |
| [azure-functions](templates/azure-functions/CLAUDE.md) | Azure Functions v4, TypeScript | Cosmos DB, Service Bus, Entra ID | 98 |
| [lambda-python](templates/lambda-python/CLAUDE.md) | AWS Lambda Python 3.12, SAM | DynamoDB, Pydantic v2, Powertools, moto | 109 |
| [dynamodb-lambda](templates/dynamodb-lambda/CLAUDE.md) | DynamoDB, Lambda Node.js 20, SST v3 | AWS SDK v3, single-table design, Vitest | 102 |
| [netlify-functions](templates/netlify-functions/CLAUDE.md) | Netlify Functions v2, TypeScript | Blob Store, Netlify Identity, Vitest | 97 |
| [supabase-edge](templates/supabase-edge/CLAUDE.md) | Supabase Edge Functions, Deno | PostgREST, Supabase Auth, Storage | 93 |
| [google-cloud-run](templates/google-cloud-run/CLAUDE.md) | Cloud Run, Express.js 4, TypeScript | Cloud SQL, Pub/Sub, Drizzle ORM | 100 |
| [prometheus-grafana](templates/prometheus-grafana/CLAUDE.md) | Prometheus v2.50+, Grafana v10+ | Alertmanager, Thanos, Loki, kube-prometheus | 108 |
| [opentelemetry-node](templates/opentelemetry-node/CLAUDE.md) | OpenTelemetry JS SDK, Node.js 20 | OTLP exporter, Jaeger, Prometheus, Collector | 99 |

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
| [bevy-rust](templates/bevy-rust/CLAUDE.md) | Bevy 0.14+, Rust | bevy_rapier3d, bevy_egui, bevy_kira_audio | 106 |
| [godot-rust](templates/godot-rust/CLAUDE.md) | Godot 4.3+, Rust (gdext) | godot::prelude, serde, ron, GDScript | 113 |
| [defold-lua](templates/defold-lua/CLAUDE.md) | Defold 1.9+, Lua 5.1 | Monarch, Druid UI, DefOS, Nakama | 117 |
| [love2d-lua](templates/love2d-lua/CLAUDE.md) | LOVE 11.5+, Lua 5.1 (LuaJIT) | bump.lua, hump, anim8, push | 101 |
| [phaser-game](templates/phaser-game/CLAUDE.md) | Phaser 3.80+, TypeScript, Vite 5 | Texture Packer, Tiled, Howler.js | 95 |
| [pygame-python](templates/pygame-python/CLAUDE.md) | Pygame 2.5+, Python 3.11+ | pytmx, pyinstaller, pydantic | 117 |
| [raylib-c](templates/raylib-c/CLAUDE.md) | raylib 5.x, C17, CMake 3.20+ | raygui, rres, gcc/clang | 108 |

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
| [r-shiny](templates/r-shiny/CLAUDE.md) | R 4.3+, Shiny 1.8+, golem | bslib, shinytest2, DBI, dbplyr | 102 |
| [turso-libsql](templates/turso-libsql/CLAUDE.md) | Turso, @libsql/client, TypeScript | Drizzle ORM, drizzle-kit, Hono/Next.js | 97 |

## Languages

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [gleam-lustre](templates/gleam-lustre/CLAUDE.md) | Gleam 1.x, BEAM runtime | Lustre 4.x, Wisp, Sqlight, gleam/json | 90 |
| [julia-project](templates/julia-project/CLAUDE.md) | Julia 1.10+, Pkg | Documenter.jl, Pluto.jl, Test stdlib | 91 |
| [v-lang](templates/v-lang/CLAUDE.md) | V 0.4.x, vweb | Built-in ORM, json module, vpm | 115 |
| [zig-project](templates/zig-project/CLAUDE.md) | Zig 0.13.x | build.zig, std.testing, Arena allocators | 81 |
| [sqlite-rust](templates/sqlite-rust/CLAUDE.md) | Rust 1.75+, rusqlite 0.31.x | r2d2-sqlite, serde, tokio, cargo-nextest | 100 |

## Database & Data

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [neo4j-graphql](templates/neo4j-graphql/CLAUDE.md) | Neo4j 5.x, @neo4j/graphql 5.x | Apollo Server 4, Cypher, neo4j-driver | 102 |
| [neon-postgres](templates/neon-postgres/CLAUDE.md) | Neon PostgreSQL, TypeScript | @neondatabase/serverless, Drizzle ORM | 100 |
| [cockroachdb](templates/cockroachdb/CLAUDE.md) | CockroachDB 24.x, Go 1.22+ | pgx 5, sqlc, golang-migrate, chi v5 | 98 |
| [clickhouse-analytics](templates/clickhouse-analytics/CLAUDE.md) | ClickHouse 24.x, Python 3.11+ | clickhouse-connect, dbt-clickhouse, Protobuf | 100 |
| [duckdb-python](templates/duckdb-python/CLAUDE.md) | DuckDB 1.x, Python 3.11+ | PyArrow, Jinja2, Polars, Ibis | 99 |
| [redis-python](templates/redis-python/CLAUDE.md) | Redis 7.2+, Python 3.11+ | redis-py 5.x, hiredis, Pydantic v2 | 93 |
| [polars-python](templates/polars-python/CLAUDE.md) | Polars 1.x, Python 3.11+ | PyArrow, DuckDB, connectorx, Pandera | 94 |
| [spark-pyspark](templates/spark-pyspark/CLAUDE.md) | Apache Spark 3.5+, PySpark | Delta Lake 3, Structured Streaming, Spark SQL | 102 |
| [dbt-project](templates/dbt-project/CLAUDE.md) | dbt Core 1.8+, SQL | SQLFluff, dbt-expectations, dbt-utils | 109 |

## Data Orchestration

| Template | Stack | Key Libraries | Lines |
|----------|-------|---------------|-------|
| [apache-airflow](templates/apache-airflow/CLAUDE.md) | Apache Airflow 2.9+, Python 3.11+ | TaskFlow API, Celery, dbt provider, Slack | 104 |
| [dagster](templates/dagster/CLAUDE.md) | Dagster 1.7+, Python 3.11+ | dagster-dbt, dagster-duckdb, Polars | 107 |
| [apache-kafka-java](templates/apache-kafka-java/CLAUDE.md) | Apache Kafka 3.7+, Java 21 | Kafka Streams, Schema Registry, Avro | 103 |
| [rabbitmq-node](templates/rabbitmq-node/CLAUDE.md) | RabbitMQ 3.13+, Node.js 20 | amqplib, Zod, Winston, Testcontainers | 97 |

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

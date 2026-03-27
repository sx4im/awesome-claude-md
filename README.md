<p align="center">
  <h1 align="center">awesome-claude-md</h1>
  <p align="center">
    <strong>200 opinionated CLAUDE.md templates for every stack.</strong><br>
    Stop writing CLAUDE.md files from scratch. Grab one, edit the placeholders, ship better code.
  </p>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>&nbsp;
    <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>&nbsp;
    <a href="https://docs.anthropic.com/en/docs/claude-code"><img src="https://img.shields.io/badge/Claude-Code-blueviolet.svg" alt="Claude Code"></a>&nbsp;
    <img src="https://img.shields.io/badge/templates-200-orange.svg" alt="200 Templates">
  </p>
</p>

<br>

> Every developer using Claude Code needs a `CLAUDE.md`. Most throw one together in 20 minutes, then spend the rest of the week wondering why Claude keeps generating barrel files or ignoring their project's conventions.
>
> A `CLAUDE.md` that says *"write clean code"* teaches it nothing. These templates fix that.

<br>

## Quick Start

```bash
# 1. Pick a template
cp templates/nextjs/CLAUDE.md ~/your-project/CLAUDE.md

# 2. Replace the [PLACEHOLDERS]
# 3. Done. Claude now knows your stack.
```

Or browse the [full catalog](CATALOG.md) with line counts and key libraries for every template.

<br>

## Templates

[Frontend](#-frontend) · [Full-Stack](#-full-stack) · [Backend](#-backend) · [AI & ML](#-ai--ml) · [Database & Messaging](#-database--messaging) · [Mobile](#-mobile) · [Desktop](#-desktop) · [CLI & Tools](#-cli--tools) · [Testing](#-testing) · [Cloud & Serverless](#-cloud--serverless) · [DevOps & Infra](#-devops--infra) · [Bots & Plugins](#-bots--plugins) · [Game Dev](#-game-dev) · [Languages](#-languages) · [Specialized](#-specialized)

<br>

### > Frontend

| Template | Stack | When to use |
|:---------|:------|:------------|
| [nextjs](templates/nextjs/CLAUDE.md) | Next.js 14+, App Router, TypeScript | Server components, RSC, full-stack React |
| [react-vite](templates/react-vite/CLAUDE.md) | React 18, Vite, TypeScript | Client-side SPAs, no SSR needed |
| [vue-vite](templates/vue-vite/CLAUDE.md) | Vue 3, Vite, Composition API | Vue SPAs with Pinia and Vue Router |
| [sveltekit](templates/sveltekit/CLAUDE.md) | SvelteKit 2, Svelte 5 runes | Full-stack Svelte with form actions |
| [svelte5-runes](templates/svelte5-runes/CLAUDE.md) | Svelte 5, SvelteKit 2, Runes | Svelte 5 runes-first reactivity |
| [nuxt](templates/nuxt/CLAUDE.md) | Nuxt 3, Vue 3, Composition API | Vue full-stack with auto-imports |
| [remix](templates/remix/CLAUDE.md) | Remix 2, React 18 | Nested routes, loaders, progressive enhancement |
| [astro](templates/astro/CLAUDE.md) | Astro 4, Content Collections | Content sites, zero JS by default |
| [angular](templates/angular/CLAUDE.md) | Angular 17+, Signals | Enterprise SPAs with standalone components |
| [analog-angular](templates/analog-angular/CLAUDE.md) | Analog.js, Angular 18, Vite | Angular meta-framework with file-based routing |
| [gatsby](templates/gatsby/CLAUDE.md) | Gatsby 5, GraphQL, MDX | Static sites with rich data layer |
| [qwik](templates/qwik/CLAUDE.md) | Qwik, Qwik City | Resumable apps, instant load times |
| [solidjs](templates/solidjs/CLAUDE.md) | SolidJS, SolidStart | Fine-grained reactivity, no virtual DOM |
| [preact](templates/preact/CLAUDE.md) | Preact, Signals, Vite | Lightweight React alternative (3kb) |
| [lit-components](templates/lit-components/CLAUDE.md) | Lit 3, Web Components | Framework-agnostic custom elements |
| [web-components](templates/web-components/CLAUDE.md) | Native Web Components, Shadow DOM | Custom elements without framework dependency |
| [eleventy](templates/eleventy/CLAUDE.md) | 11ty 3, Nunjucks, WebC | Simple static sites, no client JS |
| [docusaurus](templates/docusaurus/CLAUDE.md) | Docusaurus 3, React 18, MDX | Documentation sites with versioning |
| [alpine-js](templates/alpine-js/CLAUDE.md) | Alpine.js 3, Tailwind CSS, HTMX | Lightweight client-side interactivity |
| [ember-js](templates/ember-js/CLAUDE.md) | Ember.js 5, Glimmer, Embroider | Convention-driven ambitious web apps |
| [fresh-preact](templates/fresh-preact/CLAUDE.md) | Deno Fresh 2, Preact, Signals | Islands architecture on Deno |
| [tanstack-start](templates/tanstack-start/CLAUDE.md) | TanStack Start, React 19, TanStack Router | Type-safe full-stack React with TanStack |
| [htmx-go](templates/htmx-go/CLAUDE.md) | HTMX, Go, Templ | Hypermedia-driven, no SPA framework |
| [htmx-django](templates/htmx-django/CLAUDE.md) | HTMX 2, Django 5, Python | Server-driven UI with Django templates |
| [htmx-flask](templates/htmx-flask/CLAUDE.md) | HTMX 2, Flask 3, Jinja2 | Lightweight HTMX with Flask |
| [storybook-react](templates/storybook-react/CLAUDE.md) | Storybook 8, React 18, CSF3 | Component development and documentation |
| [threejs-r3f](templates/threejs-r3f/CLAUDE.md) | React Three Fiber, Drei | 3D scenes in React |

<br>

### > Full-Stack

| Template | Stack | When to use |
|:---------|:------|:------------|
| [t3-stack](templates/t3-stack/CLAUDE.md) | tRPC, Next.js, Prisma | End-to-end type safety |
| [saas-fullstack](templates/saas-fullstack/CLAUDE.md) | Next.js, Stripe, Clerk | SaaS with billing, auth, emails |
| [supabase-nextjs](templates/supabase-nextjs/CLAUDE.md) | Next.js, Supabase | Postgres + auth + realtime, fast MVPs |
| [clerk-nextjs](templates/clerk-nextjs/CLAUDE.md) | Next.js 14+, Clerk v5 | Auth, sessions, and organizations |
| [drizzle-nextjs](templates/drizzle-nextjs/CLAUDE.md) | Next.js 15, Drizzle ORM, PostgreSQL | Type-safe ORM with React Server Components |
| [vercel-ai](templates/vercel-ai/CLAUDE.md) | Next.js 15, Vercel AI SDK 4 | AI-powered apps with streaming |
| [convex-nextjs](templates/convex-nextjs/CLAUDE.md) | Convex, Next.js | Reactive backend, zero infra |
| [redwoodjs](templates/redwoodjs/CLAUDE.md) | RedwoodJS, GraphQL, Prisma | Opinionated full-stack with Cells |
| [blitzjs](templates/blitzjs/CLAUDE.md) | BlitzJS, Prisma, RPC | Full-stack React without API layer |
| [wasp](templates/wasp/CLAUDE.md) | Wasp, React, Node | Declarative full-stack DSL |
| [meteor](templates/meteor/CLAUDE.md) | Meteor, React, MongoDB | Realtime apps with DDP pub/sub |
| [shopify-hydrogen](templates/shopify-hydrogen/CLAUDE.md) | Hydrogen, Remix | Custom Shopify storefronts |
| [payload-cms](templates/payload-cms/CLAUDE.md) | Payload CMS 3, Next.js | Headless CMS with block-based layouts |
| [strapi-v5](templates/strapi-v5/CLAUDE.md) | Strapi v5, PostgreSQL, TypeScript | Headless CMS with Document Service API |
| [directus](templates/directus/CLAUDE.md) | Directus 11, PostgreSQL | Data platform and headless CMS |
| [keystone-js](templates/keystone-js/CLAUDE.md) | KeystoneJS 6, Prisma, GraphQL | Headless CMS and app framework |
| [medusa-js](templates/medusa-js/CLAUDE.md) | Medusa.js 2, MikroORM, PostgreSQL | E-commerce backend framework |
| [pocketbase](templates/pocketbase/CLAUDE.md) | PocketBase, Go, SQLite | Backend-in-a-file with realtime |
| [supabase-realtime](templates/supabase-realtime/CLAUDE.md) | Supabase Realtime, PostgreSQL | WebSocket channels and presence |

<br>

### > Backend

| Template | Stack | When to use |
|:---------|:------|:------------|
| [python-fastapi](templates/python-fastapi/CLAUDE.md) | FastAPI, SQLAlchemy 2.0, Pydantic v2 | Async Python APIs |
| [django](templates/django/CLAUDE.md) | Django 5, DRF, Celery | Batteries-included Python web |
| [flask](templates/flask/CLAUDE.md) | Flask, SQLAlchemy, Marshmallow | Lightweight Python APIs |
| [express-typescript](templates/express-typescript/CLAUDE.md) | Express, TypeScript, Prisma | Node.js REST APIs |
| [prisma-express](templates/prisma-express/CLAUDE.md) | Express 4, Prisma 5, PostgreSQL | Prisma-first Node.js APIs |
| [nestjs](templates/nestjs/CLAUDE.md) | NestJS 10+, TypeScript | Enterprise Node.js with DI |
| [fastify](templates/fastify/CLAUDE.md) | Fastify, TypeScript, JSON Schema | High-performance Node.js APIs |
| [hono](templates/hono/CLAUDE.md) | Hono, TypeScript, Zod OpenAPI | Edge-first APIs (Workers/Bun) |
| [bun-elysia](templates/bun-elysia/CLAUDE.md) | Bun 1.1+, Elysia.js, TypeBox | Bun-native APIs with full type inference |
| [adonisjs](templates/adonisjs/CLAUDE.md) | AdonisJS 6, Lucid ORM | Laravel-like Node.js framework |
| [koa-typescript](templates/koa-typescript/CLAUDE.md) | Koa, TypeScript, TypeORM | Middleware-composed Node.js APIs |
| [trpc-standalone](templates/trpc-standalone/CLAUDE.md) | tRPC, TypeScript, Zod | End-to-end typesafe APIs (standalone) |
| [deno-oak](templates/deno-oak/CLAUDE.md) | Deno 2, Oak 16+, Deno KV | Deno-native APIs with Oak |
| [go-api](templates/go-api/CLAUDE.md) | Go, Chi, sqlc | Idiomatic Go REST APIs |
| [gin-go](templates/gin-go/CLAUDE.md) | Go, Gin, GORM | Go APIs with Gin framework |
| [fiber-go](templates/fiber-go/CLAUDE.md) | Go, Fiber, GORM/sqlc | Express-like Go framework |
| [grpc-go](templates/grpc-go/CLAUDE.md) | Go, gRPC, Connect RPC | RPC services with Protobuf |
| [rust-axum](templates/rust-axum/CLAUDE.md) | Rust, Axum, SQLx | Rust async web services |
| [actix-web](templates/actix-web/CLAUDE.md) | Rust, Actix-web 4, SQLx | High-performance Rust APIs |
| [spring-boot](templates/spring-boot/CLAUDE.md) | Java 21+, Spring Boot 3.2 | Enterprise Java APIs |
| [ktor](templates/ktor/CLAUDE.md) | Kotlin, Ktor, Exposed | Kotlin coroutine-based APIs |
| [scala-play](templates/scala-play/CLAUDE.md) | Scala 3, Play Framework, Slick | Scala web applications |
| [dotnet-api](templates/dotnet-api/CLAUDE.md) | .NET 8, C# 12, EF Core | .NET Minimal APIs with CQRS |
| [laravel](templates/laravel/CLAUDE.md) | PHP 8.2+, Laravel 11 | PHP full-stack with Eloquent |
| [php-symfony](templates/php-symfony/CLAUDE.md) | PHP 8.3+, Symfony 7, Doctrine 3 | Enterprise PHP with Symfony |
| [ruby-on-rails](templates/ruby-on-rails/CLAUDE.md) | Ruby 3.2+, Rails 7.1+ | Convention-over-configuration web |
| [elixir-phoenix](templates/elixir-phoenix/CLAUDE.md) | Elixir, Phoenix 1.7+, Ecto | Realtime Elixir with LiveView |
| [swift-vapor](templates/swift-vapor/CLAUDE.md) | Swift 5.9+, Vapor 4, Fluent ORM | Server-side Swift APIs |
| [graphql-api](templates/graphql-api/CLAUDE.md) | Apollo/Yoga, Pothos, Prisma | GraphQL APIs with code-first schema |
| [openapi-codegen](templates/openapi-codegen/CLAUDE.md) | OpenAPI 3.1, openapi-typescript | API-first with generated types |
| [mcp-server-typescript](templates/mcp-server-typescript/CLAUDE.md) | MCP SDK, TypeScript, Node.js | Model Context Protocol servers |
| [firebase-functions](templates/firebase-functions/CLAUDE.md) | Cloud Functions v2, Firestore | Serverless Firebase backend |

<br>

### > AI & ML

| Template | Stack | When to use |
|:---------|:------|:------------|
| [langchain-python](templates/langchain-python/CLAUDE.md) | LangChain, Python | LLM chains, agents, tool calling |
| [rag-pipeline](templates/rag-pipeline/CLAUDE.md) | Embeddings, Vector DB, Python | Retrieval-augmented generation |
| [llm-api](templates/llm-api/CLAUDE.md) | OpenAI/Anthropic SDK, TypeScript | LLM API wrappers with streaming |
| [huggingface](templates/huggingface/CLAUDE.md) | Transformers, PEFT, Datasets | Model fine-tuning and inference |
| [ml-python](templates/ml-python/CLAUDE.md) | PyTorch, MLflow, polars | ML training pipelines |
| [pytorch-lightning](templates/pytorch-lightning/CLAUDE.md) | PyTorch 2, Lightning 2 | Structured deep learning training |
| [gradio-ml](templates/gradio-ml/CLAUDE.md) | Gradio 4, Transformers | ML model demo interfaces |
| [streamlit](templates/streamlit/CLAUDE.md) | Streamlit 1.38+, pandas | Data apps and dashboards |
| [mlflow](templates/mlflow/CLAUDE.md) | MLflow 2, scikit-learn/XGBoost | Experiment tracking and model registry |
| [jupyter-data-science](templates/jupyter-data-science/CLAUDE.md) | Jupyter, pandas, scikit-learn | Data analysis and exploration |
| [data-pipeline](templates/data-pipeline/CLAUDE.md) | Airflow/Dagster, dbt, Python | ETL and data orchestration |
| [apache-airflow](templates/apache-airflow/CLAUDE.md) | Airflow 2.9+, TaskFlow API | Workflow orchestration and scheduling |
| [dagster](templates/dagster/CLAUDE.md) | Dagster 1.7+, Dagster UI | Software-defined data assets |
| [dbt-project](templates/dbt-project/CLAUDE.md) | dbt Core 1.8+, SQLFluff | SQL transformation and modeling |
| [spark-pyspark](templates/spark-pyspark/CLAUDE.md) | Apache Spark 3.5+, PySpark, Delta Lake | Large-scale data processing |
| [polars-python](templates/polars-python/CLAUDE.md) | Polars 1, Python | Fast DataFrame processing (pandas alternative) |

<br>

### > Database & Messaging

| Template | Stack | When to use |
|:---------|:------|:------------|
| [mongodb-express](templates/mongodb-express/CLAUDE.md) | MongoDB 7, Mongoose 8, Express | Document database with Node.js |
| [neo4j-graphql](templates/neo4j-graphql/CLAUDE.md) | Neo4j 5, @neo4j/graphql, Apollo | Graph database with GraphQL API |
| [neon-postgres](templates/neon-postgres/CLAUDE.md) | Neon serverless PostgreSQL, TypeScript | Serverless Postgres with branching |
| [cockroachdb](templates/cockroachdb/CLAUDE.md) | CockroachDB 24, Go, pgx | Distributed SQL, multi-region |
| [clickhouse-analytics](templates/clickhouse-analytics/CLAUDE.md) | ClickHouse 24, Python, dbt | Columnar analytics at scale |
| [duckdb-python](templates/duckdb-python/CLAUDE.md) | DuckDB 1, Python | Embedded analytical SQL engine |
| [redis-python](templates/redis-python/CLAUDE.md) | Redis 7.2+, redis-py 5, Redis Stack | Caching, pub/sub, and data structures |
| [sqlite-rust](templates/sqlite-rust/CLAUDE.md) | Rust, rusqlite, SQLite 3.45+ | Embedded SQL in Rust applications |
| [turso-libsql](templates/turso-libsql/CLAUDE.md) | Turso, libSQL, TypeScript | Edge-distributed SQLite |
| [dynamodb-lambda](templates/dynamodb-lambda/CLAUDE.md) | DynamoDB, Lambda, AWS SDK v3 | Serverless NoSQL on AWS |
| [apache-kafka-java](templates/apache-kafka-java/CLAUDE.md) | Kafka 3.7+, Java 21, Kafka Streams | Event streaming and stream processing |
| [rabbitmq-node](templates/rabbitmq-node/CLAUDE.md) | RabbitMQ 3.13+, amqplib, Node.js | Message queuing with AMQP |

<br>

### > Mobile

| Template | Stack | When to use |
|:---------|:------|:------------|
| [flutter](templates/flutter/CLAUDE.md) | Flutter 3, Dart 3, Riverpod | Cross-platform from single codebase |
| [react-native-expo](templates/react-native-expo/CLAUDE.md) | Expo SDK 50+, Expo Router | Cross-platform with React Native |
| [expo-router](templates/expo-router/CLAUDE.md) | Expo SDK 52+, Expo Router v4 | File-based routing for React Native |
| [ionic-capacitor](templates/ionic-capacitor/CLAUDE.md) | Ionic 7+, Capacitor | Web-to-native with native plugins |
| [capacitor-vue](templates/capacitor-vue/CLAUDE.md) | Vue 3, Capacitor 6, Ionic 8 | Vue-based mobile apps with Capacitor |
| [nativescript-angular](templates/nativescript-angular/CLAUDE.md) | NativeScript 8, Angular 17+ | Native mobile with Angular |
| [swift-ios](templates/swift-ios/CLAUDE.md) | SwiftUI, Swift Concurrency | Native iOS apps |
| [jetpack-compose](templates/jetpack-compose/CLAUDE.md) | Kotlin 2, Jetpack Compose, Hilt | Modern Android UI with Compose |
| [kotlin-android](templates/kotlin-android/CLAUDE.md) | Jetpack Compose, Hilt | Native Android apps |
| [kotlin-multiplatform](templates/kotlin-multiplatform/CLAUDE.md) | KMP, Compose Multiplatform | Shared Kotlin across all platforms |
| [dotnet-maui](templates/dotnet-maui/CLAUDE.md) | .NET MAUI, C#, MVVM | Cross-platform .NET mobile/desktop |
| [maui-blazor](templates/maui-blazor/CLAUDE.md) | .NET 9 MAUI Blazor Hybrid | Blazor components in native shells |

<br>

### > Desktop

| Template | Stack | When to use |
|:---------|:------|:------------|
| [electron](templates/electron/CLAUDE.md) | Electron 28+, React, Vite | Cross-platform desktop with web tech |
| [tauri](templates/tauri/CLAUDE.md) | Tauri 2, Rust + React | Lightweight native desktop apps |
| [wails-go](templates/wails-go/CLAUDE.md) | Wails v2, Go, Svelte/React | Go desktop apps with web frontend |
| [compose-desktop](templates/compose-desktop/CLAUDE.md) | Compose for Desktop, Kotlin | JVM desktop with Compose UI |
| [avalonia-dotnet](templates/avalonia-dotnet/CLAUDE.md) | Avalonia 11+, C# 12, .NET 9 | Cross-platform .NET desktop |
| [swiftui-macos](templates/swiftui-macos/CLAUDE.md) | SwiftUI, SwiftData, AppKit | Native macOS applications |

<br>

### > CLI & Tools

| Template | Stack | When to use |
|:---------|:------|:------------|
| [cli-node](templates/cli-node/CLAUDE.md) | Node.js, Commander, Chalk | Node.js command-line tools |
| [cli-python](templates/cli-python/CLAUDE.md) | Python, Typer, Rich | Python command-line tools |
| [cli-go](templates/cli-go/CLAUDE.md) | Go, Cobra, Bubble Tea | Go command-line tools and TUIs |
| [rust-cli](templates/rust-cli/CLAUDE.md) | Rust, clap, indicatif | Rust command-line tools |
| [puppeteer-node](templates/puppeteer-node/CLAUDE.md) | Puppeteer 22+, TypeScript | Browser automation and scraping |
| [vscode-extension](templates/vscode-extension/CLAUDE.md) | VS Code API, TypeScript | Editor extensions and language servers |
| [chrome-extension](templates/chrome-extension/CLAUDE.md) | Chrome MV3, CRXJS | Browser extensions |

<br>

### > Testing

| Template | Stack | When to use |
|:---------|:------|:------------|
| [playwright](templates/playwright/CLAUDE.md) | Playwright, TypeScript | Cross-browser E2E testing |
| [cypress](templates/cypress/CLAUDE.md) | Cypress, TypeScript | E2E and component testing |
| [k6-load-testing](templates/k6-load-testing/CLAUDE.md) | Grafana k6, JavaScript ES6 | Load and performance testing |
| [locust-python](templates/locust-python/CLAUDE.md) | Locust 2.29+, Python, gevent | Distributed load testing |

<br>

### > Cloud & Serverless

| Template | Stack | When to use |
|:---------|:------|:------------|
| [aws-lambda-node](templates/aws-lambda-node/CLAUDE.md) | AWS Lambda Node.js 20, SAM | Serverless Node.js on AWS |
| [lambda-python](templates/lambda-python/CLAUDE.md) | AWS Lambda Python 3.12, SAM | Serverless Python on AWS |
| [aws-step-functions](templates/aws-step-functions/CLAUDE.md) | Step Functions, CDK, Lambda | Serverless workflow orchestration |
| [azure-functions](templates/azure-functions/CLAUDE.md) | Azure Functions v4, Cosmos DB | Serverless on Azure |
| [google-cloud-run](templates/google-cloud-run/CLAUDE.md) | Cloud Run, Cloud SQL, Pub/Sub | Containerized serverless on GCP |
| [cloudflare-workers](templates/cloudflare-workers/CLAUDE.md) | Workers, Hono, D1 | Edge compute on Cloudflare |
| [netlify-functions](templates/netlify-functions/CLAUDE.md) | Netlify Functions v2, TypeScript | Serverless on Netlify |
| [deno-deploy](templates/deno-deploy/CLAUDE.md) | Deno Deploy, Deno KV | Edge serverless on Deno |
| [supabase-edge](templates/supabase-edge/CLAUDE.md) | Supabase Edge Functions, Deno | Serverless on Supabase |

<br>

### > DevOps & Infra

| Template | Stack | When to use |
|:---------|:------|:------------|
| [docker-compose](templates/docker-compose/CLAUDE.md) | Docker, Compose v2 | Multi-container local dev and deploy |
| [kubernetes](templates/kubernetes/CLAUDE.md) | Kubernetes, Kustomize | Container orchestration manifests |
| [helm-chart](templates/helm-chart/CLAUDE.md) | Helm 3, Go templates | Kubernetes package management |
| [argocd](templates/argocd/CLAUDE.md) | ArgoCD 2.10+, Kustomize | GitOps continuous delivery |
| [crossplane](templates/crossplane/CLAUDE.md) | Crossplane 1.15+, Provider AWS | Control plane infrastructure |
| [skaffold](templates/skaffold/CLAUDE.md) | Skaffold 2.10+, kubectl/Helm | Continuous Kubernetes development |
| [tilt-dev](templates/tilt-dev/CLAUDE.md) | Tilt 0.33+, Tiltfile (Starlark) | Local Kubernetes dev with live updates |
| [terraform](templates/terraform/CLAUDE.md) | Terraform 1.6+, HCL | Infrastructure as code |
| [pulumi](templates/pulumi/CLAUDE.md) | Pulumi, TypeScript | IaC with real programming languages |
| [aws-cdk](templates/aws-cdk/CLAUDE.md) | AWS CDK v2, TypeScript | AWS infrastructure with constructs |
| [github-actions](templates/github-actions/CLAUDE.md) | GitHub Actions, YAML | CI/CD pipelines and automation |
| [dagger-ci](templates/dagger-ci/CLAUDE.md) | Dagger 0.14+, Go SDK, BuildKit | Programmable CI/CD pipelines |
| [earthly-ci](templates/earthly-ci/CLAUDE.md) | Earthly 0.8+, Earthfile | Containerized reproducible builds |
| [ansible](templates/ansible/CLAUDE.md) | Ansible, Jinja2, YAML | Configuration management and provisioning |
| [nix-flake](templates/nix-flake/CLAUDE.md) | Nix 2.20+, Nixpkgs, flake-utils | Reproducible dev environments and builds |
| [bazel-java](templates/bazel-java/CLAUDE.md) | Bazel 7, Java 21, bzlmod | Hermetic builds for large codebases |
| [prometheus-grafana](templates/prometheus-grafana/CLAUDE.md) | Prometheus 2.50+, Grafana 10+ | Metrics, dashboards, and alerting |
| [opentelemetry-node](templates/opentelemetry-node/CLAUDE.md) | OpenTelemetry JS SDK, OTLP | Distributed tracing and observability |

<br>

### > Bots & Plugins

| Template | Stack | When to use |
|:---------|:------|:------------|
| [discord-bot](templates/discord-bot/CLAUDE.md) | discord.js v14, TypeScript | Discord bots with slash commands |
| [slack-bot](templates/slack-bot/CLAUDE.md) | Bolt.js, Block Kit | Slack apps and workflows |
| [telegram-bot](templates/telegram-bot/CLAUDE.md) | python-telegram-bot v20 | Telegram bots with conversations |
| [obsidian-plugin](templates/obsidian-plugin/CLAUDE.md) | Obsidian API, TypeScript | Obsidian vault plugins |
| [figma-plugin](templates/figma-plugin/CLAUDE.md) | Figma Plugin API, TypeScript | Figma design tool plugins |
| [raycast-extension](templates/raycast-extension/CLAUDE.md) | Raycast API, React | Raycast launcher extensions |

<br>

### > Game Dev

| Template | Stack | When to use |
|:---------|:------|:------------|
| [unity-csharp](templates/unity-csharp/CLAUDE.md) | Unity 2022+, C# | Unity game development |
| [godot-gdscript](templates/godot-gdscript/CLAUDE.md) | Godot 4, GDScript | Godot game development |
| [godot-rust](templates/godot-rust/CLAUDE.md) | Godot 4.3+, Rust (gdext) | Godot with Rust game logic |
| [unreal-cpp](templates/unreal-cpp/CLAUDE.md) | Unreal Engine 5, C++ | AAA game development |
| [bevy-rust](templates/bevy-rust/CLAUDE.md) | Bevy 0.14+, Rust, bevy_rapier | ECS game engine in Rust |
| [phaser-game](templates/phaser-game/CLAUDE.md) | Phaser 3.80+, TypeScript, Vite | 2D browser games |
| [pixi-js](templates/pixi-js/CLAUDE.md) | PixiJS 8, TypeScript | WebGL/WebGPU 2D rendering |
| [babylon-js](templates/babylon-js/CLAUDE.md) | Babylon.js 7, TypeScript | 3D WebGL/WebGPU engine |
| [webgpu-wgsl](templates/webgpu-wgsl/CLAUDE.md) | WebGPU, WGSL, TypeScript | GPU rendering and compute |
| [pygame-python](templates/pygame-python/CLAUDE.md) | Pygame 2.5+, Python | Python 2D game development |
| [raylib-c](templates/raylib-c/CLAUDE.md) | raylib 5, C17, CMake | Lightweight C game development |
| [love2d-lua](templates/love2d-lua/CLAUDE.md) | LOVE 11.5+, Lua 5.1 | Lua 2D game framework |
| [defold-lua](templates/defold-lua/CLAUDE.md) | Defold 1.9+, Lua 5.1 | Cross-platform Lua game engine |

<br>

### > Languages

| Template | Stack | When to use |
|:---------|:------|:------------|
| [clojure-ring](templates/clojure-ring/CLAUDE.md) | Clojure 1.12, Ring, Compojure | Clojure web apps on JVM |
| [crystal-kemal](templates/crystal-kemal/CLAUDE.md) | Crystal 1.12+, Kemal | Fast compiled web framework |
| [gleam-lustre](templates/gleam-lustre/CLAUDE.md) | Gleam 1, Lustre, BEAM | Type-safe Erlang/BEAM apps |
| [haskell-servant](templates/haskell-servant/CLAUDE.md) | Haskell GHC 9.6+, Servant | Type-level HTTP APIs in Haskell |
| [julia-project](templates/julia-project/CLAUDE.md) | Julia 1.10+, Pkg | Scientific computing and HPC |
| [nim-web](templates/nim-web/CLAUDE.md) | Nim 2, Jester, Karax | Efficient compiled web apps |
| [ocaml-dream](templates/ocaml-dream/CLAUDE.md) | OCaml 5, Dream, Dune | OCaml web with multicore |
| [r-shiny](templates/r-shiny/CLAUDE.md) | R 4.3+, Shiny, golem | Interactive data dashboards |
| [v-lang](templates/v-lang/CLAUDE.md) | V 0.4, vweb | Simple compiled language for web |
| [zig-project](templates/zig-project/CLAUDE.md) | Zig 0.13, build.zig | Systems programming with Zig |

<br>

### > Specialized

| Template | Stack | When to use |
|:---------|:------|:------------|
| [monorepo](templates/monorepo/CLAUDE.md) | Turborepo, pnpm workspaces | Multi-package repositories |
| [open-source-lib](templates/open-source-lib/CLAUDE.md) | TypeScript, tsup, Changesets | Publishing npm packages |
| [stripe-integration](templates/stripe-integration/CLAUDE.md) | Stripe SDK, Webhooks | Payment processing integration |
| [websocket-node](templates/websocket-node/CLAUDE.md) | ws/Socket.IO, TypeScript | Realtime WebSocket servers |
| [wasm-rust](templates/wasm-rust/CLAUDE.md) | Rust, wasm-bindgen, wasm-pack | WebAssembly modules |
| [embedded-rust](templates/embedded-rust/CLAUDE.md) | Rust no_std, embassy, HAL | Embedded systems and microcontrollers |
| [deno-fresh](templates/deno-fresh/CLAUDE.md) | Deno, Fresh, Preact | Deno-native web framework |
| [solidity-hardhat](templates/solidity-hardhat/CLAUDE.md) | Solidity, Hardhat, Ethers.js | Smart contract development |
| [wordpress-theme](templates/wordpress-theme/CLAUDE.md) | WordPress 6, PHP, Gutenberg | WordPress block themes |

<br>

## Why this exists

Claude won't know you use named exports, prefer `date-fns` over `moment`, or have a no-`any` policy unless you tell it.

Writing good rules from scratch is tedious — file naming, import ordering, anti-patterns, library choices. Most people skip it. The sharp edges differ per stack too: what Claude gets wrong in Next.js has nothing to do with what it gets wrong in FastAPI.

**Every rule in these templates exists because someone shipped code where Claude did the wrong thing without it.**

<br>

## Contributing

New templates and fixes welcome. Read the [Contributing Guide](CONTRIBUTING.md) before opening a PR.

<br>

## Star History

<a href="https://star-history.com/#sx4im/awesome-claude-md&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date" />
 </picture>
</a>

<br>

---

<p align="center">Made by people who got tired of Claude ignoring their coding standards.</p>

<!-- GitHub Topics (for maintainers): claude-code, gemini-cli, codex-cli, antigravity, cursor, github-copilot, opencode, agentic-skills, ai-coding, llm-tools, ai-agents, autonomous-coding, mcp, ai-developer-tools, ai-pair-programming, vibe-coding, skill, skills, SKILL.md, rules.md, CLAUDE.md, GEMINI.md, CURSOR.md -->

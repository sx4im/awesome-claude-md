<p align="center">
  <h1 align="center">Awesome-Claude-md</h1>
  <p align="center">
    <strong>100 opinionated CLAUDE.md templates for every stack.</strong><br>
    Stop writing CLAUDE.md files from scratch. Grab one, edit the placeholders, ship better code.
  </p>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>&nbsp;
    <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>&nbsp;
    <a href="https://docs.anthropic.com/en/docs/claude-code"><img src="https://img.shields.io/badge/Claude-Code-blueviolet.svg" alt="Claude Code"></a>&nbsp;
    <img src="https://img.shields.io/badge/templates-100-orange.svg" alt="100 Templates">
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

[Frontend](#-frontend) · [Full-Stack](#-full-stack) · [Backend](#-backend) · [AI & ML](#-ai--ml) · [Mobile](#-mobile) · [Desktop](#-desktop) · [CLI & Tools](#-cli--tools) · [Testing](#-testing) · [DevOps & Infra](#-devops--infra) · [Bots & Plugins](#-bots--plugins) · [Game Dev](#-game-dev) · [Specialized](#-specialized)

<br>

### > Frontend

| Template | Stack | When to use |
|:---------|:------|:------------|
| [nextjs](templates/nextjs/CLAUDE.md) | Next.js 14+, App Router, TypeScript | Server components, RSC, full-stack React |
| [react-vite](templates/react-vite/CLAUDE.md) | React 18, Vite, TypeScript | Client-side SPAs, no SSR needed |
| [vue-vite](templates/vue-vite/CLAUDE.md) | Vue 3, Vite, Composition API | Vue SPAs with Pinia and Vue Router |
| [sveltekit](templates/sveltekit/CLAUDE.md) | SvelteKit 2, Svelte 5 runes | Full-stack Svelte with form actions |
| [nuxt](templates/nuxt/CLAUDE.md) | Nuxt 3, Vue 3, Composition API | Vue full-stack with auto-imports |
| [remix](templates/remix/CLAUDE.md) | Remix 2, React 18 | Nested routes, loaders, progressive enhancement |
| [astro](templates/astro/CLAUDE.md) | Astro 4, Content Collections | Content sites, zero JS by default |
| [angular](templates/angular/CLAUDE.md) | Angular 17+, Signals | Enterprise SPAs with standalone components |
| [gatsby](templates/gatsby/CLAUDE.md) | Gatsby 5, GraphQL, MDX | Static sites with rich data layer |
| [qwik](templates/qwik/CLAUDE.md) | Qwik, Qwik City | Resumable apps, instant load times |
| [solidjs](templates/solidjs/CLAUDE.md) | SolidJS, SolidStart | Fine-grained reactivity, no virtual DOM |
| [preact](templates/preact/CLAUDE.md) | Preact, Signals, Vite | Lightweight React alternative (3kb) |
| [lit-components](templates/lit-components/CLAUDE.md) | Lit 3, Web Components | Framework-agnostic custom elements |
| [eleventy](templates/eleventy/CLAUDE.md) | 11ty 3, Nunjucks, WebC | Simple static sites, no client JS |
| [threejs-r3f](templates/threejs-r3f/CLAUDE.md) | React Three Fiber, Drei | 3D scenes in React |
| [htmx-go](templates/htmx-go/CLAUDE.md) | HTMX, Go, Templ | Hypermedia-driven, no SPA framework |

<br>

### > Full-Stack

| Template | Stack | When to use |
|:---------|:------|:------------|
| [t3-stack](templates/t3-stack/CLAUDE.md) | tRPC, Next.js, Prisma | End-to-end type safety |
| [saas-fullstack](templates/saas-fullstack/CLAUDE.md) | Next.js, Stripe, Clerk | SaaS with billing, auth, emails |
| [supabase-nextjs](templates/supabase-nextjs/CLAUDE.md) | Next.js, Supabase | Postgres + auth + realtime, fast MVPs |
| [convex-nextjs](templates/convex-nextjs/CLAUDE.md) | Convex, Next.js | Reactive backend, zero infra |
| [redwoodjs](templates/redwoodjs/CLAUDE.md) | RedwoodJS, GraphQL, Prisma | Opinionated full-stack with Cells |
| [blitzjs](templates/blitzjs/CLAUDE.md) | BlitzJS, Prisma, RPC | Full-stack React without API layer |
| [wasp](templates/wasp/CLAUDE.md) | Wasp, React, Node | Declarative full-stack DSL |
| [meteor](templates/meteor/CLAUDE.md) | Meteor, React, MongoDB | Realtime apps with DDP pub/sub |
| [shopify-hydrogen](templates/shopify-hydrogen/CLAUDE.md) | Hydrogen, Remix | Custom Shopify storefronts |
| [payload-cms](templates/payload-cms/CLAUDE.md) | Payload CMS 3, Next.js | Headless CMS with block-based layouts |

<br>

### > Backend

| Template | Stack | When to use |
|:---------|:------|:------------|
| [python-fastapi](templates/python-fastapi/CLAUDE.md) | FastAPI, SQLAlchemy 2.0, Pydantic v2 | Async Python APIs |
| [django](templates/django/CLAUDE.md) | Django 5, DRF, Celery | Batteries-included Python web |
| [flask](templates/flask/CLAUDE.md) | Flask, SQLAlchemy, Marshmallow | Lightweight Python APIs |
| [express-typescript](templates/express-typescript/CLAUDE.md) | Express, TypeScript, Prisma | Node.js REST APIs |
| [nestjs](templates/nestjs/CLAUDE.md) | NestJS 10+, TypeScript | Enterprise Node.js with DI |
| [fastify](templates/fastify/CLAUDE.md) | Fastify, TypeScript, JSON Schema | High-performance Node.js APIs |
| [hono](templates/hono/CLAUDE.md) | Hono, TypeScript, Zod OpenAPI | Edge-first APIs (Workers/Bun) |
| [adonisjs](templates/adonisjs/CLAUDE.md) | AdonisJS 6, Lucid ORM | Laravel-like Node.js framework |
| [koa-typescript](templates/koa-typescript/CLAUDE.md) | Koa, TypeScript, TypeORM | Middleware-composed Node.js APIs |
| [trpc-standalone](templates/trpc-standalone/CLAUDE.md) | tRPC, TypeScript, Zod | End-to-end typesafe APIs (standalone) |
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
| [ruby-on-rails](templates/ruby-on-rails/CLAUDE.md) | Ruby 3.2+, Rails 7.1+ | Convention-over-configuration web |
| [elixir-phoenix](templates/elixir-phoenix/CLAUDE.md) | Elixir, Phoenix 1.7+, Ecto | Realtime Elixir with LiveView |
| [graphql-api](templates/graphql-api/CLAUDE.md) | Apollo/Yoga, Pothos, Prisma | GraphQL APIs with code-first schema |
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
| [jupyter-data-science](templates/jupyter-data-science/CLAUDE.md) | Jupyter, pandas, scikit-learn | Data analysis and exploration |
| [data-pipeline](templates/data-pipeline/CLAUDE.md) | Airflow/Dagster, dbt, Python | ETL and data orchestration |

<br>

### > Mobile

| Template | Stack | When to use |
|:---------|:------|:------------|
| [flutter](templates/flutter/CLAUDE.md) | Flutter 3, Dart 3, Riverpod | Cross-platform from single codebase |
| [react-native-expo](templates/react-native-expo/CLAUDE.md) | Expo SDK 50+, Expo Router | Cross-platform with React Native |
| [ionic-capacitor](templates/ionic-capacitor/CLAUDE.md) | Ionic 7+, Capacitor | Web-to-native with native plugins |
| [swift-ios](templates/swift-ios/CLAUDE.md) | SwiftUI, Swift Concurrency | Native iOS apps |
| [kotlin-android](templates/kotlin-android/CLAUDE.md) | Jetpack Compose, Hilt | Native Android apps |
| [dotnet-maui](templates/dotnet-maui/CLAUDE.md) | .NET MAUI, C#, MVVM | Cross-platform .NET mobile/desktop |

<br>

### > Desktop

| Template | Stack | When to use |
|:---------|:------|:------------|
| [electron](templates/electron/CLAUDE.md) | Electron 28+, React, Vite | Cross-platform desktop with web tech |
| [tauri](templates/tauri/CLAUDE.md) | Tauri 2, Rust + React | Lightweight native desktop apps |

<br>

### > CLI & Tools

| Template | Stack | When to use |
|:---------|:------|:------------|
| [cli-node](templates/cli-node/CLAUDE.md) | Node.js, Commander, Chalk | Node.js command-line tools |
| [cli-python](templates/cli-python/CLAUDE.md) | Python, Typer, Rich | Python command-line tools |
| [cli-go](templates/cli-go/CLAUDE.md) | Go, Cobra, Bubble Tea | Go command-line tools and TUIs |
| [rust-cli](templates/rust-cli/CLAUDE.md) | Rust, clap, indicatif | Rust command-line tools |
| [vscode-extension](templates/vscode-extension/CLAUDE.md) | VS Code API, TypeScript | Editor extensions and language servers |
| [chrome-extension](templates/chrome-extension/CLAUDE.md) | Chrome MV3, CRXJS | Browser extensions |

<br>

### > Testing

| Template | Stack | When to use |
|:---------|:------|:------------|
| [playwright](templates/playwright/CLAUDE.md) | Playwright, TypeScript | Cross-browser E2E testing |
| [cypress](templates/cypress/CLAUDE.md) | Cypress, TypeScript | E2E and component testing |

<br>

### > DevOps & Infra

| Template | Stack | When to use |
|:---------|:------|:------------|
| [docker-compose](templates/docker-compose/CLAUDE.md) | Docker, Compose v2 | Multi-container local dev and deploy |
| [kubernetes](templates/kubernetes/CLAUDE.md) | Kubernetes, Kustomize | Container orchestration manifests |
| [helm-chart](templates/helm-chart/CLAUDE.md) | Helm 3, Go templates | Kubernetes package management |
| [terraform](templates/terraform/CLAUDE.md) | Terraform 1.6+, HCL | Infrastructure as code |
| [pulumi](templates/pulumi/CLAUDE.md) | Pulumi, TypeScript | IaC with real programming languages |
| [aws-cdk](templates/aws-cdk/CLAUDE.md) | AWS CDK v2, TypeScript | AWS infrastructure with constructs |
| [github-actions](templates/github-actions/CLAUDE.md) | GitHub Actions, YAML | CI/CD pipelines and automation |
| [ansible](templates/ansible/CLAUDE.md) | Ansible, Jinja2, YAML | Configuration management and provisioning |

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
| [unreal-cpp](templates/unreal-cpp/CLAUDE.md) | Unreal Engine 5, C++ | AAA game development |

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

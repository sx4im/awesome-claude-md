# Stop writing CLAUDE.md files from scratch.

50 opinionated CLAUDE.md templates. Grab one for your stack, edit the placeholders, get useful output.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)

---

Every developer using Claude Code needs a `CLAUDE.md`. Most throw one together in 20 minutes, then spend the rest of the week confused about why Claude keeps generating barrel files or ignoring their project's conventions.

These templates fix that. Pick your stack, copy the file, fill in the blanks.

```bash
# browse, pick, copy
cp templates/nextjs/CLAUDE.md ~/your-project/CLAUDE.md
```

Replace the `[PLACEHOLDERS]` and you're done.

## Templates

[Frontend](#frontend) · [Full-stack](#full-stack) · [Backend](#backend) · [Mobile](#mobile) · [Desktop](#desktop) · [CLI and tools](#cli-and-tools) · [DevOps and infra](#devops-and-infra) · [Specialized](#specialized)

---

### Frontend

[nextjs](templates/nextjs/CLAUDE.md) · [react-vite](templates/react-vite/CLAUDE.md) · [sveltekit](templates/sveltekit/CLAUDE.md) · [nuxt](templates/nuxt/CLAUDE.md) · [remix](templates/remix/CLAUDE.md) · [astro](templates/astro/CLAUDE.md) · [angular](templates/angular/CLAUDE.md) · [qwik](templates/qwik/CLAUDE.md) · [solidjs](templates/solidjs/CLAUDE.md) · [threejs-r3f](templates/threejs-r3f/CLAUDE.md) · [htmx-go](templates/htmx-go/CLAUDE.md)

Next.js 14+ with App Router. React 18 SPAs on Vite. SvelteKit with runes. Nuxt 3 with Composition API. Remix loaders and actions. Astro content sites with zero JS by default. Angular 17+ with signals and standalone components. Qwik's resumable architecture. SolidJS fine-grained reactivity. Three.js via React Three Fiber. HTMX + Go for people who don't want an SPA.

---

### Full-stack

[t3-stack](templates/t3-stack/CLAUDE.md) · [saas-fullstack](templates/saas-fullstack/CLAUDE.md) · [supabase-nextjs](templates/supabase-nextjs/CLAUDE.md) · [shopify-hydrogen](templates/shopify-hydrogen/CLAUDE.md) · [payload-cms](templates/payload-cms/CLAUDE.md)

T3 stack with end-to-end type safety through tRPC. SaaS boilerplate with Stripe billing, Clerk auth, Resend emails. Supabase + Next.js with RLS and realtime. Shopify Hydrogen storefronts. Payload CMS 3 with block-based layouts.

---

### Backend

[python-fastapi](templates/python-fastapi/CLAUDE.md) · [django](templates/django/CLAUDE.md) · [express-typescript](templates/express-typescript/CLAUDE.md) · [nestjs](templates/nestjs/CLAUDE.md) · [go-api](templates/go-api/CLAUDE.md) · [grpc-go](templates/grpc-go/CLAUDE.md) · [rust-axum](templates/rust-axum/CLAUDE.md) · [spring-boot](templates/spring-boot/CLAUDE.md) · [dotnet-api](templates/dotnet-api/CLAUDE.md) · [laravel](templates/laravel/CLAUDE.md) · [elixir-phoenix](templates/elixir-phoenix/CLAUDE.md) · [ruby-on-rails](templates/ruby-on-rails/CLAUDE.md) · [graphql-api](templates/graphql-api/CLAUDE.md) · [firebase-functions](templates/firebase-functions/CLAUDE.md)

FastAPI with SQLAlchemy 2.0. Django with DRF and Celery. Express + TypeScript three-layer architecture. NestJS modules with DI and Guards. Go with Chi and sqlc. gRPC services with Connect RPC and Buf. Rust with Axum and SQLx. Spring Boot 3.2 with JPA and Flyway. .NET 8 Minimal APIs with MediatR CQRS. Laravel 11 with Eloquent. Elixir Phoenix LiveView. Rails 7 with Hotwire. GraphQL with Pothos and DataLoader. Firebase Cloud Functions v2.

---

### Mobile

[flutter](templates/flutter/CLAUDE.md) · [react-native-expo](templates/react-native-expo/CLAUDE.md) · [swift-ios](templates/swift-ios/CLAUDE.md) · [kotlin-android](templates/kotlin-android/CLAUDE.md)

Flutter with Riverpod and GoRouter. React Native on Expo SDK 50+ with Expo Router. Native iOS with SwiftUI and Swift Concurrency. Native Android with Jetpack Compose and Hilt.

---

### Desktop

[electron](templates/electron/CLAUDE.md) · [tauri](templates/tauri/CLAUDE.md)

Electron 28+ with context isolation and typed IPC. Tauri 2 with Rust commands and capability-based permissions.

---

### CLI and tools

[cli-node](templates/cli-node/CLAUDE.md) · [rust-cli](templates/rust-cli/CLAUDE.md) · [chrome-extension](templates/chrome-extension/CLAUDE.md) · [telegram-bot](templates/telegram-bot/CLAUDE.md)

Node.js CLIs with Commander and Chalk. Rust CLIs with clap derive. Chrome extensions on Manifest V3 with CRXJS. Telegram bots with python-telegram-bot v20.

---

### DevOps and infra

[docker-compose](templates/docker-compose/CLAUDE.md) · [terraform](templates/terraform/CLAUDE.md) · [aws-cdk](templates/aws-cdk/CLAUDE.md)

Docker multi-stage builds with Compose v2. Terraform modules with remote state. AWS CDK v2 with L3 constructs and snapshot testing.

---

### Specialized

[monorepo](templates/monorepo/CLAUDE.md) · [ml-python](templates/ml-python/CLAUDE.md) · [open-source-lib](templates/open-source-lib/CLAUDE.md) · [unity-csharp](templates/unity-csharp/CLAUDE.md) · [deno-fresh](templates/deno-fresh/CLAUDE.md) · [solidity-hardhat](templates/solidity-hardhat/CLAUDE.md) · [wordpress-theme](templates/wordpress-theme/CLAUDE.md)

Turborepo monorepos with pnpm workspaces. ML projects with PyTorch and MLflow. Open source npm packages with Changesets and tsup. Unity game dev with ScriptableObjects. Deno Fresh with islands architecture. Solidity smart contracts on Hardhat. WordPress block themes.

---

## Why this exists

Claude won't know you use named exports, prefer `date-fns` over `moment`, or have a no-`any` policy unless you tell it. A `CLAUDE.md` that says "write clean code" teaches it nothing.

Writing good rules from scratch is tedious. File naming, import ordering, anti-patterns, library choices. Most people skip it.

The sharp edges differ per stack too. What Claude gets wrong in Next.js has nothing to do with what it gets wrong in FastAPI.

Every rule here exists because someone shipped code where Claude did the wrong thing without it.

## Contributing

New templates and fixes welcome. Read the [Contributing Guide](CONTRIBUTING.md) before opening a PR.

## Star History

<a href="https://star-history.com/#sx4im/awesome-claude-md&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date" />
 </picture>
</a>

---

Made by people who got tired of Claude ignoring their coding standards.

<!-- GitHub Topics (for maintainers): claude-code, gemini-cli, codex-cli, antigravity, cursor, github-copilot, opencode, agentic-skills, ai-coding, llm-tools, ai-agents, autonomous-coding, mcp, ai-developer-tools, ai-pair-programming, vibe-coding, skill, skills, SKILL.md, rules.md, CLAUDE.md, GEMINI.md, CURSOR.md -->
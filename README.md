# Stop writing CLAUDE.md files from scratch.

**50 opinionated CLAUDE.md templates. Grab one for your stack and actually get useful output.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)

---

Every developer using Claude Code needs a `CLAUDE.md`. Most throw one together in 20 minutes and then spend the next week confused about why Claude keeps generating barrel files or ignoring their project's conventions. Pick a template for your stack, edit the placeholders, done.

## Quick start

```bash
# 1. Browse the templates
ls templates/

# 2. Pick your stack
cat templates/nextjs/CLAUDE.md

# 3. Copy it to your project root and edit the [PLACEHOLDERS]
cp templates/nextjs/CLAUDE.md ~/your-project/CLAUDE.md
```

That's it. Open the file, replace the `[PLACEHOLDERS]` with your project specifics, and Claude Code immediately starts following your conventions.

## Templates

### Frontend

- **[nextjs](templates/nextjs/CLAUDE.md)** — Next.js 14+, TypeScript, Tailwind, Prisma
- **[react-vite](templates/react-vite/CLAUDE.md)** — React 18, Vite, TanStack Query, Zustand
- **[sveltekit](templates/sveltekit/CLAUDE.md)** — SvelteKit 2.x, Svelte 5 runes, Tailwind
- **[nuxt](templates/nuxt/CLAUDE.md)** — Nuxt 3.x, Vue 3 Composition API, Pinia
- **[remix](templates/remix/CLAUDE.md)** — Remix 2.x, loader/action pattern, Prisma
- **[astro](templates/astro/CLAUDE.md)** — Astro 4.x, Content Collections, island architecture
- **[angular](templates/angular/CLAUDE.md)** — Angular 17+, Signals, standalone components
- **[qwik](templates/qwik/CLAUDE.md)** — Qwik City, resumable apps, $ optimizer
- **[solidjs](templates/solidjs/CLAUDE.md)** — SolidJS/SolidStart, fine-grained signals
- **[threejs-r3f](templates/threejs-r3f/CLAUDE.md)** — React Three Fiber, Drei, Rapier physics
- **[htmx-go](templates/htmx-go/CLAUDE.md)** — Go + HTMX + Templ, no SPA, HTML fragments

### Full-stack

- **[t3-stack](templates/t3-stack/CLAUDE.md)** — tRPC, Next.js, Prisma, NextAuth, Zod
- **[saas-fullstack](templates/saas-fullstack/CLAUDE.md)** — Next.js 14, Stripe, Clerk, Resend
- **[supabase-nextjs](templates/supabase-nextjs/CLAUDE.md)** — Next.js + Supabase, RLS, realtime
- **[shopify-hydrogen](templates/shopify-hydrogen/CLAUDE.md)** — Hydrogen, Remix, Storefront API
- **[payload-cms](templates/payload-cms/CLAUDE.md)** — Payload CMS 3.x, Next.js, Lexical

### Backend

- **[python-fastapi](templates/python-fastapi/CLAUDE.md)** — FastAPI, SQLAlchemy 2.0, Pydantic v2
- **[django](templates/django/CLAUDE.md)** — Django 5.x, DRF, Celery, PostgreSQL
- **[express-typescript](templates/express-typescript/CLAUDE.md)** — Express, TypeScript, Prisma, Zod
- **[nestjs](templates/nestjs/CLAUDE.md)** — NestJS 10+, DI, DTOs, Guards, Passport
- **[go-api](templates/go-api/CLAUDE.md)** — Go 1.22+, Chi, sqlc, PostgreSQL
- **[grpc-go](templates/grpc-go/CLAUDE.md)** — Go, gRPC, Connect RPC, Protobuf, Buf
- **[rust-axum](templates/rust-axum/CLAUDE.md)** — Rust, Axum 0.7+, SQLx, Tower, Tokio
- **[spring-boot](templates/spring-boot/CLAUDE.md)** — Java 21+, Spring Boot 3.2, JPA, Flyway
- **[dotnet-api](templates/dotnet-api/CLAUDE.md)** — .NET 8, C# 12, EF Core, MediatR CQRS
- **[laravel](templates/laravel/CLAUDE.md)** — PHP 8.2+, Laravel 11, Eloquent, Sanctum
- **[elixir-phoenix](templates/elixir-phoenix/CLAUDE.md)** — Elixir, Phoenix 1.7+, LiveView, Ecto
- **[ruby-on-rails](templates/ruby-on-rails/CLAUDE.md)** — Rails 7.1+, Hotwire, Turbo, Sidekiq
- **[graphql-api](templates/graphql-api/CLAUDE.md)** — Apollo/Yoga, Pothos, Prisma, DataLoader
- **[firebase-functions](templates/firebase-functions/CLAUDE.md)** — Cloud Functions v2, Firestore

### Mobile

- **[flutter](templates/flutter/CLAUDE.md)** — Flutter 3.x, Riverpod, GoRouter, Freezed
- **[react-native-expo](templates/react-native-expo/CLAUDE.md)** — Expo SDK 50+, Expo Router
- **[swift-ios](templates/swift-ios/CLAUDE.md)** — SwiftUI, Swift Concurrency, SwiftData
- **[kotlin-android](templates/kotlin-android/CLAUDE.md)** — Jetpack Compose, Hilt, Room, Retrofit

### Desktop

- **[electron](templates/electron/CLAUDE.md)** — Electron 28+, React, Vite, typed IPC
- **[tauri](templates/tauri/CLAUDE.md)** — Tauri 2.x, Rust commands, React frontend

### CLI and tools

- **[cli-node](templates/cli-node/CLAUDE.md)** — Node.js, Commander, Chalk, Inquirer
- **[rust-cli](templates/rust-cli/CLAUDE.md)** — Rust, clap derive, thiserror, indicatif
- **[chrome-extension](templates/chrome-extension/CLAUDE.md)** — Chrome MV3, TypeScript, CRXJS
- **[telegram-bot](templates/telegram-bot/CLAUDE.md)** — Python, python-telegram-bot v20+

### DevOps and infra

- **[docker-compose](templates/docker-compose/CLAUDE.md)** — Docker, multi-stage builds, Compose v2
- **[terraform](templates/terraform/CLAUDE.md)** — Terraform 1.6+, HCL, AWS/GCP/Azure
- **[aws-cdk](templates/aws-cdk/CLAUDE.md)** — AWS CDK v2, TypeScript, L3 constructs

### Specialized

- **[monorepo](templates/monorepo/CLAUDE.md)** — Turborepo, pnpm workspaces, TypeScript
- **[ml-python](templates/ml-python/CLAUDE.md)** — PyTorch, MLflow, scikit-learn, polars
- **[open-source-lib](templates/open-source-lib/CLAUDE.md)** — TypeScript, Vitest, tsup, Changesets
- **[unity-csharp](templates/unity-csharp/CLAUDE.md)** — Unity 2022+, C#, URP, DOTween
- **[deno-fresh](templates/deno-fresh/CLAUDE.md)** — Deno, Fresh 2.x, Preact, Deno KV
- **[solidity-hardhat](templates/solidity-hardhat/CLAUDE.md)** — Solidity 0.8+, Hardhat, Ethers.js v6
- **[wordpress-theme](templates/wordpress-theme/CLAUDE.md)** — WordPress 6.x, PHP 8.1+, Gutenberg

## Why this exists

Claude won't magically know you use named exports, prefer `date-fns` over `moment`, or have a strict no-`any` policy. A `CLAUDE.md` that says "write clean code" teaches it nothing. You need specific rules.

Writing those rules from scratch is tedious. You have to think about file naming, import ordering, anti-patterns, library choices, architecture. Most people skip it and get mediocre output.

The sharp edges are also different per stack. What Claude gets wrong in a Next.js App Router project has nothing to do with what it gets wrong in FastAPI. Generic "best practices" don't cut it.

Every rule in these templates exists because someone shipped code where Claude did the wrong thing without it.

## Contributing

New templates and fixes to existing ones are welcome. Read the [Contributing Guide](CONTRIBUTING.md) before opening a PR.

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
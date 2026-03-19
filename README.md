# Stop writing CLAUDE.md files from scratch.

**Production-ready CLAUDE.md templates for every major stack. Copy, paste, ship.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)

---

Every developer using Claude Code needs a `CLAUDE.md`. Most write a bad one in 20 minutes and spend the next week wondering why Claude keeps generating barrel files, using default exports, or ignoring their project's conventions entirely. This repo gives you a production-quality starting point for your exact stack — copy, paste, customize, and actually get useful output from day one.

## ⚡ Quick Start

```bash
# 1. Browse the templates
ls templates/

# 2. Pick your stack
cat templates/nextjs/CLAUDE.md

# 3. Copy it to your project root and edit the [PLACEHOLDERS]
cp templates/nextjs/CLAUDE.md ~/your-project/CLAUDE.md
```

That's it. Open the file, replace the `[PLACEHOLDERS]` with your project specifics, and Claude Code immediately starts following your conventions.

## 📋 Templates

| Template | Stack | Best For | Lines |
|----------|-------|----------|-------|
| **Frontend** ||||
| [nextjs](templates/nextjs/CLAUDE.md) | Next.js 14+, TypeScript, Tailwind, Prisma | Production web apps — server components, ISR | ~84 |
| [react-vite](templates/react-vite/CLAUDE.md) | React 18, Vite, TanStack Query, Zustand | SPAs, dashboards, internal tools | ~82 |
| [sveltekit](templates/sveltekit/CLAUDE.md) | SvelteKit 2.x, Svelte 5, Tailwind | Full-stack Svelte — runes, form actions | ~85 |
| [nuxt](templates/nuxt/CLAUDE.md) | Nuxt 3.x, Vue 3, Pinia, Nitro | Full-stack Vue — Composition API, auto-imports | ~91 |
| [remix](templates/remix/CLAUDE.md) | Remix 2.x, React 18, Prisma | Loader/action architecture, progressive enhancement | ~73 |
| [astro](templates/astro/CLAUDE.md) | Astro 4.x, Content Collections, MDX | Content sites — island architecture, zero-JS defaults | ~95 |
| [angular](templates/angular/CLAUDE.md) | Angular 17+, Signals, Standalone Components | Enterprise apps — OnPush, lazy routes, inject() | ~78 |
| [threejs-r3f](templates/threejs-r3f/CLAUDE.md) | React Three Fiber, Drei, Rapier | 3D web apps — declarative scenes, useFrame, instancing | ~80 |
| **Full-Stack** ||||
| [t3-stack](templates/t3-stack/CLAUDE.md) | tRPC, Next.js, Prisma, NextAuth | End-to-end type-safe apps — tRPC procedures, Zod | ~82 |
| [saas-fullstack](templates/saas-fullstack/CLAUDE.md) | Next.js 14, Stripe, Clerk, Resend | Multi-tenant SaaS with billing and auth | ~96 |
| [supabase-nextjs](templates/supabase-nextjs/CLAUDE.md) | Next.js, Supabase Auth/DB/Storage | BaaS apps — RLS, dual clients, realtime | ~79 |
| [shopify-hydrogen](templates/shopify-hydrogen/CLAUDE.md) | Hydrogen, Remix, Storefront API | Headless Shopify storefronts | ~70 |
| [payload-cms](templates/payload-cms/CLAUDE.md) | Payload CMS 3.x, Next.js, Lexical | Headless CMS — collections, blocks, access control | ~83 |
| **Backend** ||||
| [python-fastapi](templates/python-fastapi/CLAUDE.md) | Python 3.11+, FastAPI, SQLAlchemy 2.0 | Async REST APIs, service-layer architecture | ~88 |
| [django](templates/django/CLAUDE.md) | Django 5.x, DRF, Celery, PostgreSQL | REST APIs — fat models, split settings | ~98 |
| [express-typescript](templates/express-typescript/CLAUDE.md) | Express, TypeScript, Prisma, Zod | Node.js APIs — three-layer, JWT auth | ~91 |
| [go-api](templates/go-api/CLAUDE.md) | Go 1.22+, Chi, sqlc, PostgreSQL | Go backends — compile-time SQL, stdlib-first | ~89 |
| [rust-axum](templates/rust-axum/CLAUDE.md) | Rust, Axum, SQLx, Tokio | Performant APIs — Tower middleware, tracing | ~85 |
| [spring-boot](templates/spring-boot/CLAUDE.md) | Java 21+, Spring Boot 3.2, JPA | Enterprise APIs — MapStruct, Flyway, Testcontainers | ~83 |
| [dotnet-api](templates/dotnet-api/CLAUDE.md) | .NET 8, C# 12, EF Core, MediatR | Clean Architecture, Minimal APIs, CQRS | ~81 |
| [laravel](templates/laravel/CLAUDE.md) | PHP 8.2+, Laravel 11, Eloquent | PHP apps — action classes, Form Requests | ~94 |
| [graphql-api](templates/graphql-api/CLAUDE.md) | Apollo/Yoga, Pothos, Prisma | GraphQL — code-first schema, DataLoader | ~75 |
| [firebase-functions](templates/firebase-functions/CLAUDE.md) | Cloud Functions 2nd gen, Firestore | Serverless — typed Firestore, idempotent triggers | ~78 |
| **Mobile** ||||
| [flutter](templates/flutter/CLAUDE.md) | Flutter 3.x, Riverpod, GoRouter, Freezed | Cross-platform mobile — clean state management | ~91 |
| [react-native-expo](templates/react-native-expo/CLAUDE.md) | Expo SDK 50+, Expo Router, TypeScript | Mobile apps — SecureStore, managed workflow | ~86 |
| [swift-ios](templates/swift-ios/CLAUDE.md) | SwiftUI, Swift Concurrency, SwiftData | Native iOS — MVVM with @Observable | ~76 |
| [kotlin-android](templates/kotlin-android/CLAUDE.md) | Jetpack Compose, Hilt, Room, Retrofit | Native Android — Clean Architecture, StateFlow | ~86 |
| **Desktop** ||||
| [electron](templates/electron/CLAUDE.md) | Electron 28+, React, TypeScript, Vite | Desktop apps — context isolation, typed IPC | ~87 |
| [tauri](templates/tauri/CLAUDE.md) | Tauri 2.x, Rust, React, SQLite | Lightweight desktop — Rust commands, capabilities | ~76 |
| **CLI & Tools** ||||
| [cli-node](templates/cli-node/CLAUDE.md) | Node.js, Commander, Chalk, Inquirer | CLI tools — structured output, CI mode | ~83 |
| [rust-cli](templates/rust-cli/CLAUDE.md) | Rust, clap, thiserror, indicatif | Rust CLIs — derive API, library/binary split | ~77 |
| [chrome-extension](templates/chrome-extension/CLAUDE.md) | Chrome MV3, TypeScript, CRXJS | Browser extensions — service workers, typed IPC | ~84 |
| [telegram-bot](templates/telegram-bot/CLAUDE.md) | Python, python-telegram-bot v20+ | Bots — async handlers, ConversationHandler | ~79 |
| **DevOps & Infra** ||||
| [docker-compose](templates/docker-compose/CLAUDE.md) | Docker, multi-stage builds, Compose v2 | Multi-service orchestration, health checks | ~96 |
| [terraform](templates/terraform/CLAUDE.md) | Terraform 1.6+, HCL, AWS/GCP/Azure | IaC — modules, remote state, for_each | ~93 |
| **Specialized** ||||
| [monorepo](templates/monorepo/CLAUDE.md) | Turborepo, pnpm workspaces, TypeScript | Multi-app repos, turbo pipelines | ~109 |
| [ml-python](templates/ml-python/CLAUDE.md) | Python, PyTorch, MLflow, scikit-learn | ML — experiment tracking, reproducibility | ~113 |
| [open-source-lib](templates/open-source-lib/CLAUDE.md) | TypeScript, Vitest, tsup, Changesets | npm packages — semver, bundle size discipline | ~119 |
| [unity-csharp](templates/unity-csharp/CLAUDE.md) | Unity 2022+, C#, URP | Game dev — ScriptableObjects, object pooling | ~76 |
| [deno-fresh](templates/deno-fresh/CLAUDE.md) | Deno, Fresh 2.x, Preact | Edge apps — islands architecture, Deno KV | ~80 |

## 🔍 Why This Exists

- **Claude ignores your conventions without explicit instructions.** It won't magically know you use named exports, `date-fns` instead of `moment`, or that your team has a strict no-`any` policy. A generic `CLAUDE.md` that says "write clean code" teaches it nothing.
- **Writing a good CLAUDE.md from scratch is surprisingly hard.** You need to think about file naming, import ordering, anti-patterns, library preferences, and architectural decisions — all while being specific enough that an AI can actually follow the rules. Most developers skip this and get mediocre output.
- **Every stack has different sharp edges.** The things Claude gets wrong in a Next.js App Router project are completely different from what it gets wrong in a FastAPI project. You need stack-specific rules, not generic "best practices."
- **These templates encode real engineering opinions.** Every rule in every template exists because someone shipped code where Claude did the wrong thing without that rule. These aren't theoretical — they're battle-tested.

## 🤝 Contributing

We welcome new templates and improvements to existing ones. Read the [Contributing Guide](CONTRIBUTING.md) before opening a PR.

## Star History

<a href="https://star-history.com/#sx4im/awesome-claude-md&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date" />
 </picture>
</a>

---

**Built by developers who got tired of Claude ignoring their coding standards.**

<!-- GitHub Topics (for maintainers): claude-code, gemini-cli, codex-cli, antigravity, cursor, github-copilot, opencode, agentic-skills, ai-coding, llm-tools, ai-agents, autonomous-coding, mcp, ai-developer-tools, ai-pair-programming, vibe-coding, skill, skills, SKILL.md, rules.md, CLAUDE.md, GEMINI.md, CURSOR.md -->
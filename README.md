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
| [nextjs](templates/nextjs/CLAUDE.md) | Next.js 14+ App Router, TypeScript, Tailwind, Prisma | Production web apps — server components, route handlers, ISR | ~84 |
| [react-vite](templates/react-vite/CLAUDE.md) | React 18, TypeScript, Vite, TanStack Query, Zustand | SPAs, dashboards, internal tools — strict component architecture | ~82 |
| [python-fastapi](templates/python-fastapi/CLAUDE.md) | Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2 | Async REST APIs with service-layer architecture, Alembic migrations | ~88 |
| [flutter](templates/flutter/CLAUDE.md) | Flutter 3.x, Dart, Riverpod, GoRouter, Freezed | Cross-platform mobile apps with clean state management | ~91 |
| [saas-fullstack](templates/saas-fullstack/CLAUDE.md) | Next.js 14, Prisma, Stripe, Clerk, Resend | Multi-tenant SaaS with billing, auth, transactional email | ~96 |
| [monorepo](templates/monorepo/CLAUDE.md) | Turborepo, pnpm workspaces, TypeScript | Multi-app repos with shared packages, turbo pipelines | ~109 |
| [ml-python](templates/ml-python/CLAUDE.md) | Python 3.11+, PyTorch, scikit-learn, MLflow | ML projects — experiment tracking, reproducibility, model serving | ~113 |
| [open-source-lib](templates/open-source-lib/CLAUDE.md) | TypeScript, Vitest, tsup, Changesets | npm packages — public API design, semver, bundle size discipline | ~119 |
| [django](templates/django/CLAUDE.md) | Python 3.11+, Django 5.x, DRF, Celery | REST APIs with fat models, split settings, background tasks | ~98 |
| [express-typescript](templates/express-typescript/CLAUDE.md) | Node.js 20+, Express, TypeScript, Prisma | API servers — three-layer architecture, Zod validation, JWT auth | ~91 |
| [go-api](templates/go-api/CLAUDE.md) | Go 1.22+, Chi, PostgreSQL, sqlc | Go backends — compile-time SQL, dependency injection, stdlib-first | ~89 |
| [react-native-expo](templates/react-native-expo/CLAUDE.md) | React Native 0.73+, Expo SDK 50+, TypeScript | Mobile apps with Expo Router, SecureStore, managed workflow | ~86 |
| [sveltekit](templates/sveltekit/CLAUDE.md) | SvelteKit 2.x, Svelte 5, TypeScript, Tailwind | Full-stack Svelte — runes, server load, form actions | ~85 |
| [nuxt](templates/nuxt/CLAUDE.md) | Nuxt 3.x, Vue 3, TypeScript, Pinia | Full-stack Vue — Composition API, auto-imports, Nitro server | ~91 |
| [chrome-extension](templates/chrome-extension/CLAUDE.md) | Chrome Extension MV3, TypeScript, Vite, CRXJS | Browser extensions — service workers, typed IPC, minimal permissions | ~84 |
| [cli-node](templates/cli-node/CLAUDE.md) | Node.js 20+, TypeScript, Commander, Chalk | CLI tools — structured output, non-interactive CI mode, exit codes | ~83 |
| [astro](templates/astro/CLAUDE.md) | Astro 4.x, TypeScript, Content Collections, MDX | Content sites — static-first, island architecture, zero-JS defaults | ~95 |
| [rust-axum](templates/rust-axum/CLAUDE.md) | Rust, Axum 0.7+, SQLx, Tokio, PostgreSQL | Performant APIs — compile-time SQL, Tower middleware, tracing | ~85 |
| [electron](templates/electron/CLAUDE.md) | Electron 28+, React, TypeScript, Vite | Desktop apps — context isolation, typed IPC, preload bridge | ~87 |
| [laravel](templates/laravel/CLAUDE.md) | PHP 8.2+, Laravel 11, Eloquent, Redis queues | PHP web apps — action classes, Form Requests, API Resources | ~94 |

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
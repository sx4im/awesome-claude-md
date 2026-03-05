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
| [nextjs](templates/nextjs/CLAUDE.md) | Next.js 14+ App Router, TypeScript, Tailwind, Prisma | Production web apps using the App Router — server components, route handlers, ISR | ~120 |
| [react-vite](templates/react-vite/CLAUDE.md) | React 18, TypeScript, Vite, TanStack Query, Zustand | SPAs, dashboards, internal tools — strict component architecture, no SSR | ~115 |
| [python-fastapi](templates/python-fastapi/CLAUDE.md) | Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2 | REST APIs with async handlers, service-layer architecture, Alembic migrations | ~120 |
| [flutter](templates/flutter/CLAUDE.md) | Flutter 3.x, Dart, Riverpod, GoRouter, Freezed | Cross-platform mobile apps with clean state management and code generation | ~110 |
| [saas-fullstack](templates/saas-fullstack/CLAUDE.md) | Next.js 14, Prisma, Stripe, Clerk, Resend | Multi-tenant SaaS with billing, auth, transactional email — the full stack | ~130 |
| [monorepo](templates/monorepo/CLAUDE.md) | Turborepo, pnpm workspaces, TypeScript, shared packages | Multi-app repos with shared UI libraries, utils, and type packages | ~110 |
| [ml-python](templates/ml-python/CLAUDE.md) | Python 3.11+, PyTorch, scikit-learn, MLflow, Jupyter | ML projects with experiment tracking, reproducible training, and model serving | ~115 |
| [open-source-lib](templates/open-source-lib/CLAUDE.md) | TypeScript, Vitest, tsup, Changesets, GitHub Actions | Open-source npm packages — public API design, semver, bundle size discipline | ~110 |

## 🔍 Why This Exists

- **Claude ignores your conventions without explicit instructions.** It won't magically know you use named exports, `date-fns` instead of `moment`, or that your team has a strict no-`any` policy. A generic `CLAUDE.md` that says "write clean code" teaches it nothing.
- **Writing a good CLAUDE.md from scratch is surprisingly hard.** You need to think about file naming, import ordering, anti-patterns, library preferences, and architectural decisions — all while being specific enough that an AI can actually follow the rules. Most developers skip this and get mediocre output.
- **Every stack has different sharp edges.** The things Claude gets wrong in a Next.js App Router project are completely different from what it gets wrong in a FastAPI project. You need stack-specific rules, not generic "best practices."
- **These templates encode real engineering opinions.** Every rule in every template exists because someone shipped code where Claude did the wrong thing without that rule. These aren't theoretical — they're battle-tested.

## 🤝 Contributing

We welcome new templates and improvements to existing ones. Read the [Contributing Guide](CONTRIBUTING.md) before opening a PR.

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sx4im/awesome-claude-md&type=Date)](https://star-history.com/#sx4im/awesome-claude-md&Date)

---

**Built by developers who got tired of Claude ignoring their coding standards.**

# Contributing to awesome-CLAUDE.md

We want more templates. But we want *good* ones — specific, opinionated, and battle-tested. Here's how to contribute without getting your PR rejected.

## What Makes a Good Template

Every template in this repo follows five rules. If your submission breaks any of them, it won't be merged.

### 1. Every rule must be concrete

- ❌ **BAD:** "Use meaningful variable names"
- ✅ **GOOD:** "Name boolean variables with `is`/`has`/`should` prefix: `isLoading`, `hasError`, `shouldRefetch`"

### 2. Library preferences must include a reason

- ❌ **BAD:** "Use a modern date library"
- ✅ **GOOD:** "Use `date-fns` over `moment` — it's tree-shakeable, moment is 300kb and deprecated"

### 3. Anti-patterns must be stack-specific

- ❌ **BAD:** "Don't write bad code"
- ✅ **GOOD:** "Never use `getServerSideProps` in an App Router project — use server components or route handlers instead"

### 4. File examples must be real

- ❌ **BAD:** "Name files appropriately"
- ✅ **GOOD:** "Components: `PascalCase.tsx` (e.g., `UserProfile.tsx`). Hooks: `camelCase.ts` with `use` prefix (e.g., `useAuth.ts`). Utils: `camelCase.ts` (e.g., `formatCurrency.ts`)"

### 5. Commands must be copy-pasteable

If you reference a CLI command, it should work when pasted into a terminal. No pseudocode, no "run the appropriate command."

---

## How to Submit

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/awesome-CLAUDE.md.git
cd awesome-CLAUDE.md

# 2. Create a branch
git checkout -b add-template/your-stack-name

# 3. Add your template
mkdir templates/your-stack-name
# Write your CLAUDE.md — see structure below

# 4. Validate it passes
python scripts/validate.py

# 5. Commit and push
git add .
git commit -m "feat: add your-stack-name template"
git push origin add-template/your-stack-name
```

Then open a PR. That's it.

---

## Template Structure Requirements

Every `CLAUDE.md` must include these sections (order matters):

1. **Project header** — `# [PROJECT NAME] — [ONE LINE DESCRIPTION]` placeholder
2. **Tech stack** — Exact versions and key libraries
3. **Architecture / project structure** — Where files go and why
4. **Coding conventions** — Naming, imports, patterns
5. **Library preferences** — What to use and what to avoid, with reasons
6. **File naming conventions** — With real examples
7. **NEVER DO THIS section** — Minimum 5 stack-specific anti-patterns
8. **Testing conventions** — How to write and organize tests

Templates must be **80–150 lines**. If you can't say it in 150 lines, you're being too vague. If you need more than 150 lines, you're trying to cover too many stacks in one template — split it.

---

## Review Criteria

Your PR will be rejected if:

- **Any rule could apply to every project on earth.** If it's not specific to the stack, it doesn't belong.
- **The NEVER section has fewer than 5 items.** Generic "don't write bugs" doesn't count.
- **Library recommendations lack reasons.** "Use X" without "because Y" is not helpful.
- **The template is under 80 or over 150 lines.** We enforce this in CI.
- **You use placeholder text that isn't clearly marked as `[PLACEHOLDER]`.** The templates should be ready to copy — only the project-specific parts should be placeholders.
- **You duplicate an existing template's stack.** If a Next.js template already exists, you need a meaningfully different variant (e.g., Pages Router, or Next.js + tRPC).

---

Questions? Open an issue. Don't overthink it — if you've built something real with Claude Code and your `CLAUDE.md` made a noticeable difference, we probably want it here.

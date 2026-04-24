# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Frontend)

### Release Discipline
- Enforce performance budgets (bundle size, LCP, CLS) before merge.
- Preserve accessibility baselines (semantic HTML, keyboard nav, ARIA correctness).
- Block hydration/runtime errors with production build verification.

### Merge/Release Gates
- Typecheck + lint + unit tests + production build pass.
- Critical route smoke tests for navigation, auth, and error boundaries.
- No new console errors/warnings in key user flows.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Tailwind CSS v4 (next-generation engine)
- PostCSS 8+
- Lightning CSS (built into Tailwind v4)
- CSS-first configuration
- Modern browser targets (Chrome 111+, Firefox 128+, Safari 16.4+)

## Project Structure

```
src/
├── app/
│   └── globals.css             # @import "tailwindcss" and theme config
├── components/
│   └── *.tsx                   # Component files using Tailwind classes
├── styles/
│   └── theme.css               # Custom CSS theme variables (optional)
├── css/
│   └── input.css               # Entry point if not using globals.css
└── ...
package.json
tsconfig.json
```

## Architecture Rules

- **CSS-first configuration.** Tailwind v4 moves configuration to CSS using `@theme` directive. No `tailwind.config.js` in most cases.
- **Import Tailwind via CSS.** Use `@import "tailwindcss"` in your CSS entry point. Not `tailwindcss` CLI on individual files.
- **Theme customization in CSS.** Define custom colors, fonts, and spacing using `@theme` blocks in your CSS, not a JS config file.
- **Lightning CSS for transforms.** Tailwind v4 uses Lightning CSS internally for vendor prefixing and syntax lowering.

## Coding Conventions

- CSS entry file:
  ```css
  @import "tailwindcss";
  
  @theme {
    --color-primary: #3b82f6;
    --color-secondary: #64748b;
    --font-sans: Inter, system-ui, sans-serif;
  }
  ```
- Use the `@apply` directive sparingly. Prefer utility classes in markup.
- Variants use stacked classes: `hover:focus:underline` (no `@` prefix needed in v4).
- Container queries: Use `@container` and `@min-*` / `@max-*` variants.

## Library Preferences

- **Build tool:** Vite 5+ or Next.js 15+ with built-in Tailwind support.
- **CSS processing:** Lightning CSS (included with Tailwind v4). No separate Autoprefixer needed.
- **Components:** shadcn/ui or custom Radix wrappers work seamlessly.
- **Typography:** `@tailwindcss/typography` plugin for prose content.

## File Naming

- CSS files can be named anything. The entry point just needs `@import "tailwindcss"`.
- No `tailwind.config.js` means no special naming conventions for config.

## NEVER DO THIS

1. **Never use `tailwind.config.js` with v4 unless necessary.** v4 is designed to be config-free. Only create `tailwind.config.js` for complex plugin setups.
2. **Never forget the `@import "tailwindcss"` directive.** Without this, Tailwind doesn't process your CSS.
3. **Never use `@tailwind` directives.** In v4, use `@import "tailwindcss"` instead of `@tailwind base; @tailwind components; @tailwind utilities`.
4. **Never target older browsers without checking.** Tailwind v4 uses modern CSS features (like cascade layers). Verify your browser support matrix.
5. **Never mix v3 and v4 patterns.** The `@apply` syntax is slightly different. Don't copy v3 examples blindly.
6. **Never ignore the `@theme` block.** This is where you customize in v4. Putting variables elsewhere may not work as expected.
7. **Never forget to update your build pipeline.** If migrating from v3, remove `tailwindcss` CLI from npm scripts. Use your bundler's CSS processing instead.

## Testing

- Visual regression testing with Chromatic or Percy. Tailwind classes compile to CSS—test the output.
- Test responsive designs at actual breakpoints. Use browser DevTools, not just resizing the window.
- Verify CSS variable usage in `@theme` blocks renders correctly across browsers.

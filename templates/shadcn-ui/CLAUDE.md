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

- shadcn/ui component library
- Next.js 14+ (App Router)
- TypeScript 5.x (strict mode)
- Tailwind CSS 3.x
- Radix UI primitives
- Lucide React icons
- Class Variance Authority (CVA)

## Project Structure

```
app/
├── page.tsx                    # Main page using shadcn components
├── layout.tsx                  # Root layout with ThemeProvider
└── globals.css                 # Tailwind + CSS variables
components/
├── ui/                         # shadcn/ui components (auto-installed)
│   ├── button.tsx
│   ├── card.tsx
│   ├── input.tsx
│   ├── dialog.tsx
│   └── ...
├── custom/                     # Your custom components
│   └── [feature]/
lib/
├── utils.ts                    # cn() helper from shadcn
└── hooks/
hooks/
└── use-toast.ts                # Toast hook from shadcn
public/
components.json                 # shadcn/ui configuration
tailwind.config.ts              # Extended with shadcn colors
```

## Architecture Rules

- **Use shadcn/ui as the foundation.** Install components via `npx shadcn add [component]`. Never build primitive components from scratch when shadcn provides them.
- **Customize via Tailwind classes.** Override shadcn components with `className` prop and Tailwind utility classes. Never modify the component source files directly.
- **CSS variables for theming.** Define theme colors in `globals.css` using CSS variables. shadcn components read from these variables. The default setup includes `background`, `foreground`, `primary`, `secondary`, etc.
- **Composition over configuration.** shadcn components are designed to be composed. Use `asChild` prop to merge component behavior with custom elements.

## Coding Conventions

- Import shadcn components from `@/components/ui/[component]`.
- Use the `cn()` utility from `@/lib/utils` for conditional class merging.
- Apply `className` for one-off styling overrides.
- Use `cva` (Class Variance Authority) when creating component variants in custom components.
- Keep component props minimal. shadcn follows Radix patterns—extend Radix props rather than reinventing.

## Library Preferences

- **Icons:** Lucide React (comes with shadcn setup). Not `react-icons` (inconsistent sizing).
- **Animations:** Tailwind `animate-*` classes or Framer Motion for complex interactions. Not GSAP (overkill for UI components).
- **Forms:** React Hook Form + Zod. shadcn form components integrate seamlessly.
- **Themes:** `next-themes` for dark/light mode. shadcn's default setup includes this.
- **Colors:** Use CSS variables defined in `globals.css`. Modify HSL values there, not in component files.

## File Naming

- shadcn components: Match the CLI naming → `button.tsx`, `card.tsx`
- Custom components: PascalCase → `CustomButton.tsx`
- Utility files: camelCase → `utils.ts`, `use-toast.ts`

## NEVER DO THIS

1. **Never edit files in `components/ui/` directly.** These are auto-generated by the shadcn CLI. Use `className` overrides or create wrapper components in `components/custom/`.
2. **Never skip the `cn()` utility.** Manually concatenating classes with template literals breaks when conditional classes are falsy. `cn()` handles this correctly.
3. **Never use arbitrary values in Tailwind for colors.** Define colors in `globals.css` as CSS variables, then reference them in `tailwind.config.ts`.
4. **Never mix shadcn component versions.** If you upgrade one component via `shadcn add`, verify all components work together. shadcn uses Radix versions that must align.
5. **Never ignore the `asChild` prop.** When you need a Button that acts as a Link, use `<Button asChild><Link href="/">...</Link></Button>`. Don't wrap Button around Link blindly.
6. **Never use `!important` in Tailwind classes.** If you need `!important`, your CSS specificity or variable setup is wrong. Fix the root cause.
7. **Never forget to run `npx shadcn add` after updating components.json.** The CLI manages dependencies. Manual copying breaks the versioning.

## Testing

- Test shadcn components via integration tests in Playwright. Test user interactions (clicks, keyboard navigation).
- Test custom components that wrap shadcn primitives with Vitest for logic, Playwright for UI behavior.
- Verify accessibility with Axe or Lighthouse. Radix primitives are accessible, but your compositions may break a11y.

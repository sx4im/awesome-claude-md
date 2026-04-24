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

- Framer Motion v11 (React animation library)
- React 18+
- TypeScript 5.x
- Next.js 15+ or Vite

## Project Structure

```
src/
├── components/
│   ├── animations/             # Reusable animation components
│   │   ├── FadeIn.tsx
│   │   ├── SlideIn.tsx
│   │   └── StaggerContainer.tsx
│   └── features/
│       └── AnimatedCard.tsx
├── hooks/
│   └── useScrollAnimation.ts   # Custom scroll-based animations
├── lib/
│   └── animations.ts           # Shared animation variants
└── ...
```

## Architecture Rules

- **Motion components for animations.** Use `motion.div`, `motion.button` instead of regular elements for animation capabilities.
- **Variants for complex sequences.** Define animation states (hidden, visible, exit) in variant objects. Animate between them.
- **Layout animations for shared element transitions.** Use `layoutId` for smooth morphing between component states.
- **AnimatePresence for exit animations.** Wrap elements that mount/unmount with `AnimatePresence` for exit animations.

## Coding Conventions

- Import motion: `import { motion, AnimatePresence } from 'framer-motion'`.
- Define variants as const objects: `const variants = { hidden: { opacity: 0 }, visible: { opacity: 1 } }`.
- Use `initial`, `animate`, `exit` props with variant names.
- Use `transition` prop for timing: `transition={{ duration: 0.3, ease: "easeOut" }}`.
- For gestures: `whileHover`, `whileTap`, `whileDrag`, `whileFocus`.

## Library Preferences

- **Page transitions:** Use `AnimatePresence` + `motion.div` in layout files.
- **Scroll animations:** `useScroll` and `useTransform` hooks for scroll-linked effects.
- **Drag:** Built-in drag with `drag`, `dragConstraints`, `dragElastic` props.
- **Spring physics:** Use `type: "spring"` for natural-feeling animations.
- **Reduced motion:** Framer Motion respects `prefers-reduced-motion` automatically.

## File Naming

- Animation components: PascalCase with animation intent → `FadeIn.tsx`, `SlideUp.tsx`
- Variant files: `animations.ts`, `transitions.ts`
- Custom hooks: `use[Feature]Animation.ts`

## NEVER DO THIS

1. **Never animate expensive properties.** Avoid animating `width`, `height`, `top`, `left` (triggers layout). Use `transform` and `opacity`.
2. **Never create motion components inside render.** `const MotionDiv = motion.div` should be outside the component.
3. **Never forget `AnimatePresence` for exit animations.** Without it, unmounting elements disappear instantly.
4. **Never use `layoutId` on unrelated elements.** Elements with the same `layoutId` must share visual similarity.
5. **Never animate without transition configuration.** Default transitions may not match your design system.
6. **Never ignore performance in lists.** Use `layout` prop sparingly in large lists. It can be expensive.
7. **Never block the main thread with complex animations.** Use `useReducedMotion` to disable heavy effects for users who need it.

## Testing

- Test animations with React Testing Library by checking element presence after transitions.
- Use `waitFor` for async animation completion.
- Test reduced motion scenarios.
- Visual regression with Chromatic (animations can be paused for snapshots).

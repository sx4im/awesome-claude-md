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

- Chakra UI v3 (Next-generation with Zag.js)
- React 18+
- TypeScript 5.x
- Next.js 15+ or Vite
- Emotion (CSS-in-JS)

## Project Structure

```
src/
├── app/
│   ├── layout.tsx              # Providers wrapper
│   └── page.tsx
├── components/
│   ├── ui/                     # Chakra UI components
│   └── custom/                 # Your composed components
├── theme/
│   ├── index.ts                # Theme export
│   ├── tokens.ts               # Colors, fonts, spacing tokens
│   └── recipes/                # Component style recipes
├── lib/
│   └── utils.ts
└── providers/
    └── chakra-provider.tsx     # ChakraProvider setup
```

## Architecture Rules

- **Use Chakra's composition patterns.** Chakra v3 uses recipes and parts for component styling. Define styles in `theme/recipes/` not inline.
- **Theme tokens first.** Define all colors, spacing, and typography in `theme/tokens.ts`. Reference these tokens in components, not raw values.
- **Style props for one-offs.** Use Chakra's style props (`color="primary.500"`) for simple overrides. Complex styles belong in recipes.
- **Slot recipes for compound components.** Components with multiple parts (Button with icon, Input with addon) use slot recipes.

## Coding Conventions

- Use the `Box` component as the layout primitive. Build other components on top of it.
- Responsive arrays: `<Box p={[2, 4, 6]} />` for mobile-first responsive design.
- Use `forwardRef` for custom components wrapping Chakra primitives.
- Import from `@chakra-ui/react` (single package in v3).
- Type custom component props with `ComponentProps` from Chakra.

## Library Preferences

- **Icons:** Lucide React or `@chakra-ui/icons`. Not mixed icon libraries.
- **Animation:** Framer Motion for complex animations. Chakra v3 uses Zag.js for component state machines.
- **Forms:** React Hook Form integrates well with Chakra's form components.
- **Typography:** Use theme tokens for font families and sizes.

## File Naming

- Theme files: camelCase → `tokens.ts`, `buttonRecipe.ts`
- Component files: PascalCase → `CustomButton.tsx`

## NEVER DO THIS

1. **Never use Chakra UI v2 patterns in v3.** v3 is a complete rewrite with different APIs. Check the v3 docs, not old blog posts.
2. **Never skip the ChakraProvider.** Components won't have access to theme tokens without it.
3. **Never use raw CSS values.** Always reference theme tokens. `padding="4"` not `padding="16px"`.
4. **Never create one-off styled components.** If a component needs custom styling, add a recipe to the theme.
5. **Never forget to configure the Next.js compiler.** Chakra v3 uses Emotion—ensure `transpilePackages` includes `@chakra-ui/react`.
6. **Never mix v2 and v3 imports.** `import { Box } from '@chakra-ui/react'` in v3, not from layout/react packages.
7. **Never ignore the recipe pattern.** Inline `sx` props are for prototyping. Production code uses defined recipes.

## Testing

- Use Testing Library. Chakra components render correctly in JSDOM.
- Test responsive behavior by mocking window dimensions.
- Verify theme token usage matches the design system.

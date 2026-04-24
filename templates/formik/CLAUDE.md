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

- Formik v2 (form library)
- React 18+
- TypeScript 5.x
- Yup (validation)
- React 18+ features

## Project Structure

```
src/
├── components/
│   ├── forms/                  // Form components
│   │   ├── FormInput.tsx
│   │   └── FormError.tsx
│   └── features/
│       └── ContactForm.tsx
├── lib/
│   ├── validation.ts           // Yup schemas
│   └── form-utils.ts
└── schemas/
    └── contact-schema.ts
```

## Architecture Rules

- **Formik wrapper for forms.** Wrap forms in `<Formik>` component or use `useFormik` hook.
- **Field component for inputs.** Use `<Field>` for automatic form binding.
- **ErrorMessage for display.** Use `<ErrorMessage>` component for clean error display.
- **Form for semantic HTML.** Use `<Form>` component for proper form element.

## Coding Conventions

- Formik wrapper: `<Formik initialValues={{...}} validationSchema={schema} onSubmit={handleSubmit}>`.
- Field component: `<Field name="email" type="email" />`.
- Custom Field: `<Field name="custom" as={CustomInput} />` or render prop pattern.
- ErrorMessage: `<ErrorMessage name="email" component="div" />`.
- useFormik hook: `const formik = useFormik({ initialValues, onSubmit })` then `formik.values`, `formik.handleSubmit`.

## Library Preferences

- **Yup:** Validation schema library. Works seamlessly with Formik.
- **Zod:** Alternative with @stifix/formik-zod adapter.
- **Formik DevTools:** Browser extension for debugging form state.

## File Naming

- Schema files: `[domain]-schema.ts`
- Form components: `[Feature]Form.tsx`

## NEVER DO THIS

1. **Never use `onChange` without Formik handlers.** Formik tracks state internally. Manual onChange breaks sync.
2. **Never validate manually when Yup exists.** `validationSchema` prop handles it automatically.
3. **Never forget `enableReinitialize` for dynamic initial values.** Without it, prop changes don't reset form.
4. **Never use `validateOnChange` without performance consideration.** Every keystroke validates. May be slow.
5. **Never ignore `isSubmitting`.** Disable submit button during submission to prevent double-submit.
6. **Never mix controlled and Formik-managed inputs.** Pick one approach.
7. **Never use Formik for new projects if considering alternatives.** React Hook Form has better performance. Consider migration.

## Testing

- Test Formik forms by triggering submit and checking validation.
- Use RTL to simulate user input and verify Formik state changes.
- Test async submission with `waitFor` for `isSubmitting` changes.

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- TanStack Form v8
- React/Vue/Svelte/Solid
- Headless form library
- Async validation
- Array fields support

## Project Structure
```
src/
├── components/
│   └── Form/
│       ├── TextField.tsx
│       └── Form.tsx
├── hooks/
│   └── useContactForm.ts
└── validation/
    └── schemas.ts
```

## Architecture Rules

- **Headless design.** No UI included—bring your own components.
- **Reactive core.** Form state updates trigger re-renders optimally.
- **Validation flexible.** Sync, async, field-level, form-level.
- **Nested and array fields.** Complex form structures supported.

## Coding Conventions

- Form: `const form = useForm({ defaultValues: { name: '' }, onSubmit: async (values) => { await api.submit(values) } })`.
- Field: `<form.Field name="name" validators={{ onChange: ({ value }) => !value ? 'Required' : undefined }}>{(field) => <input value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />}</form.Field>`.
- Submit: `<form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting]}>{([canSubmit, isSubmitting]) => <button type="submit" disabled={!canSubmit}>{isSubmitting ? '...' : 'Submit'}</button>}</form.Subscribe>`.

## NEVER DO THIS

1. **Never mix controlled with uncontrolled carelessly.** Use `field.state.value` + `handleChange`.
2. **Never skip the `form.Field` render function.** Required for field state.
3. **Never forget to handle async validation errors.** Catch in `validators`.
4. **Never use without understanding the `Subscribe` pattern.** For reading form state.
5. **Never ignore array field helpers.** `pushValue`, `removeValue`, `swapValues`.
6. **Never validate on submit only.** Use `onChange` or `onBlur` for UX.
7. **Never mix with form libraries carelessly.** Pick one—TanStack Form is self-contained.

## Testing

- Test validation rules fire correctly.
- Test async validation handles loading states.
- Test array field operations.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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


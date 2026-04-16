# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- React Hook Form v7 (performant form library)
- React 18+
- TypeScript 5.x
- Zod or Yup (validation)
- @hookform/resolvers

## Project Structure

```
src/
├── components/
│   ├── forms/                  // Form-specific components
│   │   ├── FormInput.tsx
│   │   └── FormSelect.tsx
│   └── features/
│       └── UserForm.tsx        // Feature forms
├── hooks/
│   └── useCustomForm.ts        // Custom form hooks
├── lib/
│   ├── validation.ts           // Zod schemas
│   └── form-utils.ts           // Form helpers
└── schemas/
    └── user-schema.ts          // Domain validation schemas
```

## Architecture Rules

- **Uncontrolled by default.** RHF uses uncontrolled components for performance. Only re-render on validation/submit.
- **Controller for controlled inputs.** Use `Controller` for external controlled components (MUI, Chakra, etc.).
- **Resolvers for validation.** Zod/Yup schemas via `@hookform/resolvers` for declarative validation.
- **FormProvider for deep nesting.** Share form methods to deeply nested components without prop drilling.

## Coding Conventions

- Initialize: `const { register, handleSubmit, formState: { errors } } = useForm<FormData>({ resolver: zodResolver(schema) })`.
- Register inputs: `<input {...register("name")} />`.
- Handle submit: `const onSubmit = (data) => console.log(data)` → `<form onSubmit={handleSubmit(onSubmit)}>`.
- Controller for custom: `<Controller name="field" control={control} render={({ field }) => <CustomInput {...field} />} />`.
- Watch values: `const name = watch("name")` or `const values = watch()`.

## Library Preferences

- **@hookform/resolvers:** Zod, Yup, Joi, Valibot integration.
- **@hookform/devtools:** Visual form debugging.
- **zod:** Preferred validation (TypeScript-first, smaller than Yup).
- **@hookform/error-message:** Simplified error display.

## File Naming

- Schema files: `[domain]-schema.ts` → `user-schema.ts`
- Form components: `[Feature]Form.tsx` → `LoginForm.tsx`
- Input wrappers: `Form[Component].tsx` → `FormInput.tsx`

## NEVER DO THIS

1. **Never use controlled inputs without Controller.** Direct `value` + `onChange` breaks RHF's uncontrolled optimization.
2. **Never forget to spread `register` properly.** `{...register("name")}` provides ref, name, onChange, onBlur.
3. **Never validate on every keystroke by default.** `mode: 'onSubmit'` is the default for performance. Change intentionally.
4. **Never use `watch` for all fields.** `watch()` causes re-render on every field change. Use `useWatch` for specific fields.
5. **Never ignore `formState` re-render behavior.** `formState` properties trigger re-renders. Destructure only what you need.
6. **Never skip default values for dynamic fields.** `useFieldArray` and conditional fields need `defaultValues`.
7. **Never mix `register` and `Controller` for the same field.** Pick one approach per field.

## Testing

- Test forms by triggering submit and checking validation errors.
- Use React Testing Library's `fireEvent` or `userEvent` for interactions.
- Test validation by submitting invalid data and checking error messages.
- Test controlled components with Controller by simulating changes.


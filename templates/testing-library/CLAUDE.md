# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Testing Library (user-centric testing)
- React Testing Library (DOM)
- Jest/Vitest runner
- User Event v14
- jest-dom matchers

## Project Structure
```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx         # Co-located test
├── hooks/
│   └── useAuth.test.ts
└── test/
    └── test-utils.tsx          # Custom render
```

## Architecture Rules

- **Test behavior, not implementation.** Test what users see and do.
- **Queries prioritize accessibility.** `getByRole`, `getByLabelText` over `getByTestId`.
- **User Event for interactions.** Simulates realistic user events.
- **Avoid testing implementation details.** Don't test state, props, or internal methods.

## Coding Conventions

- Render: `render(<Component />)` from `@testing-library/react`.
- Query: `screen.getByRole('button', { name: /submit/i })`.
- User event: `const user = userEvent.setup(); await user.click(button)`.
- Async: `await screen.findByText('Loaded')` for async elements.
- Assert: `expect(button).toBeDisabled()` with `jest-dom`.
- Custom render: Create wrapper with providers (theme, router, etc.).

## NEVER DO THIS

1. **Never use `getByTestId` as first choice.** It's a last resort—prefer semantic queries.
2. **Never test implementation details.** Don't assert on `state` or check if function was called (unless it's the behavior).
3. **Never use `fireEvent` instead of `userEvent`.** `userEvent` is more realistic.
4. **Never forget `act` warnings.** Usually handled automatically, but understand when needed.
5. **Never test third-party libraries.** Test your code, not library internals.
6. **Never skip `screen` object.** It's the recommended way to query.
7. **Never use `container` queries.** They break easily—use role/label queries.

## Testing

- Test with `screen.debug()` to see rendered output.
- Test accessibility with `jest-axe`.
- Test with Testing Library Playground for query selection.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Jest v29 (testing framework)
- TypeScript (ts-jest)
- Babel (optional)
- jsdom or node environment
- Coverage built-in

## Project Structure
```
src/
├── ...                         # Source files
__tests__/
├── utils.test.ts               # Tests
jest.config.ts                  # Jest configuration
setupTests.ts                   # Setup file
```

## Architecture Rules

- **Zero config for basic projects.** Works out of the box for simple setups.
- **ts-jest for TypeScript.** Transform TypeScript to JavaScript.
- **jsdom for DOM testing.** Simulate browser environment.
- **Snapshots for UI.** Capture component output for regression testing.

## Coding Conventions

- Config: `export default { preset: 'ts-jest', testEnvironment: 'jsdom', setupFilesAfterEnv: ['<rootDir>/setupTests.ts'] }`.
- Run: `jest` for watch mode, `jest --watchAll`, `jest --coverage`.
- Mock: `jest.mock('./module')` for module mocking.
- Spy: `jest.spyOn(object, 'method')`.
- Matchers: `expect(value).toBe()`, `.toEqual()`, `.toMatchSnapshot()`.
- Async: `it('test', async () => { await expect(promise).resolves.toBe('value') })`.

## NEVER DO THIS

1. **Never use without `transform` for TypeScript.** Add `ts-jest` or `babel-jest`.
2. **Never forget to mock large modules.** Jest can be slow with big node_modules.
3. **Never commit snapshots without review.** They capture output—verify correctness.
4. **Never ignore `testEnvironment`.** Node vs jsdom affects global APIs available.
5. **Never use `setTimeout` in tests without fake timers.** `jest.useFakeTimers()`.
6. **Never skip cleaning mocks.** `clearMocks: true` or manual cleanup.
7. **Never mix ESM and CJS without configuration.** Jest ESM support requires setup.

## Testing

- Test with `jest --coverage` for coverage reports.
- Test with `jest --detectOpenHandles` for async cleanup issues.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Playwright Component Testing
- Vite/Webpack
- React/Vue/Svelte/Solid
- Isolated component tests
- Visual regression

## Project Structure
```
playwright/
├── index.html                  // Test renderer
├── ct.config.ts                // Component test config
└── src/
    └── Button.spec.tsx         // Component tests
src/
└── components/
    └── Button.tsx
```

## Architecture Rules

- **Component isolation.** Test components in real browser.
- **Vite integration.** Fast dev server for tests.
- **Mount API.** Render components with props/events.
- **Expect assertions.** Playwright's powerful assertions.

## Coding Conventions

- Test: `test('button should work', async ({ mount }) => { const component = await mount(<Button title='Submit' />); await expect(component).toContainText('Submit'); await component.click(); })`.
- Configure: `test('renders with dark mode', async ({ mount }) => { const component = await mount(<Button />, { globals: { theme: 'dark' } }) })`.
- Hooks: `test.beforeEach(async ({ page }) => { await page.goto('/'); })`.

## NEVER DO THIS

1. **Never mix CT with E2E tests.** Different test types, different config.
2. **Never skip the `mount` fixture.** Required for component tests.
3. **Never forget to handle async mounting.** `await mount()`.
4. **Never test full pages in CT.** Use E2E for page flows.
5. **Never ignore the test renderer.** `playwright/index.html` setup.
6. **Never skip visual testing in CT.** `toHaveScreenshot()` works.
7. **Never use without component compilation.** Vite/Webpack required.

## Testing

- Test components render correctly.
- Test component interactions.
- Test visual regression per component.


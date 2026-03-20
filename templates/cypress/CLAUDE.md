# [PROJECT NAME] - Cypress Test Suite

## Tech Stack

- Cypress 13+ with TypeScript
- Component Testing for isolated UI components
- E2E Testing for full user flows
- Custom commands for reusable interactions
- Cypress Cloud / your CI provider for parallelization and recordings
- Your application framework as the system under test

## Project Structure

```
cypress/
├── e2e/                       # E2E test specs by feature
│   ├── auth/
│   │   ├── login.cy.ts
│   │   └── signup.cy.ts
│   └── orders/
│       └── checkout.cy.ts
├── component/                 # Component test specs
│   └── Button.cy.tsx
├── support/
│   ├── commands.ts            # Custom commands (cy.login, cy.seedDB)
│   ├── component.ts           # Component test setup (mount config)
│   ├── e2e.ts                 # E2E test setup (intercepts, hooks)
│   └── index.d.ts             # Type declarations for custom commands
├── fixtures/                  # Static mock data JSON files
│   ├── users.json
│   └── products.json
├── plugins/                   # Node-side plugins (DB access, file ops)
├── cypress.config.ts          # Main configuration
└── tsconfig.json              # Cypress-specific TS config
```

## Architecture Rules

- **Custom commands for repeated flows.** `cy.login(email, password)` wraps the login API call (not UI interaction). `cy.seedDB(fixture)` resets test state via API. Commands live in `support/commands.ts` and are typed in `support/index.d.ts`.
- **API-based setup, UI-based assertions.** Use `cy.request()` or custom commands to set up test state (create users, seed orders). Then use the UI to verify the state is displayed correctly. Never drive a 5-step UI flow just to set up preconditions.
- **Intercept, don't mock globally.** Use `cy.intercept()` per test to stub or spy on specific API routes. Never install a global mock that silently affects all tests. Explicit intercepts make test dependencies visible.
- **Component tests are unit tests for UI.** Mount a single component with `cy.mount()`, pass props, and assert rendering. These run in a real browser but without a full app -- use them for visual logic, conditional rendering, and event handling.

## Coding Conventions

- All custom commands must have TypeScript declarations in `support/index.d.ts`. If `cy.login()` exists without a type declaration, it will compile but give no autocomplete -- treat it as a bug.
- Use `data-cy` attributes as the primary selector strategy. Not `data-testid` (Playwright convention) and not CSS classes. Cypress docs recommend `data-cy`.
- Chain assertions directly: `cy.get('[data-cy=submit]').should('be.visible').click()`. Do not assign Cypress commands to variables -- `const btn = cy.get(...)` does not work the way you think. Cypress commands are not promises.
- Use `beforeEach` for per-test setup. Use `before` only for truly expensive one-time setup (and document why). Prefer custom commands over `beforeEach` blocks that duplicate across files.
- Alias intercepts: `cy.intercept('GET', '/api/users').as('getUsers')` then `cy.wait('@getUsers')`. Named waits are readable and debuggable.

## Library Preferences

- **Assertions:** Chai (bundled). `should('have.length', 3)`, `should('contain.text', 'Success')`. Not Jest matchers -- they don't exist in Cypress.
- **Component mounting:** `@cypress/react` or `@cypress/vue` depending on framework. Not Storybook-based testing -- Cypress component tests run in a real browser with full DOM.
- **Fixtures:** Static JSON in `cypress/fixtures/`. Load with `cy.fixture('users')`. Not faker.js in E2E tests -- deterministic data avoids flaky assertion text.
- **File uploads:** `cypress-file-upload` plugin. Not manual blob injection.
- **Visual testing:** `cypress-image-snapshot` for local. Cypress Cloud for cross-run comparison.

## File Naming

- E2E specs: `kebab-case.cy.ts` -> `user-login.cy.ts`, `product-search.cy.ts`
- Component specs: `PascalCase.cy.tsx` -> `Button.cy.tsx`, `Modal.cy.tsx`
- Custom commands: all in `support/commands.ts` (single file, grouped by domain with comments)
- Fixtures: `kebab-case.json` -> `active-users.json`, `empty-cart.json`
- Plugins: `kebab-case.ts` -> `db-seed.ts`, `mail-client.ts`

## NEVER DO THIS

1. **Never use `cy.wait(3000)`.** Arbitrary waits are the number one cause of flaky Cypress tests. Wait on aliased intercepts (`cy.wait('@getUsers')`) or assert visibility (`should('be.visible')`). Cypress has built-in retry-ability.
2. **Never treat Cypress commands as promises.** `cy.get()` does not return a DOM element. It enqueues a command. You cannot `const el = cy.get(...)` and then `el.click()` in the next line. Chain everything: `cy.get(...).click()`.
3. **Never use `async/await` in Cypress test bodies.** Cypress commands are not promises. Adding `async` to an `it()` block breaks the command queue. If you need async work, put it in a `cy.task()` or `cy.then()`.
4. **Never test third-party UI (OAuth popups, Stripe Checkout).** Stub the third-party at the API boundary with `cy.intercept()`. Testing someone else's UI is slow, fragile, and violates their ToS.
5. **Never access elements across frames without `cy.iframe()`.** If embedding iframes (Stripe Elements, reCAPTCHA), use `cypress-iframe` plugin. Direct `cy.get()` cannot see into iframes.
6. **Never write tests that depend on execution order.** Cypress may run specs in any order. Each test must set up and tear down its own state. If test B relies on test A having created a record, both tests are broken.
7. **Never omit `baseUrl` in config.** Set `baseUrl` in `cypress.config.ts`. Without it, every `cy.visit()` needs a full URL, and environment switching becomes a manual find-and-replace nightmare.

## Testing

- Run E2E headed: `npx cypress open`. Run headless: `npx cypress run`.
- Run component tests: `npx cypress open --component` or `npx cypress run --component`.
- Run single spec: `npx cypress run --spec cypress/e2e/auth/login.cy.ts`.
- CI parallelization: use `--record --parallel` with Cypress Cloud, or split specs across CI jobs manually with `--spec` glob patterns.
- Write the `data-cy` attribute in the application source first. Then write the test. If you find yourself using fragile selectors, the problem is in the app, not the test.
- Test the happy path and one critical error path per flow. Full edge-case coverage belongs in unit tests, not E2E.

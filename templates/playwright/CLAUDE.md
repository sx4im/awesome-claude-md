# [PROJECT NAME] - Playwright E2E Test Suite

## Tech Stack

- Playwright 1.x with TypeScript (strict mode)
- Node.js 20+ runtime
- Page Object Model for test structure
- Custom fixtures for authentication and data seeding
- GitHub Actions / {ci-provider} for pipeline execution
- {application-framework} as the system under test

## Project Structure

```
tests/
├── e2e/                      # Test specs organized by feature
│   ├── auth/                 # Login, signup, password reset flows
│   ├── dashboard/            # Post-login feature tests
│   └── checkout/             # Purchase and payment flows
├── pages/                    # Page Object Models
│   ├── BasePage.ts           # Shared navigation, wait helpers
│   ├── LoginPage.ts          # Login form interactions
│   └── DashboardPage.ts     # Dashboard element selectors and actions
├── fixtures/                 # Custom test fixtures and extensions
│   ├── auth.fixture.ts       # Authenticated browser context
│   ├── db.fixture.ts         # Database seeding/teardown
│   └── index.ts              # Merged fixture export
├── helpers/                  # Utility functions (API calls, data generators)
├── playwright.config.ts      # Main config: baseURL, projects, retries
└── global-setup.ts           # One-time setup: auth state storage
```

## Architecture Rules

- **Page Object Model is mandatory.** Every page or major component gets a class in `pages/`. Tests never use `page.locator()` directly. They call methods like `loginPage.submitCredentials(user, pass)`. This isolates selector changes to one file.
- **Fixtures over beforeEach.** Use Playwright's custom fixtures for shared setup (authenticated state, seeded data, feature flags). Fixtures compose cleanly; `beforeEach` blocks create hidden dependencies between tests.
- **One assertion theme per test.** A test named `should display order summary after checkout` tests exactly that flow. Do not bolt on additional assertions about unrelated sidebar content. Separate concerns into separate tests.
- **Auth state is stored, not replayed.** Use `global-setup.ts` to log in once and save `storageState` to a JSON file. Tests reuse that state via fixture. Never replay the login UI flow in every test -- it wastes 3-5 seconds per test and is flaky.

## Coding Conventions

- Test files: `[feature].spec.ts`. One spec file per user-facing flow, not per page.
- Page Objects: constructor takes `Page`, all methods are `async`, return `this` for chainable actions or return extracted data.
- Use `test.describe` for grouping related scenarios. Never nest describes more than one level deep.
- Use `data-testid` attributes as the primary selector strategy. Fall back to `getByRole` and `getByText` for accessibility-aligned selectors. Never use CSS classes or XPath.
- Timeouts: set `expect.timeout` in config (default 5s). Never use `page.waitForTimeout(ms)` -- it's a sleep and hides real timing issues.

## Library Preferences

- **Assertions:** Playwright's built-in `expect` with web-first auto-retrying matchers (`toBeVisible`, `toHaveText`). Not chai or jest `expect` -- they don't auto-retry.
- **API testing:** Playwright's `request` context for API setup/teardown. Not axios or node-fetch in test helpers.
- **Visual regression:** `expect(page).toHaveScreenshot()` with threshold. Not Percy or Chromatic unless explicitly required.
- **Reporting:** HTML reporter for local, JUnit for CI. Not Allure unless the team already uses it.
- **Test data:** faker.js for generating realistic dummy data. Not hardcoded strings that collide across parallel workers.

## File Naming

- Specs: `kebab-case.spec.ts` -> `user-checkout.spec.ts`, `admin-settings.spec.ts`
- Pages: `PascalCase.ts` -> `LoginPage.ts`, `ProductListPage.ts`
- Fixtures: `kebab-case.fixture.ts` -> `auth.fixture.ts`, `db.fixture.ts`
- Helpers: `kebab-case.ts` -> `api-client.ts`, `seed-data.ts`

## NEVER DO THIS

1. **Never use `page.waitForTimeout()`.** It's a hardcoded sleep. Use `expect(locator).toBeVisible()` or `page.waitForSelector()` which auto-retry. Every `waitForTimeout` is a future flaky test.
2. **Never share mutable state between tests.** Tests run in parallel by default. If test A creates a user and test B reads the user list, they will collide. Each test seeds its own data via fixture and cleans up after.
3. **Never use `page.locator('.btn-primary')` in specs.** CSS classes are styling concerns and change without warning. Use `data-testid` or `getByRole`. Page Objects isolate selector fragility.
4. **Never skip retries in CI config.** Set `retries: 2` in CI projects. Playwright tests interact with real browsers and real (or staged) backends. Transient failures happen. Retries with trace-on-first-retry catch real bugs while filtering noise.
5. **Never run all tests in a single browser project.** Configure `projects` in `playwright.config.ts` for at least Chromium and Firefox. Cross-browser bugs are real and cheap to catch here.
6. **Never put test logic in `global-setup.ts`.** Global setup is for one-time auth state generation and environment validation only. Actual test flows belong in fixtures and specs.
7. **Never assert on auto-generated IDs or timestamps.** These change every run. Assert on user-visible text, element visibility, or count of items.

## Testing

- Run all tests: `npx playwright test`. Run single spec: `npx playwright test tests/e2e/auth/login.spec.ts`.
- Debug mode: `npx playwright test --debug` opens the inspector with step-through. Use `--headed` to watch execution.
- Trace viewer: enable `trace: 'on-first-retry'` in config. After failure, open trace with `npx playwright show-trace trace.zip` to see screenshots, network, and DOM snapshots at each step.
- CI parallelism: Playwright shards with `--shard=1/4`. Split across CI workers for faster pipelines. Each shard gets an independent test subset.
- Before writing a new test, run the existing suite to confirm the baseline passes. Never add tests on top of a broken suite.

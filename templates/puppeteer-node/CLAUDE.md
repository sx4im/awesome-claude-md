# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Node.js 20 LTS with TypeScript 5.4+
- Puppeteer 22+ for browser automation (Chromium bundled)
- Jest 29 as the test runner with jest-puppeteer preset
- pixelmatch for visual regression screenshot comparison
- pino for structured logging during automation runs
- dotenv for environment configuration
- tsx for running TypeScript scripts directly

## Project Structure

```
src/
  pages/                # Page Object Model classes
    BasePage.ts         # Abstract base with common navigation, waitFor helpers
    LoginPage.ts        # Login form interactions
    DashboardPage.ts   # Dashboard-specific selectors and actions
  flows/                # Multi-page user journey orchestrations
    checkout.flow.ts
    onboarding.flow.ts
  utils/
    browser.ts          # Browser launch config, context factory
    selectors.ts        # Centralized selector constants
    screenshots.ts      # Screenshot capture and diff utilities
    retry.ts            # Retry logic for flaky network conditions
  fixtures/
    test-data.json      # Static test input data
    cookies.json        # Pre-authenticated session cookies
tests/
  e2e/                  # End-to-end journey tests
  visual/               # Screenshot comparison tests
  smoke/                # Quick health checks
scripts/
  generate-report.ts    # HTML report from test results
config/
  puppeteer.config.ts   # Launch options per environment
```

## Architecture Rules

- Strict Page Object Model: every page interaction goes through a Page class, never raw selectors in tests
- Page classes extend BasePage which provides `goto()`, `waitForReady()`, `screenshot()`, `getTextContent()`
- All selectors use `data-testid` attributes as primary strategy, fall back to ARIA roles, never use CSS class names
- Browser instances are created per test suite, pages per test; use `browser.createBrowserContext()` for isolation
- Every navigation action must wait for `networkidle0` or a specific selector before proceeding
- Use `page.waitForSelector()` with explicit timeouts rather than arbitrary `page.waitForTimeout()` delays
- Intercept network requests with `page.setRequestInterception(true)` to mock API responses in tests

## Coding Conventions

- All Page Object methods return `Promise<this>` for fluent chaining: `await loginPage.enterEmail(e).enterPassword(p).submit()`
- Selector constants are typed string literals, grouped by page in `selectors.ts`
- Use `page.evaluate()` for DOM manipulation; keep evaluated functions pure and serializable
- Error screenshots are auto-captured in Jest `afterEach` hooks on test failure
- Timeouts: 30s for navigation, 10s for element visibility, 5s for animations
- Use `AbortController` for cancellable long-running automation scripts
- Log every navigation and click action at debug level with pino

## Library Preferences

- puppeteer over playwright (project standardized on Puppeteer API)
- jest-puppeteer preset over custom Jest setup for browser lifecycle
- pixelmatch over Percy/Applitools for self-hosted visual regression
- sharp for image resizing before screenshot comparison
- p-queue for controlled concurrency when running multiple browser instances
- cheerio for parsing HTML snapshots when full browser context is unnecessary

## File Naming

- Page objects: PascalCase matching the page name, e.g., `CheckoutPage.ts`
- Flow files: kebab-case with `.flow.ts` suffix
- Test files: kebab-case with `.test.ts` suffix matching the flow or page
- Utility modules: camelCase `.ts` files
- Screenshots: `<test-name>-<viewport>-<timestamp>.png`

## NEVER DO THIS

1. Never use `page.waitForTimeout()` with hardcoded delays; always wait for a specific condition or selector
2. Never access `page.$()` or selectors directly in test files; always go through Page Object methods
3. Never use XPath selectors; use `data-testid` attributes or ARIA queries via `page.locator()`
4. Never leave browser instances open after tests; always close in `afterAll` or use jest-puppeteer lifecycle
5. Never store screenshots in git; write to a gitignored `screenshots/` directory, archive in CI artifacts
6. Never run headed mode in CI; always use `headless: 'shell'` (the new headless mode) in CI config
7. Never disable `--no-sandbox` without understanding security implications; use it only in containerized CI

## Testing

- Smoke tests run on every PR, full E2E suite runs nightly and before releases
- Visual regression tests compare against baseline screenshots stored in cloud storage (S3/GCS)
- Set viewport to `1280x720` for desktop tests, `375x812` for mobile tests; test both
- Use `page.emulateMediaFeatures` to test dark mode and `prefers-reduced-motion`
- Mock external API calls with `page.setRequestInterception` to avoid flaky third-party dependencies
- Generate HTML reports with screenshots embedded for failed tests
- Run tests in Docker with `--cap-add=SYS_ADMIN` for Chromium sandbox support
- Flaky test threshold: if a test fails more than twice in 10 runs, fix it or quarantine it

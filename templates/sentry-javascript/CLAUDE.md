# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Sentry JavaScript SDK
- Error tracking
- Performance monitoring
- Session replay
- Release health

## Project Structure
```
src/
├── lib/
│   └── sentry.ts               // Sentry initialization
├── components/
└── main.tsx
```

## Architecture Rules

- **Error capture.** Automatic and manual error reporting.
- **Performance spans.** Track operations and requests.
- **Breadcrumbs.** Context leading to errors.
- **Source maps.** Map minified code to original.

## Coding Conventions

- Init: `Sentry.init({ dsn: process.env.SENTRY_DSN, integrations: [Sentry.browserTracingIntegration(), Sentry.replayIntegration()], tracesSampleRate: 1.0, replaysSessionSampleRate: 0.1 })`.
- Capture: `Sentry.captureException(error)` or `Sentry.captureMessage('Something happened')`.
- Scope: `Sentry.setTag('section', 'articles'); Sentry.setUser({ id: '4711', email: 'test@example.com' })`.
- Span: `const transaction = Sentry.startTransaction({ name: 'checkout', op: 'payment' })`.

## NEVER DO THIS

1. **Never commit DSN publicly.** Use environment variables.
2. **Never capture PII without scrubbing.** Use `beforeSend` to filter.
3. **Never enable 100% sampling in production.** High volume = high cost.
4. **Never ignore source map uploads.** Unreadable stack traces without.
5. **Never forget to set environment.** `environment: 'production'`.
6. **Never swallow errors after capturing.** Still handle appropriately.
7. **Never ignore rate limiting.** Sentry drops events if over limit.

## Testing

- Test errors appear in Sentry dashboard.
- Test source maps resolve correctly.
- Test performance spans are useful.


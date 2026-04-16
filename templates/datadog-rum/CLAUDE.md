# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Datadog RUM (Real User Monitoring)
- Browser SDK
- Performance tracking
- Session replays
- Analytics

## Project Structure
```
src/
├── lib/
│   └── datadog.ts              // Datadog initialization
├── components/
└── main.tsx
```

## Architecture Rules

- **Real user monitoring.** Actual user sessions, not synthetic.
- **Automatic instrumentation.** RUM SDK captures navigation, resources, errors.
- **Custom actions.** Track user interactions.
- **Session replay.** Record and replay user sessions.

## Coding Conventions

- Init: `datadogRum.init({ applicationId: 'xxx', clientToken: 'yyy', site: 'datadoghq.com', service: 'my-app', env: 'production', version: '1.0.0', sessionSampleRate: 100, sessionReplaySampleRate: 20 })`.
- Custom action: `datadogRum.addAction('checkout', { cartSize: 4, total: 100 })`.
- Error: `datadogRum.addError(error, { context: 'payment' })`.
- User: `datadogRum.setUser({ id: '123', email: 'user@example.com' })`.

## NEVER DO THIS

1. **Never commit client tokens publicly.** Use env vars.
2. **Never capture sensitive data.** Filter PII in `beforeSend`.
3. **Never use 100% replay sampling in production.** High cost.
4. **Never ignore network request whitelisting.** May capture sensitive headers.
5. **Never forget to mask sensitive elements.** Use privacy overrides for PII fields.
6. **Never skip environment tagging.** Critical for filtering.
7. **Never ignore GDPR compliance.** Consent required in some jurisdictions.

## Testing

- Test sessions appear in Datadog.
- Test custom actions are tracked.
- Test replays show correct information.
- Test performance metrics.


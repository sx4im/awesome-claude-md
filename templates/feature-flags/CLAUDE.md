# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Feature Flags (LaunchDarkly, Unleash, or custom)
- TypeScript/React/Node
- Gradual rollout support
- A/B testing capabilities
- Real-time updates

## Project Structure
```
src/
├── features/
│   ├── flags.ts                # Flag definitions
│   └── components/
│       └── feature-gate.tsx
├── flags/
│   ├── provider.ts             // Flag provider setup
│   └── hooks.ts                // useFeatureFlag hook
└── config/
    └── flags.json              // Default flag values
```

## Architecture Rules

- **Flags control visibility.** Features shown/hidden based on flag state.
- **Default values for safety.** Always have safe defaults if provider fails.
- **User targeting.** Enable flags for specific users, percentages, or segments.
- **Real-time updates.** Flags can change without deployment.

## Coding Conventions

- Check flag: `const isEnabled = useFeatureFlag('new-checkout')`.
- Gate component: `<FeatureGate flag="new-checkout"><NewCheckout /></FeatureGate>`.
- User context: `flags.setUser({ key: user.id, email: user.email, custom: { plan: user.plan } })`.
- Server check: `const isEnabled = await flags.isEnabled('new-api', userId)`.

## NEVER DO THIS

1. **Never forget default values.** If flag provider fails, app should still work.
2. **Never use flags for security.** Don't hide admin features with flags—use proper auth.
3. **Never ignore flag cleanup.** Remove flags and old code paths when features are permanent.
4. **Never test with flags disabled.** Test both on and off states.
5. **Never create flag explosion.** Too many flags create complexity—be selective.
6. **Never forget about flag evaluation latency.** Server-side flags may need caching.
7. **Never use flags for long-term configuration.** They're for temporary control.

## Testing

- Test feature with flag on and off.
- Test flag provider failure handling.
- Test user targeting rules.


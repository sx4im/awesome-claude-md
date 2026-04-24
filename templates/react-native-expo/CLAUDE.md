# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Mobile)

### Release Discipline
- Protect offline/poor-network behavior and state recovery paths.
- Avoid platform-specific regressions by validating iOS/Android parity.
- Respect battery/performance constraints in background tasks.

### Merge/Release Gates
- Build and runtime smoke tests pass on target platforms.
- Crash-prone paths (auth, navigation, persistence) validated.
- No release with unresolved permission/security handling gaps.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- React Native 0.73+ with Expo SDK 50+
- TypeScript (strict mode)
- Expo Router for file-based navigation
- TanStack Query for server state
- Zustand for client state
- Expo SecureStore for sensitive data

## Project Structure

```
app/                         # Expo Router file-based routing
├── (tabs)/                  # Tab navigator group
│   ├── index.tsx            # Home tab
│   ├── profile.tsx          # Profile tab
│   └── _layout.tsx          # Tab layout config
├── (auth)/                  # Auth flow group
│   ├── login.tsx
│   └── register.tsx
├── _layout.tsx              # Root layout (providers, fonts, splash)
└── [id].tsx                 # Dynamic routes
src/
├── components/
│   ├── ui/                  # Primitives: Button, Input, Card, Avatar
│   └── features/            # Domain: ProductCard, OrderItem
├── hooks/                   # Custom hooks
├── services/                # API client functions
├── stores/                  # Zustand stores
├── utils/                   # Pure helpers (formatCurrency, dateUtils)
├── constants/               # Colors, spacing, API URLs, config
└── types/                   # Shared TypeScript types
```

## Architecture Rules

- **Expo Router handles all navigation.** Routes are files in `app/`. Use `(groups)` for layout grouping, `[param]` for dynamic segments. Never use React Navigation's imperative `navigation.navigate()`. use `router.push()` from `expo-router` or `<Link>`.
- **All API calls go through `services/`.** Components never call `fetch` directly. Service functions return typed data, handle auth token injection, and normalize errors.
- **State management split:** server state → TanStack Query. Client-only state (theme, onboarding flags) → Zustand. Form state → local `useState`. Never store API response data in Zustand.
- **Platform-specific code uses file extensions.** `Component.ios.tsx` and `Component.android.tsx` for platform splits. For small differences, use `Platform.select()` inline. Never use `Platform.OS === 'ios'` in a chain of `if/else`. use `Platform.select()`.
- **Sensitive data goes in SecureStore.** Auth tokens, API keys saved locally, and user credentials use `expo-secure-store`. Never use AsyncStorage for secrets. it's unencrypted.

## Coding Conventions

- Components use `function` keyword: `export function ProductCard()`. Arrow functions for inline callbacks only.
- Props use an explicit interface above the component: `interface ProductCardProps { .. }`. Never use inline `{ prop1, prop2 }: { prop1: string; prop2: number }`.
- Styles use `StyleSheet.create()` at the bottom of the file. Never put style objects inline in JSX. it creates new objects on every render.
- Color values come from `constants/colors.ts`. Never hardcode hex values in components. Support light/dark themes via `useColorScheme()`.
- Spacing uses a 4px base scale from `constants/spacing.ts`: `spacing.xs` (4), `spacing.sm` (8), `spacing.md` (16), `spacing.lg` (24), `spacing.xl` (32).

## Library Preferences

- **Navigation:** Expo Router. not React Navigation directly (Expo Router wraps it with file-based routing, deep linking, and URL support out of the box).
- **HTTP:** `ky` or typed `fetch` wrapper. not `axios` (ky is smaller, fetch-native). Configure base URL and auth headers in one `services/api.ts` client.
- **Local storage:** `expo-secure-store` for sensitive data. `@react-native-async-storage/async-storage` for non-sensitive preferences.
- **Animations:** `react-native-reanimated`. not `Animated` from React Native (reanimated runs on the UI thread, no JS bridge bottleneck).
- **Icons:** `@expo/vector-icons`. bundled with Expo, no extra install step.

## File Naming

- Screens (in `app/`): `kebab-case.tsx` → `order-details.tsx`, `edit-profile.tsx`
- Components: `PascalCase.tsx` → `ProductCard.tsx`, `AvatarCircle.tsx`
- Hooks: `useCamelCase.ts` → `useAuth.ts`, `useRefreshOnFocus.ts`
- Services: `camelCase.ts` → `products.ts`, `auth.ts`
- Stores: `camelCase.store.ts` → `auth.store.ts`, `cart.store.ts`
- Constants: `camelCase.ts` → `colors.ts`, `spacing.ts`, `config.ts`

## NEVER DO THIS

1. **Never use `navigation.navigate()` from React Navigation directly.** Use Expo Router's `router.push('/path')` or `<Link href="/path">`. Mixing navigation APIs creates broken back stacks.
2. **Never store auth tokens in AsyncStorage.** It's unencrypted plain text. Use `expo-secure-store`. it uses Keychain on iOS and EncryptedSharedPreferences on Android.
3. **Never put inline styles in JSX.** `<View style={{ marginTop: 16 }}>` creates a new object every render. Use `StyleSheet.create()` and reference named styles.
4. **Never hardcode colors or spacing values.** All visual tokens come from `constants/`. Hardcoded `#FF0000` or `marginTop: 16` breaks theming and consistency.
5. **Never use `console.log` in production code.** Use a logger that can be disabled in production builds. `console.log` in React Native hits the JS bridge and causes performance issues in release builds.
6. **Never block the JS thread with synchronous operations.** File reads, JSON parsing of large payloads, and crypto operations should use async APIs or move to a native module.
7. **Never use `expo eject` unless you absolutely must.** Stay in the managed workflow. If you need a custom native module, use `expo-dev-client` with a development build instead.

## Testing

- Use Jest + React Native Testing Library. Test user-visible behavior: press buttons, check text, verify navigation.
- Mock API calls at the service layer with `jest.mock('./services/products')`.
- Test hooks independently with `renderHook` from `@testing-library/react-hooks`.
- E2E tests with Detox or Maestro for critical flows (sign up, purchase, onboarding).
- Test on both iOS Simulator and Android Emulator in CI. platform-specific bugs are real.

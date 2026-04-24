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

- Framework: Expo SDK 52+ with Expo Router v4 for file-based routing
- Language: TypeScript 5.4+ in strict mode
- UI: React Native core components + Expo SDK modules
- Styling: NativeWind 4 (Tailwind CSS for React Native) with `className` prop
- State: Zustand 5 with persist middleware using expo-secure-store
- Data Fetching: TanStack Query 5 (React Query) with typed API hooks
- Navigation: Expo Router with file-based routing and typed routes
- Auth: Expo AuthSession + expo-secure-store for token storage
- Build: EAS Build and EAS Submit for CI/CD

## Project Structure

```
app/
  _layout.tsx              # Root layout with Stack navigator, providers, fonts
  (tabs)/
    _layout.tsx            # Tab layout with Tabs component, tab bar icons
    index.tsx              # Home tab screen
    explore.tsx            # Explore tab screen
    profile.tsx            # Profile tab screen
  (auth)/
    _layout.tsx            # Auth group layout (no tab bar)
    sign-in.tsx            # Sign in screen
    sign-up.tsx            # Sign up screen
  [id].tsx                 # Dynamic route for detail screens
  +not-found.tsx           # 404 fallback screen
  +html.tsx                # Custom HTML wrapper for web export
src/
  components/
    ui/                    # Primitive UI components (Button, Card, Input, Badge)
    features/              # Feature-specific composed components
  hooks/
    useAuth.ts             # Authentication state and actions
    useColorScheme.ts      # Dark/light mode detection and toggle
  stores/
    auth.store.ts          # Zustand store for auth state with secure persistence
    app.store.ts           # Zustand store for app-wide preferences
  services/
    api.ts                 # Fetch wrapper with base URL, auth headers, error handling
    queries/
      useItems.ts          # TanStack Query hooks (useQuery, useMutation) per resource
      useUser.ts
  types/
    models.ts              # Domain entity interfaces
    navigation.ts          # Route parameter type declarations
  constants/
    tokens.ts              # Design tokens (spacing, colors, typography scales)
  utils/
    format.ts              # Date, currency, number formatting utilities
assets/
  fonts/                   # Custom font files loaded via expo-font
  images/                  # Static images and icons
```

## Architecture Rules

- File-based routing is the source of truth for navigation; every file in `app/` becomes a route
- Route groups `(groupName)` organize layouts without affecting URL paths
- All data fetching goes through TanStack Query hooks in `src/services/queries/`; never fetch in components
- Zustand stores manage client-side state; server state belongs in TanStack Query cache
- Business logic lives in hooks and services, not in screen components
- Screen files in `app/` are thin: they compose components and connect to hooks/stores

## Coding Conventions

- Use `<Stack.Screen options={{ title: "..." }}>` for per-screen header configuration
- Type route params with `useLocalSearchParams<{ id: string }>()` for type-safe access
- NativeWind classes go on the `className` prop: `<View className="flex-1 bg-white p-4">`
- Use `expo-image` (Image component) instead of React Native's Image for better caching and format support
- Prefer `expo-haptics` for tactile feedback on button presses and important actions
- Use `expo-constants` for app version, build number, and environment config
- Define TanStack Query keys as constants: `const itemKeys = { all: ['items'], detail: (id: string) => ['items', id] }`

## Library Preferences

- Image loading: expo-image (supports AVIF, WebP, animated GIF, blurhash placeholders)
- Icons: @expo/vector-icons (includes Ionicons, MaterialIcons, FontAwesome)
- Animations: react-native-reanimated 3 with layout animations for list transitions
- Gestures: react-native-gesture-handler for swipe, pan, and long-press interactions
- Forms: React Hook Form with Zod schema resolver
- Secure storage: expo-secure-store for tokens and sensitive data
- Date/time: date-fns for formatting and manipulation
- Toast/alerts: Burnt (native toast notifications) or expo-notifications for local alerts

## File Naming

- Route screens: lowercase with hyphens matching URL segments (`sign-in.tsx`, `[id].tsx`)
- Layouts: `_layout.tsx` in each route directory
- Components: PascalCase (`ItemCard.tsx`, `AuthForm.tsx`)
- Hooks: `useFeature.ts` (e.g., `useAuth.ts`)
- Stores: `feature.store.ts` (e.g., `auth.store.ts`)
- Query hooks: `useResource.ts` in `services/queries/`

## NEVER DO THIS

1. Never use React Navigation directly; Expo Router wraps it and manages the navigation tree via the file system
2. Never store auth tokens in AsyncStorage; use expo-secure-store which uses Keychain on iOS and EncryptedSharedPreferences on Android
3. Never use inline styles for layout; use NativeWind className for consistency and theme support
4. Never create API calls inside components; always use TanStack Query hooks from the services layer
5. Never eject from Expo managed workflow; use config plugins and EAS Build for native customization
6. Never use `react-native-gesture-handler` without wrapping the app in `<GestureHandlerRootView>`
7. Never import from `react-native` when an Expo SDK module provides the same capability (Camera, FileSystem, etc.)

## Testing

- Unit tests with Jest and React Native Testing Library (`@testing-library/react-native`)
- Test screen components by mocking Expo Router hooks (`useRouter`, `useLocalSearchParams`)
- TanStack Query tests wrap components in `<QueryClientProvider>` with a fresh `QueryClient` per test
- Zustand store tests call actions directly and assert state without React rendering
- Mock Expo modules with `jest.mock('expo-image')` providing minimal component stubs
- Run tests with `npx expo run:test` or `npx jest --watchAll` during development
- E2E tests with Maestro for native flow automation; YAML test files in `e2e/` directory
- EAS Build includes test step: configure `eas.json` build profile with `"test"` channel

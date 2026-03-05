# [PROJECT NAME] — [ONE LINE DESCRIPTION]

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

- **Expo Router handles all navigation.** Routes are files in `app/`. Use `(groups)` for layout grouping, `[param]` for dynamic segments. Never use React Navigation's imperative `navigation.navigate()` — use `router.push()` from `expo-router` or `<Link>`.
- **All API calls go through `services/`.** Components never call `fetch` directly. Service functions return typed data, handle auth token injection, and normalize errors.
- **State management split:** server state → TanStack Query. Client-only state (theme, onboarding flags) → Zustand. Form state → local `useState`. Never store API response data in Zustand.
- **Platform-specific code uses file extensions.** `Component.ios.tsx` and `Component.android.tsx` for platform splits. For small differences, use `Platform.select()` inline. Never use `Platform.OS === 'ios'` in a chain of `if/else` — use `Platform.select()`.
- **Sensitive data goes in SecureStore.** Auth tokens, API keys saved locally, and user credentials use `expo-secure-store`. Never use AsyncStorage for secrets — it's unencrypted.

## Coding Conventions

- Components use `function` keyword: `export function ProductCard()`. Arrow functions for inline callbacks only.
- Props use an explicit interface above the component: `interface ProductCardProps { ... }`. Never use inline `{ prop1, prop2 }: { prop1: string; prop2: number }`.
- Styles use `StyleSheet.create()` at the bottom of the file. Never put style objects inline in JSX — it creates new objects on every render.
- Color values come from `constants/colors.ts`. Never hardcode hex values in components. Support light/dark themes via `useColorScheme()`.
- Spacing uses a 4px base scale from `constants/spacing.ts`: `spacing.xs` (4), `spacing.sm` (8), `spacing.md` (16), `spacing.lg` (24), `spacing.xl` (32).

## Library Preferences

- **Navigation:** Expo Router — not React Navigation directly (Expo Router wraps it with file-based routing, deep linking, and URL support out of the box).
- **HTTP:** `ky` or typed `fetch` wrapper — not `axios` (ky is smaller, fetch-native). Configure base URL and auth headers in one `services/api.ts` client.
- **Local storage:** `expo-secure-store` for sensitive data. `@react-native-async-storage/async-storage` for non-sensitive preferences.
- **Animations:** `react-native-reanimated` — not `Animated` from React Native (reanimated runs on the UI thread, no JS bridge bottleneck).
- **Icons:** `@expo/vector-icons` — bundled with Expo, no extra install step.

## File Naming

- Screens (in `app/`): `kebab-case.tsx` → `order-details.tsx`, `edit-profile.tsx`
- Components: `PascalCase.tsx` → `ProductCard.tsx`, `AvatarCircle.tsx`
- Hooks: `useCamelCase.ts` → `useAuth.ts`, `useRefreshOnFocus.ts`
- Services: `camelCase.ts` → `products.ts`, `auth.ts`
- Stores: `camelCase.store.ts` → `auth.store.ts`, `cart.store.ts`
- Constants: `camelCase.ts` → `colors.ts`, `spacing.ts`, `config.ts`

## NEVER DO THIS

1. **Never use `navigation.navigate()` from React Navigation directly.** Use Expo Router's `router.push('/path')` or `<Link href="/path">`. Mixing navigation APIs creates broken back stacks.
2. **Never store auth tokens in AsyncStorage.** It's unencrypted plain text. Use `expo-secure-store` — it uses Keychain on iOS and EncryptedSharedPreferences on Android.
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
- Test on both iOS Simulator and Android Emulator in CI — platform-specific bugs are real.

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Framework: Vue 3.5+ with Composition API and `<script setup>` syntax
- Mobile Runtime: Capacitor 6 with native iOS and Android shells
- UI Components: Ionic 8 for Vue (ion-page, ion-content, ion-list, etc.)
- State: Pinia 2 with persistence via Capacitor Preferences plugin
- Routing: Vue Router 4 with Ionic's `IonRouterOutlet` for native transitions
- Language: TypeScript 5.4+ in strict mode
- Build: Vite 6 with `@vitejs/plugin-vue`
- Testing: Vitest + Vue Test Utils + Cypress for E2E
- Styling: Ionic CSS utilities + scoped CSS with CSS custom properties

## Project Structure

```
src/
  App.vue                    # IonApp root, IonRouterOutlet
  main.ts                    # createApp, router, pinia, Ionic plugin registration
  router/
    index.ts                 # Route definitions with lazy loading via () => import()
  views/
    HomePage.vue             # Full page components using IonPage wrapper
    SettingsPage.vue
    DetailPage.vue
  components/
    AppHeader.vue            # Reusable IonHeader with IonToolbar
    ItemCard.vue             # Shared card component
    EmptyState.vue
  composables/
    useCamera.ts             # Wraps @capacitor/camera plugin
    useGeolocation.ts        # Wraps @capacitor/geolocation plugin
    useNetwork.ts            # Network status listener via @capacitor/network
    usePlatform.ts           # Capacitor.getPlatform() and platform-specific logic
  stores/
    auth.store.ts            # Pinia store for authentication state
    items.store.ts           # Pinia store for primary data
  services/
    api.service.ts           # Axios or fetch wrapper with base URL and interceptors
    storage.service.ts       # Wraps @capacitor/preferences for key-value persistence
  types/
    models.ts                # TypeScript interfaces for domain entities
    api.ts                   # Request/response type definitions
  theme/
    variables.css            # Ionic CSS custom property overrides
ios/                         # Xcode project (managed by Capacitor CLI)
android/                     # Android Studio project (managed by Capacitor CLI)
capacitor.config.ts          # Capacitor configuration (appId, plugins, server settings)
```

## Architecture Rules

- Every page component must be wrapped in `<ion-page>` as the root element for Ionic navigation to work
- Use Capacitor plugins through composables that abstract the native API and provide reactive state
- Pinia stores handle all shared state; components access data via `storeToRefs()` for reactivity
- API calls live in service files, not in components or stores; stores call services and update state
- Platform-specific behavior uses `Capacitor.getPlatform()` checks inside composables, never in templates
- All routes use lazy loading with dynamic imports to minimize initial bundle size

## Coding Conventions

- Use `<script setup lang="ts">` in every Vue SFC; never use the Options API
- Define props with `defineProps<{ title: string; count: number }>()` using TypeScript generics
- Emit events with `defineEmits<{ (e: 'update', value: string): void }>()` typed syntax
- Use `ref()` for primitives and `reactive()` for objects; prefer `ref()` when in doubt
- Ionic lifecycle hooks: use `onIonViewDidEnter` and `onIonViewWillLeave` instead of `onMounted` for page data refresh
- Prefix composable files and functions with `use` (e.g., `useCamera.ts` exports `useCamera()`)
- Use `toastController.create()` from `@ionic/vue` for user notifications, not browser alerts

## Library Preferences

- HTTP client: Axios with a configured instance (baseURL, interceptors for auth tokens)
- Storage: @capacitor/preferences for key-value; @capacitor/filesystem for file storage
- Camera: @capacitor/camera with photo gallery and camera source options
- Push notifications: @capacitor/push-notifications with Firebase Cloud Messaging
- Icons: Ionicons 7 via `@ionic/vue` icon components
- Forms: VeeValidate 4 with Zod schema validation
- Date formatting: date-fns (not Moment.js)

## File Naming

- Pages: `FeaturePage.vue` in the views folder (matches Ionic convention)
- Components: `PascalCase.vue` (e.g., `ItemCard.vue`)
- Composables: `useFeature.ts` (e.g., `useCamera.ts`)
- Stores: `feature.store.ts` (e.g., `auth.store.ts`)
- Services: `feature.service.ts` (e.g., `api.service.ts`)
- Types: `feature.ts` in the types folder

## NEVER DO THIS

1. Never use `document.addEventListener` for hardware back button; use Ionic's `useBackButton` hook with priority
2. Never import from `@capacitor/core` in components directly; wrap all plugin calls in composables for testability
3. Never use `window.location.href` for navigation; use Vue Router's `useRouter().push()` or `useIonRouter()`
4. Never mutate Pinia state outside of store actions; always define actions for state modifications
5. Never skip `npx cap sync` after adding or updating a Capacitor plugin; native projects must stay in sync
6. Never use `localStorage` or `sessionStorage`; use @capacitor/preferences which works correctly on all platforms
7. Never hardcode the API base URL; use Vite environment variables (`import.meta.env.VITE_API_URL`)

## Testing

- Unit tests with Vitest and `@vue/test-utils` for component rendering and composable logic
- Mock Capacitor plugins in tests using `vi.mock('@capacitor/camera')` with typed mock implementations
- Pinia stores tested by creating a fresh `setActivePinia(createPinia())` in each test
- E2E tests with Cypress running against `vite preview` for web behavior validation
- Run `npx vitest run` for unit tests; `npx cypress run` for E2E
- Test Ionic-specific behavior (page transitions, modal lifecycle) with `mountIonicComponent` test helper
- Native-specific features tested manually on device via `npx cap run ios` and `npx cap run android`

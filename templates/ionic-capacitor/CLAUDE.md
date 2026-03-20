# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Ionic 7+ with Capacitor 5+
- [Angular 17+ / React 18+] as the UI framework
- TypeScript (strict mode)
- Capacitor native plugins for device APIs (Camera, Geolocation, Push Notifications)
- Ionic Storage or SQLite for local persistence
- [Tailwind CSS / Ionic CSS utilities] for styling

## Project Structure

```
{project-root}/
├── src/
│   ├── app/
│   │   ├── pages/                   # Route-level page components
│   │   │   ├── home/
│   │   │   ├── settings/
│   │   │   └── profile/
│   │   ├── components/              # Shared UI components
│   │   ├── services/                # Business logic and API calls
│   │   ├── guards/                  # Route guards (auth, onboarding)
│   │   ├── models/                  # TypeScript interfaces and types
│   │   └── utils/                   # Pure utility functions
│   ├── theme/
│   │   └── variables.css            # Ionic CSS custom properties
│   └── assets/
├── android/                         # Native Android project (Capacitor-managed)
├── ios/                             # Native iOS project (Capacitor-managed)
├── capacitor.config.ts              # Capacitor configuration
├── ionic.config.json
└── [angular.json / vite.config.ts]
```

## Architecture Rules

- **Pages are thin.** Pages compose components and call services. If a page component exceeds 150 lines, extract logic into a service or child component. Pages handle routing and layout, not business logic.
- **All native access goes through services.** Never call `Capacitor.Plugins.Camera` directly in a component. Wrap every plugin in a service (`CameraService`, `LocationService`) that handles permission checks, error mapping, and web fallbacks in one place.
- **Platform-aware, not platform-specific.** Use `Capacitor.isNativePlatform()` to branch behavior, never to hide features. If a feature requires native, provide a graceful web fallback or a clear "not available on web" state. Never crash on web.
- **Offline-first data layer.** Cache API responses in Ionic Storage or SQLite. Load from cache first, then sync with the server. Never show a blank screen because the network request failed. Users open mobile apps in elevators and subways.
- **Deep linking from day one.** Configure `appUrlOpen` listener in `app.component.ts` and register URL schemes in `capacitor.config.ts`. Retrofitting deep links into an app with 30 pages is painful.

## Coding Conventions

- **Use Ionic components for everything interactive.** `<ion-button>`, `<ion-input>`, `<ion-list>`, not `<button>`, `<input>`, `<ul>`. Ionic components handle platform-specific styling (Material on Android, Cupertino on iOS) and accessibility. Raw HTML elements look broken on native.
- **Lifecycle methods over constructor logic.** Use `ionViewWillEnter` / `ionViewDidLeave` for page-level setup and teardown, not `ngOnInit` / `ngOnDestroy` (Angular) or `useEffect` (React). Ionic's page lifecycle accounts for navigation stack caching.
- **Safe area handling.** Always use `ion-content` with proper padding. Apply `env(safe-area-inset-top)` and `env(safe-area-inset-bottom)` for notched devices. Never position fixed elements without accounting for safe areas — they will be hidden behind the notch or home indicator.
- **Lazy-load routes.** Every page is a lazy-loaded route module. The initial bundle contains only the shell and first screen. Never eagerly import all 20 pages.
- **Status bar and keyboard handling.** Configure `StatusBar` plugin in app initialization. Listen for `Keyboard.addListener('keyboardWillShow')` to adjust layouts. Never let the keyboard cover input fields.

## Library Preferences

- **HTTP:** Angular HttpClient (Angular) or axios with interceptors (React). Not raw fetch — you need auth token injection and error interceptors.
- **State:** NgRx/Signals (Angular) or Zustand (React) for global state. Not prop drilling through 5 navigation levels.
- **Storage:** `@ionic/storage` with SQLite driver for structured data. Not raw localStorage (5MB limit, synchronous, blocks UI thread on large reads).
- **Push notifications:** `@capacitor/push-notifications` with Firebase Cloud Messaging. Not a third-party wrapper unless you need cross-platform push abstraction.
- **Camera/media:** `@capacitor/camera` with `CameraResultType.Uri`. Not Base64 (memory-heavy for large images, causes OOM on older devices).

## File Naming

- Pages: `feature-name.page.ts` and `feature-name.page.html` (Angular) or `FeatureName.tsx` (React)
- Services: `feature-name.service.ts`
- Components: `component-name.component.ts` (Angular) or `ComponentName.tsx` (React)
- Models: `feature-name.model.ts` containing interfaces only
- Guards: `auth.guard.ts`, `onboarding.guard.ts`

## NEVER DO THIS

1. **Never modify `android/` or `ios/` directories manually for configuration.** Use `capacitor.config.ts` for plugin settings and Capacitor's config merging. Manual edits get overwritten by `npx cap sync` and create drift between platforms.
2. **Never use `window.location.href` for navigation.** Use Ionic's `NavController` or the framework router. `window.location` triggers a full page reload, destroys app state, and breaks the navigation stack and transition animations.
3. **Never store auth tokens in localStorage on native.** Use `@capacitor/preferences` (encrypted on iOS via Keychain, SharedPreferences on Android) or a Capacitor secure storage plugin. localStorage is unencrypted and readable by other apps on rooted devices.
4. **Never use `position: fixed` for bottom bars.** Use `<ion-footer>` or `<ion-tab-bar>`. Fixed positioning breaks on iOS when the keyboard opens, causing elements to float in the middle of the screen.
5. **Never skip `npx cap sync` after installing plugins.** Capacitor plugins have native code that must be synced to the platform projects. Installing an npm package alone does nothing on device. The plugin will throw "not implemented" at runtime.
6. **Never request all permissions at app launch.** Request Camera permission when the user taps the camera button, not on first open. iOS and Android reject apps that request permissions without immediate context. Users deny blanket permission requests.
7. **Never test only in the browser.** `ionic serve` does not test Capacitor plugins, native performance, gestures, safe areas, or keyboard behavior. Test on real devices or at minimum emulators for each target platform before every release.

## Testing

- Unit test services with mocked Capacitor plugins. Create a `MockCameraService` that returns a test image URI without invoking the native camera.
- Use Cypress or Playwright against `ionic serve` for end-to-end web flows. These catch routing bugs, form validation issues, and API integration problems.
- Test on physical devices for native-specific features: push notifications, camera, biometric auth, deep links. Emulators miss real-world issues like permission dialogs and memory pressure.
- Run `npx cap doctor` in CI to verify native project health and plugin compatibility before building platform binaries.

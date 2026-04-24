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

- Flutter 3.x / Dart 3.x
- Riverpod 2.x for state management
- GoRouter for navigation
- Freezed + json_serializable for data models
- Dio for HTTP requests
- Hive or SharedPreferences for local storage

## Project Structure

```
lib/
├── app/                     # App-level config (router, theme, providers)
│   ├── app.dart
│   ├── router.dart          # GoRouter configuration
│   └── theme.dart
├── features/
│   ├── auth/
│   │   ├── pages/           # Full-screen route destinations
│   │   ├── views/           # Sub-sections of a page
│   │   ├── widgets/         # Feature-specific reusable widgets
│   │   ├── providers/       # Riverpod providers for this feature
│   │   ├── models/          # Freezed data classes
│   │   └── services/        # API calls, business logic
│   └── home/
│       └── ..              # Same structure per feature
├── shared/
│   ├── widgets/             # Cross-feature widgets (AppButton, AppCard)
│   ├── providers/           # Global providers (authProvider, dioProvider)
│   ├── models/              # Shared data models
│   ├── services/            # Shared services (storage, analytics)
│   └── utils/               # Pure utility functions
└── main.dart                # Entry point: ProviderScope wraps the app
```

## Architecture Rules

- **Feature-first organization.** Every feature gets its own directory under `features/`. Code is co-located by domain, not by type.
- **Three widget tiers:**
  - **Pages**. full-screen route destinations. Registered in GoRouter. Named `XxxPage` (e.g., `LoginPage`, `ProfilePage`).
  - **Views**. major sub-sections of a page. Named `XxxView` (e.g., `ProfileHeaderView`). Can have their own providers.
  - **Widgets**. small, reusable UI components. Named `XxxWidget` or descriptively (e.g., `AvatarCircle`, `PriceTag`).
- **Riverpod is the only state management.** No `setState` in any file longer than 50 lines. No `ChangeNotifier`. No `Bloc`.
- **All data models use Freezed.** Immutable by default, union types for state, `copyWith` for updates. Run `build_runner` after changing any model.
- **GoRouter handles all navigation.** Define routes in `app/router.dart`. Use named routes with `context.goNamed()`. Never use `Navigator.push` directly.

## Coding Conventions

- Riverpod provider naming: `xxxProvider` for simple providers, `xxxProvider.family` for parameterized. Always type annotate the return: `final userProvider = FutureProvider.autoDispose<User>((ref) => ...)`.
- Files: one class per file, `snake_case.dart`. The file name matches the class: `user_profile_page.dart` contains `UserProfilePage`.
- Prefer `const` constructors everywhere. Mark widgets as `const` when all parameters are compile-time constants.
- Use `ref.watch()` in `build()` for reactive state. Use `ref.read()` in callbacks and event handlers only. never in `build()`.
- Dio interceptors go in `shared/services/dio_service.dart`. Add auth token, logging, and error mapping interceptors in one place.

## Library Preferences

- **State management:** Riverpod. not Bloc (too much boilerplate for most apps), not Provider (Riverpod is its successor with compile-time safety).
- **Navigation:** GoRouter. not auto_route (GoRouter has first-party Flutter team involvement) and not Navigator 2.0 directly (too verbose).
- **Models:** Freezed + json_serializable. not manually written `fromJson`/`toJson`. Freezed gives you `copyWith`, equality, and union types for free.
- **HTTP:** Dio. not `http` package (Dio has interceptors, cancellation, and upload progress built in).
- **Local storage:** Hive for structured local data, SharedPreferences for simple key-value. Not sqflite unless you genuinely need relational queries on-device.

## File Naming

- Pages: `xxx_page.dart` → `login_page.dart`, `profile_page.dart`
- Views: `xxx_view.dart` → `profile_header_view.dart`
- Widgets: `xxx_widget.dart` or descriptive → `avatar_circle.dart`, `price_tag.dart`
- Providers: `xxx_provider.dart` → `auth_provider.dart`, `user_provider.dart`
- Models: `xxx_model.dart` → `user_model.dart` (contains Freezed class)
- Services: `xxx_service.dart` → `auth_service.dart`, `dio_service.dart`

## NEVER DO THIS

1. **Never use `setState` in a file longer than 50 lines.** If the widget has enough complexity to exceed 50 lines, it needs Riverpod. `setState` causes full widget rebuilds and becomes unmaintainable fast.
2. **Never put business logic in `build()`.** The `build` method is for UI composition only. Calculations, formatting, and side effects go in providers or service classes.
3. **Never use `BuildContext` across async gaps without checking `mounted`.** After any `await`, the widget may have been disposed. Always check `if (!context.mounted) return;` before using context post-await.
4. **Never import `dart:io` in web-compatible code.** Use the `universal_io` package or conditional imports if the code must run on both mobile and web.
5. **Never use `dynamic` type.** It disables type checking entirely. Use `Object?` for truly unknown types and cast with pattern matching.
6. **Never use `Navigator.push` when GoRouter is configured.** All navigation goes through GoRouter's `context.go()`, `context.push()`, or `context.goNamed()`. Mixing navigators creates back-stack bugs.
7. **Never forget to run `build_runner` after modifying Freezed models.** Generated files (`.freezed.dart`, `.g.dart`) must be up to date. Add `dart run build_runner build --delete-conflicting-outputs` to your workflow.

## Testing

- Use `flutter_test` for widget tests. Test widget behavior (tap → state change), not widget tree structure.
- Use `mocktail` for mocking. not `mockito` (mocktail doesn't need codegen).
- Test providers in isolation using `ProviderContainer` with overrides.
- Integration tests go in `integration_test/` using `patrol` or Flutter's built-in integration test framework.
- Golden tests for critical UI components. compare rendered widgets against reference screenshots.

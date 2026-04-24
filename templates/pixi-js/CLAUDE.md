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

## Production Delivery Playbook (Category: Game Dev)

### Release Discipline
- Protect frame-time stability and memory budgets on core loops.
- Preserve deterministic gameplay logic where networking/replay depends on it.
- Validate save/load compatibility before schema changes.

### Merge/Release Gates
- Runtime performance spot checks pass on representative scenes.
- Input, physics, and save-state regression checks pass.
- No shipping with crash-on-start or asset-load blockers.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- PixiJS 8.x as the WebGL/WebGPU 2D renderer
- TypeScript 5.x with strict mode enabled
- Vite 5.x for bundling, HMR, and asset handling
- @pixi/sound for audio playback and filters
- @pixi/ui for accessible interactive UI components
- @pixi/spine for Spine skeletal animations
- gsap for complex timeline animations and tweens
- texture-packer-loader for optimized sprite atlas loading

## Project Structure

```
src/
  main.ts                    # Application bootstrap, renderer init
  app/
    Application.ts           # PixiJS Application wrapper, resize logic
    AssetLoader.ts           # Asset manifest and bundle loading
    SceneManager.ts          # Scene stack with transitions
  scenes/
    LoadingScene.ts          # Progress bar, asset preloading
    MenuScene.ts             # Main menu with interactive buttons
    GameScene.ts             # Core gameplay container
  display/
    Player.ts                # Player sprite with animation states
    ParticleEffect.ts        # Particle container presets
    TilingBackground.ts      # Scrolling tiled background
    SpriteButton.ts          # Interactive button with states
  systems/
    InputSystem.ts           # Pointer + keyboard input abstraction
    PhysicsSystem.ts         # Simple AABB or SAT collision
    AnimationSystem.ts       # Frame-based animation controller
    SoundSystem.ts           # Audio channel management
  utils/
    math.ts                  # Clamp, lerp, distance helpers
    pool.ts                  # Generic display object pool
    responsive.ts            # Layout helpers for multi-resolution
  config/
    assets.ts                # Asset manifest with bundles
    settings.ts              # Game configuration constants
public/
  assets/
    spritesheets/            # JSON atlas + PNG pairs
    spine/                   # Spine JSON + atlas + PNG
    audio/                   # MP3 + OGG sound files
    fonts/                   # WOFF2 web fonts, bitmap font XML
```

## Architecture Rules

- Scenes are `Container` subclasses managed by a SceneManager that handles transitions and lifecycle
- The SceneManager maintains a stack; only the top scene receives update ticks
- All display objects that leave the stage must call `destroy({ children: true })` to prevent memory leaks
- Use `Assets.load()` with bundle manifests defined in `assets.ts`; never use raw `fetch` for game assets
- Resize handling uses a fixed game resolution with `application.renderer.resize()` and CSS scaling
- Input events bind to display objects via `eventMode = 'static'` and pointer events, not DOM listeners
- The main game loop uses `app.ticker.add()` for all per-frame updates with `ticker.deltaMS` for timing

## Coding Conventions

- Scene classes: PascalCase with `Scene` suffix (`GameScene`, `MenuScene`)
- Display objects: PascalCase matching their role (`Player`, `HealthBar`, `Coin`)
- Systems: PascalCase with `System` suffix (`InputSystem`, `PhysicsSystem`)
- Use `Ticker.shared` delta for all movement calculations; never assume fixed frame rate
- Prefer `Container` composition over deep inheritance hierarchies
- Type all event callbacks: `sprite.on('pointerdown', (e: FederatedPointerEvent) => {})`
- Asset keys are kebab-case strings: `'player-idle'`, `'bg-music'`

## Library Preferences

- gsap over manual ticker tweens for UI animations, transitions, and easing
- @pixi/sound over Howler.js for audio (better PixiJS integration)
- @pixi/spine over frame-by-frame for character animations with complex rigs
- PixiJS Assets class over custom loaders for all asset management
- @pixi/ui over custom button/input implementations

## File Naming

- Source files: PascalCase for classes (`GameScene.ts`), camelCase for utilities (`math.ts`)
- Asset files: kebab-case (`player-walk.json`, `coin-collect.mp3`)
- Config files: camelCase (`assets.ts`, `settings.ts`)
- Test files: same name with `.test.ts` suffix (`GameScene.test.ts`)

## NEVER DO THIS

1. Never add display objects without eventually removing and destroying them - always call `destroy({ children: true })` when done
2. Never use `document.addEventListener` for game input - use PixiJS `eventMode` and `FederatedEvent` system
3. Never create `new Texture()` from raw images - use `Assets.load()` pipeline for proper GPU upload and caching
4. Never render text with `HTMLText` in performance-critical paths - use `BitmapText` for frequently updating text like scores
5. Never use `filters` on large containers in mobile builds - filters trigger full re-renders and destroy performance
6. Never set `interactive = true` on old API - use `eventMode = 'static'` or `'dynamic'` in PixiJS 8

## Testing

- Unit test game logic (scoring, collision math, state) with Vitest, decoupled from PixiJS
- Stub the renderer with `{ width: 800, height: 600 }` mocks for scene layout tests
- Visual regression tests capture canvas screenshots with Playwright and compare against baselines
- Test input handling by dispatching synthetic `FederatedPointerEvent` on display objects
- Run `tsc --noEmit` in CI as a type-checking gate before build
- Performance benchmarks measure draw calls via `renderer.renderingToScreen` and object count per scene

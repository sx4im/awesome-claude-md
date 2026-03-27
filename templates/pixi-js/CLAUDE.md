# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

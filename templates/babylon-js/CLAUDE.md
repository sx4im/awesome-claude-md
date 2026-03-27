# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Babylon.js 7.x as the 3D WebGL/WebGPU engine
- TypeScript 5.x with strict mode enabled
- Vite 5.x for development server and production bundling
- Havok physics plugin for rigid body simulation
- Babylon.js GUI (2D) for in-game UI overlays
- Babylon.js Inspector for runtime debugging (dev only)
- Babylon.js Loaders for GLTF/GLB model import

## Project Structure

```
src/
  main.ts                     # Engine and scene bootstrap
  engine/
    EngineManager.ts          # Engine init, render loop, resize
    SceneFactory.ts           # Scene creation and disposal
    InputManager.ts           # Unified keyboard, mouse, gamepad
  scenes/
    MainMenuScene.ts          # Menu UI scene
    GameScene.ts              # Primary gameplay scene
    LoadingScene.ts           # Asset preloading with progress
  entities/
    Player.ts                 # Player mesh, controller, animations
    Enemy.ts                  # Enemy with NavMesh pathfinding
    Projectile.ts             # Physics-driven projectile
    Pickup.ts                 # Collectible item with trigger volume
  world/
    LevelBuilder.ts           # Procedural or loaded level assembly
    LightingRig.ts            # Scene lights, shadows, environment
    SkyboxManager.ts          # HDR skybox and environment texture
    TerrainGenerator.ts       # Heightmap terrain with LOD
  systems/
    PhysicsSystem.ts          # Havok body creation and management
    AnimationSystem.ts        # Animation group blending, state machine
    AudioSystem.ts            # Positional audio, ambient sounds
    ParticleSystem.ts         # GPU particle system presets
  ui/
    HUD.ts                    # Health, ammo, minimap (AdvancedDynamicTexture)
    DialogBox.ts              # NPC dialog with choices
  utils/
    math.ts                   # Vector3 helpers, quaternion utils
    pool.ts                   # Mesh instance pool
    debug.ts                  # Inspector toggle, axis viewer
  config/
    settings.ts               # Render quality, physics params
    assets.ts                 # Asset manifest with paths
public/
  assets/
    models/                   # GLB/GLTF 3D models
    textures/                 # PBR texture sets (albedo, normal, roughness)
    audio/                    # Spatial audio OGG files
    environments/             # HDR environment maps
```

## Architecture Rules

- One Scene per game state; dispose the previous scene fully before creating the next
- Use TransformNode as empty parent nodes for grouping; never parent directly to scene root for movable entities
- Physics bodies use Havok plugin exclusively; register shapes via `PhysicsAggregate` with `PhysicsShapeType`
- Meshes loaded from GLB are cloned or instanced with `mesh.createInstance()` for duplicates, never re-loaded
- Shadow generators attach to DirectionalLight only; use cascaded shadow maps for outdoor scenes
- Camera setup uses `ArcRotateCamera` for orbit views, `UniversalCamera` for FPS, `FollowCamera` for third-person
- GUI uses `AdvancedDynamicTexture.CreateFullscreenUI()` for HUD; attach to mesh with `CreateForMesh()` for world-space UI

## Coding Conventions

- Scene classes encapsulate setup in `build()` async method, cleanup in `dispose()`
- Entity classes hold their root `TransformNode` and expose `update(deltaTime: number)` method
- Use `Observable` pattern from Babylon.js for custom events: `onDamageObservable.notifyObservers(data)`
- Prefer `Vector3.Zero()`, `Vector3.Up()` static constructors over `new Vector3(0,0,0)`
- Materials use PBRMaterial exclusively; never use StandardMaterial in production builds
- All async loading returns `Promise<void>` and is awaited in scene build methods

## Library Preferences

- Havok over Cannon.js or Oimo for physics (official Babylon.js integration, WASM performance)
- Babylon.js GUI over HTML/CSS overlays for all in-game UI
- Babylon.js Animation over gsap for 3D object animations
- Babylon.js AssetContainer over manual loader calls for asset management
- Navigation plugin with Recast for AI pathfinding

## File Naming

- Source files: PascalCase for classes (`GameScene.ts`, `Player.ts`)
- Utility files: camelCase (`math.ts`, `pool.ts`, `debug.ts`)
- Asset files: kebab-case (`robot-character.glb`, `stone-wall-normal.png`)
- PBR texture sets: `{name}-albedo.png`, `{name}-normal.png`, `{name}-roughness.png`

## NEVER DO THIS

1. Never call `scene.render()` manually - use `engine.runRenderLoop()` and let the engine manage the render cycle
2. Never use `StandardMaterial` in production - always use `PBRMaterial` for physically correct lighting
3. Never load the same GLB file multiple times - use `AssetContainer.instantiateModelsToScene()` for copies
4. Never create physics impostors with the legacy API - use `PhysicsAggregate` with Havok plugin
5. Never add the Inspector bundle in production builds - gate it behind `import.meta.env.DEV` checks
6. Never forget to dispose scenes, textures, and materials - Babylon.js does not garbage collect GPU resources automatically
7. Never use `setInterval` for game loops - all timing goes through `scene.onBeforeRenderObservable`

## Testing

- Unit test game logic (inventory, damage, scoring) with Vitest decoupled from Babylon.js
- Scene tests use `NullEngine` for headless rendering without a WebGL context
- Physics tests create a minimal scene with Havok, step simulation manually, and assert positions
- Use `scene.onReadyObservable` in integration tests to wait for all assets before assertions
- Visual regression tests render to offscreen canvas and compare screenshots with Playwright
- Run `tsc --noEmit` and `vite build` in CI to catch type and bundle errors

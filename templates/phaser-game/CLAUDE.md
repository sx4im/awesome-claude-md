# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Phaser 3.80+ as the game framework
- TypeScript 5.x with strict mode enabled
- Vite 5.x for bundling and dev server
- Texture Packer for sprite atlases (JSON Hash format)
- Tiled Map Editor for tilemaps (exported as JSON)
- Howler.js for advanced audio needs beyond Phaser's built-in sound manager

## Project Structure

```
src/
  scenes/
    BootScene.ts          # Asset preloading, progress bar
    MainMenuScene.ts      # Title screen, settings access
    GameScene.ts          # Core gameplay loop
    UIScene.ts            # HUD overlay, runs parallel to GameScene
    PauseScene.ts         # Pause menu, launched over GameScene
  entities/
    Player.ts             # Extends Phaser.Physics.Arcade.Sprite
    Enemy.ts              # Base enemy class
    Projectile.ts         # Bullet pool objects
  systems/
    InputManager.ts       # Keyboard + gamepad abstraction
    SaveManager.ts        # LocalStorage persistence
    AudioManager.ts       # Sound effect and music controller
  config/
    game.config.ts        # Phaser.Types.Core.GameConfig
    physics.config.ts     # Arcade/Matter physics settings
    animations.ts         # Animation registry definitions
  utils/
    math.ts               # Lerp, clamp, angle utilities
    pool.ts               # Generic object pooling
  main.ts                 # Game bootstrap entry point
public/
  assets/
    sprites/              # PNG atlases + JSON data
    tilemaps/             # Tiled JSON exports
    audio/                # OGG + MP3 pairs for cross-browser
    fonts/                # Bitmap font XML + PNG
```

## Architecture Rules

- Every game entity extends a Phaser GameObject or Physics body directly; never wrap GameObjects in plain classes
- Scenes communicate through the EventEmitter on `this.game.events`, never by importing scene instances
- Use object pooling via `Phaser.GameObjects.Group` with `maxSize`, `classType`, and `runChildUpdate` for bullets, particles, and enemies
- Preload all assets in BootScene only; other scenes must not call `this.load` after boot
- Physics bodies use Arcade Physics unless complex shapes require Matter.js; never mix both in one scene
- Store game state in a singleton registry via `this.registry` (Phaser's DataManager), not in global variables

## Coding Conventions

- Name scenes with the `Scene` suffix: `GameScene`, `MenuScene`
- Name entities as singular nouns: `Player`, `Skeleton`, `Coin`
- Use `Phaser.Math.Vector2` for all positional math, never raw `{x, y}` objects
- Type all event payloads with interfaces: `interface DamageEvent { target: string; amount: number; }`
- Prefer `this.time.addEvent()` over `setTimeout` for all delayed actions
- Use `this.tweens.add()` for UI animations, physics for gameplay movement

## Library Preferences

- Phaser's built-in loader over fetch/axios for game assets
- Phaser.Input.Keyboard.KeyCodes over raw key strings
- Phaser.Display.Color for color manipulation
- rexUI plugin for complex UI elements (buttons, dialogs, sliders)

## File Naming

- Scene files: PascalCase with `Scene` suffix (`GameScene.ts`)
- Entity files: PascalCase singular (`Player.ts`, `Goblin.ts`)
- Utility files: camelCase (`math.ts`, `pool.ts`)
- Asset files: kebab-case (`player-run.png`, `level-01.json`)
- Config files: kebab-case with `.config.ts` suffix

## NEVER DO THIS

1. Never use `setInterval` or `setTimeout` - use `this.time.addEvent()` or `this.time.delayedCall()` for frame-accurate timing
2. Never create textures or game objects in the constructor - use `create()` lifecycle method
3. Never access `this.scene.scenes` to get references to other scenes - use `this.scene.get('SceneKey')` or events
4. Never load assets outside BootScene - all asset loading happens in one centralized preload
5. Never use DOM elements for game UI - use Phaser GameObjects or the rexUI plugin
6. Never update physics bodies manually with `x/y` assignment - use `setVelocity()`, `applyForce()`, or `moveTo()`
7. Never forget to call `this.destroy()` on objects removed from play - return them to pools instead

## Testing

- Unit test game logic (damage calc, inventory, state machines) with Vitest, decoupled from Phaser
- Scene integration tests use Phaser in headless mode (`type: Phaser.HEADLESS`) with a custom test harness
- Snapshot test animation frame sequences by asserting against `anims.currentFrame.index`
- Test input sequences by emitting synthetic keyboard events through `this.input.keyboard.emit()`
- Run `npx vite build` as a smoke test in CI to catch import and type errors

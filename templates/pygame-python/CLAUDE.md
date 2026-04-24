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

- Python 3.11+ as the language runtime
- Pygame 2.5+ (pygame-ce community edition preferred) for rendering, input, and audio
- pytmx for Tiled TMX map loading and rendering
- pyinstaller for building standalone executables
- pydantic for configuration validation and save data schemas
- pytest for testing game logic

## Project Structure

```
src/
  main.py                     # Entry point, pygame.init(), game loop
  game/
    game.py                   # Game class with main loop, state management
    settings.py               # Constants: FPS, TILE_SIZE, colors, paths
  states/
    base_state.py             # Abstract base state with enter/exit/update/draw
    menu_state.py             # Main menu with button navigation
    play_state.py             # Core gameplay state
    pause_state.py            # Pause overlay state
    game_over_state.py        # Score display, restart option
  entities/
    player.py                 # Player sprite with animation and input
    enemy.py                  # Base enemy sprite with AI
    projectile.py             # Bullet sprite with velocity
    pickup.py                 # Collectible item sprite
  components/
    animator.py               # Sprite sheet animation controller
    health.py                 # Health component with damage/heal
    physics.py                # Velocity, gravity, AABB collision
  systems/
    camera.py                 # Camera offset with follow and bounds
    collision.py              # Sprite group collision detection
    input_handler.py          # Key mapping abstraction layer
    sound_manager.py          # Sound effect and music playback
    particle_system.py        # Particle emitter and renderer
    save_system.py            # JSON save/load with pydantic models
  ui/
    hud.py                    # Health bar, score, timer drawing
    button.py                 # Clickable UI button with hover state
    text.py                   # Text rendering utility with caching
  maps/
    map_loader.py             # pytmx map loading and object spawning
    tilemap_renderer.py       # Efficient tilemap surface rendering
  utils/
    spritesheet.py            # Sprite sheet slicing utility
    timer.py                  # Cooldown and delay timer class
    math_utils.py             # Lerp, clamp, distance functions
assets/
  images/
    sprites/                  # PNG sprite sheets
    tilesets/                 # Tileset PNG files
    ui/                       # UI element images
  audio/
    sfx/                      # WAV sound effects
    music/                    # OGG background music
  maps/                       # Tiled TMX map files
  fonts/                      # TTF font files
```

## Architecture Rules

- Game states inherit from `BaseState` and implement `enter()`, `exit()`, `handle_event(event)`, `update(dt)`, `draw(surface)`
- A `StateManager` maintains a stack of states; only the top state receives input and updates
- All sprites extend `pygame.sprite.Sprite` and belong to `pygame.sprite.Group` instances for batch updates and draws
- Collision detection uses `pygame.sprite.groupcollide()` and `pygame.sprite.spritecollide()` with appropriate masks
- Delta time (`dt`) in seconds is passed to every `update()` call; compute as `clock.tick(FPS) / 1000.0`
- Asset loading happens once in the game's `__init__` and is stored in a shared `assets` dictionary
- The display surface is a fixed logical resolution; scale to window size with `pygame.transform.scale`

## Coding Conventions

- Classes: PascalCase (`Player`, `MenuState`, `SoundManager`)
- Functions and methods: snake_case (`handle_input`, `spawn_enemy`, `load_spritesheet`)
- Constants: UPPER_SNAKE_CASE in `settings.py` (`SCREEN_WIDTH`, `FPS`, `GRAVITY`, `TILE_SIZE`)
- Private methods: single underscore prefix (`_calculate_damage`, `_load_frame`)
- Type hints on all function signatures: `def update(self, dt: float) -> None:`
- Use `dataclass` or `pydantic.BaseModel` for structured data (save files, configs, level metadata)
- One class per file for entities and states; utilities may have multiple functions per file

## Library Preferences

- pygame-ce (community edition) over standard pygame for better performance and maintenance
- pytmx over custom map parsing for Tiled map integration
- pydantic over raw dicts for save data and configuration validation
- pygame.sprite.Group over manual list management for all entity collections
- pygame.mixer over separate audio libraries for sound and music

## File Naming

- Python source files: snake_case (`player.py`, `menu_state.py`, `sound_manager.py`)
- Asset files: snake_case (`player_idle.png`, `coin_pickup.wav`)
- Map files: snake_case (`level_01.tmx`, `dungeon.tmx`)
- Test files: `test_` prefix (`test_player.py`, `test_collision.py`)

## NEVER DO THIS

1. Never call `pygame.image.load()` inside the game loop - load all images at startup and store references
2. Never use `pygame.display.update()` with no arguments for partial redraws - use `pygame.display.flip()` for full frame updates
3. Never hardcode pixel positions - use constants from `settings.py` and compute relative to `TILE_SIZE` or screen dimensions
4. Never use `time.sleep()` in the game loop - use `pygame.time.Clock.tick()` for frame rate control
5. Never blit text every frame without caching - render text surfaces once with `font.render()` and cache until content changes
6. Never use `pygame.event.get()` in multiple places per frame - poll events once in the main loop and distribute to the active state

## Testing

- Unit test game logic (damage, inventory, state transitions) with pytest, no pygame initialization required
- Entity tests instantiate sprites with mock surfaces and call `update(dt)` with fixed delta values
- Collision tests create sprite groups with known positions and assert `spritecollide` results
- State machine tests verify `enter()` and `exit()` callbacks fire correctly on transitions
- Run `mypy src/ --strict` in CI for static type checking
- Run `ruff check src/` for linting and `ruff format --check src/` for formatting verification
- Integration tests initialize pygame in headless mode with `os.environ['SDL_VIDEODRIVER'] = 'dummy'`

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- raylib 5.x for rendering, input, audio, and window management
- C17 standard (ISO/IEC 9899:2018) compiled with gcc or clang
- CMake 3.20+ for cross-platform build configuration
- raygui for immediate-mode GUI widgets
- rres for resource packaging and loading
- Make or Ninja as the build backend

## Project Structure

```
src/
  main.c                     # Entry point, game loop, InitWindow/CloseWindow
  game/
    game.h                   # Game state struct, init/update/draw declarations
    game.c                   # Core game state management
    player.h                 # Player struct, movement, animation
    player.c                 # Player implementation
    enemy.h                  # Enemy struct, AI, spawning
    enemy.c                  # Enemy implementation
    projectile.h             # Projectile pool struct and functions
    projectile.c             # Projectile update, collision, recycle
    level.h                  # Level data, tilemap loading
    level.c                  # Level rendering, collision map
  systems/
    input.h                  # Input abstraction (keyboard, gamepad)
    input.c                  # Rebindable input mapping
    audio.h                  # Sound and music management
    audio.c                  # Audio loading, playback, volume
    camera.h                 # Camera2D/Camera3D helpers
    camera.c                 # Follow, shake, lerp, bounds
    collision.h              # AABB and circle collision helpers
    collision.c              # Overlap tests, resolution
    particles.h              # Particle system struct
    particles.c              # Emit, update, draw particles
  ui/
    hud.h                    # HUD drawing functions
    hud.c                    # Health bar, score, minimap
    menu.h                   # Menu state and navigation
    menu.c                   # Menu rendering, selection
  utils/
    mathutils.h              # Lerp, clamp, remap, easing functions
    pool.h                   # Generic object pool macros
    config.h                 # Game constants and tuning values
resources/
  textures/                  # PNG sprite sheets and tilesets
  sounds/                    # WAV sound effects
  music/                     # OGG music tracks
  fonts/                     # TTF font files
  shaders/                   # GLSL shader files (if custom)
CMakeLists.txt               # Build configuration
```

## Architecture Rules

- Single game state struct holds all mutable state; pass pointer to all update and draw functions
- Game loop in `main.c` follows: `InitWindow` > `InitGame` > `while (!WindowShouldClose())` > `UpdateGame` > `DrawGame` > `CloseGame` > `CloseWindow`
- All entity types use plain C structs with a fixed-size array pool; never use `malloc` in the game loop
- Collision detection happens in the update phase; rendering in the draw phase; never mix the two
- Resource loading happens once at startup in `InitGame()`; all textures, sounds, and fonts are stored in the game state struct
- Use `BeginMode2D(camera)` / `EndMode2D()` for world rendering; draw HUD outside the camera transform
- Screen transitions use a simple enum state machine: `SCREEN_MENU`, `SCREEN_GAME`, `SCREEN_PAUSE`, `SCREEN_GAMEOVER`

## Coding Conventions

- Functions: PascalCase verbs matching raylib style (`UpdatePlayer`, `DrawEnemy`, `SpawnProjectile`)
- Structs: PascalCase nouns (`Player`, `Enemy`, `GameState`, `ParticleEmitter`)
- Constants and macros: UPPER_SNAKE_CASE (`MAX_ENEMIES`, `SCREEN_WIDTH`, `PLAYER_SPEED`)
- Local variables: camelCase (`deltaTime`, `playerPos`, `enemyCount`)
- Header files use include guards: `#ifndef PLAYER_H` / `#define PLAYER_H` / `#endif`
- Each `.c` file includes only its own `.h` and required system headers; avoid transitive includes
- Prefer stack allocation and fixed arrays over heap allocation in gameplay code

## Library Preferences

- raylib's built-in audio over OpenAL or SDL_mixer
- raygui over custom UI rendering for debug tools and menus
- raylib's built-in math (`Vector2Add`, `Vector2Scale`) over custom math functions
- raylib's texture atlas support over manual UV calculation
- CMake over raw Makefiles for cross-platform builds

## File Naming

- Source files: snake_case (`player.c`, `game_state.c`, `audio.c`)
- Header files: matching snake_case (`player.h`, `game_state.h`)
- Asset files: snake_case (`player_run.png`, `jump_sound.wav`)
- Shader files: snake_case with stage suffix (`blur.fs`, `default.vs`)

## NEVER DO THIS

1. Never call `malloc` or `free` inside the game loop - preallocate all pools at init, reuse with index cycling
2. Never call `LoadTexture` or `LoadSound` after initialization - all resources load in `InitGame()` and unload in `CloseGame()`
3. Never use `DrawText` with the default font in production - load a custom TTF font with `LoadFontEx` for consistent rendering
4. Never forget `BeginDrawing()` / `EndDrawing()` pairs or `BeginMode2D()` / `EndMode2D()` pairs - mismatched calls cause rendering artifacts
5. Never read input in the draw phase - all `IsKeyPressed`, `IsGamepadButtonPressed` calls belong in the update phase
6. Never use global mutable variables - pass `GameState*` explicitly to all functions that need state

## Testing

- Unit test game logic (collision math, state transitions, damage) by compiling test files linking against game modules
- Use Unity Test Framework (ThrowTheSwitch) for structured C unit tests with assertions
- Collision tests call detection functions with known coordinates and assert overlap results
- Build tests compile the full project with `-Wall -Wextra -Werror` to catch warnings as errors
- CI runs `cmake --build . --config Release` and executes the test binary
- Memory leak checks use Valgrind on Linux or AddressSanitizer (`-fsanitize=address`) in debug builds

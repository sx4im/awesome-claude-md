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

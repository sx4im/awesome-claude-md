# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- LOVE 11.5+ (love2d) as the game framework
- Lua 5.1 (LuaJIT) as the scripting language
- bump.lua for AABB collision detection and response
- hump library (gamestate, timer, vector, camera modules)
- anim8 for sprite animation management
- push library for resolution-independent rendering
- moonshine for lighting and shadows (if needed)

## Project Structure

```
src/
  main.lua                 # love.load, love.update, love.draw bootstrap
  conf.lua                 # LOVE configuration (window, modules)
  states/
    menu.lua               # Main menu gamestate
    game.lua               # Core gameplay gamestate
    pause.lua              # Pause overlay gamestate
    gameover.lua           # Game over screen
  entities/
    player.lua             # Player entity with input, animation
    enemy.lua              # Base enemy with AI behavior
    projectile.lua         # Bullet/projectile entity
    entity.lua             # Base entity class (middleclass)
  systems/
    input.lua              # Input mapping and action abstraction
    camera.lua             # Camera with follow, shake, bounds
    collision.lua          # bump.lua world and response handling
    audio.lua              # Sound effect and music manager
    particles.lua          # Particle system presets
  ui/
    hud.lua                # Health bar, score, minimap overlay
    button.lua             # Clickable UI button component
    dialog.lua             # Text dialog box with typewriter effect
  lib/                     # Third-party libraries (bump, hump, anim8)
  data/
    levels.lua             # Level definitions and spawn tables
    constants.lua          # Game-wide constants and tuning values
assets/
  sprites/                 # PNG sprite sheets
  maps/                    # Tiled-exported Lua map files
  sounds/                  # OGG sound effects
  music/                   # OGG background tracks
  fonts/                   # TTF font files
```

## Architecture Rules

- Use hump.gamestate for all screen management; each state implements `enter`, `update`, `draw`, `leave`
- Entity base class uses middleclass for OOP; all entities inherit from `Entity` and override `update(dt)` and `draw()`
- Collision world is a single bump.lua instance stored in the game state; entities register and unregister themselves
- Delta time (`dt`) must be passed through every update call; never use `love.timer.getDelta()` inside entity updates
- All coordinates use world space; camera translation happens only in the draw phase via hump.camera
- Asset loading happens once in `love.load()`; reference loaded assets through a global assets table

## Coding Conventions

- Use local variables everywhere; never pollute the global table except for the `assets` and `game` singletons
- Name files and variables in snake_case: `player.lua`, `max_health`, `spawn_enemy()`
- Classes use PascalCase: `Player`, `Enemy`, `ProjectilePool`
- Constants in UPPER_SNAKE_CASE in `constants.lua`: `MAX_SPEED`, `GRAVITY`, `TILE_SIZE`
- Indent with 2 spaces, no tabs
- Use early returns to avoid deep nesting in update and collision callbacks

## Library Preferences

- bump.lua over love.physics (Box2D) for 2D platformer and top-down games
- hump.vector over manual x,y math for all vector operations
- hump.timer over manual dt accumulation for tweens and delayed calls
- anim8 over manual frame counting for sprite animation
- push over manual scaling for resolution independence
- middleclass over manual metatables for OOP

## File Naming

- All Lua source files: snake_case (`player.lua`, `game_state.lua`)
- Asset files: snake_case (`player_idle.png`, `jump_sound.ogg`)
- Libraries in `lib/` keep their original names (`bump.lua`, `anim8.lua`)
- Map files from Tiled: snake_case (`level_01.lua`)

## NEVER DO THIS

1. Never use `love.graphics.setColor` without resetting it to `{1, 1, 1, 1}` at the end of the draw call
2. Never load assets inside `love.update()` or `love.draw()` - all loading happens in `love.load()`
3. Never use `love.physics` (Box2D) for simple AABB games - bump.lua is simpler and faster
4. Never modify tables while iterating them with `ipairs` or `pairs` - collect removals and process after
5. Never use global variables for entity state - use local variables and pass references explicitly
6. Never forget to multiply movement by `dt` - all motion must be frame-rate independent

## Testing

- Use busted framework for unit testing game logic (damage, inventory, state machines)
- Test entity behavior by instantiating entities and calling `update(dt)` with fixed dt values
- Collision tests create a temporary bump world, add entities, and assert response types
- Run `busted --pattern=_spec src/` to execute all spec files
- CI runs `luacheck src/ --std=love+luajit` for static analysis alongside tests
- Performance profiling with `jit.p` module to identify hot paths in update loops

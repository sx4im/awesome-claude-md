# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Bevy 0.14+ as the ECS game engine
- Rust 2021 edition with clippy lints at warn level
- bevy_rapier3d for physics simulation
- bevy_egui for debug UI and editor overlays
- bevy_asset_loader for declarative asset collection loading
- bevy_kira_audio for advanced audio playback with effects
- serde + ron for configuration and save data serialization

## Project Structure

```
src/
  main.rs                  # App builder, plugin registration
  plugins/
    mod.rs
    game_plugin.rs         # Core gameplay plugin
    menu_plugin.rs         # Main menu and pause screens
    audio_plugin.rs        # Audio systems and resources
    debug_plugin.rs        # Dev-only egui overlays, gizmos
  components/
    mod.rs
    player.rs              # Player marker, stats, inventory
    enemy.rs               # Enemy type enum, AI state
    physics.rs             # Velocity, collider markers
    animation.rs           # AnimationTimer, SpriteIndex
  resources/
    mod.rs
    game_state.rs          # GameState resource, score, level
    asset_handles.rs       # Typed asset collections
    input_config.rs        # Rebindable input mappings
  systems/
    mod.rs
    movement.rs            # Player and entity movement
    combat.rs              # Damage, health, death
    spawning.rs            # Entity spawning, wave management
    camera.rs              # Camera follow, shake, zoom
    ui.rs                  # HUD rendering systems
  events/
    mod.rs
    damage.rs              # DamageEvent, HealEvent
    game.rs                # LevelComplete, GameOver
  bundles/
    mod.rs
    player_bundle.rs       # PlayerBundle with all components
    enemy_bundle.rs        # EnemyBundle variants
assets/
  models/                  # GLTF/GLB 3D models
  textures/                # PNG textures and sprite sheets
  audio/                   # OGG audio files
  config/                  # RON configuration files
```

## Architecture Rules

- One plugin per major feature; register all plugins in `main.rs` with `app.add_plugins()`
- Components are pure data structs with `#[derive(Component)]`; never put methods on components
- All game logic lives in systems; systems are plain functions with query parameters
- Use `Events<T>` and `EventReader<T>` / `EventWriter<T>` for cross-system communication, not direct mutation
- State transitions use Bevy's `States` derive macro with `OnEnter`, `OnExit`, and `in_state()` run conditions
- Resources hold global singleton data; prefer resources over marker-entity patterns for unique state
- System ordering uses explicit `.before()` / `.after()` or system sets, never rely on implicit ordering

## Coding Conventions

- Components: PascalCase structs (`Health`, `Velocity`, `PlayerMarker`)
- Systems: snake_case functions named as verb phrases (`move_player`, `apply_damage`, `spawn_enemies`)
- Plugins: PascalCase with `Plugin` suffix (`GamePlugin`, `AudioPlugin`)
- Events: PascalCase with `Event` suffix (`DamageEvent`, `CollisionEvent`)
- Use `Query<Entity, With<Player>>` marker pattern instead of storing entity IDs in resources
- Prefer `Commands` for structural changes, direct `&mut Transform` queries for per-frame updates

## Library Preferences

- bevy_rapier over custom physics for all collision and rigid body needs
- bevy_asset_loader over manual `AssetServer::load` calls for organized loading states
- ron over json for all game config files (more readable, supports Rust types)
- bevy_egui for any debug/editor UI, Bevy UI nodes for in-game HUD

## File Naming

- All Rust source files: snake_case (`player_bundle.rs`, `movement.rs`)
- Asset files: snake_case (`goblin_walk.png`, `sword_hit.ogg`)
- Config files: snake_case with `.ron` extension (`level_01.ron`)
- Module declarations in `mod.rs` files, not inline `mod name { }` blocks

## NEVER DO THIS

1. Never store `Entity` IDs in components or resources long-term - they can be invalidated; use marker components with queries instead
2. Never use `std::thread` or `tokio` directly - use Bevy's `AsyncComputeTaskPool` for background work
3. Never mutate the `World` outside of systems - use `Commands` or exclusive systems if direct world access is required
4. Never put logic in `Component` impl blocks - components are data only, logic belongs in systems
5. Never use `Timer` without calling `.tick(time.delta())` in an update system
6. Never query `&mut Transform` and `&Transform` for overlapping archetypes in parallel systems - Bevy will panic at runtime

## Testing

- Unit test systems by constructing a minimal `App` with `app.add_systems()` and `app.update()`
- Assert component state with `app.world.query::<&Health>()` after running systems
- Test events by inserting them with `app.world.send_event()` and checking side effects
- Use `#[cfg(test)]` modules in each system file for colocated tests
- Integration tests in `tests/` directory spin up full plugin sets with mock assets
- Run `cargo clippy -- -D warnings` and `cargo test` in CI on every push

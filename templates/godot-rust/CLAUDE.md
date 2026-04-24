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

- Godot 4.3+ as the game engine
- Rust via godot-rust (gdext) for game logic
- GDScript only for rapid prototyping UI scripts and editor tools
- Cargo workspace for Rust library organization
- godot::prelude for all GDExtension bindings
- serde + ron for data-driven configuration files

## Project Structure

```
godot/
  project.godot               # Godot project configuration
  scenes/
    main.tscn                 # Root scene, autoloads
    levels/
      level_01.tscn           # Level scenes with tilemap
    ui/
      main_menu.tscn          # Main menu UI scene
      hud.tscn                # In-game HUD overlay
      pause_menu.tscn         # Pause menu popup
    entities/
      player.tscn             # Player scene (CharacterBody2D)
      enemy.tscn              # Enemy scene template
  assets/
    sprites/                  # PNG sprite assets
    audio/                    # OGG Vorbis audio files
    fonts/                    # TTF/OTF font resources
    tilesets/                 # Tileset .tres resources
  addons/                     # Godot editor plugins
rust/
  Cargo.toml                  # Workspace manifest
  src/
    lib.rs                    # GDExtension entry point, class registration
    player/
      mod.rs
      player.rs               # Player struct with #[derive(GodotClass)]
      player_state.rs         # State machine enum for player
    enemies/
      mod.rs
      enemy_base.rs           # Base enemy with shared behavior
      patrol_enemy.rs         # Patrol AI pattern
      chase_enemy.rs          # Chase and attack AI
    systems/
      mod.rs
      health.rs               # Health component, damage handling
      inventory.rs            # Item pickup and storage
      save_system.rs          # Save/load game state to file
    resources/
      mod.rs
      game_config.rs          # Custom Resource for game settings
      weapon_data.rs          # Weapon stats as Godot Resource
    autoloads/
      mod.rs
      game_manager.rs         # Global game state singleton
      audio_manager.rs        # Sound playback singleton
```

## Architecture Rules

- Every Rust struct exposed to Godot uses `#[derive(GodotClass)]` with `#[class(base=Node2D)]` or appropriate base
- Signals are declared with `#[signal]` attribute and emitted via `self.base_mut().emit_signal()`
- Node references use `#[export]` with `OnReady<Gd<Node>>` pattern; never hardcode node paths as strings
- Autoloads are registered in `project.godot`; access them via `Engine::singleton().get_singleton::<GameManager>()`
- Scene tree communication uses signals upward and method calls downward; siblings never reference each other directly
- Data-driven design: weapon stats, enemy configs, and level data live in Godot Resource files (`.tres`), not hardcoded
- Rust handles all gameplay logic; GDScript is permitted only for UI animations and editor tooling scripts

## Coding Conventions

- Rust structs: PascalCase matching the Godot node name (`Player`, `PatrolEnemy`, `HealthBar`)
- Rust functions exposed to Godot: snake_case with `#[func]` attribute
- Signals: snake_case past tense (`health_changed`, `enemy_died`, `item_collected`)
- Godot scene files: snake_case (`player.tscn`, `main_menu.tscn`)
- Use `real` type alias over `f32`/`f64` for Godot-compatible float values
- Implement `INode2D` (or appropriate `I*` trait) for virtual method overrides like `ready()` and `process()`

## Library Preferences

- godot-rust (gdext) over GDNative (gdnative) for Godot 4 projects
- Godot's built-in physics (CharacterBody2D, RigidBody2D) over custom physics
- Godot's AnimationPlayer over code-driven animation for complex sequences
- Godot's TileMap node over custom tile rendering
- ron format over json for Rust-side config files

## File Naming

- Rust source files: snake_case (`player.rs`, `health.rs`, `game_manager.rs`)
- Godot scene files: snake_case (`main_menu.tscn`, `level_01.tscn`)
- Godot resource files: snake_case (`sword_data.tres`, `goblin_config.tres`)
- Asset files: snake_case (`player_run.png`, `hit_sound.ogg`)
- GDScript files (when used): snake_case (`button_hover.gd`)

## NEVER DO THIS

1. Never use `get_node("hardcoded/path")` string paths - use `#[export]` node references with `OnReady<Gd<T>>`
2. Never call `queue_free()` on a node from within its own `process()` without deferring - emit a signal and let the parent handle removal
3. Never use `unsafe` blocks in gameplay code - the gdext bindings handle all FFI safely
4. Never mix GDScript and Rust for the same node's logic - pick one language per class
5. Never store `Gd<Node>` references long-term without checking validity - nodes can be freed externally
6. Never put game logic in `_input()` - use `_unhandled_input()` to respect UI input consumption

## Testing

- Unit test pure Rust logic (damage calculation, state machines, inventory) with `cargo test` without Godot
- Integration tests use `godot-rust`'s test harness with `#[itest]` attribute for in-engine testing
- Run `cargo clippy --workspace -- -D warnings` in CI for lint checks
- Test signal emission by connecting to signals in test scenes and asserting callback invocation
- Scene validation tests load `.tscn` files and verify required node structure exists
- Export a debug build and run automated play tests with Godot's `--headless` mode

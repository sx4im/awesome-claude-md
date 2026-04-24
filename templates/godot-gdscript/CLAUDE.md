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

- Godot 4.x (4.2+ recommended)
- GDScript (static typing enforced)
- Godot Physics (Godot Physics 3D or Jolt)
- [RENDERING: Forward+ / Mobile / Compatibility] renderer
- Version control via Git with `.godot/` in `.gitignore`

## Project Structure

```
project/
├── project.godot             # Project settings, autoloads, input map
├── scenes/
│   ├── levels/               # Level scenes (.tscn): Level1.tscn, Level2.tscn
│   ├── entities/
│   │   ├── player/           # Player scene + scripts: Player.tscn, player.gd
│   │   ├── enemies/          # Enemy scenes: Slime.tscn, slime.gd
│   │   └── pickups/          # Collectible scenes
│   ├── ui/
│   │   ├── hud/              # In-game HUD: HUD.tscn, hud.gd
│   │   ├── menus/            # Menu scenes: MainMenu.tscn, PauseMenu.tscn
│   │   └── dialogs/          # Dialog boxes, popups
│   └── components/           # Reusable scene components (hitbox, hurtbox, state machine)
├── scripts/
│   ├── autoload/             # Autoloaded singletons: GameManager.gd, AudioManager.gd
│   ├── resources/            # Custom Resource scripts: PlayerStats.gd, WeaponData.gd
│   └── classes/              # Base classes and abstract scripts
├── assets/
│   ├── sprites/              # 2D textures and sprite sheets
│   ├── models/               # 3D models (.glb, .gltf)
│   ├── audio/                # SFX (.wav) and music (.ogg)
│   └── fonts/                # Font files (.ttf, .otf)
└── addons/                   # Third-party plugins (git-ignored or vendored)
```

## Architecture Rules

- **Scenes are the building blocks.** Every game entity is a scene (`.tscn`) with an attached script. Scenes are composed into larger scenes via instantiation. A `Player.tscn` contains its sprite, collision shape, animation player, and state machine as child nodes.
- **Signals for upward communication, calls for downward.** A child node emits signals to notify its parent. A parent node calls methods on its children. Never have a child call `get_parent().do_thing()`. This creates tight coupling and breaks when the scene tree changes.
- **Autoloads are singletons for global state.** Game state, audio manager, scene transitions, and save/load systems are autoloaded scripts registered in Project Settings. Access them by name: `GameManager.score`. Never use `get_node("/root/GameManager")` — autoloads are global.
- **Custom Resources for data.** Game data (weapon stats, enemy configurations, dialog lines) is stored as custom `Resource` classes, not dictionaries or JSON. Resources are saved as `.tres` files, editable in the inspector, and type-safe.
- **State machines for complex behavior.** Player and enemy behavior uses an explicit state machine pattern: `State` base class with `enter()`, `exit()`, `update()`, `physics_update()`. Never use deeply nested `if/elif` chains for state transitions.

## Coding Conventions

- **Static typing everywhere.** Every variable, parameter, and return type has a type annotation: `var speed: float = 200.0`, `func take_damage(amount: int) -> void`. Enable "Treat warnings as errors" for untyped variables.
- **`@export` for inspector-tunable values.** All gameplay-tunable parameters (speed, damage, jump height) use `@export`. Never hardcode gameplay values in scripts. Designers should be able to tweak them in the inspector without opening code.
- **`@onready` replaces `get_node` in `_ready`.** Use `@onready var sprite: Sprite2D = $Sprite2D` instead of assigning in `_ready()`. It's cleaner and ensures the node reference exists before `_ready` body runs.
- **Group related nodes with scene composition.** A "Hitbox" is its own scene (Area2D + CollisionShape2D + hitbox.gd) instanced wherever needed. Never duplicate collision setup across entity scenes.
- **Use `StringName` for frequently compared strings.** Signal names, input actions, and animation names use `&"action_name"` syntax for `StringName` instead of `"action_name"`. StringName comparisons are pointer-fast.

## Library Preferences

- **Physics:** Godot's built-in physics for 2D. Jolt Physics extension for serious 3D physics. Not GodotPhysics 3D for production 3D games (less stable).
- **State machines:** Hand-rolled state machine pattern with a `StateMachine` node. Not a plugin unless the project is complex enough to warrant GDScript FSM addons.
- **UI framework:** Godot's built-in Control nodes and themes. Not HTML-based UI. Style with Godot themes and `StyleBoxFlat` resources.
- **Audio:** Godot's AudioStreamPlayer nodes with an AudioManager autoload for bus management. Not FMOD unless the audio design requires it.

## File Naming

- Scenes: `PascalCase.tscn` → `Player.tscn`, `MainMenu.tscn`, `Slime.tscn`
- Scripts: `snake_case.gd` matching the scene → `player.gd`, `main_menu.gd`, `slime.gd`
- Resources: `PascalCase.tres` or `snake_case.tres` matching the resource type → `SwordData.tres`
- Autoloads: `PascalCase.gd` → `GameManager.gd`, `AudioManager.gd`
- Folders: `snake_case/` → `player/`, `enemies/`, `pickups/`

## NEVER DO THIS

1. **Never use `get_node()` with long absolute paths.** `get_node("/root/Main/World/Entities/Player")` breaks when you rearrange the scene tree. Use signals, groups (`get_tree().get_nodes_in_group("player")`), or autoloads to find nodes.
2. **Never put game logic in `_process()` that belongs in `_physics_process()`.** Movement, collision response, and physics queries must use `_physics_process()` for consistent behavior regardless of framerate. `_process()` is for visuals and UI only.
3. **Never use `load()` in `_process` or `_physics_process`.** `load()` is synchronous and blocks the game thread. Preload resources with `@export` or `preload()` at the top of the script. For runtime loading, use `ResourceLoader.load_threaded_request()`.
4. **Never connect signals in code without disconnecting.** If you `connect("signal", callable)` on a node that outlives the listener, the signal fires into a freed object and crashes. Use `connect("signal", callable, CONNECT_ONE_SHOT)` for one-time signals, or disconnect in `_exit_tree()`.
5. **Never store node references across scene changes.** When a scene is freed, all node references become invalid. Store data (not nodes) in autoloads. Reconstruct node references after scene transitions.
6. **Never use untyped dictionaries for game data.** `var weapon = {"damage": 10, "speed": 1.5}` has no autocomplete, no validation, and typos in keys fail silently. Use custom Resource classes with typed properties.
7. **Never commit the `.godot/` folder.** It contains imported asset cache, editor layouts, and shader cache. It is machine-specific and regenerated automatically. Add `.godot/` to `.gitignore`.

## Testing

- Use GUT (Godot Unit Test) addon for GDScript unit tests. Test scripts go in `test/` with filenames prefixed `test_`.
- Test game logic (damage calculation, state transitions, inventory management) in isolation without scene tree dependencies.
- For integration tests, create minimal test scenes that instantiate the entity and verify behavior over simulated frames with `await get_tree().physics_frame`.
- Test custom Resources by creating instances in code and verifying property defaults and serialization.
- Playtest frequently. Automated tests cannot catch feel, timing, and game design issues. Build a debug overlay (F3 key) showing FPS, physics state, and current game state.

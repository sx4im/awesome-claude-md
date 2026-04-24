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

- Unity 2022.3+ LTS (or latest LTS)
- C# 11 (via Unity's .NET profile)
- Universal Render Pipeline (URP) or HDRP
- Unity Input System (new, not legacy)
- Addressable Asset System for content loading
- Unity Test Framework for testing

## Project Structure

```
Assets/
├── _Project/                # All project-specific assets (prefix avoids conflicts with packages)
│   ├── Scripts/
│   │   ├── Runtime/
│   │   │   ├── Core/        # Game manager, state machine, event system
│   │   │   ├── Player/      # Player controller, abilities, stats
│   │   │   ├── AI/          # Enemy behavior, pathfinding, state trees
│   │   │   ├── UI/          # HUD, menus, dialogs
│   │   │   └── Systems/     # Inventory, save/load, audio, pooling
│   │   └── Editor/          # Custom editor tools and inspectors
│   ├── Prefabs/             # Organized by category (Characters/, UI/, Environment/)
│   ├── Scenes/
│   │   ├── Persistent/      # Bootstrap scene (always loaded)
│   │   ├── Levels/          # Gameplay scenes
│   │   └── UI/              # Additive UI scenes
│   ├── Art/                 # Models, textures, materials, animations
│   ├── Audio/               # SFX and music
│   └── Resources/           # Only assets loaded via Resources.Load (minimize this)
├── Packages/                # Unity Package Manager packages
└── ProjectSettings/
```

## Architecture Rules

- **ScriptableObject for data.** Game settings, enemy stats, item databases, dialogue trees. all ScriptableObjects. Never hardcode values in MonoBehaviours. SOs are assets you can tweak in the Inspector without touching code.
- **Event-driven communication.** Use ScriptableObject-based events or C# events for cross-system communication. `PlayerHealth` fires `OnDeath` event. `GameManager` listens. Never use `FindObjectOfType<T>()` to get references at runtime.
- **Composition over inheritance.** Split behavior into small, focused components. A player has `PlayerMovement`, `PlayerCombat`, `PlayerInventory`. not one giant `PlayerController` MonoBehaviour. Require components via `[RequireComponent]`.
- **Object pooling for frequently spawned objects.** Bullets, particles, enemies. pool them. Never `Instantiate`/`Destroy` every frame. Use Unity's built-in ObjectPool<T> or a custom pool manager.
- **One bootstrap scene pattern.** A persistent scene loads first and initializes singletons (AudioManager, GameManager, EventSystem). Gameplay scenes load additively. Never rely on one specific scene being loaded first.

## Coding Conventions

- **Naming:** PascalCase for public fields and methods. `_camelCase` with underscore prefix for private fields. `[SerializeField] private float _moveSpeed`. never public fields for Inspector exposure.
- **`[SerializeField]` instead of public fields.** Expose fields to the Inspector with `[SerializeField] private`. not `public`. Public fields pollute the API and can be changed from any script.
- **Null checks with `TryGetComponent`.** `if (TryGetComponent<Rigidbody>(out var rb))`. not `GetComponent<Rigidbody>()` followed by a null check. `TryGetComponent` doesn't allocate garbage on failure.
- **Assembly definitions.** Create `.asmdef` files for each major folder: `Core.asmdef`, `Player.asmdef`, `UI.asmdef`. This enables incremental compilation (only changed assemblies recompile) and enforces dependency boundaries.
- **Coroutines for timed sequences only.** Use coroutines for visual sequences (fade in, wait, fade out). For game logic timing, use state machines or a tick-based system. Never use coroutines as a general-purpose async pattern.

## Library Preferences

- **Input:** New Input System. not `Input.GetKey()` (legacy, no rebinding, no device management). Define Input Actions assets with action maps per context (Gameplay, UI, Menu).
- **DI:** VContainer or Zenject. only for large projects with complex dependency graphs. Small projects don't need DI frameworks. manual wiring is fine.
- **Serialization:** Unity's JsonUtility for simple data. Newtonsoft JSON (via Unity package) for complex types. Not `System.Text.Json` (compatibility issues).
- **Tweening:** DOTween. not LeanTween (less maintained). Use DOTween for UI animations, camera shakes, and VFX timing.
- **Networking:** Netcode for GameObjects (Unity's official solution) or Mirror for community-maintained networking.

## NEVER DO THIS

1. **Never use `Find`, `FindObjectOfType`, or `FindWithTag` at runtime.** They search the entire hierarchy every call. Cache references in `Awake()` or inject via the Inspector. These methods are performance killers in the game loop.
2. **Never use `Resources.Load` for most assets.** The `Resources/` folder is loaded into memory at startup and can't be unloaded granularly. Use Addressables for dynamic asset loading. `Resources/` only for bootstrap-critical assets.
3. **Never allocate in `Update()`.** No `new List<T>()`, no string concatenation, no LINQ queries in `Update`, `FixedUpdate`, or `LateUpdate`. Allocations trigger garbage collection which causes frame spikes.
4. **Never use public fields for Inspector-exposed values.** Use `[SerializeField] private`. Public fields are accessible from any script and break encapsulation.
5. **Never hardcode magic numbers.** `if (health < 0)`. what's 0? Use `const float MIN_HEALTH = 0f` or a ScriptableObject setting. Magic numbers make balancing impossible.
6. **Never commit generated files.** `Library/`, `Temp/`, `obj/`, and `*.csproj` files are generated by Unity. Only commit `Assets/`, `Packages/`, and `ProjectSettings/`. Set `.gitignore` correctly.
7. **Never use `DontDestroyOnLoad` freely.** It creates objects that live forever and accumulate across scene loads. Use it only for the bootstrap scene's manager objects. Everything else should be scene-scoped.

## Testing

- Use Unity Test Framework with Edit Mode tests for pure logic (no MonoBehaviour dependency).
- Play Mode tests for integration testing with actual GameObjects and components.
- Test ScriptableObject data validation. verify all stats are in valid ranges.
- Playtest builds on target platform. editor behavior differs from builds (timing, input, rendering).

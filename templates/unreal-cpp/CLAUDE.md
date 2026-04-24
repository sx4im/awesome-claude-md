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

- Unreal Engine 5.x (specify version)
- C++ (C++17, UE coding standard)
- Blueprints for designer-facing logic and prototyping
- Unreal Build System (UBT) and Unreal Header Tool (UHT)
- {module-name} primary game module

## Project Structure

```
Source/{ModuleName}/
├── {ModuleName}.Build.cs        # Module build rules, dependencies
├── {ModuleName}GameMode.h/cpp   # Game mode: rules, spawning, match state
├── Characters/
│   ├── {Project}Character.h/cpp  # Player character: movement, input, camera
│   └── BaseEnemy.h/cpp           # Enemy base class
├── Components/
│   ├── HealthComponent.h/cpp     # Reusable actor component: health, damage
│   ├── InventoryComponent.h/cpp  # Inventory management component
│   └── InteractionComponent.h/cpp
├── Actors/
│   ├── Projectile.h/cpp          # Projectile actor
│   └── Pickup.h/cpp              # Pickup base class
├── GameFramework/
│   ├── {Project}GameInstance.h/cpp    # Persistent state across maps
│   ├── {Project}GameState.h/cpp      # Replicated match state
│   └── {Project}PlayerState.h/cpp    # Per-player replicated state
├── UI/
│   ├── {Project}HUD.h/cpp        # HUD manager
│   └── Widgets/                  # UMG widget C++ bases
├── Data/
│   ├── ItemDataAsset.h/cpp       # UDataAsset / UPrimaryDataAsset definitions
│   └── GameTypes.h               # Shared enums, structs, gameplay tags
└── Subsystems/
    └── {System}Subsystem.h/cpp   # UGameInstanceSubsystem / UWorldSubsystem
Content/
├── Blueprints/                   # Blueprint assets extending C++ classes
├── Maps/                         # Level .umap files
├── UI/                           # Widget Blueprints
└── Data/                         # Data assets, data tables, curves
```

## Architecture Rules

- **C++ for systems, Blueprints for content.** Base classes, components, subsystems, and core gameplay mechanics are written in C++. Blueprints extend C++ classes to add content-specific behavior (animations, VFX, specific AI trees). Never write core game systems in pure Blueprint.
- **The gameplay framework hierarchy matters.** `GameMode` (server authority) → `GameState` (replicated match state) → `PlayerState` (per-player replicated) → `PlayerController` (input, UI) → `Pawn/Character` (physical representation). Never put match rules in the Character or input handling in the GameMode.
- **Components over inheritance.** Favor `UActorComponent` and `USceneComponent` for reusable behavior (health, inventory, interaction) over deep class hierarchies. An actor's behavior is defined by its component composition, not its class lineage.
- **UObject system rules apply to all allocations.** Never use `new` for UObject-derived classes; use `NewObject<T>()` or `CreateDefaultSubobject<T>()`. Never use `delete`; the garbage collector manages UObject lifetimes. Raw `new`/`delete` is only for non-UObject types.
- **Properties exposed with `UPROPERTY`, functions with `UFUNCTION`.** The reflection system requires these macros. Without `UPROPERTY()`, a member is invisible to GC (dangling pointer risk), Blueprints, serialization, and replication.

## Coding Conventions

- **Follow Unreal's naming conventions.** Classes: `A` prefix for Actors, `U` for UObjects/Components, `F` for structs, `E` for enums, `I` for interfaces, `T` for templates. Boolean variables: `bIsAlive`, `bCanJump`. This is non-negotiable; the entire engine assumes these prefixes.
- **UPROPERTY specifiers control visibility.** `EditAnywhere` = editable in editor, `BlueprintReadWrite` = accessible in BP, `Replicated` = networked. Use `Category = "Combat|Damage"` for inspector organization. Never leave UPROPERTY without a category on public members.
- **UFUNCTION specifiers for Blueprint exposure.** `BlueprintCallable` = BP can call it. `BlueprintImplementableEvent` = BP overrides it (no C++ body). `BlueprintNativeEvent` = BP can override but C++ provides default via `_Implementation()`. Use `BlueprintPure` for const getters.
- **Use `TObjectPtr<T>` for UPROPERTY pointers (UE 5.x).** Not raw `T*` in UPROPERTY declarations. `TObjectPtr` provides access tracking and lazy loading. Raw pointers are acceptable for local/stack variables.
- **Gameplay Tags over enums for extensible categories.** For damage types, ability categories, and state flags, use `FGameplayTag` and `FGameplayTagContainer`. Enums require recompilation to add values; tags are data-driven.

## Library Preferences

- **Input:** Enhanced Input System (`UInputAction`, `UInputMappingContext`). Not the legacy input system. Enhanced Input is the UE5 standard.
- **AI:** Behavior Trees + Environment Query System for AI. Not custom state machines unless the AI is trivially simple.
- **UI:** UMG (Unreal Motion Graphics) with C++ base widgets and Blueprint widget extensions. Not Slate directly for game UI (Slate is for editor tools).
- **Networking:** Unreal's built-in replication (`DOREPLIFETIME`, RPCs). Not custom socket code. The framework handles relevancy, dormancy, and bandwidth.
- **Data:** `UDataAsset` and `UDataTable` for game data. Not JSON files loaded at runtime (loses editor tooling and type safety).

## File Naming

- Headers and source: `PascalCase.h` / `PascalCase.cpp` → `HealthComponent.h`, `BaseEnemy.cpp`
- One class per file. The filename matches the class name without the prefix: `AProjectileActor` → `ProjectileActor.h`
- Blueprint assets: `BP_PascalCase` → `BP_PlayerCharacter`, `BP_Slime`
- Widget Blueprints: `WBP_PascalCase` → `WBP_HealthBar`, `WBP_MainMenu`
- Data assets: `DA_PascalCase` → `DA_SwordItem`, `DA_EnemyConfig`

## NEVER DO THIS

1. **Never use `new`/`delete` on UObject-derived types.** The garbage collector manages UObject memory. Use `NewObject<T>()`, `CreateDefaultSubobject<T>()`, or `SpawnActor<T>()`. Manual `delete` on a UObject corrupts the GC and crashes.
2. **Never store `UObject*` without `UPROPERTY()`.** An undecorated pointer is invisible to the garbage collector. The GC will free the object, leaving a dangling pointer. Every `UObject*` member must be a `UPROPERTY()`.
3. **Never access the world in a constructor.** Constructors (`CDO` creation) run before any world exists. `GetWorld()` returns `nullptr` in constructors. Use `BeginPlay()` for world-dependent initialization.
4. **Never use `FString` comparisons for gameplay logic.** String comparisons are slow and error-prone. Use `FGameplayTag`, `FName`, or enums for type identification. String-based type checking (`if (Name == "Sword")`) is a code smell.
5. **Never tick every actor every frame.** Disable `PrimaryActorTick` by default. Enable ticking only on actors that genuinely need per-frame updates. Use timers (`GetWorldTimerManager().SetTimer()`) for periodic logic.
6. **Never ignore `const` correctness.** Getter functions must be `const`. Mark UFUNCTION getters as `BlueprintPure`. The engine's type system relies on `const` for optimization and thread safety.
7. **Never put gameplay code in the constructor.** The constructor initializes the CDO (Class Default Object), which is a template. Logic in the constructor runs once during class registration, not per-instance. Use `BeginPlay()` for instance initialization.

## Testing

- Use Unreal's Automation Framework (`FAutomationTestBase`) for C++ unit and integration tests. Place test files in a `Tests/` directory within the module.
- Test gameplay logic by spawning actors in a test world: `UWorld* TestWorld = FAutomationEditorCommonUtils::CreateNewMap()`.
- Use `IMPLEMENT_SIMPLE_AUTOMATION_TEST` for simple tests, `IMPLEMENT_CUSTOM_COMPLEX_AUTOMATION_TEST` for parameterized tests.
- Test components in isolation by creating a minimal actor, attaching the component, and calling methods directly.
- Run tests via the Session Frontend (`Window → Developer Tools → Session Frontend → Automation`) or command line with `-ExecCmds="Automation RunTests {filter}"`.

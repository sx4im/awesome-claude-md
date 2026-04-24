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

- WebGPU API for GPU-accelerated rendering and compute
- WGSL (WebGPU Shading Language) for all shader programs
- TypeScript 5.x with strict mode for host application code
- Vite 5.x for development server and bundling
- wgpu-matrix for CPU-side matrix and vector math
- dat.gui or lil-gui for runtime parameter tweaking
- Tint or Naga for offline WGSL validation (CI)

## Project Structure

```
src/
  main.ts                      # Entry point, adapter/device request
  renderer/
    Renderer.ts                # Core render loop, swap chain management
    RenderPipeline.ts          # Render pipeline factory and cache
    ComputePipeline.ts         # Compute pipeline factory and dispatch
    PassEncoder.ts             # Render/compute pass helper
  resources/
    BufferManager.ts           # GPU buffer creation, mapping, upload
    TextureManager.ts          # Texture loading, sampling, mipmaps
    BindGroupManager.ts        # Bind group layout and creation
    UniformManager.ts          # Uniform buffer ring-buffering
  shaders/
    vertex/
      basic.vert.wgsl          # Standard vertex transform
      skinned.vert.wgsl        # Skeletal animation vertex shader
      fullscreen.vert.wgsl     # Full-screen triangle (no vertex buffer)
    fragment/
      pbr.frag.wgsl            # PBR material fragment shader
      unlit.frag.wgsl          # Unlit texture-only fragment shader
      postprocess.frag.wgsl    # Tone mapping, gamma correction
    compute/
      particles.comp.wgsl      # GPU particle simulation
      culling.comp.wgsl        # Frustum culling compute shader
      blur.comp.wgsl           # Gaussian blur compute pass
    common/
      types.wgsl               # Shared struct definitions
      lighting.wgsl             # Light calculation functions
      noise.wgsl               # Noise generation functions
  scene/
    Camera.ts                  # Perspective/orthographic camera, controls
    Transform.ts               # Model matrix, hierarchy
    Mesh.ts                    # Vertex/index buffer geometry
    Material.ts                # Material properties, bind group
    SceneGraph.ts              # Scene tree traversal and rendering
  utils/
    math.ts                    # glMatrix wrappers, frustum math
    debug.ts                   # GPU timestamp queries, stats overlay
    loader.ts                  # OBJ/GLTF geometry loading
public/
  assets/
    models/                    # OBJ/GLTF geometry files
    textures/                  # PNG/KTX2 texture files
    hdri/                      # HDR environment maps
```

## Architecture Rules

- Request GPU adapter and device once at startup; pass `GPUDevice` to all managers via constructor injection
- Never create GPU resources in the render loop; all pipelines, buffers, and textures are created during initialization or explicit load phases
- Use a ring buffer (double or triple) for uniform buffers to avoid GPU/CPU synchronization stalls
- Bind group layouts are defined once per pipeline and reused; use `@group(0)` for per-frame data, `@group(1)` for per-material, `@group(2)` for per-object
- Compute passes execute before render passes in the command encoder; never mix compute and render in the same pass
- All shader source files are loaded as raw strings via Vite's `?raw` import suffix
- Prefer storage buffers over uniform buffers for large data sets (over 64KB) like instance transforms or particle data

## Coding Conventions

- WGSL files use `.vert.wgsl`, `.frag.wgsl`, `.comp.wgsl` suffixes matching their stage
- WGSL struct names: PascalCase (`VertexOutput`, `CameraUniforms`, `ParticleData`)
- WGSL function names: snake_case (`calculate_lighting`, `apply_fog`, `hash_position`)
- WGSL binding annotations always explicit: `@group(0) @binding(0) var<uniform> camera: CameraUniforms;`
- TypeScript classes managing GPU resources implement `destroy()` for cleanup
- Buffer sizes always align to 16 bytes using `Math.ceil(size / 16) * 16`
- Use `label` property on every GPU object for WebGPU error message debugging

## Library Preferences

- wgpu-matrix over gl-matrix for matrix math (designed for WebGPU's column-major layout)
- KTX2 with Basis Universal over raw PNG for compressed GPU textures
- Native WebGPU timestamp queries over `performance.now()` for GPU profiling
- Raw WGSL strings over shader generator libraries for transparency and debuggability
- lil-gui over dat.gui for parameter controls (smaller, maintained, TypeScript types)

## File Naming

- WGSL shaders: snake_case with stage suffix (`pbr.frag.wgsl`, `particles.comp.wgsl`)
- TypeScript classes: PascalCase (`Renderer.ts`, `BufferManager.ts`, `Camera.ts`)
- Utility files: camelCase (`math.ts`, `debug.ts`, `loader.ts`)
- Texture files: kebab-case (`stone-wall-albedo.png`, `sky-hdri.hdr`)

## NEVER DO THIS

1. Never call `buffer.mapAsync()` on a buffer currently in use by a submitted command - use ring buffering or wait for `onSubmittedWorkDone()`
2. Never create pipelines inside the render loop - pipeline compilation is expensive; cache and reuse all pipelines
3. Never use `navigator.gpu` without checking for `undefined` first - WebGPU is not available in all browsers
4. Never exceed device limits (`maxUniformBufferBindingSize`, `maxStorageBufferBindingSize`) without querying `device.limits`
5. Never forget to call `pass.end()` before `encoder.finish()` - open passes cause validation errors and silent failures
6. Never mix binding indices between shader and TypeScript - always verify `@group/@binding` matches `GPUBindGroupLayoutEntry`
7. Never use `writeBuffer` with unaligned data - all offsets and sizes must be multiples of 4 bytes

## Testing

- Unit test math utilities (matrix ops, frustum planes, AABB) with Vitest
- Validate WGSL shaders offline using Tint CLI (`tint --validate shader.wgsl`) in CI
- Integration tests use `navigator.gpu` with `requestAdapter({ powerPreference: 'low-power' })` in headless Chrome
- GPU buffer read-back tests map staging buffers and assert compute shader output values
- Visual regression tests render reference scenes and compare pixel output with tolerance thresholds
- Monitor `device.lost` promise in tests to detect GPU crashes and resource exhaustion

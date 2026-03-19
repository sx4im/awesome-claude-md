# [PROJECT NAME] — [ONE LINE DESCRIPTION]

## Tech Stack

- React 18 with TypeScript
- Three.js via React Three Fiber (R3F)
- Drei (R3F utility library)
- React Three Rapier (physics) or Cannon
- GSAP or Framer Motion for UI animations
- Vite for bundling

## Project Structure

```
src/
├── components/
│   ├── canvas/              # 3D scene components (inside <Canvas>)
│   │   ├── Scene.tsx        # Root 3D scene setup
│   │   ├── Player.tsx       # Player mesh, controls, animations
│   │   ├── Environment.tsx  # Lights, sky, fog, post-processing
│   │   └── models/          # GLTF/GLB model components
│   │       └── Robot.tsx    # Generated via gltfjsx
│   ├── ui/                  # HTML overlay UI (outside <Canvas>)
│   │   ├── HUD.tsx          # Heads-up display
│   │   └── LoadingScreen.tsx
│   └── shared/              # Shared between 3D and UI
├── hooks/
│   ├── useGameState.ts      # Zustand store for 3D state
│   └── useKeyboard.ts      # Input management
├── lib/
│   ├── materials.ts         # Reusable Three.js materials
│   ├── geometries.ts        # Reusable geometries
│   └── shaders/             # Custom GLSL shaders
│       ├── water.vert
│       └── water.frag
├── assets/                  # Static 3D models, textures, HDRIs
├── App.tsx                  # Canvas + UI composition
└── main.tsx
```

## Architecture Rules

- **Everything inside `<Canvas>` is R3F components.** 3D objects, lights, cameras, and controls are declarative React components inside `<Canvas>`. Never use raw `THREE.Scene`, `THREE.Mesh`, or imperative Three.js inside a Canvas component.
- **UI lives outside `<Canvas>`.** HUD, menus, and HTML overlays are regular React components positioned over the canvas with CSS. Never use `<Html>` from Drei for primary UI — it's for in-world labels only.
- **State management with Zustand.** R3F components access shared state (score, player health, game phase) via Zustand. Not React Context — context re-renders the entire scene tree. Zustand's selectors ensure only affected meshes re-render.
- **Models use gltfjsx.** Convert `.glb` files to React components with `npx gltfjsx model.glb --typescript`. The generated component is a proper R3F node with typed props. Never load models imperatively with `GLTFLoader` in effects.
- **`useFrame` is the render loop.** All per-frame updates (movement, rotation, animation) go in `useFrame`. One `useFrame` per component that needs frame updates. Never use `requestAnimationFrame` directly.

## Coding Conventions

- **Component refs use `useRef<THREE.Mesh>` or specific types.** `const meshRef = useRef<THREE.Mesh>(null!)`. Use the specific Three.js type, not a generic `any`. The `null!` assertion avoids null checks when you know the ref will be assigned.
- **Drei utilities over raw Three.js.** `<OrbitControls>`, `<Environment>`, `<useGLTF>`, `<Text>`, `<Float>` from `@react-three/drei` — they're R3F-native wrappers that handle lifecycle correctly.
- **Materials are shared instances.** Define materials in `lib/materials.ts` and pass them as props. Never create `new THREE.MeshStandardMaterial()` inside a component — it creates a new GPU resource on every render.
- **Dispose resources on unmount.** Geometries, materials, and textures consume GPU memory. Use `useEffect` cleanup or R3F's automatic disposal. Watch for memory leaks in dynamic scenes.
- **Performance:** disable auto-clear and use `frameloop="demand"` for static scenes. Use `<Instances>` or `<InstancedMesh>` for repeated objects (trees, particles). Never render 1000 identical meshes as separate components.

## Library Preferences

- **3D framework:** React Three Fiber — not raw Three.js (R3F gives you React lifecycle, declarative scene graph, and automatic disposal). Not Babylon.js (smaller React ecosystem).
- **Helpers:** Drei — camera controls, environment maps, text, loaders, performance monitors. Don't rebuild what Drei provides.
- **Physics:** Rapier (via `@react-three/rapier`) — fast, deterministic, WASM-based. Not Cannon (slower, less actively maintained).
- **Post-processing:** `@react-three/postprocessing` — Bloom, SSAO, vignette as R3F components. Not raw EffectComposer.
- **Animation:** `useFrame` for 3D. GSAP or Framer Motion for HTML UI animations. Not animating DOM and 3D with the same library.

## NEVER DO THIS

1. **Never use `new THREE.Mesh()` inside R3F components.** Use `<mesh>`, `<boxGeometry>`, `<meshStandardMaterial>` JSX elements. Imperative Three.js inside R3F bypasses React's lifecycle and causes memory leaks.
2. **Never trigger re-renders for 60fps updates.** Use `useFrame` and mutate refs directly: `meshRef.current.rotation.y += 0.01`. Calling `setState` 60 times per second kills performance.
3. **Never create materials or geometries inline in JSX without memoization.** `<meshStandardMaterial color="red" />` is fine (R3F handles this). But `material={new THREE.ShaderMaterial(...)}` creates a new instance every render.
4. **Never use React Context for game state in 3D scenes.** Context changes re-render everything. Use Zustand with selectors: `useGameStore(s => s.score)` — only components subscribing to `score` re-render.
5. **Never skip the loading phase.** Use `<Suspense fallback={<LoadingScreen />}>` around your scene. Models and textures are async — without Suspense, you get a blank canvas until everything downloads.
6. **Never use `position={[x, y, z]}` with variables that change every frame.** Create a `Vector3` ref and mutate it in `useFrame`. Array literals in props create new arrays every render.
7. **Never forget to dispose of dynamically created resources.** If you create textures, render targets, or geometries dynamically, dispose them on unmount. GPU memory doesn't get garbage collected automatically.

## Testing

- Visual regression tests with Storybook + Chromatic for 3D components (render to canvas, screenshot, compare).
- Unit test hooks and state stores with Vitest.
- Performance testing: monitor draw calls, triangle count, and memory with `<Stats />` from Drei and Chrome DevTools performance tab.
- Test on target devices (mobile GPUs are 10-50x weaker than desktop).

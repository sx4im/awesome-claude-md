# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Framer Motion v11 (React animation library)
- React 18+
- TypeScript 5.x
- Next.js 15+ or Vite

## Project Structure

```
src/
├── components/
│   ├── animations/             # Reusable animation components
│   │   ├── FadeIn.tsx
│   │   ├── SlideIn.tsx
│   │   └── StaggerContainer.tsx
│   └── features/
│       └── AnimatedCard.tsx
├── hooks/
│   └── useScrollAnimation.ts   # Custom scroll-based animations
├── lib/
│   └── animations.ts           # Shared animation variants
└── ...
```

## Architecture Rules

- **Motion components for animations.** Use `motion.div`, `motion.button` instead of regular elements for animation capabilities.
- **Variants for complex sequences.** Define animation states (hidden, visible, exit) in variant objects. Animate between them.
- **Layout animations for shared element transitions.** Use `layoutId` for smooth morphing between component states.
- **AnimatePresence for exit animations.** Wrap elements that mount/unmount with `AnimatePresence` for exit animations.

## Coding Conventions

- Import motion: `import { motion, AnimatePresence } from 'framer-motion'`.
- Define variants as const objects: `const variants = { hidden: { opacity: 0 }, visible: { opacity: 1 } }`.
- Use `initial`, `animate`, `exit` props with variant names.
- Use `transition` prop for timing: `transition={{ duration: 0.3, ease: "easeOut" }}`.
- For gestures: `whileHover`, `whileTap`, `whileDrag`, `whileFocus`.

## Library Preferences

- **Page transitions:** Use `AnimatePresence` + `motion.div` in layout files.
- **Scroll animations:** `useScroll` and `useTransform` hooks for scroll-linked effects.
- **Drag:** Built-in drag with `drag`, `dragConstraints`, `dragElastic` props.
- **Spring physics:** Use `type: "spring"` for natural-feeling animations.
- **Reduced motion:** Framer Motion respects `prefers-reduced-motion` automatically.

## File Naming

- Animation components: PascalCase with animation intent → `FadeIn.tsx`, `SlideUp.tsx`
- Variant files: `animations.ts`, `transitions.ts`
- Custom hooks: `use[Feature]Animation.ts`

## NEVER DO THIS

1. **Never animate expensive properties.** Avoid animating `width`, `height`, `top`, `left` (triggers layout). Use `transform` and `opacity`.
2. **Never create motion components inside render.** `const MotionDiv = motion.div` should be outside the component.
3. **Never forget `AnimatePresence` for exit animations.** Without it, unmounting elements disappear instantly.
4. **Never use `layoutId` on unrelated elements.** Elements with the same `layoutId` must share visual similarity.
5. **Never animate without transition configuration.** Default transitions may not match your design system.
6. **Never ignore performance in lists.** Use `layout` prop sparingly in large lists. It can be expensive.
7. **Never block the main thread with complex animations.** Use `useReducedMotion` to disable heavy effects for users who need it.

## Testing

- Test animations with React Testing Library by checking element presence after transitions.
- Use `waitFor` for async animation completion.
- Test reduced motion scenarios.
- Visual regression with Chromatic (animations can be paused for snapshots).


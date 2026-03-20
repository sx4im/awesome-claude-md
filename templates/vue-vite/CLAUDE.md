# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Vue 3 with TypeScript (strict mode)
- Vite 5.x as build tool and dev server
- Composition API exclusively (no Options API)
- Pinia for state management
- Vue Router 4.x for routing
- Tailwind CSS 3.x

## Project Structure

```
src/
├── components/
│   ├── ui/               # Primitives: VButton, VInput, VModal, VTooltip
│   └── features/         # Domain components: UserCard, OrderSummary
├── composables/           # Composable functions (useAuth, useDebounce, usePagination)
├── views/                 # Route-level components, one per route
├── stores/                # Pinia stores, one file per store
├── services/              # API call functions (never call fetch in components)
├── types/                 # Shared TypeScript interfaces and types
├── utils/                 # Pure utility functions (formatDate, cn, etc.)
├── router/                # Router config and route guards
│   └── index.ts
├── assets/                # Static assets processed by Vite
└── App.vue                # Root component with <RouterView />
```

## Architecture Rules

- **Composition API only.** No `data()`, `methods`, `computed`, or `watch` from Options API. Use `ref()`, `computed()`, `watch()`, and composable functions exclusively. Every component uses `<script setup lang="ts">`.
- **State management decision tree:**
  - UI-only state (open/closed, form input) → `ref()` or `reactive()` inside the component
  - Server state (data from APIs) → VueQuery (`@tanstack/vue-query`) or composables wrapping API calls
  - Cross-component client state (auth, cart, preferences) → Pinia store
  - URL state (filters, pagination, search) → Vue Router query params
- **API calls go in `services/`.** Never call `fetch` directly in a component or composable. Each service file maps to a backend domain: `services/users.ts`, `services/orders.ts`. These return typed data, never raw `Response` objects.
- **Composables extract reusable reactive logic.** A composable is a function prefixed with `use` that encapsulates reactive state and side effects. It returns refs and functions, not raw values.

## Coding Conventions

- All components use `<script setup lang="ts">`. No `defineComponent()` wrapper. No `export default`. The `<script setup>` syntax is the component definition.
- Props use `defineProps<{ title: string; count: number }>()` with TypeScript generics. Not the runtime `defineProps({ title: String })` form. TypeScript generics give full type safety.
- Emits use `defineEmits<{ (e: 'update', id: string): void }>()`. Always typed, never the array shorthand `defineEmits(['update'])`.
- Use `ref()` for primitives and `reactive()` for objects. Never wrap a reactive object in ref. Never use `reactive()` for a single value.
- Template refs use `const inputRef = useTemplateRef<HTMLInputElement>('input')`. Not the old `ref="input"` + `this.$refs` pattern.
- Import order: Vue core → external packages → `@/` aliased imports → relative imports → type-only imports.
- Use the `@/` path alias mapped to `src/`. Configured in `vite.config.ts` and `tsconfig.json`. Never use `../../../` chains.

## Library Preferences

- **State management:** Pinia. not Vuex (deprecated patterns, mutation boilerplate). Pinia stores use `defineStore` with the setup syntax (function form), not the options form.
- **Data fetching:** `@tanstack/vue-query` for complex caching needs. For simple cases, composables wrapping services are fine.
- **Styling:** Tailwind CSS with `clsx` + `tailwind-merge` wrapped in a `cn()` utility. Not scoped CSS for layout. Scoped `<style>` blocks only for animations or truly component-specific overrides.
- **Forms:** VeeValidate 4 with Zod schemas. Not the old VeeValidate 3 class-based API. Use `useForm()` and `useField()` composables.
- **Dates:** `date-fns`. not `moment` (deprecated, not tree-shakeable).
- **HTTP client:** `ky` or plain `fetch` with a typed wrapper in services. Not `axios`.

## File Naming

- Components: `PascalCase.vue` → `UserCard.vue`, `OrderSummary.vue`
- Composables: `useCamelCase.ts` → `useAuth.ts`, `useDebounce.ts`
- Stores: `camelCase.ts` → `auth.ts`, `cart.ts` (inside `stores/`)
- Services: `camelCase.ts` → `users.ts`, `orders.ts`
- Views: `PascalCase.vue` → `HomePage.vue`, `UserProfile.vue`
- Utils: `camelCase.ts` → `formatDate.ts`, `cn.ts`
- Test files: co-located as `ComponentName.test.ts`

## NEVER DO THIS

1. **Never use Options API.** No `data()`, `methods`, `computed`, `watch`, `mounted()`. Use `<script setup>` with Composition API exclusively. Options API components will not pass code review.
2. **Never use `ref()` and then access `.value` in templates.** Vue auto-unwraps refs in templates. Writing `{{ count.value }}` in a template is a bug. Write `{{ count }}`. The `.value` is only needed in `<script>`.
3. **Never use `reactive()` on primitives.** `reactive('hello')` silently fails. Use `ref()` for strings, numbers, booleans. Use `reactive()` only for objects you want deep reactivity on.
4. **Never mutate props.** `props.items.push(newItem)` mutates the parent's data and causes untraceable bugs. Emit an event: `emit('add-item', newItem)`. The parent owns the data.
5. **Never register components manually in `<script setup>`.** Imported components are automatically available in the template. There is no `components: { MyComponent }` registration step with `<script setup>`.
6. **Never use `this` in `<script setup>`.** There is no component instance. `this` is `undefined`. Access the router with `useRouter()`, the route with `useRoute()`, the store with `useMyStore()`.
7. **Never use `v-if` and `v-for` on the same element.** `v-if` has higher priority than `v-for` in Vue 3 (reversed from Vue 2). Wrap the list in a `<template v-for>` and put `v-if` on the child element, or filter the list in a `computed`.

## Testing

- Use Vitest + Vue Test Utils. Tests live next to the component: `UserCard.test.ts` alongside `UserCard.vue`.
- Mount components with `mount()` from `@vue/test-utils`. Use `shallowMount()` only when you explicitly need to stub child components.
- Test behavior, not implementation: trigger events with `wrapper.find('button').trigger('click')`, assert on rendered output with `wrapper.text()` and `wrapper.html()`.
- Mock Pinia stores with `createTestingPinia()` from `@pinia/testing`. Never mock the store module directly.
- Test composables by wrapping them in a host component or using `withSetup` test helper.

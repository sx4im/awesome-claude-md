# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Storybook 8 with React 18 framework integration
- Component Story Format 3 (CSF3) with TypeScript
- Vite 5 as the Storybook builder (@storybook/builder-vite)
- Chromatic for visual regression testing and review
- Storybook Test with @storybook/test (Vitest-compatible expect, fn, userEvent)
- Tailwind CSS 4 for component styling
- @storybook/addon-a11y for accessibility audits
- MSW 2 (Mock Service Worker) for API mocking in stories

## Project Structure

```
src/
  components/
    atoms/              # Basic UI elements (Button, Input, Badge)
      Button/
        Button.tsx
        Button.stories.tsx
        Button.test.tsx
        index.ts
    molecules/          # Composed components (SearchBar, Card)
    organisms/          # Complex sections (Header, DataTable)
    templates/          # Page-level layouts
  hooks/                # Shared React hooks
  lib/                  # Utility functions
  types/                # Shared TypeScript types
.storybook/
  main.ts              # Storybook configuration
  preview.ts           # Global decorators, parameters, loaders
  manager.ts           # Storybook UI customization
  test-runner.ts       # Test runner configuration
```

## Architecture Rules

- Every component directory contains the component file, its stories file, an optional test file, and a barrel `index.ts`.
- Stories use CSF3 object syntax exclusively. Each story is an exported object with `args`, never a function returning JSX.
- The default export (`meta`) must include `component`, `title`, and `argTypes` with controls for every prop.
- Use `play` functions for interaction tests directly in stories using `@storybook/test` utilities.
- Global decorators in `preview.ts` wrap all stories with ThemeProvider, router context, and Tailwind base styles.
- MSW handlers are defined per-story using the `msw` parameter for stories that need API data.
- Component hierarchy follows Atomic Design: atoms, molecules, organisms, templates.

## Coding Conventions

- Stories files are co-located with components: `ComponentName.stories.tsx`.
- Story names use PascalCase: `Primary`, `WithIcon`, `Loading`, `ErrorState`.
- Every component must have a `Default` story showing baseline props, plus stories for each major visual state.
- Use `satisfies Meta<typeof Component>` for type-safe meta and `satisfies StoryObj<typeof meta>` for stories.
- Args use realistic data, not placeholder text like "Lorem ipsum" or "Test". Use content that reflects actual usage.
- Controls are configured in `argTypes` to use the most appropriate control type (select, radio, range, color).
- Autodocs are enabled via `tags: ['autodocs']` on the meta object for every component.

## Library Preferences

- Interaction testing: @storybook/test (wraps Vitest expect and Testing Library userEvent)
- Visual testing: Chromatic (never screenshot diffing with Playwright)
- API mocking: MSW 2 with msw-storybook-addon (never manual fetch mocks)
- Accessibility: @storybook/addon-a11y powered by axe-core
- Viewport testing: @storybook/addon-viewport with custom breakpoints matching Tailwind
- Documentation: @storybook/blocks for MDX documentation pages
- Design tokens: @storybook/addon-designs for linking Figma frames

## File Naming

- Components: `PascalCase.tsx`
- Stories: `PascalCase.stories.tsx`
- Tests: `PascalCase.test.tsx`
- Hooks: `useCamelCase.ts`
- Utilities: `camelCase.ts`
- Types: `camelCase.ts` with PascalCase type exports
- Story documentation: `PascalCase.mdx` alongside stories

## NEVER DO THIS

1. Never write stories using CSF2 render functions or the `Template.bind({})` pattern. Use CSF3 object syntax with `args`.
2. Never import `@testing-library/react` or `@testing-library/user-event` in stories. Use `@storybook/test` which bundles compatible versions.
3. Never use `any` type for component props. Define explicit TypeScript interfaces and pass them to `Meta<typeof Component>`.
4. Never put global CSS imports in individual stories. Configure global styles in `.storybook/preview.ts` decorators.
5. Never create stories that depend on external API calls. Use MSW handlers to mock all network requests.
6. Never skip the accessibility addon check. Every component must pass axe-core automated checks at the story level.
7. Never hardcode colors or spacing values. Use Tailwind design tokens or CSS custom properties defined in the theme.

## Testing

- Interaction tests run inside stories using `play` functions with `await expect()` assertions.
- Run all story tests with `npx test-storybook` which executes play functions in a real browser.
- Visual regression tests run via `npx chromatic` on every pull request in CI.
- Accessibility tests are automatic: every story is scanned by axe-core through the a11y addon.
- Smoke test: `npx storybook build` must complete without errors to verify all stories compile.
- Unit tests for complex component logic use Vitest with @testing-library/react in separate `.test.tsx` files.
- Coverage reports combine Vitest unit coverage and Storybook interaction test coverage.

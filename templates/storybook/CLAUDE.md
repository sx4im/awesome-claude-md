# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Storybook v8 (UI component development)
- React/Vue/Svelte/Angular support
- CSF 3 story format
- Addon ecosystem
- TypeScript support

## Project Structure
```
src/
├── components/
│   ├── Button.tsx
│   └── Button.stories.tsx      # Component stories
├── stories/
│   └── Introduction.mdx
.storybook/
├── main.ts                     # Storybook config
├── preview.ts                  # Preview config
└── preview-head.html           # HTML head modifications
```

## Architecture Rules

- **Stories showcase component states.** Each story is a component state.
- **CSF 3 format.** `export default { component: Button }; export const Primary = { args: { primary: true } }`.
- **Args for dynamic props.** Controls panel adjusts component props.
- **Docs generation automatic.** MDX or autodocs from JSDoc/TypeScript.

## Coding Conventions

- Meta: `const meta: Meta<typeof Button> = { component: Button, tags: ['autodocs'] }; export default meta`.
- Story: `export const Primary: Story = { args: { primary: true, label: 'Button' } }`.
- Render: `export const CustomRender: Story = { render: (args) => <Button {...args} icon={<Icon />} /> }`.
- Decorators: `export default { decorators: [(Story) => <ThemeProvider><Story /></ThemeProvider>] }`.
- Play function: `export const WithInteraction: Story = { play: async ({ canvasElement }) => { const canvas = within(canvasElement); await userEvent.click(canvas.getByRole('button')); } }`.

## NEVER DO THIS

1. **Never write stories that don't compile.** Stories are type-checked—keep them valid.
2. **Never ignore the `args` type safety.** Use `StoryObj<typeof Component>` for typed args.
3. **Never commit build output.** `storybook-static/` should be gitignored.
4. **Never forget to configure staticDirs.** For serving static assets in stories.
5. **Never use real API in stories.** Use MSW or mock data for isolated development.
6. **Never skip the viewport addon.** Test responsive designs with viewport presets.
7. **Never ignore accessibility testing.** Install `@storybook/addon-a11y` and check.

## Testing

- Test stories with `storybook test` (experimental).
- Test with play functions for interaction tests.
- Test with Chromatic for visual regression.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Jest/Vitest Snapshots
- Storybook Snapshots
- Playwright Visual Snapshots
- Regression detection
- Snapshot review workflow

## Project Structure
```
src/
├── components/
│   └── Button.tsx
├── __snapshots__/              // Jest snapshots
├── tests/
│   └── visual/                 // Visual regression tests
└── .storybook/
    └── snapshots/              // Storybook snapshots
```

## Architecture Rules

- **Capture baseline.** First run creates reference.
- **Detect changes.** Subsequent runs compare.
- **Review changes.** Update intentionally, fix unintentionally.
- **CI integration.** Fail on unexpected changes.

## Coding Conventions

- Jest: `expect(tree).toMatchSnapshot()`.
- Vitest: Same API, `expect(component).toMatchSnapshot()`.
- Storybook: `storybook test --coverage` with snapshot addon.
- Visual: `expect(page).toHaveScreenshot('landing.png')`.
- Update: `--updateSnapshot` or `-u` flag to update.

## NEVER DO THIS

1. **Never commit snapshots without review.** Verify changes are intentional.
2. **Never ignore snapshot failures.** Investigate each failure.
3. **Never store large binary snapshots in git.** Use LFS or external storage.
4. **Never skip naming snapshots descriptively.** Default names are cryptic.
5. **Never use for data that changes.** Dates, IDs, random values.
6. **Never forget to update snapshots after intentional changes.** CI will fail.
7. **Never ignore platform differences.** Fonts, rendering vary by OS.

## Testing

- Test snapshots pass in CI.
- Test snapshot update workflow.
- Test cross-platform consistency.


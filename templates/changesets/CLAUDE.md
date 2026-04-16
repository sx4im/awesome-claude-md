# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Changesets (versioning and changelog tool)
- pnpm/npm/yarn monorepos
- Semantic versioning
- Automated releases

## Project Structure

```
.changeset/                     # Changeset files
├── README.md
├── config.json
├── BASE.json                   # Base for prereleases
└── *.md                        # Individual changesets
packages/
└── ...
package.json
.github/
└── workflows/
    └── release.yml             # Release workflow
```

## Architecture Rules

- **Changesets document intent.** Create a changeset for every user-facing change.
- **Semantic versioning driven by changesets.** Changeset type (patch/minor/major) determines version bump.
- **Aggregated changelogs.** Changesets generate per-package changelogs.
- **CI-friendly.** Programmatic versioning and publishing in CI.

## Coding Conventions

- Create changeset: `npx changeset` (interactive CLI).
- Select packages affected by change.
- Choose bump type: patch (bugfix), minor (feature), major (breaking).
- Write summary for changelog.
- Version: `npx changeset version` updates versions and changelogs.
- Publish: `npx changeset publish` publishes to registry.
- Tag: `npx changeset tag` creates git tags.

## NEVER DO THIS

1. **Never commit without a changeset if the change affects users.** Every PR that changes behavior needs a changeset.
2. **Never manually bump versions.** Let `changeset version` do it.
3. **Never forget to configure `.changeset/config.json`.** `commit: false`, `access: public`, etc.
4. **Never skip the GitHub Action.** Automate versioning and publishing in CI.
5. **Never create empty changesets.** They're noise. Delete if created by mistake.
6. **Never ignore the "none" option.** Internal changes that don't affect users use "none".
7. **Never forget to add `.changeset/*.md` to git.** They need to be committed to work.

## Testing

- Test changeset creation locally: `npx changeset`.
- Test versioning: `npx changeset version` (dry run first).
- Test in CI with test npm registry or dry run.


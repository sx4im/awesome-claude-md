# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- conventional-changelog
- Conventional Commits
- Changelog generation
- Multiple presets
- Customizable templates

## Project Structure
```
package.json
CHANGELOG.md                    // Generated
conventional-changelog.config.js // or in package.json
```

## Architecture Rules

- **Conventional commits to changelog.** Parse commits to Markdown.
- **Presets available.** Angular, Atom, Ember, ESLint, etc.
- **Customizable.** Writer, parser, template options.
- **Integration ready.** Works with CI/CD.

## Coding Conventions

- Config: `module.exports = { preset: 'angular', releaseCount: 0, compareUrlFormat: '{{host}}/{{owner}}/{{repository}}/compare/{{previousTag}}...{{currentTag}}' }`.
- Generate: `npx conventional-changelog -p angular -i CHANGELOG.md -s -r 0`.
- Package.json: `{ "scripts": { "changelog": "conventional-changelog -p angular -i CHANGELOG.md -s" } }`.
- Presets: `angular`, `atom`, `ember`, `eslint`, `express`, `jquery`.

## NEVER DO THIS

1. **Never edit CHANGELOG.md manually.** Regenerate from commits.
2. **Never use without conventional commits.** Empty changelog otherwise.
3. **Never forget the `-s` flag.** Appends to file, doesn't replace.
4. **Never skip the preset.** Determines commit parsing rules.
5. **Never ignore writerOpts.** Customize output format.
6. **Never generate changelog without version bump.** Tag first.
7. **Never forget to commit CHANGELOG.md.** Should be in version control.

## Testing

- Test changelog generates with correct sections.
- Test links work correctly.
- Test with different presets.
- Test changelog links work.
- Test changelog formatting.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Lume (Deno static site generator)
- Deno v2
- TypeScript/JSX
- Template engines (Nunjucks, Pug, Eta)
- No build step required

## Project Structure

```
_site/                          # Generated site (gitignored)
src/
├── _includes/                  # Layouts and partials
│   ├── layouts/
│   │   └── main.njk
│   └── partials/
│       └── header.njk
├── _data/                      # Global data files
│   └── site.yml
├── posts/                      # Content
│   └── hello.md
├── about.md
└── index.njk
_config.ts                      # Lume configuration
deno.json                       # Deno config
```

## Architecture Rules

- **File-based routing.** Files in `src/` become pages based on their path.
- **Front matter for metadata.** YAML front matter in markdown/content files.
- **Layouts in `_includes`.** Reusable page layouts.
- **Data files for dynamic content.** `_data/` contains JSON/JS/YAML for templates.

## Coding Conventions

- Create page: `src/about.md` with front matter: `--- layout: layouts/main.njk ---`.
- Configure: `site.use(jsx())` in `_config.ts` for JSX/TSX support.
- Processors: `site.process(['.css'], (pages) => ...)` for custom processing.
- Helpers: `site.helper('upper', (text) => text.toUpperCase(), { type: 'tag' })`.

## NEVER DO THIS

1. **Never edit `_site/` directly.** It's generated. Modify source files.
2. **Never forget front matter delimiter.** `---` at start and end of front matter.
3. **Never ignore the `_config.ts`.** It's where plugins and processors are configured.
4. **Never use Deno modules that aren't Deno-compatible.** Check deno.land/x or esm.sh.
5. **Never forget to run `deno task lume` or similar.** Lume needs explicit build command.
6. **Never use Node.js-only packages without checking.** Deno has different module resolution.
7. **Never skip the `_data` folder for global data.** It's the idiomatic way to share data across templates.

## Testing

- Build site and verify output in `_site/`.
- Test links with `deno run --allow-all https://deno.land/x/lume/plugins/check_urls.ts`.
- Validate HTML output with validators.


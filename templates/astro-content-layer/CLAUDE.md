# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Astro 4+ with Content Layer
- Content collections with loader API
- TypeScript 5.x
- Zod schema validation
- Server-side rendering

## Project Structure
```
src/
├── content/
│   ├── config.ts               // Content config with loaders
│   └── blog/
│       └── hello.md            // Content files
├── pages/
│   └── blog/
│       └── [slug].astro
└── components/
    └── BlogPost.astro
```

## Architecture Rules

- **Loader API.** Define how content is loaded (file system, remote, etc.).
- **Schema validation.** Zod schemas for type-safe content.
- **Render function.** Custom rendering for different formats.
- **Real-time updates.** Content layer can refresh without rebuild.

## Coding Conventions

- Config: `import { defineCollection, z } from 'astro:content'; const blog = defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/blog' }), schema: z.object({ title: z.string(), date: z.date() }) })`.
- Query: `import { getCollection, getEntry } from 'astro:content'; const posts = await getCollection('blog');`.
- Render: `const { Content } = await post.render();`.

## NEVER DO THIS

1. **Never mix old and new content APIs.** Content Layer replaces old collections.
2. **Never skip the loader configuration.** Required for Content Layer.
3. **Never forget to validate schema.** Zod catches content errors early.
4. **Never use without understanding the cache.** Content Layer has caching behavior.
5. **Never ignore the `render` result.** Must destructure to use.
6. **Never query content in client-side code.** Server-only API.
7. **Never forget to regenerate types.** `astro sync` after content changes.

## Testing

- Test content loads correctly with loader.
- Test schema validation catches errors.
- Test render output is valid HTML.


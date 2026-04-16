# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Figma REST API
- Figma Plugin API
- Personal Access Tokens
- File exports
- Design system sync

## Project Structure
```
src/
├── figma/
│   ├── client.ts               // API client
│   ├── export.ts               // Export utilities
│   └── sync.ts                 // Sync functionality
├── tokens/
└── components/
```

## Architecture Rules

- **REST API for data.** Fetch file structure, comments.
- **Plugin API for Figma.** Run code inside Figma.
- **Personal Access Tokens.** Authentication for REST API.
- **Webhooks (beta).** Real-time updates.

## Coding Conventions

- Client: `const response = await fetch('https://api.figma.com/v1/files/${fileKey}', { headers: { 'X-Figma-Token': process.env.FIGMA_TOKEN } })`.
- Export: `GET /v1/images/{file_key}?ids=1:2&format=svg`.
- Plugin: `figma.showUI(__html__); figma.ui.onmessage = msg => { if (msg.type === 'create-rect') { figma.createRectangle() } }`.
- Tokens: Parse `document` JSON to extract design tokens.

## NEVER DO THIS

1. **Never commit Figma tokens.** Use environment variables.
2. **Never poll API excessively.** Rate limits apply.
3. **Never ignore the `plugin-api` vs `rest-api` distinction.** Different use cases.
4. **Never forget error handling.** Network failures common.
5. **Never use synchronous API calls.** Always async.
6. **Never ignore image export expiration.** URLs expire after 2 weeks.
7. **Never skip the `file_key` documentation.** How to find file keys.

## Testing

- Test with test Figma file.
- Test token extraction accuracy.
- Test plugin in Figma desktop and browser.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Kobweb (Kotlin web framework)
- Compose HTML
- Gradle
- Full-stack Kotlin
- Static site generation

## Project Structure
```
site/
├── src/
│   ├── jsMain/
│   │   └── kotlin/
│   │       └── pages/
│   │           └── Index.kt    // Page components
│   └── jvmMain/
│       └── kotlin/
│           └── api/
│               └── Api.kt      // Server-side API
├── build.gradle.kts
└── kobweb.yaml
```

## Architecture Rules

- **Compose HTML.** Kotlin DSL for generating HTML.
- **File-based routing.** `pages/` directory structure.
- **Full-stack Kotlin.** Shared code between frontend and backend.
- **Static export.** Generate static sites or run server.

## Coding Conventions

- Page: `@Page fun HomePage() { Div { Text("Hello") } }`.
- Component: `@Composable fun MyButton(onClick: () -> Unit) { Button(attrs = { onClick { onClick() } }) { Text("Click me") } }`.
- API: `@Api fun addUser(ctx: ApiContext) { val user = ctx.req.body?.let { Json.decodeFromString<User>(it) } ?: return; ctx.res.body = "Added" }`.
- Layout: `@Layout fun MyLayout(content: @Composable () -> Unit) { Div { content() } }`.

## NEVER DO THIS

1. **Never use JVM classes in JS target.** Keep shared code in commonMain.
2. **Never skip the @Page annotation.** Required for routing.
3. **Never mix Compose HTML with Jetpack Compose blindly.** Similar but different.
4. **Never ignore the `kobweb export` command.** For static sites.
5. **Never forget `jsMain` vs `jvmMain`.** Different compilation targets.
6. **Never use blocking calls in JS.** JS is single-threaded—use suspend.
7. **Never skip Gradle configuration.** Kobweb requires specific setup.

## Testing

- Test with Kotlin test framework.
- Test JS output in browser.
- Test API routes with HTTP client.


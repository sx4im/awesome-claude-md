# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Cursor IDE
- AI-native editor
- Cursor Tab (completions)
- Cursor Chat
- Composer (multi-file)

## Project Structure
```
├── .cursor/
│   └── instructions.md         // Project instructions
├── src/
└── cursor-rules                // Optional rules file
```

## Architecture Rules

- **VS Code fork.** Familiar interface with AI features.
- **Tab for completions.** Beyond Copilot—whole function suggestions.
- **Chat for questions.** Inline or sidebar chat.
- **Composer for large changes.** Multi-file generation.

## Coding Conventions

- Instructions: Add project context in `Settings > General > Rules for AI` or `.cursor/instructions.md`.
- Tab: Press Tab to accept, Ctrl+K to generate from prompt.
- Chat: Ctrl+L to open, `@` to reference files/context.
- Composer: Ctrl+I for agentic coding.
- Commands: Use `/edit`, `/doc`, `/test` in chat.

## NEVER DO THIS

1. **Never accept multi-file changes without review.** Check all modified files.
2. **Never ignore the context window.** Large files may be truncated.
3. **Never skip custom instructions.** Improves code generation quality.
4. **Never use in production without review.** Generated code needs verification.
5. **Never ignore file references.** `@` references help context.
6. **Never commit API keys in generated code.** Check for hardcoded secrets.
7. **Never forget to save before generating.** Unsaved changes may be lost.

## Testing

- Test generated code in isolation.
- Test that all referenced files were updated.
- Test edge cases AI might miss.


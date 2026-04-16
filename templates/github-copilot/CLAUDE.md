# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- GitHub Copilot
- VS Code/IntelliJ/Vim/Neovim
- Copilot Chat
- Inline completions
- Pull request summaries

## Project Structure
```
├── .github/
│   └── copilot-instructions.md // Custom instructions
├── src/
└── docs/
```

## Architecture Rules

- **AI pair programmer.** Suggests code as you type.
- **Context-aware.** Uses open files, recent edits.
- **Copilot Chat.** Ask questions, get explanations.
- **Custom instructions.** `.github/copilot-instructions.md` for project context.

## Coding Conventions

- Instructions: Create `.github/copilot-instructions.md` with project conventions.
- Chat: Use `/explain`, `/tests`, `/fix` commands.
- Suggestions: Tab to accept, Esc to dismiss, Ctrl+Enter for alternatives.
- Comments: Write descriptive comments for better suggestions.

## NEVER DO THIS

1. **Never accept suggestions blindly.** Review generated code.
2. **Never use for sensitive code.** Copilot trains on public code.
3. **Never ignore security issues in generated code.** Check for vulnerabilities.
4. **Never commit without review.** Copilot can hallucinate APIs.
5. **Never skip custom instructions.** Improves relevance.
6. **Never use in regulated environments without approval.** Compliance concerns.
7. **Never forget it learns from you.** Your edits improve future suggestions.

## Testing

- Test generated code compiles/runs.
- Test security of generated code.
- Test edge cases Copilot might miss.


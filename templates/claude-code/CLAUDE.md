# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Claude Code (Claude's agentic coding tool)
- CLAUDE.md context files
- MCP servers for extended capabilities
- Git integration
- Bash command execution

## Project Structure
```
├── CLAUDE.md                   // Project context
├── .claude/
│   ├── mcp.json                // MCP server configuration
│   └── settings.json           // Claude Code settings
├── docs/
│   └── architecture.md         // Additional context
└── scripts/
    └── setup.sh                // One-time setup
```

## Architecture Rules

- **CLAUDE.md is context.** Define tech stack, patterns, constraints.
- **MCP servers extend capabilities.** Tools, resources, prompts for domain-specific help.
- **Git for safety.** All changes tracked, easy to review/revert.
- **Iterate with review.** Check Claude's work before accepting.

## Coding Conventions

- CLAUDE.md sections: Tech Stack, Project Structure, Architecture Rules, Coding Conventions, NEVER DO THIS, Testing.
- Be specific: "Use named exports" not "Write clean code".
- Include file patterns: "Components in PascalCase: `Button.tsx`".
- Document anti-patterns: "Never use `any` type."
- MCP: Add `mcpServers` to `.claude/mcp.json` for external tools.

## NEVER DO THIS

1. **Never accept changes without reviewing.** Always check what Claude modified.
2. **Never skip CLAUDE.md maintenance.** Update as project evolves.
3. **Never let Claude run untrusted commands.** Review bash commands before execution.
4. **Never ignore Claude's errors.** If it says something seems wrong, investigate.
5. **Never use without Git.** Safety net for all changes.
6. **Never ignore the cost.** Claude Code uses API credits—monitor usage.
7. **Never forget about rate limits.** Large operations may hit limits.

## Testing

- Test changes work as expected.
- Test edge cases mentioned in prompts.
- Review git diff before committing.


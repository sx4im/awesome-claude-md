# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- AutoGen v0.4+ (multi-agent conversation framework)
- Python 3.11+
- OpenAI/Anthropic/Azure OpenAI
- Code execution capabilities
- Group chat patterns

## Project Structure
```
src/
├── agents/
│   ├── assistant.py            # Assistant agent
│   ├── user_proxy.py           # User proxy agent
│   └── group_chat.py           # Group chat manager
├── teams/
│   └── coding_team.py          # Predefined agent teams
├── tools/
│   └── code_executor.py        # Code execution
├── config/
│   └── llm_config.py           # LLM configuration
└── conversations/
    └── *.json                  # Saved conversations
```

## Architecture Rules

- **Conversable agents.** Agents send and receive messages.
- **User proxy for human input.** Bridges human and agent conversations.
- **Group chat for collaboration.** Multiple agents discuss and solve problems together.
- **Code execution built-in.** Agents can write and execute code (safely configure).

## Coding Conventions

- Create assistant: `AssistantAgent(name="assistant", llm_config=llm_config)`.
- Create user proxy: `UserProxyAgent(name="user", code_execution_config={"work_dir": "coding", "use_docker": False})`.
- Initiate chat: `user_proxy.initiate_chat(assistant, message="Task description")`.
- Group chat: `GroupChat(agents=[user, assistant, critic], messages=[], max_round=12)`.
- Group manager: `GroupChatManager(groupchat=groupchat, llm_config=llm_config)`.

## NEVER DO THIS

1. **Never enable code execution without safeguards.** Docker isolation or restricted environment.
2. **Never ignore the max_round limit.** Conversations can loop forever without it.
3. **Never create agents without clear system messages.** They define agent behavior.
4. **Never skip the user proxy for interactive tasks.** Human oversight is often needed.
5. **Never ignore conversation cost.** Each round = multiple LLM calls.
6. **Never forget to save important conversations.** `chat_history` contains valuable context.
7. **Never use without understanding termination conditions.** Conversations need exit criteria.

## Testing

- Test single agent responses first.
- Test group chat with limited rounds.
- Test code execution in isolated environment.


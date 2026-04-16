# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- CrewAI v0.86+ (multi-agent framework)
- Python 3.11+
- LangChain integration
- OpenAI/Anthropic/Ollama LLMs
- Optional: external tools (Serper, Browser, etc.)

## Project Structure
```
src/
├── crew/
│   ├── __init__.py
│   ├── crew.py                 # Crew definition
│   ├── agents.py               # Agent definitions
│   └── tasks.py                # Task definitions
├── tools/
│   ├── search.py               # Custom tools
│   └── browser.py
├── config/
│   └── agents.yaml             # Agent configurations
└── main.py                     # Entry point
```

## Architecture Rules

- **Agents with roles and goals.** Define agent personality, backstory, capabilities.
- **Tasks assigned to agents.** Each task has description, expected output, assigned agent.
- **Crew orchestrates execution.** Sequential or hierarchical process management.
- **Tools extend capabilities.** Search, browser, code execution, custom APIs.

## Coding Conventions

- Define agent: `Agent(role='Researcher', goal='Find information', backstory='...', llm=llm, tools=[search_tool])`.
- Define task: `Task(description='Research topic', expected_output='Summary', agent=researcher)`.
- Create crew: `Crew(agents=[researcher, writer], tasks=[research_task, write_task], process=Process.sequential)`.
- Run: `result = crew.kickoff()`.
- Tools: Use built-in or create `BaseTool` subclasses with `_run` method.

## NEVER DO THIS

1. **Never create agents without clear goals.** Vague goals produce vague results.
2. **Never skip the backstory.** It significantly influences agent behavior.
3. **Never assign tasks to wrong agents.** Match capabilities to requirements.
4. **Never ignore the process type.** `sequential` vs `hierarchical` changes behavior dramatically.
5. **Never use without defining expected outputs.** Tasks need clear output specifications.
6. **Never forget to handle rate limits.** Multiple agents = multiple LLM calls.
7. **Never ignore tool output limitations.** Some tools return truncated data.

## Testing

- Test individual agent responses to sample tasks.
- Test full crew execution with known inputs.
- Test tool integration separately.


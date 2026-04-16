# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Ollama (local LLM runner)
- Python/Node.js/Go clients
- Llama 3, Mistral, Gemma, etc.
- Docker or native installation
- Optional: GPU acceleration

## Project Structure
```
src/
├── ollama/
│   ├── client.py               # Ollama client setup
│   └── models.py               # Model management
├── chat/
│   ├── __init__.py
│   └── session.py              # Chat sessions
└── utils/
    └── prompts.py              # Prompt templates
```

## Architecture Rules

- **Local first.** Run models locally for privacy and offline access.
- **Pull models on demand.** `ollama pull llama3` downloads models.
- **Modelfiles for customization.** Create custom models with system prompts and parameters.
- **Embeddings support.** Generate embeddings locally with `nomic-embed-text`.

## Coding Conventions

- Python client: `import ollama; response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': 'Hello'}])`.
- Generate: `ollama.generate(model='llama3', prompt='Why is the sky blue?')`.
- Embeddings: `ollama.embeddings(model='nomic-embed-text', prompt='The sky is blue')`.
- Pull model: `ollama.pull('llama3')`.
- Modelfile: `FROM llama3\nSYSTEM You are a helpful assistant.` then `ollama create mymodel -f ./Modelfile`.

## NEVER DO THIS

1. **Never run production loads without GPU.** CPU inference is very slow at scale.
2. **Never forget to pull models before use.** `ollama run llama3` auto-pulls, API doesn't.
3. **Never ignore context window limits.** Local models have limited context—track token usage.
4. **Never skip model quantization.** Use Q4_K_M or similar for reasonable speed/quality tradeoff.
5. **Never use without monitoring memory.** Models can consume significant RAM/VRAM.
6. **Never forget the Modelfile for consistency.** System prompts belong in Modelfiles.
7. **Never assume all models work the same.** Different architectures have different capabilities.

## Testing

- Test model responses for quality.
- Test embedding similarity with known pairs.
- Test memory usage with different model sizes.


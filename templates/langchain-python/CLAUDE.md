# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: AI & ML)

### Release Discipline
- Never expose raw secrets, prompts, or proprietary training data.
- Validate model outputs before side effects (tool calls, writes, automations).
- Track model/version/config used in each production-impacting change.

### Merge/Release Gates
- Evaluation set checks pass on quality, safety, and regression thresholds.
- Hallucination-sensitive flows have deterministic fallback behavior.
- Prompt/template changes include before/after examples.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- Python 3.11+
- LangChain 0.3+ (core, community, and partner packages)
- LangSmith for tracing and evaluation
- a vector store (Chroma / Pinecone / Qdrant / pgvector)
- an LLM provider (OpenAI / Anthropic / local via Ollama)
- FastAPI for serving chains as API endpoints
- Pydantic v2 for structured output and data validation

## Project Structure

```
src/
├── chains/                      # LangChain chain definitions
│   ├── rag_chain.py             # Retrieval-augmented generation chain
│   ├── structured_output.py     # Chains that return Pydantic models
│   └── conversational.py        # Multi-turn conversation with memory
├── prompts/
│   ├── templates/               # Prompt template strings (version-controlled)
│   │   ├── rag_system.txt       # System prompt for RAG
│   │   └── extraction.txt       # Extraction prompt template
│   └── registry.py              # Central prompt loading and management
├── retrieval/
│   ├── vectorstore.py           # Vector store init and retrieval config
│   ├── embeddings.py            # Embedding model configuration
│   └── loaders.py               # Document loaders (PDF, web, API)
├── tools/                       # LangChain tools for agent use
│   ├── search.py
│   └── database.py
├── output_parsers/
│   └── schemas.py               # Pydantic models for structured LLM output
├── evaluation/
│   ├── evaluators.py            # Custom LangSmith evaluators
│   └── datasets.py              # Evaluation dataset management
├── api/
│   ├── app.py                   # FastAPI app with chain endpoints
│   └── schemas.py               # API request/response models
├── config.py                    # LLM, embedding, vectorstore configuration
└── utils/
    ├── callbacks.py             # Custom callback handlers
    └── rate_limiter.py          # Token/request rate limiting
```

## Architecture Rules

- **Use LCEL (LangChain Expression Language) for all chains.** Compose with `|` pipe operator: `prompt | llm | parser`. Never use the legacy `LLMChain`, `SequentialChain`, or `ConversationalRetrievalChain` classes. They are deprecated and removed in LangChain 0.3+.
- **Prompts are external files, not inline strings.** Store prompt templates in `prompts/templates/` as `.txt` files. Load with `ChatPromptTemplate.from_messages()`. Version control prompts separately from logic—prompt changes are the most common iteration.
- **Every chain is traceable.** Enable LangSmith tracing in config. Set `LANGCHAIN_TRACING_V2=true`. Name every chain with `.with_config({"run_name": "rag_chain"})`. Debugging without traces is guesswork.
- **Structured output uses Pydantic models.** Use `llm.with_structured_output(MyModel)` instead of regex parsing or manual JSON extraction. The LLM generates typed output validated by Pydantic. Parsing failures are caught, not silently wrong.
- **Vector store retrieval is configurable, not hardcoded.** Expose `k` (number of results), `score_threshold`, and `search_type` (similarity, mmr) as config parameters. Different use cases need different retrieval strategies.

## Coding Conventions

- **Chain composition:** `chain = prompt | llm | StrOutputParser()` for text. `chain = prompt | llm.with_structured_output(Schema)` for structured data. `chain = RunnablePassthrough.assign(context=retriever) | prompt | llm | parser` for RAG.
- **Prompt templates:** Use `ChatPromptTemplate.from_messages([("system", system_text), ("human", "{input}")])`. Always include a system message. Use named variables: `{input}`, `{context}`, `{chat_history}`. Never use f-strings for prompt construction.
- **Error handling:** Wrap LLM calls with `chain.with_retry(stop_after_attempt=3)` for transient failures. Use `chain.with_fallbacks([fallback_chain])` for graceful degradation. Never let a raw API error reach the user.
- **Callbacks and tracing:** Attach callbacks at the chain level, not per-call. Use `chain.with_config({"callbacks": [handler]})`. Log token usage, latency, and model parameters for every invocation.
- **Document processing:** Chunk documents with `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)`. Always include metadata (source, page, section) in document chunks. Metadata enables filtered retrieval.

## Library Preferences

- **LLM integration:** Use LangChain's provider-specific packages: `langchain-openai`, `langchain-anthropic`, `langchain-community`. Not raw API clients (LangChain adds retries, caching, tracing, and streaming for free).
- **Structured output:** `llm.with_structured_output(PydanticModel)`. Not `PydanticOutputParser` with format instructions in the prompt (the native method uses function calling/tool use, which is more reliable).
- **Vector store:** Use LangChain's vector store integration matching your backend. `langchain-chroma` for local dev, `langchain-pinecone` for production scale, `langchain-qdrant` for self-hosted.
- **Text splitting:** `RecursiveCharacterTextSplitter` for general text. `MarkdownHeaderTextSplitter` for Markdown. `HTMLSectionSplitter` for HTML. Never use `CharacterTextSplitter` (splits mid-sentence).
- **Evaluation:** LangSmith for tracing + evaluation. Not custom logging (LangSmith provides dataset management, comparison, and annotation out of the box).

## File Naming

- Source files: `snake_case.py` → `rag_chain.py`, `vectorstore.py`
- Prompt templates: `snake_case.txt` → `rag_system.txt`, `extraction.txt`
- Test files: `test_snake_case.py` → `test_rag_chain.py`
- Config files: `.env` for secrets, `config.py` for typed configuration

## NEVER DO THIS

1. **Never use legacy chain classes.** `LLMChain`, `ConversationalRetrievalChain`, `RetrievalQA`, `load_qa_chain` are all deprecated. Use LCEL pipe syntax: `prompt | llm | parser`. Legacy chains have been removed in LangChain 0.3.
2. **Never put API keys in code or config files.** Load from environment variables: `os.environ["OPENAI_API_KEY"]`. LangChain reads them automatically. Never commit `.env` files.
3. **Never construct prompts with f-strings or `.format()`.** Use `ChatPromptTemplate` with named variables. f-strings bypass LangChain's prompt tracking, break tracing, and make prompt injection trivially easy.
4. **Never ignore token limits.** Count tokens before sending to the LLM with `llm.get_num_tokens(text)`. Truncate or summarize context that exceeds the model's window. Silent truncation by the API loses critical context with no warning.
5. **Never use `CharacterTextSplitter`.** It splits on a single character (default newline), producing chunks that break mid-sentence. Use `RecursiveCharacterTextSplitter` which tries multiple separators hierarchically.
6. **Never embed documents without metadata.** Every `Document` in the vector store must have `metadata` with at least `source` and `chunk_index`. Without metadata, you cannot trace retrieved chunks back to their origin or filter by source.
7. **Never skip evaluation.** Build a LangSmith dataset with representative queries and expected answers. Run evaluations after every prompt change. "It seems to work" is not a testing strategy for LLM applications.

## Testing

- Unit test chains by mocking the LLM with `FakeListLLM` or `FakeListChatModel` from `langchain_core.language_models.fake`. Assert on prompt formatting and output parsing, not LLM intelligence.
- Integration test retrieval pipelines with a small, known document set. Assert that relevant chunks are retrieved for test queries.
- Use LangSmith evaluators for end-to-end quality: `correctness`, `relevance`, `faithfulness` (hallucination detection). Run as CI checks against evaluation datasets.
- Test structured output with edge cases: missing fields, extra fields, nested objects. Ensure Pydantic validation catches malformed LLM output.
- Never test prompt quality with unit tests. Use LangSmith evaluation datasets with human-labeled expected outputs.

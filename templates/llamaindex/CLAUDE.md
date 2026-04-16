# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- LlamaIndex v0.12+ (data framework for LLM apps)
- Python 3.11+
- OpenAI/Anthropic/Ollama LLM
- Vector stores (Pinecone, Chroma, Qdrant)
- Optional: FastAPI for serving

## Project Structure
```
src/
├── indexing/
│   ├── loaders.py              # Document loaders
│   ├── pipeline.py             # Ingestion pipeline
│   └── transformations.py      # Text splitters, embeddings
├── query/
│   ├── engines.py              # Query engines
│   ├── retrievers.py           # Custom retrievers
│   └── templates.py            # Prompt templates
├── agents/
│   └── research_agent.py       # LlamaIndex agents
├── storage/
│   └── vector_store.py         # Vector store config
└── config/
    └── settings.py
```

## Architecture Rules

- **Ingestion pipeline for documents.** Load, transform, embed, store in standardized pipeline.
- **Indices for data organization.** VectorStoreIndex, SummaryIndex, TreeIndex for different access patterns.
- **Query engines for retrieval.** Vector search, summary, or recursive retrieval via query engines.
- **Agents for complex workflows.** Multi-step reasoning with tool use.

## Coding Conventions

- Load documents: `SimpleDirectoryReader("data").load_data()`.
- Create index: `VectorStoreIndex.from_documents(documents, storage_context=storage_context)`.
- Query: `query_engine = index.as_query_engine(); response = query_engine.query("question")`.
- Custom retriever: Subclass `BaseRetriever` for specific logic.
- Agents: `OpenAIAgent.from_tools(tools, llm=llm, verbose=True)`.

## NEVER DO THIS

1. **Never index documents without chunking.** Token limits require splitting.
2. **Never use default chunk size blindly.** Tune based on your content and questions.
3. **Never skip metadata extraction.** Metadata enables filtering and improves relevance.
4. **Never ignore the response mode.** `compact`, `tree_summarize`, etc. affect answer quality.
5. **Never forget to persist index.** Save to disk/vector store or rebuild on every run.
6. **Never mix embedding models.** Consistency is critical for vector search.
7. **Never ignore evaluation.** Use LlamaIndex eval modules to measure retrieval quality.

## Testing

- Test document loading with various formats.
- Test query responses for factual correctness.
- Test retrieval with known relevant documents.


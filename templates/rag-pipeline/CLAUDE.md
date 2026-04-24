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
- {vector-db} (Pinecone / Chroma / Qdrant / Weaviate / pgvector)
- {embedding-model} (OpenAI text-embedding-3-small / Cohere embed-v3 / local sentence-transformers)
- {llm-provider} (OpenAI / Anthropic / local via vLLM or Ollama)
- LangChain or LlamaIndex for orchestration (or custom pipeline)
- FastAPI for serving the RAG API
- Pydantic v2 for schemas and configuration

## Project Structure

```
src/
├── ingestion/
│   ├── loaders/                 # Document loaders per source type
│   │   ├── pdf_loader.py        # PDF → Document with page metadata
│   │   ├── web_loader.py        # URL crawling → Document
│   │   └── api_loader.py        # API data → Document
│   ├── chunking/
│   │   ├── strategies.py        # Chunking strategies: recursive, semantic, sentence
│   │   └── metadata.py          # Metadata enrichment post-chunking
│   ├── embeddings.py            # Embedding model wrapper with batching
│   └── pipeline.py              # End-to-end ingestion: load → chunk → embed → store
├── retrieval/
│   ├── vectorstore.py           # Vector DB client initialization + search
│   ├── reranker.py              # Cross-encoder reranking (Cohere, BGE, ColBERT)
│   ├── hybrid.py                # Hybrid search: vector + BM25/keyword fusion
│   └── filters.py               # Metadata filtering and access control
├── generation/
│   ├── prompts/
│   │   ├── rag_system.txt       # System prompt with citation instructions
│   │   └── query_transform.txt  # Query rewriting prompt
│   ├── chain.py                 # Retrieval → prompt → LLM → response
│   ├── query_transform.py       # HyDE, step-back, multi-query decomposition
│   └── citations.py             # Source attribution and grounding
├── evaluation/
│   ├── metrics.py               # Retrieval: recall@k, MRR, NDCG. Generation: faithfulness
│   ├── datasets.py              # Gold-standard Q&A pairs for eval
│   └── ragas_eval.py            # RAGAS framework evaluation
├── api/
│   ├── app.py                   # FastAPI endpoints
│   └── schemas.py               # Request/response with source citations
├── config.py                    # All pipeline parameters, typed with Pydantic
└── utils/
    ├── token_counter.py         # Token counting for context window management
    └── cost_tracker.py          # Embedding + LLM cost estimation
```

## Architecture Rules

- **Ingestion and retrieval are separate pipelines.** Ingestion runs offline (batch or scheduled). Retrieval runs online (per-request). Never embed documents at query time. The vector store is pre-populated.
- **Chunking strategy is the most important decision.** Default to `RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)` for general text. Use semantic chunking for documents with clear topic boundaries. Use sentence-level splitting for QA over precise facts. Always experiment and measure.
- **Every chunk carries metadata.** At minimum: `source` (filename/URL), `chunk_index`, `total_chunks`, `page_number` (if applicable), `section_title`. Metadata enables filtered retrieval, source attribution, and debugging.
- **Retrieval is retrieve → rerank → filter.** Step 1: Retrieve top-k (k=20) candidates from vector search. Step 2: Rerank with a cross-encoder to top-n (n=5). Step 3: Apply metadata filters (access control, recency). Never skip reranking—it dramatically improves precision.
- **Context window management is explicit.** Count tokens in retrieved chunks + system prompt + user query. If total exceeds 80% of the model's context window, truncate the lowest-ranked chunks. Never silently overflow.

## Coding Conventions

- **Chunking config is always explicit.** Never use default chunk sizes without documenting why. Define in config: `chunk_size: int = 512`, `chunk_overlap: int = 50`, `strategy: Literal["recursive", "semantic", "sentence"]`. Log chunking stats: total chunks, avg size, min/max size.
- **Embedding calls are batched.** Never embed one document at a time. Batch with `batch_size=100` or the provider's max. Rate-limit with exponential backoff. Log embedding costs per batch.
- **Retrieval returns `RetrievedChunk` objects.** Define: `class RetrievedChunk(BaseModel): content: str; score: float; metadata: dict; source: str`. Never return raw vector DB responses to the generation layer.
- **Prompts instruct citation.** The system prompt must tell the LLM: "Answer based only on the provided context. Cite sources using [1], [2] notation. If the context doesn't contain the answer, say so." Never let the LLM hallucinate beyond the context.
- **All config is in `config.py`.** Chunk size, overlap, embedding model, LLM model, temperature, top-k, reranker model—everything is typed and centralized. No magic numbers scattered across files.

## Library Preferences

- **Vector DB:** Chroma for local dev/prototyping. Pinecone for managed production. Qdrant for self-hosted production. pgvector if you already have PostgreSQL and the dataset is under 1M vectors.
- **Embeddings:** OpenAI `text-embedding-3-small` (cost-effective, good quality). Cohere `embed-v3` (multilingual, supports search/classification modes). `sentence-transformers` for local/private deployment.
- **Reranking:** Cohere Rerank API for managed. `cross-encoder/ms-marco-MiniLM-L-6-v2` for local. Reranking is the highest-ROI improvement to any RAG pipeline.
- **Evaluation:** RAGAS framework for automated RAG metrics (faithfulness, relevance, context recall). Not vibes-based evaluation.
- **Orchestration:** LangChain LCEL for complex chains, or plain Python functions for simple retrieve→generate pipelines. Not LangChain legacy chains.

## File Naming

- Source files: `snake_case.py` → `vectorstore.py`, `query_transform.py`
- Prompt templates: `snake_case.txt` → `rag_system.txt`
- Evaluation datasets: `eval_{name}.jsonl` → `eval_product_qa.jsonl`
- Config: `config.py` for typed config, `.env` for secrets

## NEVER DO THIS

1. **Never use chunk_size > 1500 tokens without benchmarking.** Large chunks dilute relevance—the LLM sees mostly irrelevant text surrounding the answer. Start with 512, measure retrieval recall, and increase only if precision isn't suffering.
2. **Never skip overlap between chunks.** Zero overlap means answers that span chunk boundaries are lost. Use at least 10% overlap (e.g., `chunk_overlap=50` for `chunk_size=512`). Semantic chunking mitigates this but doesn't eliminate it.
3. **Never use cosine similarity alone for retrieval.** Vector similarity retrieves semantically similar passages, not necessarily correct answers. Always add a reranking step with a cross-encoder model. Reranking typically improves precision by 10-30%.
4. **Never embed queries and documents with different models.** The query embedding and document embedding must come from the same model. Mixing models produces embeddings in different vector spaces—similarity scores become meaningless.
5. **Never let the LLM answer without grounding instructions.** Without explicit "answer only from context" instructions, the LLM will hallucinate confidently. Include citation instructions and a "say I don't know" fallback in every RAG system prompt.
6. **Never evaluate RAG with "it looks good."** Measure retrieval recall@k (are the right chunks retrieved?), faithfulness (does the answer match the context?), and answer relevance (does it actually answer the question?). Use RAGAS or a custom eval pipeline.
7. **Never store embeddings without the original text.** Vector DBs store vectors, but you need the text for the LLM context. Store the full chunk text alongside the embedding. Reconstructing text from chunk IDs at query time adds latency and complexity.

## Testing

- Test chunking strategies with known documents: assert chunk count, average size, and that no chunk exceeds max size. Test overlap by checking that boundary content appears in adjacent chunks.
- Test retrieval with a gold-standard dataset: 50+ queries with known relevant document IDs. Measure recall@5, recall@10, and MRR. Fail CI if recall drops below the configured threshold.
- Test generation with RAGAS: faithfulness > 0.8, answer relevance > 0.7 on the evaluation dataset. Track metrics over time.
- Test metadata filtering: assert that access-controlled documents are not returned for unauthorized queries.
- Integration test the full pipeline end-to-end: ingest a small document set, query, assert that the response cites the correct source.

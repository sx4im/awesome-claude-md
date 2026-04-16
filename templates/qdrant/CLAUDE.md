# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Qdrant (vector database)
- Python or JavaScript/TypeScript client
- REST or gRPC API
- Docker for local development
- Optional: FastAPI/Node backend

## Project Structure

```
src/
├── db/
│   ├── qdrant_client.py        # Client configuration
│   └── collections.py          # Collection management
├── embeddings/
│   ├── __init__.py
│   └── generator.py            # Embedding generation
├── search/
│   ├── __init__.py
│   └── semantic_search.py      # Search operations
└── models/
    └── document.py             # Document models
```

## Architecture Rules

- **Collections for document types.** Create separate collections for different document types.
- **Vectors + payloads.** Store embeddings as vectors, metadata as payloads.
- **Filtering on payloads.** Use payload filters for pre-filtering or post-filtering.
- **HNSW for approximate search.** Configure HNSW index for large-scale similarity search.

## Coding Conventions

- Create client: `QdrantClient(url="localhost", port=6333)`.
- Create collection: `client.create_collection('docs', vectors_config=VectorParams(size=768, distance=Distance.COSINE))`.
- Upsert points: `client.upsert('docs', points=[PointStruct(id=1, vector=embedding, payload=metadata)])`.
- Search: `client.search('docs', query_vector=query_embedding, limit=10)`.
- Filter: `client.search(..., query_filter=Filter(must=[FieldCondition(key='status', match=MatchValue(value='active'))]))`.

## NEVER DO THIS

1. **Never store vectors without metadata.** Payloads are essential for filtering and result context.
2. **Never ignore the distance metric.** Choose COSINE for normalized embeddings, EUCLID for raw.
3. **Never skip index configuration.** Default HNSW is good, but tune `ef_construct` and `m` for your data.
4. **Never forget batch upserts.** Individual upserts are slow. Batch for performance.
5. **Never use wrong vector dimension.** Collection vector size must match embedding model output.
6. **Never ignore payload schema.** Consistent payload structure enables reliable filtering.
7. **Never run without replication in production.** Configure replication factor for high availability.

## Testing

- Test search quality with known similar documents.
- Test payload filtering returns expected subsets.
- Test batch operations for performance.


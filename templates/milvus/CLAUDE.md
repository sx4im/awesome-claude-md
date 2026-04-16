# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Milvus/Zilliz (vector database)
- Python or Node.js SDK
- Kubernetes or Docker deployment
- gRPC or REST API

## Project Structure

```
src/
├── milvus/
│   ├── connection.py           # Connection management
│   ├── collections.py          # Collection operations
│   └── index.py                # Index configuration
├── search/
│   ├── vector_search.py
│   └── hybrid_search.py
└── models/
    └── document.py
```

## Architecture Rules

- **Collections like database tables.** Create collections for each entity type.
- **Partitions for data organization.** Partition by date, tenant, or category.
- **Index types for different needs.** IVF_FLAT, IVF_SQ8, HNSW for different speed/accuracy tradeoffs.
- **Hybrid search capabilities.** Combine vector search with attribute filtering.

## Coding Conventions

- Connect: `connections.connect(alias="default", host="localhost", port="19530")`.
- Create collection: `Collection(name="docs", schema=schema)`.
- Define fields: `FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)`.
- Create index: `collection.create_index(field_name="embedding", index_params={"index_type": "HNSW", "metric_type": "COSINE"})`.
- Insert: `collection.insert([[...], [...]])`.
- Search: `collection.search(data=[query_vec], anns_field="embedding", param={"metric_type": "COSINE"}, limit=10)`.
- Load: `collection.load()` before searching (memory maps index).

## NEVER DO THIS

1. **Never search without loading collection.** `collection.load()` must be called first.
2. **Never ignore index type selection.** Wrong index = slow queries or poor accuracy.
3. **Never forget to flush after insert.** `collection.flush()` persists to storage.
4. **Never use growing segments for search.** Seal segments or compaction hurts less.
5. **Never ignore the metric type.** Must match index metric_type in search params.
6. **Never skip partitioning for large collections.** Partitions improve query performance.
7. **Never forget release after search.** `collection.release()` frees memory resources.

## Testing

- Test search accuracy with ground truth data.
- Test index building time for different index types.
- Test concurrent operations with multiple clients.


# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Pinecone (managed vector database)
- Python or Node.js SDK
- REST API
- No infrastructure management
- Serverless or pod-based

## Project Structure
```
src/
├── pinecone/
│   ├── client.py               # Client initialization
│   └── index.py                # Index operations
├── embeddings/
│   └── generator.py
└── search/
    └── query.py
```

## Architecture Rules

- **Serverless or pod-based.** Choose serverless for variable traffic, pods for predictable high throughput.
- **Indexes for each use case.** Separate indexes for different vector dimensions or access patterns.
- **Namespaces for multi-tenancy.** Isolate data within an index using namespaces.
- **Metadata filtering.** Filter by metadata before or during vector search.

## Coding Conventions

- Initialize: `pc = Pinecone(api_key="...")`.
- Create index: `pc.create_index(name="docs", dimension=1536, metric="cosine", spec=ServerlessSpec(cloud="aws", region="us-west-2"))`.
- Get index: `index = pc.Index("docs")`.
- Upsert: `index.upsert(vectors=[{"id": "1", "values": embedding, "metadata": {...}}], namespace="ns1")`.
- Query: `index.query(vector=query_embedding, top_k=10, namespace="ns1", filter={"genre": {"$eq": "comedy"}})`.
- Fetch: `index.fetch(ids=["1", "2"], namespace="ns1")`.
- Delete: `index.delete(ids=["1"], namespace="ns1")`.

## NEVER DO THIS

1. **Never forget namespace isolation.** Without namespace, operations affect entire index.
2. **Never exceed metadata size limits.** 40KB per vector metadata limit.
3. **Never use wrong metric.** Define cosine/euclidean/dotproduct at index creation.
4. **Never upsert without idempotency considerations.** Upserts overwrite by ID.
5. **Never ignore quota limits.** Monitor usage to avoid throttling.
6. **Never expose API keys in client-side code.** Proxy through your backend.
7. **Never skip sparse-dense hybrid if relevant.** Use sparse-dense vectors for keyword+semantic.

## Testing

- Test query results with known similar items.
- Test metadata filtering accuracy.
- Test upsert idempotency with duplicate IDs.


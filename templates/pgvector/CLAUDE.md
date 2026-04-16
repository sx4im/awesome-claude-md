# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- pgvector (PostgreSQL vector extension)
- PostgreSQL 14+
- Python/SQLAlchemy or TypeScript/Drizzle
- Vector similarity search in SQL

## Project Structure

```
src/
├── db/
│   ├── schema.py               # SQLAlchemy models with vector
│   ├── migrations/
│   └── session.py
├── embeddings/
│   └── generator.py            # Embedding generation
└── search/
    └── vector_search.py        # Vector search queries
```

## Architecture Rules

- **Vectors as native PostgreSQL type.** Use `vector` column type from pgvector.
- **IVFFlat or HNSW indexes.** Create approximate search indexes for performance.
- **SQL for everything.** Use familiar SQL for vector + metadata filtering.
- **ACID compliant.** Vector operations are transactional.

## Coding Conventions

- Enable extension: `CREATE EXTENSION IF NOT EXISTS vector;`.
- Define table: `CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(1536));`.
- Insert: `INSERT INTO items (embedding) VALUES ('[1,2,3]');` or `[:embedding]` with SQLAlchemy.
- Exact search: `SELECT * FROM items ORDER BY embedding <-> query_vector LIMIT 5;`.
- Approximate with HNSW: `CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);`.
- Cosine similarity: `SELECT 1 - (embedding <=> query_vector) AS similarity FROM items;`.

## NEVER DO THIS

1. **Never skip index creation on large tables.** Sequential scan is O(N) and slow at scale.
2. **Never use exact search without checking performance.** Measure before and after HNSW/IVFFlat.
3. **Never ignore vacuum requirements.** pgvector indexes benefit from `VACUUM` and `ANALYZE`.
4. **Never forget dimension constraints.** Vector dimensions must match your embedding model.
5. **Never use wrong operator.** `<->` is L2 distance, `<#>` is inner product, `<=>` is cosine.
6. **Never store huge vectors without need.** Consider dimensionality reduction if possible.
7. **Never ignore the ef_search parameter.** Tune for speed/accuracy tradeoff with HNSW.

## Testing

- Test vector similarity results match expected ordering.
- Test index usage with `EXPLAIN ANALYZE`.
- Test concurrent access and transactions.


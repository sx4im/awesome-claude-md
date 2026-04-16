# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Weaviate (vector search engine)
- Python or JavaScript client
- GraphQL interface
- Optional: OpenAI/Cohere/Ollama for vectors
- Docker Compose for local

## Project Structure

```
src/
├── weaviate/
│   ├── client.py               # Client setup
│   ├── schema.py               # Class schema definitions
│   └── import_data.py          # Data ingestion
├── search/
│   ├── __init__.py
│   ├── vector_search.py
│   └── hybrid_search.py
└── models/
    └── document.py
```

## Architecture Rules

- **Schema-first class definition.** Define classes with properties and vector configurations upfront.
- **Built-in vectorization.** Configure vectorizer (OpenAI, Cohere, etc.) or provide vectors manually.
- **Hybrid search.** Combine vector similarity with BM25 keyword search.
- **Multi-tenancy support.** Tenant isolation for SaaS applications.

## Coding Conventions

- Create client: `weaviate.Client("http://localhost:8080")`.
- Define class: `client.schema.create_class({'class': 'Article', 'vectorizer': 'text2vec-openai', 'properties': [...]})`.
- Import data: `client.batch.configure(batch_size=100); with client.batch as batch: batch.add_data_object(properties, 'Article')`.
- Vector search: `client.query.get('Article', ['title']).with_near_vector({'vector': query_vec}).do()`.
- Hybrid search: `client.query.get('Article').with_hybrid(query='keyword', vector=query_vec).do()`.

## NEVER DO THIS

1. **Never skip schema definition.** Weaviate requires explicit class definitions.
2. **Never mix vectorized and non-vectorized classes.** Configure consistently.
3. **Never forget to set API keys for vectorizers.** OpenAI/Cohere need keys configured.
4. **Never ignore the inverted index.** Configure for properties you want to filter on.
5. **Never batch import without batching.** Single imports are extremely slow.
6. **Never use GraphQL without understanding the structure.** Weaviate's GraphQL is specialized.
7. **Never forget about backups.** Configure backup to S3/GCS for production.

## Testing

- Test schema creation and validation.
- Test search result quality with known data.
- Test hybrid search combining keyword and vector.


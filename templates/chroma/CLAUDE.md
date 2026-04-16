# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Chroma (AI-native vector database)
- Python or JavaScript client
- Embeddings built-in or bring your own
- Persistent or in-memory modes
- Local or hosted

## Project Structure

```
src/
├── chroma/
│   ├── client.py               # Client setup
│   └── collections.py          # Collection management
├── embeddings/
│   └── generator.py            # Custom embedding logic
└── search/
    └── query.py              # Search operations
```

## Architecture Rules

- **Collections for document groups.** Separate collections for different document types.
- **Embeddings optional.** Chroma can generate embeddings with built-in models or accept your own.
- **Metadata for filtering.** Store document metadata alongside vectors for filtering.
- **Local first, scale to hosted.** Start with local Chroma, migrate to Chroma Cloud if needed.

## Coding Conventions

- Create client: `chromadb.Client()` or `chromadb.PersistentClient(path="./chroma_db")`.
- Get/create collection: `collection = client.get_or_create_collection(name="docs")`.
- Add documents: `collection.add(documents=["text"], ids=["id1"], metadatas=[{"source": "web"}])`.
- Query: `collection.query(query_texts=["search"], n_results=5)`.
- With embeddings: `collection.add(embeddings=[[...]], ...)` or let Chroma embed.
- Update: `collection.update(ids=["id1"], documents=["new text"])`.
- Delete: `collection.delete(ids=["id1"])`.

## NEVER DO THIS

1. **Never use in-memory client for production data.** Use `PersistentClient` or `HttpClient`.
2. **Never forget unique IDs.** IDs must be unique within a collection.
3. **Never mix embedding models.** Inconsistent embeddings produce meaningless results.
4. **Never store large documents without chunking.** Embed chunks, not whole documents.
5. **Never ignore metadata limits.** Very large metadata objects cause issues.
6. **Never forget `n_results` in queries.** Default might not match your needs.
7. **Never use without checking distance function.** Default is L2; cosine may be better.

## Testing

- Test similarity search with known relevant documents.
- Test metadata filtering with where clauses.
- Test persistence by restarting client and querying.


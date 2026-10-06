"""Generate embeddings for PR #11 chunks and index them in Pinecone."""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "text-embedding-3-small"
DEFAULT_BATCH_SIZE = 64

class EmbeddingError(RuntimeError):
    pass

def load_chunks(chunks_dir="data/processed/chunks"):
    directory = Path(chunks_dir)

    if not directory.exists():
        raise EmbeddingError(
            f"Chunk directory does not exist: {directory}"
        )

    chunks = []

    for path in sorted(directory.glob("*_chunks.json")):
        try:
            payload = json.loads(
                path.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            raise EmbeddingError(
                f"Could not read chunk file: {path}"
            ) from exc

        # PR #11 stores chunks inside a "chunks" field.
        if isinstance(payload, dict):
            file_chunks = payload.get("chunks")

            if not isinstance(file_chunks, list):
                raise EmbeddingError(
                    f"Invalid chunk structure: {path}"
                )

            chunks.extend(file_chunks)

        # Also support a plain list for compatibility.
        elif isinstance(payload, list):
            chunks.extend(payload)

        else:
            raise EmbeddingError(
                f"Invalid chunk JSON format: {path}"
            )

    return chunks

def _batches(items, size):
    if size <= 0:
        raise ValueError("batch_size must be greater than zero")
    for i in range(0, len(items), size):
        yield items[i:i + size]

def _embedding_client():
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise EmbeddingError("Install the 'openai' package first.") from exc
    key = os.getenv("EMBEDDING_API_KEY")
    if not key:
        raise EmbeddingError("EMBEDDING_API_KEY is not set.")
    kwargs = {"api_key": key}
    base_url = os.getenv("EMBEDDING_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url.rstrip("/")
    return OpenAI(**kwargs)

def embed_chunks(chunks, *, model=None, batch_size=DEFAULT_BATCH_SIZE, client=None):
    if not chunks:
        return []
    client = client or _embedding_client()
    model = model or os.getenv("EMBEDDING_MODEL", DEFAULT_MODEL)
    result = []
    for batch in _batches(chunks, batch_size):
        texts = [str(c.get("text", "")).strip() for c in batch]
        if any(not t for t in texts):
            raise EmbeddingError("Every chunk must contain non-empty text.")
        try:
            response = client.embeddings.create(model=model, input=texts)
            vectors = [item.embedding for item in response.data]
        except Exception as exc:
            raise EmbeddingError(f"Embedding request failed: {exc}") from exc
        if len(vectors) != len(batch):
            raise EmbeddingError("Unexpected embedding count returned by provider.")
        for chunk, vector in zip(batch, vectors):
            item = dict(chunk)
            item["embedding"] = vector
            item["embedding_model"] = model
            result.append(item)
    return result

def _pinecone_index():
    try:
        from pinecone import Pinecone
    except ImportError as exc:
        raise EmbeddingError("Install the 'pinecone' package first.") from exc
    key = os.getenv("PINECONE_API_KEY")
    name = os.getenv("PINECONE_INDEX_NAME")
    if not key or not name:
        raise EmbeddingError("PINECONE_API_KEY and PINECONE_INDEX_NAME are required.")
    return Pinecone(api_key=key).Index(name)

def _metadata(chunk):
    """Build Pinecone metadata and preserve the chunk text."""

    text = str(chunk.get("text", "")).strip()

    if not text:
        raise EmbeddingError(
            f"Chunk {chunk.get('chunk_id')} has empty text."
        )

    metadata = {
        "document_id": str(chunk["document_id"]),
        "chunk_id": str(chunk["chunk_id"]),
        "text": text,
    }

    optional_fields = (
        "document_name",
        "source_file",
        "page_number",
        "section",
        "section_chunk_index",
        "version",
        "effective_date",
        "document_type",
    )

    for field in optional_fields:
        value = chunk.get(field)

        if value not in (None, ""):
            metadata[field] = value

    return metadata

def index_chunks(embedded_chunks, *, index=None, namespace=None,
                 batch_size=DEFAULT_BATCH_SIZE):
    if not embedded_chunks:
        return 0
    index = index or _pinecone_index()
    namespace = os.getenv("PINECONE_NAMESPACE", "") if namespace is None else namespace
    vectors = []
    for chunk in embedded_chunks:
        if not chunk.get("chunk_id") or not isinstance(chunk.get("embedding"), list):
            raise EmbeddingError("Each chunk needs chunk_id and embedding.")
        vectors.append({
            "id": str(chunk["chunk_id"]),
            "values": chunk["embedding"],
            "metadata": _metadata(chunk),
        })
    for batch in _batches(vectors, batch_size):
        kwargs = {"vectors": batch}
        if namespace:
            kwargs["namespace"] = namespace
        index.upsert(**kwargs)
    return len(vectors)

def run(chunks_dir="data/processed/chunks", *, model=None, batch_size=DEFAULT_BATCH_SIZE):
    chunks = load_chunks(chunks_dir)
    embedded = embed_chunks(chunks, model=model, batch_size=batch_size)
    return index_chunks(embedded, batch_size=batch_size)

if __name__ == "__main__":
    print(f"Indexed {run()} chunks in Pinecone.")

"""Semantic retrieval from the FOLIO Pinecone index."""

import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

DEFAULT_EMBEDDING_MODEL = "openai/text-embedding-3-small"
DEFAULT_TOP_K = 5
DEFAULT_NAMESPACE = ""


class RetrievalError(RuntimeError):
    """Raised when FOLIO retrieval cannot be completed."""


def _config():
    api_key = os.getenv("EMBEDDING_API_KEY")
    base_url = os.getenv("EMBEDDING_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    pinecone_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "folio")
    namespace = os.getenv("PINECONE_NAMESPACE", DEFAULT_NAMESPACE)

    if not api_key:
        raise RetrievalError("EMBEDDING_API_KEY is not configured")
    if not pinecone_key:
        raise RetrievalError("PINECONE_API_KEY is not configured")
    if not index_name:
        raise RetrievalError("PINECONE_INDEX_NAME is not configured")

    return api_key, base_url, model, pinecone_key, index_name, namespace


def retrieve(query: str, top_k: int = DEFAULT_TOP_K, *, namespace: str | None = None,
             filter: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Embed a query and return the most relevant FOLIO chunks."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")
    if not isinstance(top_k, int) or top_k < 1:
        raise ValueError("top_k must be a positive integer")

    api_key, base_url, model, pinecone_key, index_name, configured_namespace = _config()

    embedding_client = OpenAI(api_key=api_key, base_url=base_url)
    response = embedding_client.embeddings.create(model=model, input=query.strip())
    vector = response.data[0].embedding

    pinecone_client = Pinecone(api_key=pinecone_key)
    index = pinecone_client.Index(index_name)

    kwargs = {
        "vector": vector,
        "top_k": top_k,
        "include_metadata": True,
    }

    selected_namespace = configured_namespace if namespace is None else namespace
    if selected_namespace:
        kwargs["namespace"] = selected_namespace
    if filter is not None:
        kwargs["filter"] = filter

    try:
        response = index.query(**kwargs)
    except Exception as exc:
        raise RetrievalError(f"Pinecone retrieval failed: {exc}") from exc

    matches = getattr(response, "matches", None)
    if matches is None and isinstance(response, dict):
        matches = response.get("matches", [])

    results = []
    for match in matches or []:
        if isinstance(match, dict):
            match_id = match.get("id")
            score = match.get("score")
            metadata = match.get("metadata") or {}
        else:
            match_id = getattr(match, "id", None)
            score = getattr(match, "score", None)
            metadata = getattr(match, "metadata", None) or {}

        results.append({
            "id": match_id,
            "score": score,
            "text": metadata.get("text", ""),
            "document_id": metadata.get("document_id"),
            "chunk_id": metadata.get("chunk_id"),
            "source_file": metadata.get("source_file"),
            "page_number": metadata.get("page_number"),
            "section": metadata.get("section"),
            "section_chunk_index": metadata.get("section_chunk_index"),
        })

    return results

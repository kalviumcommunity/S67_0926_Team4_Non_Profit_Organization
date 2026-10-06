from types import SimpleNamespace
from unittest.mock import MagicMock
import importlib

import pytest

retrieval_module = importlib.import_module("src.retrieval.retrieve")


def _set_env(monkeypatch):
    monkeypatch.setenv("EMBEDDING_API_KEY", "test-key")
    monkeypatch.setenv("EMBEDDING_BASE_URL", "https://openrouter.ai/api/v1")
    monkeypatch.setenv("EMBEDDING_MODEL", "openai/text-embedding-3-small")
    monkeypatch.setenv("PINECONE_API_KEY", "pinecone-test")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "folio")
    monkeypatch.setenv("PINECONE_NAMESPACE", "")


def test_retrieve_returns_metadata(monkeypatch):
    embedding_client = MagicMock()
    embedding_client.embeddings.create.return_value = SimpleNamespace(
        data=[SimpleNamespace(embedding=[0.1, 0.2, 0.3])]
    )

    index = MagicMock()
    index.query.return_value = SimpleNamespace(matches=[
        SimpleNamespace(
            id="chunk-001",
            score=0.91,
            metadata={
                "text": "Eligible animal welfare expenses include veterinary care.",
                "document_id": "doc-001",
                "chunk_id": "chunk-001",
                "source_file": "grant_guidelines.pdf",
                "page_number": 2,
                "section": "Eligible Expenses",
                "section_chunk_index": 0,
            },
        )
    ])

    monkeypatch.setattr(retrieval_module, "OpenAI", MagicMock(return_value=embedding_client))
    pinecone_cls = MagicMock()
    pinecone_cls.return_value.Index.return_value = index
    monkeypatch.setattr(retrieval_module, "Pinecone", pinecone_cls)
    _set_env(monkeypatch)

    results = retrieval_module.retrieve("What expenses are eligible?", top_k=3)

    assert len(results) == 1
    assert results[0]["score"] == 0.91
    assert results[0]["document_id"] == "doc-001"
    assert results[0]["text"].startswith("Eligible animal welfare")
    assert index.query.call_args.kwargs["top_k"] == 3
    assert index.query.call_args.kwargs["include_metadata"] is True


def test_retrieve_supports_metadata_filter(monkeypatch):
    embedding_client = MagicMock()
    embedding_client.embeddings.create.return_value = SimpleNamespace(
        data=[SimpleNamespace(embedding=[0.1, 0.2])]
    )

    index = MagicMock()
    index.query.return_value = {"matches": []}

    monkeypatch.setattr(retrieval_module, "OpenAI", MagicMock(return_value=embedding_client))
    pinecone_cls = MagicMock()
    pinecone_cls.return_value.Index.return_value = index
    monkeypatch.setattr(retrieval_module, "Pinecone", pinecone_cls)
    _set_env(monkeypatch)

    metadata_filter = {"document_id": {"$eq": "doc-001"}}
    assert retrieval_module.retrieve("animal grant", filter=metadata_filter) == []
    assert index.query.call_args.kwargs["filter"] == metadata_filter


def test_retrieve_rejects_empty_query():
    with pytest.raises(ValueError, match="non-empty"):
        retrieval_module.retrieve("   ")


def test_retrieve_rejects_invalid_top_k():
    with pytest.raises(ValueError, match="positive integer"):
        retrieval_module.retrieve("animal grant", top_k=0)

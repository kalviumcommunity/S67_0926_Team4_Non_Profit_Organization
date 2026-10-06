from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import src.rag.answer as answer_module
from src.rag.context import build_context


def test_build_context():
    results = [{
        "text": "Veterinary care is eligible.",
        "source_file": "grant_guidelines.pdf",
        "page_number": 2,
        "section": "Eligible Expenses",
        "document_id": "doc-1",
        "chunk_id": "chunk-1",
        "score": 0.91,
    }]

    context, sources = build_context(results)

    assert "[Source 1]" in context
    assert "grant_guidelines.pdf, page 2" in context
    assert "Veterinary care is eligible." in context
    assert sources[0]["document_id"] == "doc-1"


def test_build_context_skips_empty_chunks():
    context, sources = build_context([{"text": "   "}])
    assert context == ""
    assert sources == []


def test_ask_returns_grounded_answer(monkeypatch):
    monkeypatch.setattr(
        answer_module,
        "retrieve",
        lambda question, top_k=5, filter=None: [{
            "text": "Veterinary care is eligible.",
            "source_file": "grant_guidelines.pdf",
            "page_number": 2,
            "section": "Eligible Expenses",
            "document_id": "doc-1",
            "chunk_id": "chunk-1",
            "score": 0.91,
        }],
    )

    client = MagicMock()
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="Veterinary care is eligible. [Source 1]"
                )
            )
        ]
    )

    monkeypatch.setattr(
        answer_module,
        "OpenAI",
        MagicMock(return_value=client),
    )
    monkeypatch.setenv("EMBEDDING_API_KEY", "test-key")
    monkeypatch.setenv("EMBEDDING_BASE_URL", "https://openrouter.ai/api/v1")
    monkeypatch.setenv("RAG_MODEL", "openai/gpt-4o-mini")

    result = answer_module.ask(
        "What expenses are eligible?",
        top_k=3,
    )

    assert "Veterinary care is eligible" in result["answer"]
    assert result["retrieved_chunks"] == 1
    assert result["sources"][0]["source_file"] == "grant_guidelines.pdf"
    assert client.chat.completions.create.called


def test_ask_returns_no_information_when_no_context(monkeypatch):
    monkeypatch.setattr(answer_module, "retrieve", lambda *args, **kwargs: [])

    result = answer_module.ask("What is eligible?")

    assert result["retrieved_chunks"] == 0
    assert result["sources"] == []
    assert "could not find enough information" in result["answer"]


def test_ask_rejects_empty_question():
    with pytest.raises(ValueError, match="non-empty"):
        answer_module.ask("   ")

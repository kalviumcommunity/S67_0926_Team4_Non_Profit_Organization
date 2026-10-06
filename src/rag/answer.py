"""Grounded RAG answer generation for FOLIO."""

import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from src.retrieval.retrieve import retrieve
from .context import build_context

load_dotenv()

DEFAULT_CHAT_MODEL = "openai/gpt-4o-mini"


class RAGError(RuntimeError):
    """Raised when grounded answer generation fails."""


def _client_config():
    api_key = os.getenv("EMBEDDING_API_KEY")
    base_url = os.getenv(
        "EMBEDDING_BASE_URL",
        "https://openrouter.ai/api/v1",
    )
    model = os.getenv("RAG_MODEL", DEFAULT_CHAT_MODEL)

    if not api_key:
        raise RAGError("EMBEDDING_API_KEY is not configured")

    return api_key, base_url, model


SYSTEM_PROMPT = """You are FOLIO, a grant intelligence assistant for nonprofit staff.

Answer the user's question using only the provided source context.

Rules:
- Do not invent facts.
- Do not use outside knowledge.
- If the context does not contain enough information, say:
  "I could not find enough information in the provided documents."
- Keep the answer concise and factual.
- When making a factual claim, cite the relevant source using [Source N].
"""


def ask(
    question: str,
    *,
    top_k: int = 5,
    filter: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Retrieve relevant chunks and generate a grounded answer."""

    if not isinstance(question, str) or not question.strip():
        raise ValueError("question must be a non-empty string")

    try:
        results = retrieve(question, top_k=top_k, filter=filter)
    except Exception as exc:
        raise RAGError(f"Retrieval failed: {exc}") from exc

    context, sources = build_context(results)

    if not context:
        return {
            "answer": "I could not find enough information in the provided documents.",
            "sources": [],
            "retrieved_chunks": 0,
        }

    api_key, base_url, model = _client_config()
    client = OpenAI(api_key=api_key, base_url=base_url)

    user_prompt = (
        f"Source context:\n\n{context}\n\n"
        f"User question: {question.strip()}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
    except Exception as exc:
        raise RAGError(f"LLM answer generation failed: {exc}") from exc

    answer = response.choices[0].message.content

    if not answer:
        raise RAGError("LLM returned an empty answer")

    return {
        "answer": answer.strip(),
        "sources": sources,
        "retrieved_chunks": len(results),
    }
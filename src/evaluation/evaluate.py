"""Lightweight evaluation helpers for FOLIO RAG outputs."""

from __future__ import annotations

from typing import Any, Callable

from .citation_validator import validate_citations


def evaluate_single(
    question: str,
    rag_result: dict[str, Any],
    *,
    expected_answer: str | None = None,
    expected_sources: list[int] | None = None,
) -> dict[str, Any]:
    """Evaluate one RAG response for citation and optional reference checks.

    This is a deterministic evaluation helper. It does not use an LLM to
    judge semantic answer accuracy. When an expected answer is supplied,
    exact normalized string equality is reported as a simple reference check.
    """
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question must be a non-empty string")
    if not isinstance(rag_result, dict):
        raise ValueError("rag_result must be a dictionary")

    answer = rag_result.get("answer", "")
    sources = rag_result.get("sources", [])

    citation = validate_citations(answer, sources)

    result: dict[str, Any] = {
        "question": question.strip(),
        "citation_valid": citation["valid"],
        "citation_count": citation["citation_count"],
        "invalid_citations": citation["invalid_citations"],
        "no_information": citation["no_information"],
        "retrieved_chunks": rag_result.get("retrieved_chunks", len(sources)),
    }

    if expected_sources is not None:
        expected = sorted(set(expected_sources))
        result["expected_sources"] = expected
        result["source_recall"] = (
            len(set(citation["cited_sources"]) & set(expected)) / len(expected)
            if expected
            else 1.0
        )

    if expected_answer is not None:
        normalize = lambda text: " ".join(text.lower().split())
        result["reference_answer_match"] = (
            normalize(answer) == normalize(expected_answer)
        )

    return result


def evaluate_dataset(
    dataset: list[dict[str, Any]],
    ask_fn: Callable[[str], dict[str, Any]],
) -> dict[str, Any]:
    """Run deterministic evaluation over a list of evaluation questions."""
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list")

    results = []

    for item in dataset:
        if not isinstance(item, dict) or not item.get("question"):
            raise ValueError("each evaluation item needs a question")

        question = item["question"]
        rag_result = ask_fn(question)

        results.append(
            evaluate_single(
                question,
                rag_result,
                expected_answer=item.get("expected_answer"),
                expected_sources=item.get("expected_sources"),
            )
        )

    total = len(results)
    citation_valid_rate = (
        sum(item["citation_valid"] for item in results) / total
        if total
        else 0.0
    )

    reference_items = [
        item for item in results if "reference_answer_match" in item
    ]
    reference_match_rate = (
        sum(item["reference_answer_match"] for item in reference_items)
        / len(reference_items)
        if reference_items
        else None
    )

    source_items = [
        item for item in results if "source_recall" in item
    ]
    source_recall = (
        sum(item["source_recall"] for item in source_items)
        / len(source_items)
        if source_items
        else None
    )

    return {
        "total_questions": total,
        "citation_valid_rate": citation_valid_rate,
        "reference_answer_match_rate": reference_match_rate,
        "average_source_recall": source_recall,
        "results": results,
    }

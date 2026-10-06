"""Validate citations produced by grounded FOLIO answers."""

from __future__ import annotations

import re
from typing import Any

_CITATION_PATTERN = re.compile(r"\[Source\s+(\d+)\]")


class CitationValidationError(ValueError):
    """Raised when citation validation input is invalid."""


def validate_citations(
    answer: str,
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate that answer citations refer to returned sources.

    A response is considered citation-complete when every factual answer
    contains at least one valid [Source N] citation. This utility cannot
    determine factual correctness; it only checks citation presence and
    validity against the supplied source list.
    """
    if not isinstance(answer, str):
        raise CitationValidationError("answer must be a string")
    if not isinstance(sources, list):
        raise CitationValidationError("sources must be a list")

    cited_numbers = [int(n) for n in _CITATION_PATTERN.findall(answer)]
    source_count = len(sources)

    invalid = sorted({n for n in cited_numbers if n < 1 or n > source_count})
    valid = sorted({n for n in cited_numbers if 1 <= n <= source_count})

    no_information = (
        "I could not find enough information in the provided documents."
        in answer
    )

    if no_information:
        complete = True
    else:
        complete = bool(valid) and not invalid

    return {
        "valid": complete,
        "citation_count": len(cited_numbers),
        "cited_sources": valid,
        "invalid_citations": invalid,
        "no_information": no_information,
        "source_count": source_count,
    }

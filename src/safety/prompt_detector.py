"""Deterministic sensitive-prompt detection for FOLIO."""

from dataclasses import dataclass
import re
from typing import Optional


@dataclass(frozen=True)
class PromptSafetyResult:
    flagged: bool
    category: Optional[str]
    reason: Optional[str]


_RULES = (
    (
        "prompt_injection",
        re.compile(
            r"\b(ignore|disregard|forget|override|bypass)\b.{0,80}"
            r"\b(instructions?|rules?|system prompt|previous instructions?)\b",
            re.IGNORECASE | re.DOTALL,
        ),
        "Prompt attempts to override or bypass system instructions.",
    ),
    (
        "secret_extraction",
        re.compile(
            r"\b(reveal|show|give|provide|tell|print|expose|leak)\b.{0,80}"
            r"\b(api key|apikey|secret|password|token|credential|private key)\b",
            re.IGNORECASE | re.DOTALL,
        ),
        "Prompt requests secrets or authentication credentials.",
    ),
    (
        "confidential_information",
        re.compile(
            r"\b(reveal|show|give|provide|tell|expose|leak)\b.{0,80}"
            r"\b(confidential|private|restricted|internal-only)\b",
            re.IGNORECASE | re.DOTALL,
        ),
        "Prompt requests potentially confidential or restricted information.",
    ),
)


def detect_sensitive_prompt(question: str) -> PromptSafetyResult:
    """Classify a user question using deterministic safety rules."""
    if not isinstance(question, str):
        raise TypeError("question must be a string")

    normalized = question.strip()
    if not normalized:
        raise ValueError("question must not be empty")

    for category, pattern, reason in _RULES:
        if pattern.search(normalized):
            return PromptSafetyResult(True, category, reason)

    return PromptSafetyResult(False, None, None)

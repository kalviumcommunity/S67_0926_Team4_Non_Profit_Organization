"""Evaluation and citation validation utilities for FOLIO."""

from .citation_validator import CitationValidationError, validate_citations
from .evaluate import evaluate_dataset, evaluate_single

__all__ = [
    "CitationValidationError",
    "validate_citations",
    "evaluate_dataset",
    "evaluate_single",
]

"""
FOLIO Platform - LLM Utilities Interface (OpenRouter / Gemini Drop-in).
Provides backwards compatibility for modules.gemini_utils powered by OpenRouter API.
"""

from modules.openrouter_utils import (
    PERSONA_PROMPTS,
    FORMAT_PROMPTS,
    get_openrouter_response,
    get_gemini_response,
    resolve_openrouter_api_key,
    DEFAULT_OPENROUTER_MODEL,
    POPULAR_MODELS
)

__all__ = [
    "PERSONA_PROMPTS",
    "FORMAT_PROMPTS",
    "get_gemini_response",
    "get_openrouter_response",
    "resolve_openrouter_api_key",
    "DEFAULT_OPENROUTER_MODEL",
    "POPULAR_MODELS"
]

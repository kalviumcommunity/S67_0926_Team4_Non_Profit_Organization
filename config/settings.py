"""Folio Platform - Configuration and Runtime Settings."""

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    """Application global settings."""
    APP_NAME: str = "FOLIO"
    APP_TAGLINE: str = "Grant Intelligence Platform"
    INSTITUTION_NAME: str = "Helios Foundation 2025–26 Grants"
    ACTIVE_AGREEMENTS_COUNT: int = 4
    PORTAL_STATUS: str = "PORTAL VERIFIED SPECIFICATION"
    DEMO_MODE: bool = True
    SIMULATE_LATENCY: bool = True
    DEFAULT_LATENCY_SECS: float = 0.4
    
    # API Backend (for future real RAG backend)
    RAG_API_URL: str = os.getenv("RAG_API_URL", "https://api.folio-intel.internal/v1")
    RAG_API_KEY: str = os.getenv("RAG_API_KEY", "")
    DOCUMENT_API_URL: str = os.getenv("DOCUMENT_API_URL", "https://api.folio-intel.internal/v1/documents")

settings = Settings()

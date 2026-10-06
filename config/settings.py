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
    
    # Vector Database & Indexing Configurations
    VECTOR_DB_PROVIDER: str = "ChromaDB / In-Memory HNSW"
    VECTOR_COLLECTION_NAME: str = "folio_grant_instruments_v1"
    VECTOR_DIMENSION: int = 1536
    DISTANCE_METRIC: str = "Cosine Distance"
    HNSW_M: int = 16
    HNSW_EF_CONSTRUCTION: int = 128
    HNSW_EF_SEARCH: int = 64
    HNSW_INDEX_STATUS: str = "ACTIVE (Synced)"
    TOTAL_INDEXED_VECTORS: int = 48
    
    # API Backend (for future real RAG backend)
    RAG_API_URL: str = os.getenv("RAG_API_URL", "https://api.folio-intel.internal/v1")
    RAG_API_KEY: str = os.getenv("RAG_API_KEY", "")
    DOCUMENT_API_URL: str = os.getenv("DOCUMENT_API_URL", "https://api.folio-intel.internal/v1/documents")

settings = Settings()

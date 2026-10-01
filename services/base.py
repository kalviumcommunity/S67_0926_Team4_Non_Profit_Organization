"""Folio Platform - Service Abstraction Layer."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseRAGService(ABC):
    """Abstract interface for RAG question answering and query intelligence."""
    
    @abstractmethod
    def ask_question(self, query: str) -> Dict[str, Any]:
        """Execute a query and return structured grounded response with citations."""
        pass

    @abstractmethod
    def execute_rag_pipeline(self, query: str) -> Dict[str, Any]:
        """Execute the end-to-end RAG pipeline with step-by-step telemetry."""
        pass
    
    @abstractmethod
    def get_suggested_queries(self) -> List[str]:
        """Retrieve default or dynamic suggested queries."""
        pass

class BaseDocumentService(ABC):
    """Abstract interface for document archive management and clause search."""
    
    @abstractmethod
    def get_documents(self, category: str = "All", search_query: str = "") -> List[Dict[str, Any]]:
        """Retrieve documents matching optional category filter and search string."""
        pass
    
    @abstractmethod
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve full details of a specific document."""
        pass
    
    @abstractmethod
    def search_clauses(self, query: str) -> List[Dict[str, Any]]:
        """Search across all indexed documents for matching clauses with context."""
        pass
    
    @abstractmethod
    def upload_document(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Process and index a newly uploaded grant document."""
        pass

class BaseEvidenceService(ABC):
    """Abstract interface for provenance traceability and cross-instrument diffing."""
    
    @abstractmethod
    def get_evidence_for_query(self, query: str) -> Dict[str, Any]:
        """Retrieve lineage tree and verified physical excerpts for a query."""
        pass
    
    @abstractmethod
    def export_audit_dossier(self, evidence_data: Dict[str, Any]) -> bytes:
        """Generate downloadable PDF/Text audit dossier."""
        pass

"""Folio Platform - RAG Service Implementation."""

import time
from typing import Dict, Any, List, Optional
from services.base import BaseRAGService
from data.mock_queries import MOCK_QUERIES
from data.mock_documents import MOCK_DOCUMENTS
from config.settings import settings

class MockRAGService(BaseRAGService):
    """Mock implementation of RAG Question Answering service."""
    
    def __init__(self, simulate_latency: bool = True):
        self.simulate_latency = simulate_latency
        
    def ask_question(self, query: str) -> Dict[str, Any]:
        """Execute a query and return structured grounded response with citations."""
        if not query or not query.strip():
            return {
                "status": "empty",
                "message": "No question asked yet."
            }
            
        clean_query = query.strip()
        
        # Check for direct match
        for known_q, data in MOCK_QUERIES.items():
            if clean_query.lower() in known_q.lower() or known_q.lower() in clean_query.lower():
                return {
                    "status": "success",
                    "data": data
                }
                
        # Keyword-based dynamic matching
        lower_q = clean_query.lower()
        if "indirect" in lower_q or "overhead" in lower_q or "cost" in lower_q:
            return {"status": "success", "data": MOCK_QUERIES["What are the indirect costs rules?"]}
        elif "annual" in lower_q or "impact" in lower_q or "narrative" in lower_q:
            return {"status": "success", "data": MOCK_QUERIES["When is the annual impact report due?"]}
        elif "budget" in lower_q or "reallocat" in lower_q or "variance" in lower_q:
            return {"status": "success", "data": MOCK_QUERIES["What are the budget reallocation limits?"]}
        elif "audit" in lower_q or "gaap" in lower_q or "cpa" in lower_q:
            return {"status": "success", "data": MOCK_QUERIES["What are the financial audit requirements?"]}
        elif "miss" in lower_q or "late" in lower_q or "deadline" in lower_q or "freeze" in lower_q:
            return {"status": "success", "data": MOCK_QUERIES["What happens if a reporting deadline is missed?"]}
        elif "report" in lower_q or "quarter" in lower_q or "due" in lower_q:
            return {"status": "success", "data": MOCK_QUERIES["What are the reporting requirements?"]}
            
        # Fallback for queries with no matching evidence
        return {
            "status": "no_results",
            "message": f"No sufficiently relevant supporting evidence found in active Helios Foundation charters for “{clean_query}”.",
            "data": {
                "query_normalized": clean_query,
                "question": clean_query,
                "editorial_headline": "NO VERIFIED CLAUSE MATCH",
                "answer_lead": "The institutional knowledge vault does not currently contain verified clauses addressing this specific inquiry.",
                "answer_body": "To maintain zero-extrapolation compliance, Folio does not generate ungrounded estimations. Please search for reporting deadlines, indirect cost caps, audit rules, or upload additional donor agreements.",
                "verified_count": "0 sources verified",
                "spec_badge": "UNVERIFIED INQUIRY",
                "confidence_score": 0.0,
                "metrics": [],
                "sources": [],
                "evidence_ref": "REF #UNMATCHED",
                "sub_note": "No cryptographic match found in active repository."
            }
        }
        
    def get_suggested_queries(self) -> List[str]:
        """Retrieve suggested queries."""
        return list(MOCK_QUERIES.keys())

# Default Singleton Instance
rag_service = MockRAGService()

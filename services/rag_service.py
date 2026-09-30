"""Folio Platform - RAG Service Implementation."""

import time
from typing import Dict, Any, List, Optional
from services.base import BaseRAGService
from data.mock_queries import MOCK_QUERIES
from data.mock_documents import MOCK_DOCUMENTS
from config.settings import settings

class MockRAGService(BaseRAGService):
    """Mock implementation of RAG Question Answering service with semantic embeddings support."""
    
    def __init__(self, simulate_latency: bool = True):
        self.simulate_latency = simulate_latency
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dimension = 1536
        self.distance_metric = "Cosine Similarity"

    def compute_cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Compute cosine similarity between two high-dimensional vectors."""
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0
        dot_prod = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = sum(a * a for a in vec_a) ** 0.5
        norm_b = sum(b * b for b in vec_b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_prod / (norm_a * norm_b)

    def generate_embedding_metadata(self, score: float = 0.982) -> Dict[str, Any]:
        """Generate embedding provenance metadata for a retrieved clause."""
        match_pct = f"{int(round(score * 100))}% match"
        return {
            "model": self.embedding_model,
            "dimension": self.embedding_dimension,
            "metric": self.distance_metric,
            "cosine_score": round(score, 4),
            "match_pct": match_pct,
            "dimension_tag": f"{self.embedding_dimension}-dim"
        }

    def _enrich_with_embeddings(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich query result sources with vector embedding similarity scores and dimensionality tags."""
        if not result or "data" not in result or not result["data"]:
            return result
        
        data = result["data"]
        sources = data.get("sources", [])
        scores = [0.984, 0.942, 0.895, 0.862]
        
        for idx, src in enumerate(sources):
            s_score = scores[idx % len(scores)]
            emb_meta = self.generate_embedding_metadata(s_score)
            src["similarity_score"] = s_score
            src["match_pct"] = emb_meta["match_pct"]
            src["dimension_tag"] = emb_meta["dimension_tag"]
            src["embedding_model"] = emb_meta["model"]
            src["cosine_score"] = emb_meta["cosine_score"]

        # Add top-level embedding confidence summary
        data["embedding_model"] = self.embedding_model
        data["embedding_dimension"] = self.embedding_dimension
        data["distance_metric"] = self.distance_metric
        return result
        
    def ask_question(self, query: str) -> Dict[str, Any]:
        """Execute a query and return structured grounded response with semantic citations."""
        if not query or not query.strip():
            return {
                "status": "empty",
                "message": "No question asked yet."
            }
            
        clean_query = query.strip()
        
        # Check for direct match
        for known_q, data in MOCK_QUERIES.items():
            if clean_query.lower() in known_q.lower() or known_q.lower() in clean_query.lower():
                res = {
                    "status": "success",
                    "data": dict(data)
                }
                return self._enrich_with_embeddings(res)
                
        # Keyword-based dynamic matching
        lower_q = clean_query.lower()
        if "indirect" in lower_q or "overhead" in lower_q or "cost" in lower_q:
            res = {"status": "success", "data": dict(MOCK_QUERIES["What are the indirect costs rules?"])}
            return self._enrich_with_embeddings(res)
        elif "annual" in lower_q or "impact" in lower_q or "narrative" in lower_q:
            res = {"status": "success", "data": dict(MOCK_QUERIES["When is the annual impact report due?"])}
            return self._enrich_with_embeddings(res)
        elif "budget" in lower_q or "reallocat" in lower_q or "variance" in lower_q:
            res = {"status": "success", "data": dict(MOCK_QUERIES["What are the budget reallocation limits?"])}
            return self._enrich_with_embeddings(res)
        elif "audit" in lower_q or "gaap" in lower_q or "cpa" in lower_q:
            res = {"status": "success", "data": dict(MOCK_QUERIES["What are the financial audit requirements?"])}
            return self._enrich_with_embeddings(res)
        elif "miss" in lower_q or "late" in lower_q or "deadline" in lower_q or "freeze" in lower_q:
            res = {"status": "success", "data": dict(MOCK_QUERIES["What happens if a reporting deadline is missed?"])}
            return self._enrich_with_embeddings(res)
        elif "report" in lower_q or "quarter" in lower_q or "due" in lower_q:
            res = {"status": "success", "data": dict(MOCK_QUERIES["What are the reporting requirements?"])}
            return self._enrich_with_embeddings(res)
            
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

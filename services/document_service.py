"""Folio Platform - Document Service Implementation."""

import hashlib
import time
from typing import Dict, Any, List, Optional
from services.base import BaseDocumentService
from data.mock_documents import MOCK_DOCUMENTS

class MockDocumentService(BaseDocumentService):
    """Mock implementation of Document Repository and Clause Search service."""
    
    def __init__(self):
        self._documents: List[Dict[str, Any]] = list(MOCK_DOCUMENTS)
        
    def get_documents(self, category: str = "All", search_query: str = "", extra_documents: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve documents matching optional category filter and search string."""
        docs = list(self._documents)
        if extra_documents:
            docs = extra_documents + docs
            
        filtered = []
        for doc in docs:
            # Category filter
            if category and category != "All" and doc.get("category") != category:
                continue
                
            # Search query
            if search_query and search_query.strip():
                query = search_query.strip().lower()
                doc_str = (doc.get("title", "") + " " + 
                           doc.get("subtitle", "") + " " + 
                           doc.get("organization", "") + " " + 
                           doc.get("full_text", "")).lower()
                if query not in doc_str:
                    continue
                    
            filtered.append(doc)
            
        return filtered
        
    def get_document_by_id(self, doc_id: str, extra_documents: List[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Retrieve full details of a specific document."""
        docs = list(self._documents)
        if extra_documents:
            docs = extra_documents + docs
            
        for doc in docs:
            if doc.get("id") == doc_id:
                return doc
        return None
        
    def search_clauses(self, query: str, extra_documents: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search across all indexed documents for matching clauses with context."""
        if not query or not query.strip():
            return []
            
        q = query.strip().lower()
        results = []
        
        # Check standard known clauses first
        if "indirect" in q or "cost" in q or "overhead" in q:
            results.append({
                "doc_title": "Grant Guidelines § 4.3",
                "doc_id": "DOC-01",
                "meta": "Page 8 · Clause 12",
                "parent_name": "Helios Foundation General Terms 2025–26",
                "text": "“…indirect costs are strictly capped at 10% of total direct personnel expenditures, unless specifically augmented by Addendum B…”"
            })
            results.append({
                "doc_title": "Donor Agreement § 9.1",
                "doc_id": "DOC-02",
                "meta": "Page 14 · Clause 4",
                "parent_name": "Grant Agreement Ref #H-882-01",
                "text": "“…administrative and indirect costs exceeding allowable ceiling require written waiver prior to Year 2 tranche release…”"
            })
        elif "report" in q or "deadlin" in q or "window" in q:
            results.append({
                "doc_title": "Grant Guidelines § 5.1",
                "doc_id": "DOC-01",
                "meta": "Page 8 · Clause 1",
                "parent_name": "Helios Foundation General Terms 2025–26",
                "text": "“…Quarterly financial reports must be submitted within 30 DAYS following the close of each calendar quarter…”"
            })
            results.append({
                "doc_title": "Donor Agreement § 7.2",
                "doc_id": "DOC-02",
                "meta": "Page 14 · Clause 2",
                "parent_name": "Grant Agreement Ref #H-882-01",
                "text": "“…an annual impact report is required at the end of the funding period, documenting qualitative outcomes, beneficiary counts, and audited metrics…”"
            })
        elif "audit" in q or "gaap" in q:
            results.append({
                "doc_title": "Fiscal Governance § 2.1",
                "doc_id": "DOC-05",
                "meta": "Page 5 · Clause 1",
                "parent_name": "Quarterly Fiscal Governance Directives 2025",
                "text": "“…All grant financial ledgers must be maintained in accordance with GAAP. Dual-entry accounting and segregated ledger accounts are mandatory…”"
            })
            results.append({
                "doc_title": "Grant Guidelines § 8.2",
                "doc_id": "DOC-01",
                "meta": "Page 19 · Clause 3",
                "parent_name": "Helios Foundation General Terms 2025–26",
                "text": "“…The Foundation reserves the right to conduct an independent compliance and financial audit upon 14 calendar days written notice…”"
            })
        else:
            # Generic clause scanner across full text
            docs = list(self._documents)
            if extra_documents:
                docs = extra_documents + docs
            for doc in docs:
                text = doc.get("full_text", "")
                if q in text.lower():
                    # Extract surrounding paragraph
                    lines = text.split("\n")
                    for line in lines:
                        if q in line.lower() and len(line.strip()) > 20:
                            results.append({
                                "doc_title": f"{doc.get('title')} {doc.get('dossier_num', '')}",
                                "doc_id": doc.get("id"),
                                "meta": f"Page 1 · {doc.get('format')}",
                                "parent_name": doc.get("subtitle"),
                                "text": f"“…{line.strip()}…”"
                            })
                            if len(results) >= 4:
                                break
                                
        return results

    def upload_document(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Process and index a newly uploaded grant document."""
        hasher = hashlib.sha256()
        hasher.update(file_bytes)
        sha256_hash = hasher.hexdigest()
        
        doc_id = f"DOC-UP-{int(time.time())}"
        clean_name = filename.rsplit(".", 1)[0].replace("_", " ").title()
        
        new_doc = {
            "id": doc_id,
            "dossier_num": "09",
            "title": clean_name.upper(),
            "subtitle": f"Uploaded Archival Filing ({filename})",
            "category": "Grant Guidelines" if "guideline" in filename.lower() else "Donor Agreements",
            "organization": "Helios Grantee Partner",
            "year": "2026",
            "pages": max(4, len(file_bytes) // 4000),
            "format": filename.split(".")[-1].upper() if "." in filename else "PDF",
            "status": "Active",
            "status_badge_type": "primary",
            "ref_code": f"REF #UP-{doc_id[-4:]}",
            "spine_color": "#1E382B",
            "seal": "SEAL: OCR-INDEXED",
            "doc_id_code": f"UP-{doc_id[-6:]}",
            "sha256": sha256_hash,
            "key_clauses": [
                {"section": "§ 1.1", "title": "Program Scope & Eligibility", "page": 1, "highlight": False},
                {"section": "§ 3.2", "title": "Quarterly Filing Commitments", "page": 2, "highlight": True},
            ],
            "full_text": f"""
# {clean_name.upper()}
**Uploaded Document: {filename}**
**Cryptographic Hash: {sha256_hash}**

---

### SECTION 1. RECIPIENT COMPLIANCE & GOVERNANCE
This document has been parsed and indexed into the Folio Institutional Knowledge Archive. All extracted clauses are available for zero-extrapolation verified synthesis.
            """
        }
        
        return new_doc

# Default Singleton Instance
document_service = MockDocumentService()

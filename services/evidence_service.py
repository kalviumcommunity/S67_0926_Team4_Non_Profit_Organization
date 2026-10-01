"""Folio Platform - Evidence & Provenance Service Implementation."""

from typing import Dict, Any, Optional
from services.base import BaseEvidenceService
from data.mock_evidence import MOCK_EVIDENCE_MAP
from data.mock_queries import MOCK_QUERIES

class MockEvidenceService(BaseEvidenceService):
    """Mock implementation of Provenance and Evidence Traceability service."""
    
    def get_evidence_for_query(self, query: str) -> Dict[str, Any]:
        """Retrieve lineage tree and verified physical excerpts for a query."""
        if not query or not query.strip():
            query = "What are the reporting requirements?"
            
        clean_q = query.strip()
        
        # Exact or fuzzy match in evidence map
        if clean_q in MOCK_EVIDENCE_MAP:
            return MOCK_EVIDENCE_MAP[clean_q]
            
        for known_q, data in MOCK_EVIDENCE_MAP.items():
            if clean_q.lower() in known_q.lower() or known_q.lower() in clean_q.lower():
                return data
                
        # Generate dynamic evidence structure from RAG query
        rag_data = MOCK_QUERIES.get(clean_q) or MOCK_QUERIES.get("What are the reporting requirements?")
        
        return {
            "evidence_ref": rag_data.get("evidence_ref", "REF #EV-2025-GEN"),
            "inquiry_title": "Primary Synthesis Inquiry",
            "inquiry_text": rag_data.get("question", clean_q),
            "lineage_root": {
                "title": "Synthesized Answer Statement",
                "statement": rag_data.get("answer_lead", "Verified Grantee Requirement"),
                "meta": f"{len(rag_data.get('sources', []))} Authoritative Records · Zero Extrapolations"
            },
            "branch_a": {
                "category": "Primary Regulatory Framework",
                "doc_name": rag_data["sources"][0]["document_title"] if rag_data.get("sources") else "GRANT GUIDELINES",
                "doc_sub": "Helios Operational Directives 2025–26",
                "clause_tag": rag_data["sources"][0]["citation_ref"] if rag_data.get("sources") else "§ 5.1 · Page 8",
                "badge_color": "primary",
                "doc_id": rag_data["sources"][0]["doc_id"] if rag_data.get("sources") else "DOC-01"
            },
            "branch_b": {
                "category": "Binding Grantee Instrument",
                "doc_name": rag_data["sources"][1]["document_title"] if len(rag_data.get("sources", [])) > 1 else "DONOR AGREEMENT",
                "doc_sub": "Bilateral Compact #H-882",
                "clause_tag": rag_data["sources"][1]["citation_ref"] if len(rag_data.get("sources", [])) > 1 else "§ 7.2 · Page 14",
                "badge_color": "secondary",
                "doc_id": rag_data["sources"][1]["doc_id"] if len(rag_data.get("sources", [])) > 1 else "DOC-02"
            },
            "excerpts": [
                {
                    "sheet_id": "SHEET-A",
                    "deckle_color": "var(--folio-primary)",
                    "ledger_tag": "Archival Ledger 2025.1",
                    "doc_title": rag_data["sources"][0]["document_title"] if rag_data.get("sources") else "Grant Guidelines",
                    "clause_badge": rag_data["sources"][0]["citation_ref"] if rag_data.get("sources") else "§ 5.1",
                    "status_text": "Verified Active",
                    "section_header": "SECTION 5. REPORTING SCHEDULE AND DISBURSEMENT CONDITIONS",
                    "sub_clause": "5.1 Operational Directives.",
                    "body_text": f"The Grantee shall adhere to all requirements as specified. <mark class=\"ink-highlight-primary font-medium text-primary\">{rag_data.get('answer_lead')}</mark> All filings must be signed by authorized financial controllers.",
                    "footnote": "“Submissions received past cutoff undergo secondary compliance review.”",
                    "doc_id_label": "Doc ID: HL-GDL-2025-V4",
                    "doc_id": "DOC-01"
                }
            ],
            "reconciler": MOCK_EVIDENCE_MAP["What are the reporting requirements?"]["reconciler"]
        }

    def export_audit_dossier(self, evidence_data: Dict[str, Any]) -> str:
        """Generate text/markdown audit dossier for download."""
        ref = evidence_data.get("evidence_ref", "REF #EV-2025-419")
        inquiry = evidence_data.get("inquiry_text", "")
        root = evidence_data.get("lineage_root", {})
        
        dossier = f"""================================================================================
FOLIO — VERIFIED INSTITUTIONAL PROVENANCE AUDIT DOSSIER
================================================================================
AUDIT REFERENCE : {ref}
DATE COMPILED   : 2026-09-18
INSTITUTION     : Helios Foundation 2025–2026 Grant Portfolio
INTEGRITY CHECK : SHA-256 Verified · 100% Deterministic Lineage

INQUIRY:
"{inquiry}"

SYNTHESIZED DETERMINATION:
{root.get('statement', '')}
({root.get('meta', '')})

AUTHORITY BRANCHES:
1. Primary Regulatory Framework:
   - Document : {evidence_data.get('branch_a', {}).get('doc_name')}
   - Clause   : {evidence_data.get('branch_a', {}).get('clause_tag')}
2. Binding Grantee Instrument:
   - Document : {evidence_data.get('branch_b', {}).get('doc_name')}
   - Clause   : {evidence_data.get('branch_b', {}).get('clause_tag')}

MATERIAL EXCERPTS AUDIT TRAIL:
"""
        for i, sheet in enumerate(evidence_data.get("excerpts", []), 1):
            clean_body = sheet.get("body_text", "").replace('<mark class="ink-highlight-primary font-medium text-primary">', '').replace('<mark class="ink-highlight-secondary font-medium text-primary">', '').replace('</mark>', '')
            dossier += f"""
[EXCERPT {i}]
Source   : {sheet.get('doc_title')} ({sheet.get('clause_badge')})
Status   : {sheet.get('status_text')} | {sheet.get('doc_id_label')}
Excerpt  : {clean_body}
"""

        dossier += """
================================================================================
END OF DOSSIER — FOLIO INSTITUTIONAL ARCHIVE
================================================================================
"""
        return dossier

# Default Singleton Instance
evidence_service = MockEvidenceService()

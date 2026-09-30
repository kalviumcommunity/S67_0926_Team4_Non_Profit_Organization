"""Folio Platform - Mock Evidence & Provenance Traceability Repository."""

from typing import Dict, Any, List

MOCK_EVIDENCE_MAP: Dict[str, Dict[str, Any]] = {
    "What are the reporting requirements?": {
        "evidence_ref": "REF #EV-2025-419",
        "inquiry_title": "Primary Synthesis Inquiry",
        "inquiry_text": "What are the mandatory reporting deadlines & disbursement conditions?",
        "lineage_root": {
            "title": "Synthesized Answer Statement",
            "statement": "Quarterly within 30 days · Annual at year-end",
            "meta": "2 Authoritative Records · Zero Extrapolations"
        },
        "branch_a": {
            "category": "Primary Regulatory Framework",
            "doc_name": "GRANT GUIDELINES",
            "doc_sub": "Helios Operational Directives 2025–26",
            "clause_tag": "§ 5.1 · Page 8",
            "badge_color": "primary",
            "doc_id": "DOC-01"
        },
        "branch_b": {
            "category": "Binding Grantee Instrument",
            "doc_name": "DONOR AGREEMENT",
            "doc_sub": "Bilateral Compact #H-882 (Nov 2024)",
            "clause_tag": "§ 7.2 · Page 14",
            "badge_color": "secondary",
            "doc_id": "DOC-02"
        },
        "excerpts": [
            {
                "sheet_id": "SHEET-A",
                "deckle_color": "var(--folio-primary)",
                "ledger_tag": "Archival Ledger 2025.1",
                "doc_title": "Helios Foundation Grant Guidelines (2025–2026)",
                "clause_badge": "§ 5.1 · p. 8",
                "status_text": "Verified Active",
                "section_header": "SECTION 5. REPORTING SCHEDULE AND DISBURSEMENT CONDITIONS",
                "sub_clause": "5.1 Quarterly Financial Filings.",
                "body_text": "The Grantee shall submit quarterly expenditure reports, prepared according to GAAP standards and attested by an authorized financial controller. <mark class=\"ink-highlight-primary font-medium text-primary\">Quarterly financial reports must be submitted within 30 DAYS following the close of each calendar quarter.</mark> Failure to lodge within this designated timeframe triggers automatic payment withholding until reconciliation is satisfied by the board.",
                "footnote": "“Submissions received past day 30 will undergo secondary compliance assessment before upcoming disbursement tranches are approved.”",
                "doc_id_label": "Doc ID: HL-GDL-2025-V4",
                "doc_id": "DOC-01"
            },
            {
                "sheet_id": "SHEET-B",
                "deckle_color": "var(--folio-terracotta)",
                "ledger_tag": "Counterpart Execution Record",
                "doc_title": "Bilateral Donor Agreement #H-882",
                "clause_badge": "§ 7.2 · p. 14",
                "status_text": "Signed Nov 2024",
                "section_header": "ARTICLE 7. ANNUAL IMPACT REPORTING & EVALUATION",
                "sub_clause": "7.2 Closeout Narrative.",
                "body_text": "In addition to routine periodic ledgers, <mark class=\"ink-highlight-secondary font-medium text-primary\">an annual impact report is required at the end of the funding period,</mark> documenting qualitative outcomes, beneficiary counts, and audited metrics. The annual packet shall be accompanied by an independent auditor's commentary.",
                "footnote": "“No subsequent multi-year tranches will execute prior to committee approval of the Year-End Summary Narrative.”",
                "doc_id_label": "Signature: E. Vance, Exec. VP (Executed 18 Nov 2024)",
                "doc_id": "DOC-02"
            }
        ],
        "reconciler": {
            "status_text": "Conflict check: No direct contradiction found (1 variance note)",
            "active_column": {
                "title": "GRANT GUIDELINES (Active)",
                "meta": "Current 2025–26 Cycle",
                "metrics": [
                    {
                        "label": "Quarterly Lodging Window",
                        "numeral": "30 DAYS",
                        "pill": "Strict Cutoff",
                        "description": "Section 5.1 designates calendar day 30 as absolute disbursement freeze limit."
                    },
                    {
                        "label": "Line Item Variance Allowance",
                        "numeral": "10% CAP",
                        "pill": "Standard Policy",
                        "description": "Budget shifts exceeding 10% between categories require prior written consent."
                    }
                ]
            },
            "historical_column": {
                "title": "DONOR AGREEMENT / HISTORICAL",
                "meta": "Historical Precedent",
                "metrics": [
                    {
                        "label": "Previous 2023–24 Rule",
                        "numeral": "45 DAYS",
                        "numeral_style": "line-through opacity-70",
                        "pill": "Superseded",
                        "description": "Contract #H-882 confirms adherence to newly reduced 30-day timeline for 2025."
                    },
                    {
                        "label": "Allowable Variance Exception",
                        "numeral": "15% MAX",
                        "pill": "If Notified",
                        "description": "Article 8.3 permits up to 15% shift strictly if written notice is filed within 5 days."
                    }
                ]
            },
            "diff_drawer": {
                "header": "STRUCTURAL CLAUSE DELTA CHECK",
                "classification": "Variance Classification: Minor / Reconciled",
                "items": [
                    {
                        "type": "minus",
                        "prefix": "- [2023 Baseline §4.8]:",
                        "text": "Reports receivable within forty-five (45) consecutive calendar days post-quarter."
                    },
                    {
                        "type": "plus",
                        "prefix": "+ [2025 Active §5.1]:",
                        "text": "Reports receivable within thirty (30) consecutive calendar days post-quarter."
                    },
                    {
                        "type": "note",
                        "prefix": "~ [Reconciliation Note]:",
                        "text": "Agreement #H-882 Annex B executes 30-day requirement; 45-day window is void."
                    }
                ]
            }
        }
    }
}

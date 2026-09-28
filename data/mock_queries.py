"""Folio Platform - Mock RAG Query & Answer Synthesis Repository."""

from typing import Dict, Any, List

MOCK_QUERIES: Dict[str, Dict[str, Any]] = {
    "What are the reporting requirements?": {
        "query_normalized": "reporting requirements",
        "question": "What are the reporting requirements?",
        "editorial_headline": "REPORTING REQUIREMENTS",
        "answer_lead": "Quarterly financial reports are required within 30 days after each calendar quarter.",
        "answer_body": "An annual comprehensive impact narrative is required at the end of the funding period. All submissions must be uploaded directly via the Helios grantee portal.",
        "verified_count": "2 sources verified",
        "spec_badge": "PORTAL VERIFIED SPECIFICATION",
        "confidence_score": 0.98,
        "metrics": [
            {
                "pill_text": "Deadline",
                "pill_type": "green",
                "pill_icon": "calendar_today",
                "sub_pill": "Q1-Q4",
                "numeral": "18 DAYS",
                "numeral_color": "primary",
                "title": "Quarterly financial filing",
                "subtext": "Due 30 days post quarter-end"
            },
            {
                "pill_text": "Required",
                "pill_type": "green",
                "pill_icon": "check_circle",
                "sub_pill": "ANNUAL",
                "numeral": "YEAR END",
                "numeral_color": "primary",
                "title": "Annual Impact Narrative",
                "subtext": "Final grant closeout protocol"
            },
            {
                "pill_text": "Restriction",
                "pill_type": "terracotta",
                "pill_icon": "warning",
                "sub_pill": "BUDGET",
                "numeral": "10% CAP",
                "numeral_color": "secondary",
                "title": "Variance allowance",
                "subtext": "Written approval above $15k"
            }
        ],
        "sources": [
            {
                "doc_id": "DOC-01",
                "document_title": "GRANT GUIDELINES 2025",
                "citation_ref": "§ 5.1 Financial Disclosures · p. 8",
                "excerpt": "“...financial expenditure reports must be submitted within 30 days of quarter end via the authorized recipient management system...”",
                "border_color": "var(--folio-primary)",
                "evidence_id": "EV-01"
            },
            {
                "doc_id": "DOC-02",
                "document_title": "DONOR AGREEMENT #H-882",
                "citation_ref": "§ 7.2 Annual Evaluation · p. 14",
                "excerpt": "“...grantee agrees to provide a formal narrative impact report upon year end detailing measurable programmatic metrics and community cohort outcomes...”",
                "border_color": "var(--folio-terracotta)",
                "evidence_id": "EV-02"
            }
        ],
        "evidence_ref": "REF #EV-2025-419",
        "sub_note": "Full cross-referenced dossier compiled from original executed charters."
    },
    "What are the indirect costs rules?": {
        "query_normalized": "indirect costs",
        "question": "What are the indirect costs rules?",
        "editorial_headline": "INDIRECT COSTS & OVERHEAD POLICY",
        "answer_lead": "Indirect costs are strictly capped at 10% of total direct personnel expenditures.",
        "answer_body": "Any administrative overhead allocations exceeding this ceiling require prior written authorization. Contract Amendment Addendum A permits reallocations for field logistics up to $45,000 upon 5 days written notice.",
        "verified_count": "2 sources verified",
        "spec_badge": "PORTAL VERIFIED SPECIFICATION",
        "confidence_score": 0.95,
        "metrics": [
            {
                "pill_text": "Ceiling",
                "pill_type": "terracotta",
                "pill_icon": "lock",
                "sub_pill": "DIRECT",
                "numeral": "10% CAP",
                "numeral_color": "secondary",
                "title": "Personnel Overhead Limit",
                "subtext": "Direct personnel calculation"
            },
            {
                "pill_text": "Flexibility",
                "pill_type": "green",
                "pill_icon": "tune",
                "sub_pill": "ADDENDUM",
                "numeral": "$45,000",
                "numeral_color": "primary",
                "title": "Field Logistics Scope",
                "subtext": "Latin America cohort allowance"
            },
            {
                "pill_text": "Notification",
                "pill_type": "green",
                "pill_icon": "mail",
                "sub_pill": "NOTICE",
                "numeral": "5 DAYS",
                "numeral_color": "primary",
                "title": "Advance Written Filing",
                "subtext": "Filed with Grant Officer"
            }
        ],
        "sources": [
            {
                "doc_id": "DOC-01",
                "document_title": "GRANT GUIDELINES 2025",
                "citation_ref": "§ 4.3 Indirect costs ceiling · p. 8",
                "excerpt": "“...indirect costs are strictly capped at 10% of total direct personnel expenditures, unless specifically augmented by Addendum B...”",
                "border_color": "var(--folio-primary)",
                "evidence_id": "EV-01"
            },
            {
                "doc_id": "DOC-04",
                "document_title": "CONTRACT AMENDMENT ADDENDUM A",
                "citation_ref": "§ Clause 1 Reallocation Threshold · p. 2",
                "excerpt": "“...The Grantee is authorized to shift funds between Travel and Direct Operational Supplies up to a cumulative ceiling of $45,000 without requiring prior Board assembly...”",
                "border_color": "var(--folio-terracotta)",
                "evidence_id": "EV-04"
            }
        ],
        "evidence_ref": "REF #EV-2025-420",
        "sub_note": "Cross-referenced with Master Guidelines and Executed Addendum A."
    },
    "When is the annual impact report due?": {
        "query_normalized": "annual impact report due",
        "question": "When is the annual impact report due?",
        "editorial_headline": "ANNUAL IMPACT REPORT TIMELINE",
        "answer_lead": "The annual comprehensive impact narrative is due at the close of each 12-month funding period (January 30).",
        "answer_body": "Submissions must document qualitative beneficiary outcomes, verified outreach statistics, and be accompanied by independent certified auditor commentary prior to Year 2 tranche execution.",
        "verified_count": "2 sources verified",
        "spec_badge": "PORTAL VERIFIED SPECIFICATION",
        "confidence_score": 0.96,
        "metrics": [
            {
                "pill_text": "Closeout",
                "pill_type": "green",
                "pill_icon": "event",
                "sub_pill": "ANNUAL",
                "numeral": "YEAR END",
                "numeral_color": "primary",
                "title": "Narrative Filing Deadline",
                "subtext": "Within 30 days of cycle close"
            },
            {
                "pill_text": "Audit",
                "pill_type": "green",
                "pill_icon": "verified",
                "sub_pill": "CPA",
                "numeral": "AUDITED",
                "numeral_color": "primary",
                "title": "Third-Party Review",
                "subtext": "Independent attestation"
            },
            {
                "pill_text": "Tranche Gate",
                "pill_type": "terracotta",
                "pill_icon": "payments",
                "sub_pill": "YEAR 2",
                "numeral": "$312,500",
                "numeral_color": "secondary",
                "title": "Tranche Disbursement",
                "subtext": "Locked until board clearance"
            }
        ],
        "sources": [
            {
                "doc_id": "DOC-02",
                "document_title": "DONOR AGREEMENT #H-882",
                "citation_ref": "§ 7.2 Closeout Narrative · p. 14",
                "excerpt": "“...an annual impact report is required at the end of the funding period, documenting qualitative outcomes, beneficiary counts, and audited metrics...”",
                "border_color": "var(--folio-terracotta)",
                "evidence_id": "EV-02"
            },
            {
                "doc_id": "DOC-03",
                "document_title": "ANNUAL IMPACT REPORT 2025",
                "citation_ref": "Executive Summary · p. 2",
                "excerpt": "“...Year 1 programmatic deployment achieved 94% of targeted outreach indicators across regional implementation centers...”",
                "border_color": "var(--folio-primary)",
                "evidence_id": "EV-03"
            }
        ],
        "evidence_ref": "REF #EV-2025-421",
        "sub_note": "Governed by Agreement #H-882 Article 7 and Master Guidelines Section 5."
    },
    "What are the budget reallocation limits?": {
        "query_normalized": "budget reallocation limits",
        "question": "What are the budget reallocation limits?",
        "editorial_headline": "BUDGET LINE ITEM REALLOCATION",
        "answer_lead": "Standard line item variances exceeding 10% require prior written consent from the Foundation Board.",
        "answer_body": "Under Addendum A, travel and direct supplies in regional Latin America cohorts allow up to $45,000 flexibility upon 5 business days written notice to the Grant Officer.",
        "verified_count": "2 sources verified",
        "spec_badge": "PORTAL VERIFIED SPECIFICATION",
        "confidence_score": 0.94,
        "metrics": [
            {
                "pill_text": "Standard",
                "pill_type": "green",
                "pill_icon": "pie_chart",
                "sub_pill": "BASELINE",
                "numeral": "10% CAP",
                "numeral_color": "primary",
                "title": "General Variance Limit",
                "subtext": "Across major line items"
            },
            {
                "pill_text": "Addendum A",
                "pill_type": "green",
                "pill_icon": "check_circle",
                "sub_pill": "REGIONAL",
                "numeral": "$45,000",
                "numeral_color": "primary",
                "title": "Field Logistics Scope",
                "subtext": "Latin America cohort"
            },
            {
                "pill_text": "Notice",
                "pill_type": "terracotta",
                "pill_icon": "schedule",
                "sub_pill": "FILING",
                "numeral": "5 DAYS",
                "numeral_color": "secondary",
                "title": "Advance Written Notice",
                "subtext": "Prior to disbursement"
            }
        ],
        "sources": [
            {
                "doc_id": "DOC-04",
                "document_title": "CONTRACT AMENDMENT ADDENDUM A",
                "citation_ref": "§ Clause 1 Reallocation · p. 2",
                "excerpt": "“...The Grantee is authorized to shift funds between Travel and Direct Operational Supplies up to a cumulative ceiling of $45,000...”",
                "border_color": "var(--folio-terracotta)",
                "evidence_id": "EV-04"
            },
            {
                "doc_id": "DOC-01",
                "document_title": "GRANT GUIDELINES 2025",
                "citation_ref": "§ 4.3 Overhead & Allocation · p. 8",
                "excerpt": "“...Budget shifts exceeding 10% between categories require prior written consent...”",
                "border_color": "var(--folio-primary)",
                "evidence_id": "EV-01"
            }
        ],
        "evidence_ref": "REF #EV-2025-422",
        "sub_note": "Ratified under Addendum A and Master Guidelines."
    },
    "What are the financial audit requirements?": {
        "query_normalized": "financial audit requirements",
        "question": "What are the financial audit requirements?",
        "editorial_headline": "FINANCIAL AUDIT & GAAP GOVERNANCE",
        "answer_lead": "All grant accounts must be maintained according to GAAP with segregated dual-entry ledgers.",
        "answer_body": "An annual independent certified audit is required before Year 2 funding tranches are released. The Foundation reserves the right to conduct an independent financial review on 14 days notice.",
        "verified_count": "2 sources verified",
        "spec_badge": "PORTAL VERIFIED SPECIFICATION",
        "confidence_score": 0.97,
        "metrics": [
            {
                "pill_text": "Standard",
                "pill_type": "green",
                "pill_icon": "verified_user",
                "sub_pill": "MANDATORY",
                "numeral": "GAAP",
                "numeral_color": "primary",
                "title": "Accounting Standard",
                "subtext": "Dual-entry segregated ledgers"
            },
            {
                "pill_text": "Notice",
                "pill_type": "green",
                "pill_icon": "calendar_month",
                "sub_pill": "REVIEW",
                "numeral": "14 DAYS",
                "numeral_color": "primary",
                "title": "Funder Audit Window",
                "subtext": "Written notice protocol"
            },
            {
                "pill_text": "Threshold",
                "pill_type": "terracotta",
                "pill_icon": "inventory_2",
                "sub_pill": "CAPEX",
                "numeral": "$5,000+",
                "numeral_color": "secondary",
                "title": "Capital Equipment Tagging",
                "subtext": "Pre-approval required"
            }
        ],
        "sources": [
            {
                "doc_id": "DOC-05",
                "document_title": "FISCAL GOVERNANCE DIRECTIVES",
                "citation_ref": "§ 2.1 GAAP Compliance · p. 5",
                "excerpt": "“...All grant financial ledgers must be maintained in accordance with GAAP. Dual-entry accounting and segregated ledger accounts are mandatory...”",
                "border_color": "var(--folio-primary)",
                "evidence_id": "EV-05"
            },
            {
                "doc_id": "DOC-01",
                "document_title": "GRANT GUIDELINES 2025",
                "citation_ref": "§ 8.1 Periodic Review · p. 19",
                "excerpt": "“...The Foundation reserves the right to conduct an independent compliance and financial audit upon 14 calendar days written notice...”",
                "border_color": "var(--folio-primary)",
                "evidence_id": "EV-01"
            }
        ],
        "evidence_ref": "REF #EV-2025-423",
        "sub_note": "Institutional audit framework under Helios Fiscal Governance 2025."
    },
    "What happens if a reporting deadline is missed?": {
        "query_normalized": "reporting deadline missed",
        "question": "What happens if a reporting deadline is missed?",
        "editorial_headline": "DISBURSEMENT FREEZE & REMEDIATION",
        "answer_lead": "Failure to lodge quarterly financial reports within 30 days triggers an automatic disbursement freeze.",
        "answer_body": "Submissions received past the 30-day window undergo secondary compliance review before subsequent semi-annual tranches are released by the Governance Committee.",
        "verified_count": "2 sources verified",
        "spec_badge": "PORTAL VERIFIED SPECIFICATION",
        "confidence_score": 0.99,
        "metrics": [
            {
                "pill_text": "Sanction",
                "pill_type": "terracotta",
                "pill_icon": "block",
                "sub_pill": "AUTOMATIC",
                "numeral": "FREEZE",
                "numeral_color": "secondary",
                "title": "Disbursement Hold",
                "subtext": "Tranche payments paused"
            },
            {
                "pill_text": "Cutoff",
                "pill_type": "green",
                "pill_icon": "timer",
                "sub_pill": "WINDOW",
                "numeral": "30 DAYS",
                "numeral_color": "primary",
                "title": "Lodging Deadline",
                "subtext": "Strict calendar day limit"
            },
            {
                "pill_text": "Clearing",
                "pill_type": "green",
                "pill_icon": "approval",
                "sub_pill": "REVIEW",
                "numeral": "BOARD",
                "numeral_color": "primary",
                "title": "Governance Action",
                "subtext": "Secondary review required"
            }
        ],
        "sources": [
            {
                "doc_id": "DOC-01",
                "document_title": "GRANT GUIDELINES 2025",
                "citation_ref": "§ 5.1 Reporting Schedule · p. 8",
                "excerpt": "“...Failure to lodge within this designated timeframe triggers automatic payment withholding until reconciliation is satisfied by the board...”",
                "border_color": "var(--folio-primary)",
                "evidence_id": "EV-01"
            },
            {
                "doc_id": "DOC-02",
                "document_title": "DONOR AGREEMENT #H-882",
                "citation_ref": "§ 3.2 Pre-Conditions · p. 4",
                "excerpt": "“...No subsequent disbursement tranche will be authorized until the preceding period's financial filings and milestone narratives have been formally cleared...”",
                "border_color": "var(--folio-terracotta)",
                "evidence_id": "EV-02"
            }
        ],
        "evidence_ref": "REF #EV-2025-424",
        "sub_note": "Governed by Master Guidelines § 5.1 and Donor Agreement Article 3."
    }
}

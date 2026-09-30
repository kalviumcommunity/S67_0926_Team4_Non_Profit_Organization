"""Folio Platform - Mock Institutional Grant Documents Repository."""

from typing import List, Dict, Any

MOCK_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "DOC-01",
        "dossier_num": "01",
        "title": "GRANT GUIDELINES",
        "subtitle": "Helios Foundation General Terms 2025–26",
        "category": "Grant Guidelines",
        "organization": "Helios Foundation",
        "year": "2026",
        "pages": 32,
        "format": "PDF/A",
        "status": "Active",
        "status_badge_type": "primary",
        "ref_code": "REF #HG-25-A",
        "spine_color": "#1E382B",
        "doc_id_code": "HL-GDL-2025-V4",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "key_clauses": [
            {"section": "§ 5.1", "title": "Reporting Windows", "page": 8, "highlight": False},
            {"section": "§ 4.3", "title": "Indirect costs ceiling (10% Cap)", "page": 8, "highlight": True},
            {"section": "§ 8.2", "title": "Independent Audits & GAAP", "page": 19, "highlight": False},
            {"section": "§ 6.4", "title": "Travel & Field Allowances", "page": 12, "highlight": False},
        ],
        "metrics_block": {
            "type": "clauses_list",
        },
        "full_text": """
# HELIOS FOUNDATION GENERAL GRANT GUIDELINES (2025–2026)
**Document Ref: HL-GDL-2025-V4**
**Issued: January 2025 | Institutional Archival Copy**

---

### SECTION 4. FINANCIAL ALLOCATION AND ALLOWABLE EXPENDITURES

#### 4.1 General Expenditure Principles
Grant funds may only be disbursed for verified direct program activities delineated in the approved budget appendix. All accounting ledgers must follow standard Generally Accepted Accounting Principles (GAAP).

#### 4.2 Personnel and Contractor Fees
Salaries and contractor disbursements must correspond directly to time allocated towards milestone fulfillment. Detailed timesheets attested by program directors are required for audit trails.

#### 4.3 Indirect Costs and Administrative Overhead
Indirect costs and administrative overhead are strictly capped at 10% of total direct personnel expenditures, unless specifically augmented by Addendum B or authorized by the Foundation Board in writing. Any overhead allocation exceeding this threshold without prior authorization will result in an immediate funding hold.

---

### SECTION 5. REPORTING SCHEDULE AND DISBURSEMENT CONDITIONS

#### 5.1 Quarterly Financial Filings
The Grantee shall submit quarterly expenditure reports, prepared according to GAAP standards and attested by an authorized financial controller. Quarterly financial reports must be submitted within 30 DAYS following the close of each calendar quarter. Failure to lodge within this designated timeframe triggers automatic payment withholding until reconciliation is satisfied by the board.

#### 5.2 Reporting Deadlines Schedule
- Q1 Report: Due April 30
- Q2 Report: Due July 30
- Q3 Report: Due October 30
- Q4 / Annual Reconciliation: Due January 30

#### 5.3 Currency and Exchange Adjustments
All expenditures incurred in non-USD currencies must use the interbank spot rate recorded on the date of transaction or the certified monthly weighted average.

---

### SECTION 8. AUDIT PROTOCOLS & GOVERNANCE

#### 8.1 Periodic Review
The Foundation reserves the right to conduct an independent compliance and financial audit upon 14 calendar days written notice.
        """
    },
    {
        "id": "DOC-02",
        "dossier_num": "02",
        "title": "DONOR AGREEMENT",
        "subtitle": "Grant Agreement Ref #H-882-01",
        "category": "Donor Agreements",
        "organization": "Helios Foundation & Grantee Compact",
        "year": "2025",
        "pages": 18,
        "format": "Countersigned",
        "status": "Fully Executed",
        "status_badge_type": "primary",
        "ref_code": "REF #H-882-01",
        "spine_color": "#DDD7CA",
        "seal": "SEAL: EXEC-VERIFIED",
        "doc_id_code": "AGR-H882-2024-FINAL",
        "sha256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
        "obligation_matrix": {
            "amount": "$1,250,000",
            "term": "Term: 24 Months (2025–2027)",
            "note": "“Subject to bi-annual disbursement verification by Board of Trustees.”"
        },
        "key_clauses": [
            {"section": "§ 3.1", "title": "Disbursement Schedule", "page": 4, "highlight": False},
            {"section": "§ 7.2", "title": "Annual Evaluation & Closeout", "page": 14, "highlight": True},
            {"section": "§ 9.1", "title": "Indirect Cost Waivers", "page": 14, "highlight": True},
        ],
        "full_text": """
# BILATERAL DONOR COMPACT & GRANT AGREEMENT #H-882
**Executed: November 18, 2024 | Between Helios Foundation & Lead Grantee Institution**

---

### ARTICLE 3. TRANCHE SCHEDULE & DISBURSEMENT PREREQUISITES

#### 3.1 Total Grant Commitment
The Funder commits a total sum of $1,250,000 across a 24-month lifecycle, payable in four (4) equal semi-annual tranches of $312,500, contingent upon satisfactory milestone verification.

#### 3.2 Pre-Conditions for Subsequent Tranches
No subsequent disbursement tranche will be authorized until the preceding period's financial filings and milestone narratives have been formally reviewed and cleared by the Governance Committee.

---

### ARTICLE 7. ANNUAL IMPACT REPORTING & EVALUATION

#### 7.1 Mid-Year Checkpoint
A concise mid-year progress memo must be submitted within 15 days of the midpoint of each project operating cycle.

#### 7.2 Closeout Narrative
In addition to routine periodic ledgers, an annual impact report is required at the end of the funding period, documenting qualitative outcomes, beneficiary counts, and audited metrics. The annual packet shall be accompanied by an independent auditor's commentary. No subsequent multi-year tranches will execute prior to committee approval of the Year-End Summary Narrative.

---

### ARTICLE 9. ADMINISTRATIVE LIMITATIONS & INDIRECT COSTS

#### 9.1 Indirect Costs Ceiling
Administrative and indirect costs exceeding allowable ceiling require written waiver prior to Year 2 tranche release. The standard rate is set at 10% direct costs.
        """
    },
    {
        "id": "DOC-03",
        "dossier_num": "03",
        "title": "ANNUAL IMPACT REPORT",
        "subtitle": "Year 1 Milestone & Metric Outcomes",
        "category": "Impact Reports",
        "organization": "Program Evaluation Office",
        "year": "2025",
        "pages": 24,
        "format": "Audited",
        "status": "Approved",
        "status_badge_type": "primary",
        "ref_code": "PUB: ED-2025-Q4",
        "spine_color": "#E4E2DE",
        "seal": "SEAL: AUDITED-2025",
        "doc_id_code": "REP-IMP-2025-Y1",
        "sha256": "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
        "milestone_ledger": {
            "completed": "3 milestones completed",
            "pending": "1 milestone pending",
            "progress": 75
        },
        "key_clauses": [
            {"section": "§ 1.2", "title": "Beneficiary Outreach Totals", "page": 4, "highlight": False},
            {"section": "§ 3.4", "title": "Budget Variance Ledger", "page": 16, "highlight": False},
            {"section": "§ 5.1", "title": "Program KPI Attainment", "page": 21, "highlight": True},
        ],
        "full_text": """
# ANNUAL IMPACT REPORT: YEAR 1 MILESTONE REVIEW
**Helios Community Innovation Portfolio | Published Q4 2025**

---

### EXECUTIVE SUMMARY
Year 1 of the Grant Agreement #H-882 programmatic deployment achieved 94% of targeted outreach indicators across regional implementation centers. Total direct beneficiaries reached: 42,800 individuals.

---

### MILESTONE COMPLETION SUMMARY
1. **Milestone 1.1 (Community Clinic Mobile Units):** COMPLETED (100% operational).
2. **Milestone 1.2 (Healthcare Provider Training):** COMPLETED (320 practitioners certified).
3. **Milestone 1.3 (Digital Diagnostic Rollout):** COMPLETED (14 rural partner clinics connected).
4. **Milestone 1.4 (Secondary Longitudinal Outcome Study):** IN PROGRESS (Target completion Q2 2026).

---

### FINANCIAL RECONCILIATION SUMMARY
Total Year 1 expenditure: $598,400 against $625,000 allocated tranche. Variance under budget: 4.25% ($26,600 reserved for longitudinal data collection).
        """
    },
    {
        "id": "DOC-04",
        "dossier_num": "04",
        "title": "CONTRACT AMENDMENT",
        "subtitle": "Addendum A: Reallocation Authorization",
        "category": "Contracts & Amendments",
        "organization": "Helios Legal & Compliance",
        "year": "2025",
        "pages": 6,
        "format": "Sign-off: Nov 14",
        "status": "Active Amendment",
        "status_badge_type": "terracotta",
        "ref_code": "AUTH: AMEND-01",
        "spine_color": "#D96B43",
        "seal": "Verified Legal Ratification",
        "doc_id_code": "AMD-2025-01-REALLOC",
        "sha256": "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4",
        "executive_scope": "Extends travel & supply budget flexibility up to $45,000 across Latin America project cohorts.",
        "key_clauses": [
            {"section": "§ 2.1", "title": "Budget Line Item Shifts", "page": 2, "highlight": True},
            {"section": "§ 3.2", "title": "Field Travel Cap Adjustment", "page": 4, "highlight": False},
        ],
        "full_text": """
# CONTRACT AMENDMENT ADDENDUM A
**Authorization for Reallocation & Scope Adjustment | November 14, 2025**

---

### RECITALS
Pursuant to Article 12 of Grant Agreement #H-882, the parties hereby execute this formal Addendum modifying the line item reallocation constraints.

### CLAUSE 1: REALLOCATION THRESHOLD
Section 4.3 of the Master Guidelines is modified solely with respect to Regional Latin America field logistics. The Grantee is authorized to shift funds between Travel and Direct Operational Supplies up to a cumulative ceiling of $45,000 without requiring prior Board convened assembly, provided 5 business days written notice is filed with the Grant Officer.

### CLAUSE 2: PRESERVATION OF REMAINING TERMS
All other stipulations, including the 10% indirect costs ceiling and 30-day quarterly filing requirements, remain in full binding effect.
        """
    },
    {
        "id": "DOC-05",
        "dossier_num": "05",
        "title": "FISCAL GOVERNANCE DIRECTIVES",
        "subtitle": "Quarterly Accounting & Capital Expenditure Guide",
        "category": "Grant Guidelines",
        "organization": "Helios Foundation",
        "year": "2025",
        "pages": 20,
        "format": "PDF/A",
        "status": "Active",
        "status_badge_type": "primary",
        "ref_code": "REF #QF-25-B",
        "spine_color": "#1E382B",
        "doc_id_code": "HL-FGOV-2025",
        "sha256": "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0",
        "key_clauses": [
            {"section": "§ 2.1", "title": "GAAP Compliance Protocol", "page": 5, "highlight": False},
            {"section": "§ 3.4", "title": "Equipment Capitalization ($5,000+)", "page": 11, "highlight": True},
            {"section": "§ 6.1", "title": "Unspent Balance Clawback", "page": 17, "highlight": False},
        ],
        "full_text": """
# QUARTERLY FISCAL GOVERNANCE DIRECTIVES 2025
**Helios Grantee Compliance Handbook**

---

### 1. ACCOUNTING STANDARDS
All grant financial ledgers must be maintained in accordance with GAAP. Dual-entry accounting and segregated ledger accounts for grant proceeds are mandatory.

### 2. CAPITAL EXPENDITURES
Any single equipment item exceeding $5,000 in acquisition value requires pre-approval and asset tracking tagging. Title to capital equipment remains with the Project unless otherwise conveyed.
        """
    },
    {
        "id": "DOC-06",
        "dossier_num": "06",
        "title": "FELLOWSHIP COMPACT #F-412",
        "subtitle": "Community Leadership Fellowship Agreement",
        "category": "Donor Agreements",
        "organization": "Helios Education Trust",
        "year": "2025",
        "pages": 14,
        "format": "Countersigned",
        "status": "Fully Executed",
        "status_badge_type": "primary",
        "ref_code": "REF #F-412-2025",
        "spine_color": "#DDD7CA",
        "seal": "SEAL: EXEC-FELLOW",
        "doc_id_code": "CMP-F412-2025",
        "sha256": "c8d9e0f1a2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d",
        "obligation_matrix": {
            "amount": "$850,000",
            "term": "Term: 18 Months (2025–2026)",
            "note": "“Stipend disbursements released on bi-monthly cohort attendance verification.”"
        },
        "key_clauses": [
            {"section": "§ 2.4", "title": "Fellow Stipend Allocations", "page": 6, "highlight": False},
            {"section": "§ 5.2", "title": "Quarterly Milestone Reviews", "page": 10, "highlight": True},
        ],
        "full_text": """
# COMMUNITY LEADERSHIP FELLOWSHIP COMPACT #F-412
**Helios Education Trust & Institutional Fellow Alliance**

---

### OBLIGATIONS & STIPEND SCHEDULE
Funding commitment of $850,000 to support 25 regional grassroots leaders. Disbursements occur bi-monthly against verified participation records.
        """
    }
]

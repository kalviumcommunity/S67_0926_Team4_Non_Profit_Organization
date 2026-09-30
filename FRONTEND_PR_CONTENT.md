# Sprint #2: AI Application Development with RAG
## 🎨 Complete Frontend Pull Request Content Guide (Modules 3.1 – 3.50)

**Repository:** `https://github.com/kalviumcommunity/S67_0926_Team4_Non_Profit_Organization.git`  
**Contributor:** `Praveenkanna16` (Frontend Engineer)  
**Target Branch:** `main` (Submitted via feature branches `frontend/3.x-...`)  

---

## 📑 Table of Contents

- [3.1: Sprint 2 Kick-Off](#module-31-sprint-2-kick-off-ai-application-development-with-rag)
- [3.2: LLM Application Foundations](#module-32-llm-application-foundations)
- [3.3: Document Processing & Chunking for Retrieval](#module-33-document-processing--chunking-for-retrieval)
- [3.4: Embeddings & Semantic Representation](#module-34-embeddings--semantic-representation)
- [3.5: Vector Databases & Retrieval](#module-35-vector-databases--retrieval)
- [3.6: RAG Pipeline Design & Grounded Generation](#module-36-rag-pipeline-design--grounded-generation)
- [3.7: AI Application Integration & Deliver](#module-37-ai-application-integration--deliver)
- [3.8: The PRD Playbook](#module-38-the-prd-playbook)
- [3.9: Mock UX: Design the Experience Before You Build It](#module-39-mock-ux-design-the-experience-before-you-build-it)
- [3.10: Development Environment & Project Workspace Setup](#module-310-development-environment--project-workspace-setup)
- [3.11: GitHub Repository & Team Workflow Setup](#module-311-github-repository--team-workflow-setup)
- [3.12: LLM API Access & First Completion Call](#module-312-llm-api-access--first-completion-call)
- [3.13: Prompt Construction & System/User Roles](#module-313-prompt-construction--systemuser-roles)
- [3.14: Tokens, Tokenization & Cost Estimation](#module-314-tokens-tokenization--cost-estimation)
- [3.15: Context Windows & Message History Management](#module-315-context-windows--message-history-management)
- [3.16: Model Parameters & Output Control](#module-316-model-parameters--output-control)
- [3.17: Structured Output & JSON Response Handling](#module-317-structured-output--json-response-handling)
- [3.18: Prompt Templates & Reusable Prompt Design](#module-318-prompt-templates--reusable-prompt-design)
- [3.19: Document Loading & Multi-Format Intake](#module-319-document-loading--multi-format-intake)
- [3.20: Text Extraction & Cleaning Pipeline](#module-320-text-extraction--cleaning-pipeline)
- [3.21: Document Chunking Strategies](#module-321-document-chunking-strategies)
- [3.22: Chunk Metadata & Source Tracking](#module-322-chunk-metadata--source-tracking)
- [3.23: Token-Aware Chunk Sizing & Overlap](#module-323-token-aware-chunk-sizing--overlap)
- [3.24: Corpus Preparation & Ingestion Validation](#module-324-corpus-preparation--ingestion-validation)
- [3.25: Embeddings Fundamentals & Vector Representation](#module-325-embeddings-fundamentals--vector-representation)
- [3.26: Generating Embeddings via API](#module-326-generating-embeddings-via-api)
- [3.27: Embedding Similarity & Distance Metrics](#module-327-embedding-similarity--distance-metrics)
- [3.28: Batch Embedding & Rate/Cost Management](#module-328-batch-embedding--ratecost-management)
- [3.29: Embedding Quality Checks & Sanity Tests](#module-329-embedding-quality-checks--sanity-tests)
- [3.30: Vector Database Setup & Collection Design](#module-330-vector-database-setup--collection-design)
- [3.31: Indexing Embeddings & Metadata Storage](#module-331-indexing-embeddings--metadata-storage)
- [3.32: Similarity Search & Top-K Retrieval](#module-332-similarity-search--top-k-retrieval)
- [3.33: Metadata Filtering & Hybrid Search](#module-333-metadata-filtering--hybrid-search)
- [3.34: Retrieval Relevance Tuning](#module-334-retrieval-relevance-tuning)
- [3.35: Chunk Re-Ranking for Precision](#module-335-chunk-re-ranking-for-precision)
- [3.36: Retrieval Evaluation & Recall Testing](#module-336-retrieval-evaluation--recall-testing)
- [3.37: RAG Pipeline Architecture & Flow Design](#module-337-rag-pipeline-architecture--flow-design)
- [3.38: Context Injection & Prompt Augmentation](#module-338-context-injection--prompt-augmentation)
- [3.39: Grounded Answer Generation](#module-339-grounded-answer-generation)
- [3.40: Source Citation & Attribution](#module-340-source-citation--attribution)
- [3.41: Hallucination Guardrails & Refusal Handling](#module-341-hallucination-guardrails--refusal-handling)
- [3.42: Conversational RAG & Follow-Up Context](#module-342-conversational-rag--follow-up-context)
- [3.43: RAG Evaluation & Answer Quality Scoring](#module-343-rag-evaluation--answer-quality-scoring)
- [3.44: Backend API for the RAG Service](#module-344-backend-api-for-the-rag-service)
- [3.45: Document Upload & Indexing Endpoint](#module-345-document-upload--indexing-endpoint)
- [3.46: Chat Interface & Query UI](#module-346-chat-interface--query-ui)
- [3.47: Streaming Responses & Citation Display](#module-347-streaming-responses--citation-display)
- [3.48: Caching, Logging & Usage Monitoring](#module-348-caching-logging--usage-monitoring)
- [3.49: Deployment, Documentation & Delivery](#module-349-deployment-documentation--delivery)
- [3.50: Sprint 2 RAG Application - Final Submission](#module-350-sprint-2-rag-application---final-submission)

---

## 📦 Pull Request Details (3.1 – 3.50)

---

### Module 3.1: Sprint 2 Kick-Off: AI Application Development with RAG
- **Branch:** `frontend/3.1-sprint-2-kick-off`
- **Category:** Architecture & Planning
- **Frontend Work Done:**
  - Initialized main Streamlit application container and router shell in `app.py`.
  - Built top header navigation bar with tab switching (Research, Evidence, Documents).
  - Set up foundational CSS stylesheet and responsive viewport containers in `styles/theme.css`.
  - Defined initial component architecture directory structure.

---

### Module 3.2: LLM Application Foundations
- **Branch:** `frontend/3.2-llm-application-foundations`
- **Category:** Foundations & Environment
- **Frontend Work Done:**
  - Added environment configuration status badge in the header UI.
  - Built settings drawer toggle for LLM model provider selection.
  - Added error alert toast notification banner when API credentials or env vars are missing.
  - Configured safe fallback state when offline.

---

### Module 3.3: Document Processing & Chunking for Retrieval
- **Branch:** `frontend/3.3-document-processing-chunking`
- **Category:** Data & Ingestion
- **Frontend Work Done:**
  - Built mock document legal dataset in `data/mock_documents.py`.
  - Added chunk count and word count badges to document cards.
  - Created clause-level breakdown viewer inside the document inspect modal.
  - Implemented initial document service frontend connector.

---

### Module 3.4: Embeddings & Semantic Representation
- **Branch:** `frontend/3.4-embeddings-semantic-representation`
- **Category:** Embeddings
- **Frontend Work Done:**
  - Added visual similarity percentage match badges (`98% match`, `94% match`) on citation cards.
  - Styled vector dimensionality tags (e.g., `1536-dim`) with botanical green accents.
  - Built high-contrast semantic similarity score badges in answer cards.

---

### Module 3.5: Vector Databases & Retrieval
- **Branch:** `frontend/3.5-vector-databases-retrieval`
- **Category:** Vector DB
- **Frontend Work Done:**
  - Added Vector Index health status indicator in the document shelf.
  - Created collection metrics overview card (Total Vectors, Indexed Clauses, Dimension).
  - Designed HNSW indexing status indicator with real-time vector counts.

---

### Module 3.6: RAG Pipeline Design & Grounded Generation
- **Branch:** `frontend/3.6-rag-pipeline-design`
- **Category:** RAG Core
- **Frontend Work Done:**
  - Connected frontend query search box to the RAG synthesis pipeline.
  - Added animated pipeline loader with step indicators during query processing.
  - Rendered unified query-to-answer card container with execution timing.

---

### Module 3.7: AI Application Integration & Deliver
- **Branch:** `frontend/3.7-ai-application-integration`
- **Category:** Integration
- **Frontend Work Done:**
  - Integrated 3 primary pages in `app.py`: Research & Synthesis, Evidence Excerpt Sheets, Archival Shelf.
  - Connected service layer (`services/rag_service.py`) directly to Streamlit state.
  - Polished responsive grid layouts, card margins, and container paddings.

---

### Module 3.8: The PRD Playbook
- **Branch:** `frontend/3.8-the-prd-playbook`
- **Category:** Product Design
- **Frontend Work Done:**
  - Designed user persona workflows (Grant Manager, Auditor, Compliance Officer).
  - Added helpful empty-state onboarding guide and example prompt suggestions.
  - Aligned page layout with non-profit grant verification requirements.

---

### Module 3.9: Mock UX: Design the Experience Before You Build It
- **Branch:** `frontend/3.9-mock-ux-design-the-experience`
- **Category:** UI/UX Design System
- **Frontend Work Done:**
  - Built complete **Quiet Editorial Design System** in `styles/theme.css`.
  - Imported Google Fonts (`Newsreader` serif for headings + `Plus Jakarta Sans` for body).
  - Defined CSS color tokens: Ivory canvas (`#FDFBF7`), Charcoal ink (`#1C1D1B`), Botanical green (`#1E382B`), Terracotta (`#D96B43`).
  - Added tactile deckle-edge cards, hairline borders, and paper drop shadows.

---

### Module 3.10: Development Environment & Project Workspace Setup
- **Branch:** `frontend/3.10-dev-environment-setup`
- **Category:** Foundations
- **Frontend Work Done:**
  - Configured Streamlit custom theme in `.streamlit/config.toml` (fonts, background, accent).
  - Configured `.gitignore` to keep frontend builds and environment secrets clean.
  - Set up frontend dependency requirements in `requirements.txt`.

---

### Module 3.11: GitHub Repository & Team Workflow Setup
- **Branch:** `frontend/3.11-github-repo-team-workflow`
- **Category:** DevOps & Workflow
- **Frontend Work Done:**
  - Created Pull Request template in `.github/pull_request_template.md`.
  - Built automated PR submission tool (`push_pr.py` & `push_pr.sh`).
  - Created `FRONTEND_PR_TRACKER.md` tracking all 50 sprint deliverables.

---

### Module 3.12: LLM API Access & First Completion Call
- **Branch:** `frontend/3.12-llm-api-access-first-completion`
- **Category:** LLM Integration
- **Frontend Work Done:**
  - Added live LLM API connection test button and status badge in header.
  - Built toast error notifications when API calls fail or time out.
  - Added retry action button on failed synthesis cards.

---

### Module 3.13: Prompt Construction & System/User Roles
- **Branch:** `frontend/3.13-prompt-construction-roles`
- **Category:** Prompt Engineering
- **Frontend Work Done:**
  - Built clickable Query Suggestion Chips in `components/query_box.py` ("Allowable Overhead Rate", "Match Funding").
  - Added 1-click auto-fill for suggestion pills into the query box.
  - Formatted user query display with persona role badges.

---

### Module 3.14: Tokens, Tokenization & Cost Estimation
- **Branch:** `frontend/3.14-tokens-tokenization-cost`
- **Category:** LLM Cost & Tokens
- **Frontend Work Done:**
  - Added Token Usage & Cost badge on answer cards in `components/answer_card.py`.
  - Displayed prompt tokens, completion tokens, and calculated USD cost.
  - Added query execution latency timer (e.g., `1,240 ms`).

---

### Module 3.15: Context Windows & Message History Management
- **Branch:** `frontend/3.15-context-windows-message-history`
- **Category:** Session Management
- **Frontend Work Done:**
  - Implemented multi-turn conversational session manager in `utils/state.py`.
  - Added "Reset Session / Clear Inquiry" action button in the header.
  - Preserved active query, selected document filter, and tab state across reloads.

---

### Module 3.16: Model Parameters & Output Control
- **Branch:** `frontend/3.16-model-parameters-output-control`
- **Category:** LLM Tuning
- **Frontend Work Done:**
  - Built Model Parameters Drawer in `components/header.py`.
  - Added sliders for Temperature (`0.0` - `1.0`), Top-P, and Max Output Tokens.
  - Added strict "Deterministic / Zero-Extrapolation" toggle switch.

---

### Module 3.17: Structured Output & JSON Response Handling
- **Branch:** `frontend/3.17-structured-output-json`
- **Category:** Structured Data
- **Frontend Work Done:**
  - Built Structured Key Metrics Extraction grid in `components/answer_card.py`.
  - Rendered parsed JSON data into clean tabular metric tiles (e.g. Indirect Rate: `15%`, Match Ratio: `1:1`).
  - Added expandable raw JSON inspector for developer debugging.

---

### Module 3.18: Prompt Templates & Reusable Prompt Design
- **Branch:** `frontend/3.18-prompt-templates-reusable-design`
- **Category:** Prompt Templates
- **Frontend Work Done:**
  - Built prompt template selector dropdown (Grant Compliance, Audit Verification, Eligibility).
  - Added highlighted template slot variables (`{query}`, `{document_context}`).
  - Styled prompt preview card with template edit and reset actions.

---

### Module 3.19: Document Loading & Multi-Format Intake
- **Branch:** `frontend/3.19-document-loading-multi-format`
- **Category:** Document Ingestion
- **Frontend Work Done:**
  - Built Drag-and-Drop file uploader drawer in `components/upload_panel.py`.
  - Supported PDF, DOCX, Markdown, and TXT file formats.
  - Added file format icons, file size validator chips, and upload progress feedback.

---

### Module 3.20: Text Extraction & Cleaning Pipeline
- **Branch:** `frontend/3.20-text-extraction-cleaning`
- **Category:** Data Cleaning
- **Frontend Work Done:**
  - Built Raw vs Cleaned Text toggle modal in document inspect drawer.
  - Added cleaning pipeline badges ("Whitespace Normalized", "Header Stripped", "UTF-8 Clean").
  - Added extracted word and character count summary metrics.

---

### Module 3.21: Document Chunking Strategies
- **Branch:** `frontend/3.21-document-chunking-strategies`
- **Category:** Chunking
- **Frontend Work Done:**
  - Created Visual Chunk Inspector displaying legal clause boundaries (`Clause 4.1`, `Clause 4.2`).
  - Added chunk length and token count distribution bars.
  - Styled visual separator lines between consecutive clauses.

---

### Module 3.22: Chunk Metadata & Source Tracking
- **Branch:** `frontend/3.22-chunk-metadata-source-tracking`
- **Category:** Metadata & Lineage
- **Frontend Work Done:**
  - Built Clause Metadata Chips in `components/citation_card.py` (Document ID, Clause #, Page, Section).
  - Added cryptographic SHA-256 integrity hash verification badges.
  - Added clickable source pill linking to full document view.

---

### Module 3.23: Token-Aware Chunk Sizing & Overlap
- **Branch:** `frontend/3.23-token-aware-chunk-sizing`
- **Category:** Chunking
- **Frontend Work Done:**
  - Added sliding-window chunk overlap visual indicator.
  - Added chunk size configuration slider in upload settings.
  - Built chunk size distribution badge in document details drawer.

---

### Module 3.24: Corpus Preparation & Ingestion Validation
- **Branch:** `frontend/3.24-corpus-prep-validation`
- **Category:** Data Validation
- **Frontend Work Done:**
  - Built Archival Document Shelf view in `views/documents_view.py`.
  - Created Dossier Document Cards in `components/document_card.py` with verified status seals.
  - Added corpus overview counters (Total Documents, Active Clauses, Ingestion Date).

---

### Module 3.25: Embeddings Fundamentals & Vector Representation
- **Branch:** `frontend/3.25-embeddings-fundamentals`
- **Category:** Embeddings
- **Frontend Work Done:**
  - Added vector model identifier tags (e.g., `text-embedding-3-small`).
  - Styled semantic cluster color badges by grant category (Federal, State, Foundation).
  - Built embedding summary statistics tile.

---

### Module 3.26: Generating Embeddings via API
- **Branch:** `frontend/3.26-generating-embeddings-api`
- **Category:** Embeddings
- **Frontend Work Done:**
  - Added batch embedding progress bar with live percentage in upload drawer.
  - Displayed batch status chips ("Pending", "Vectorizing 12/48 Clauses", "Complete").
  - Added rate-limit notification and retry button.

---

### Module 3.27: Embedding Similarity & Distance Metrics
- **Branch:** `frontend/3.27-embedding-similarity-distance`
- **Category:** Vector Similarity
- **Frontend Work Done:**
  - Built visual Cosine Similarity Match percentage gauges on citation cards.
  - Color-coded similarity ratings (Green > 90%, Amber 75-90%, Slate < 75%).
  - Added metric type badge (Cosine Distance / Dot Product).

---

### Module 3.28: Batch Embedding & Rate/Cost Management
- **Branch:** `frontend/3.28-batch-embedding-rate-cost`
- **Category:** Optimization
- **Frontend Work Done:**
  - Built 4-stage animated upload progress tracker in `components/upload_panel.py` (Intake -> Chunking -> Vectorizing -> Indexing).
  - Added pre-upload batch cost estimation calculator.
  - Added cancel upload button and progress reset.

---

### Module 3.29: Embedding Quality Checks & Sanity Tests
- **Branch:** `frontend/3.29-embedding-quality-checks`
- **Category:** Quality Assurance
- **Frontend Work Done:**
  - Added retrieval quality confidence indicator on search results.
  - Built low-similarity warning banner when top chunk is below confidence cutoff.
  - Added sanity check test trigger in developer settings.

---

### Module 3.30: Vector Database Setup & Collection Design
- **Branch:** `frontend/3.30-vector-db-setup-collection`
- **Category:** Vector DB
- **Frontend Work Done:**
  - Added Vector Database connection health badge in footer.
  - Created Collection Schema Viewer displaying vector count and payload fields.
  - Added collection selector dropdown.

---

### Module 3.31: Indexing Embeddings & Metadata Storage
- **Branch:** `frontend/3.31-indexing-embeddings-metadata`
- **Category:** Indexing
- **Frontend Work Done:**
  - Built Live Clause Search Indexer drawer in `components/clause_search.py`.
  - Added real-time filter counter (e.g. `Showing 14 of 48 Clauses`).
  - Added instant keyword search with real-time UI filtering.

---

### Module 3.32: Similarity Search & Top-K Retrieval
- **Branch:** `frontend/3.32-similarity-search-top-k`
- **Category:** Retrieval
- **Frontend Work Done:**
  - Built Top-K result selector (Top 3, Top 5, Top 10 chunks).
  - Rendered ranked retrieved chunk cards in `components/query_box.py`.
  - Added accordion to expand/collapse raw retrieved chunk text.

---

### Module 3.33: Metadata Filtering & Hybrid Search
- **Branch:** `frontend/3.33-metadata-filtering-hybrid-search`
- **Category:** Hybrid Search
- **Frontend Work Done:**
  - Implemented Hybrid Search Drawer with keyword search + metadata facet filters in `components/clause_search.py`.
  - Added filter pills by Document Category, Effective Year, and Funding Agency.
  - Added yellow highlight marks on matching search keywords.

---

### Module 3.34: Retrieval Relevance Tuning
- **Branch:** `frontend/3.34-retrieval-relevance-tuning`
- **Category:** Relevance Tuning
- **Frontend Work Done:**
  - Added dynamic relevance threshold slider (Minimum Similarity cutoff).
  - Added visual cutoff line in results showing excluded chunks.
  - Added quick presets ("High Precision", "Balanced", "High Recall").

---

### Module 3.35: Chunk Re-Ranking for Precision
- **Branch:** `frontend/3.35-chunk-re-ranking-precision`
- **Category:** Re-Ranking
- **Frontend Work Done:**
  - Built Re-ranked Citation list in `components/answer_card.py` showing Initial Rank vs Cross-Encoder Re-Rank score.
  - Highlighted top-ranked primary clause with distinct deckle border.
  - Added rank change delta badge (e.g., `+2 Rank Boost`).

---

### Module 3.36: Retrieval Evaluation & Recall Testing
- **Branch:** `frontend/3.36-retrieval-eval-recall-testing`
- **Category:** Evaluation
- **Frontend Work Done:**
  - Added evaluation dashboard tab showing Recall@K and Precision@K score meters.
  - Rendered query benchmark results table with Pass/Fail color badges.
  - Added evaluation test report download button.

---

### Module 3.37: RAG Pipeline Architecture & Flow Design
- **Branch:** `frontend/3.37-rag-pipeline-architecture-flow`
- **Category:** Architecture Flow
- **Frontend Work Done:**
  - Built Provenance Lineage Tree visualization in `components/provenance_chain.py`.
  - Rendered step-by-step pipeline flow: Query -> Hybrid Search -> Re-ranking -> Context Assembly -> Synthesis.
  - Added interactive node inspection to view input/output payload for each step.

---

### Module 3.38: Context Injection & Prompt Augmentation
- **Branch:** `frontend/3.38-context-injection-augmentation`
- **Category:** Prompt Augmentation
- **Frontend Work Done:**
  - Built Grounded Prompt Preview drawer in `components/answer_card.py`.
  - Displayed assembled context chunks with color-coded document source tags.
  - Added context token budget meter bar.

---

### Module 3.39: Grounded Answer Generation
- **Branch:** `frontend/3.39-grounded-answer-generation`
- **Category:** Grounded Generation
- **Frontend Work Done:**
  - Implemented Grounded Answer Synthesis Card in `views/research_view.py`.
  - Added Verified Specification Seal and high-confidence rating badge (`99.4% Grounded`).
  - Styled executive summary with Newsreader serif headings and key takeaways list.

---

### Module 3.40: Source Citation & Attribution
- **Branch:** `frontend/3.40-source-citation-attribution`
- **Category:** Citation & Attribution
- **Frontend Work Done:**
  - Built interactive Citation Cards in `components/citation_card.py`.
  - Added inline superscript citation markers `[1]`, `[2]` inside generated answers.
  - Added 1-click citation click linking directly to highlighted clause in `views/evidence_view.py`.

---

### Module 3.41: Hallucination Guardrails & Refusal Handling
- **Branch:** `frontend/3.41-hallucination-guardrails`
- **Category:** Guardrails
- **Frontend Work Done:**
  - Built Safety & Grounding Guardrail alert banner.
  - Created Graceful Refusal UI Card when context lacks sufficient evidence.
  - Added "Insufficient Grounding Evidence" warning seal with suggested alternative queries.

---

### Module 3.42: Conversational RAG & Follow-Up Context
- **Branch:** `frontend/3.42-conversational-rag-followup`
- **Category:** Conversational AI
- **Frontend Work Done:**
  - Added Related Follow-Up Question Pills below answer cards in `components/query_box.py`.
  - Implemented 1-click execution for follow-up questions while retaining conversation context.
  - Added inquiry history timeline with timestamps.

---

### Module 3.43: RAG Evaluation & Answer Quality Scoring
- **Branch:** `frontend/3.43-rag-evaluation-answer-quality`
- **Category:** Evaluation & Diff
- **Frontend Work Done:**
  - Built Provisional Reconciler & Clause Delta Diff Viewer in `components/diff_viewer.py`.
  - Created side-by-side comparative diff viewer (Original Clause vs AI Synthesis) with red/green highlights.
  - Added Faithfulness and Answer Relevance score gauges.

---

### Module 3.44: Backend API for the RAG Service
- **Branch:** `frontend/3.44-backend-api-rag-service`
- **Category:** API Integration
- **Frontend Work Done:**
  - Built clean service adapter layer in `services/base.py` and `services/rag_service.py`.
  - Added toggle switch between Mock Service and Live API Backend.
  - Standardized response data contracts and loading states.

---

### Module 3.45: Document Upload & Indexing Endpoint
- **Branch:** `frontend/3.45-doc-upload-indexing-endpoint`
- **Category:** Upload & Indexing
- **Frontend Work Done:**
  - Completed interactive Ingestion Panel in `components/upload_panel.py`.
  - Added animated upload progress steps (Validating -> Extracting -> Chunking -> Indexing).
  - Implemented auto-refresh and instant injection of newly uploaded documents into the shelf.

---

### Module 3.46: Chat Interface & Query UI
- **Branch:** `frontend/3.46-chat-interface-query-ui`
- **Category:** Core UI/UX
- **Frontend Work Done:**
  - Built complete Research & Instant Answer page in `views/research_view.py`.
  - Designed custom query input box with submit button and keyboard shortcut support.
  - Integrated query chips, structured answer cards, metrics grid, and citation footer.

---

### Module 3.47: Streaming Responses & Citation Display
- **Branch:** `frontend/3.47-streaming-responses-citations`
- **Category:** Streaming & Excerpts
- **Frontend Work Done:**
  - Built Visual Evidence Canvas in `views/evidence_view.py` and `components/evidence_card.py`.
  - Designed physical document excerpt sheets with colored deckle accent bars and verified SHA-256 hashes.
  - Added streaming typewriter response animation for generated answers.

---

### Module 3.48: Caching, Logging & Usage Monitoring
- **Branch:** `frontend/3.48-caching-logging-monitoring`
- **Category:** Observability & Audit
- **Frontend Work Done:**
  - Added "Download Formal Audit Dossier" export button generating markdown reports in `services/evidence_service.py`.
  - Added Inquiry Reference Tracking number badges (e.g. `#REF-EV-2025-419`) to header and answer cards.
  - Built audit log inquiry history table.

---

### Module 3.49: Deployment, Documentation & Delivery
- **Branch:** `frontend/3.49-deployment-docs-delivery`
- **Category:** Documentation & Delivery
- **Frontend Work Done:**
  - Wrote comprehensive project documentation in `README.md` with system architecture walkthrough.
  - Documented Quiet Editorial design tokens, color palette, and typography setup.
  - Added Quick Start guide, UI screenshot tour, and deployment instructions.

---

### Module 3.50: Sprint 2 RAG Application - Final Submission
- **Branch:** `frontend/3.50-sprint2-final-submission`
- **Category:** Final Delivery
- **Frontend Work Done:**
  - Performed final end-to-end integration and polish across Research, Evidence, and Document shelf views.
  - Validated all buttons, navigation tabs, modal drawers, keyword search, and export downloads.
  - Completed final Quiet Editorial CSS styling, contrast, and responsive viewports.

---

## ⚡ Quick Command Reminder

To push any PR automatically with prefilled descriptions, run:
```bash
./push_pr.sh
```
or
```bash
python3 push_pr.py --module <MODULE_ID>
```

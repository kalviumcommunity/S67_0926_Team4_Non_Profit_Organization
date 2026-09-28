# Sprint #2: AI Application Development with RAG
## 🎨 Frontend Daily Pull Request Roadmap & Execution Tracker

**Repository:** `https://github.com/kalviumcommunity/S67_0926_Team4_Non_Profit_Organization.git`  
**Frontend Contributor:** `Praveenkanna16`  
**Target Base Branch:** `main` (Direct pushes to `main` are strictly prohibited)

---

## ⚡ Quick Start: How to Push Your Daily Frontend PR

You have an automated helper script (`push_pr.py` / `./push_pr.sh`) built into the root of this project.

### 1. Interactive Menu (Recommended)
Simply run:
```bash
./push_pr.sh
```
or
```bash
python3 push_pr.py
```
This will display an interactive menu where you can:
- Type any Module ID (e.g. `3.9`, `3.46`, `3.10`, etc.)
- Automatically create and switch to the correct feature branch
- Stage all frontend changes cleanly
- Commit with a standard descriptive commit message
- Push the branch to `origin`
- Generate a **1-click GitHub Pull Request URL** with title, description, checklist, and metadata prefilled!

### 2. Direct CLI Command
```bash
# Push PR for a specific module (e.g., 3.9 Mock UX)
python3 push_pr.py --module 3.9

# Dry run preview (test without pushing)
python3 push_pr.py --module 3.9 --dry-run

# View all 50 modules and their status
python3 push_pr.py --list

# View past PR submission history
python3 push_pr.py --history
```

---

## 📅 Complete 50-Module Frontend Daily PR Matrix

| Module | Topic Title | Role Focus | Deliverables & Frontend Files | Branch Name | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **3.1** | Sprint 2 Kick-Off: AI Application Development with RAG | 🎨 Frontend | Architecture, stack overview, UI layout | `frontend/3.1-sprint-2-kick-off` | `[x]` |
| **3.2** | LLM Application Foundations | ⚙️ Shared | Environment setup, API key config | `frontend/3.2-llm-application-foundations` | `[x]` |
| **3.3** | Document Processing & Chunking for Retrieval | ⚙️ Shared | Document service interface, mock data | `frontend/3.3-document-processing-chunking` | `[x]` |
| **3.4** | Embeddings & Semantic Representation | ⚙️ Shared | Embedding vector models & metrics | `frontend/3.4-embeddings-semantic-representation` | `[ ]` |
| **3.5** | Vector Databases & Retrieval | ⚙️ Shared | Vector collection schema & indexing | `frontend/3.5-vector-databases-retrieval` | `[ ]` |
| **3.6** | RAG Pipeline Design & Grounded Generation | ⚙️ Shared | Retrieval + synthesis pipeline flow | `frontend/3.6-rag-pipeline-design` | `[ ]` |
| **3.7** | AI Application Integration & Deliver | 🎨 Frontend | Streamlit app entrypoint (`app.py`), service bridge | `frontend/3.7-ai-application-integration` | `[ ]` |
| **3.8** | The PRD Playbook | 🎨 Frontend | Product Requirement Document & user stories | `frontend/3.8-the-prd-playbook` | `[ ]` |
| **3.9** | Mock UX: Design the Experience Before You Build It | 🎨 Frontend | Quiet Editorial design system, typography, CSS tokens (`styles/theme.css`, `stitch_folio/`) | `frontend/3.9-mock-ux-design-the-experience` | `[ ]` |
| **3.10** | Development Environment & Project Workspace Setup | 🎨 Frontend | Workspace setup, `.gitignore`, Streamlit theme (`.streamlit/config.toml`) | `frontend/3.10-dev-environment-setup` | `[ ]` |
| **3.11** | GitHub Repository & Team Workflow Setup | 🎨 Frontend | PR template (`.github/pull_request_template.md`), PR automation tool (`push_pr.py`) | `frontend/3.11-github-repo-team-workflow` | `[ ]` |
| **3.12** | LLM API Access & First Completion Call | ⚙️ Shared | Client configuration & connection test | `frontend/3.12-llm-api-access-first-completion` | `[ ]` |
| **3.13** | Prompt Construction & System/User Roles | 🎨 Frontend | Query suggestion chips, role prompts (`components/query_box.py`) | `frontend/3.13-prompt-construction-roles` | `[ ]` |
| **3.14** | Tokens, Tokenization & Cost Estimation | 🎨 Frontend | Token usage metrics badge on answer card (`components/answer_card.py`) | `frontend/3.14-tokens-tokenization-cost` | `[ ]` |
| **3.15** | Context Windows & Message History Management | 🎨 Frontend | Session state multi-turn manager (`utils/state.py`) | `frontend/3.15-context-windows-message-history` | `[ ]` |
| **3.16** | Model Parameters & Output Control | 🎨 Frontend | Temperature & parameters drawer (`components/header.py`) | `frontend/3.16-model-parameters-output-control` | `[ ]` |
| **3.17** | Structured Output & JSON Response Handling | 🎨 Frontend | Structured JSON answer cards with metric grids (`components/answer_card.py`) | `frontend/3.17-structured-output-json` | `[ ]` |
| **3.18** | Prompt Templates & Reusable Prompt Design | 🎨 Frontend | Modular prompt templates (`services/rag_service.py`) | `frontend/3.18-prompt-templates-reusable-design` | `[ ]` |
| **3.19** | Document Loading & Multi-Format Intake | 🎨 Frontend | Multi-format drag-and-drop file uploader UI (`components/upload_panel.py`) | `frontend/3.19-document-loading-multi-format` | `[ ]` |
| **3.20** | Text Extraction & Cleaning Pipeline | ⚙️ Shared | Text clean-up & encoding normalization | `frontend/3.20-text-extraction-cleaning` | `[ ]` |
| **3.21** | Document Chunking Strategies | ⚙️ Shared | Clause-aware semantic chunking | `frontend/3.21-document-chunking-strategies` | `[ ]` |
| **3.22** | Chunk Metadata & Source Tracking | 🎨 Frontend | Clause metadata chips & SHA-256 badges (`components/citation_card.py`) | `frontend/3.22-chunk-metadata-source-tracking` | `[ ]` |
| **3.23** | Token-Aware Chunk Sizing & Overlap | ⚙️ Shared | Chunk size tuning & sliding window overlap | `frontend/3.23-token-aware-chunk-sizing` | `[ ]` |
| **3.24** | Corpus Preparation & Ingestion Validation | 🎨 Frontend | Archival shelf dossier cards & corpus validation (`views/documents_view.py`) | `frontend/3.24-corpus-prep-validation` | `[ ]` |
| **3.25** | Embeddings Fundamentals & Vector Representation | ⚙️ Shared | Semantic representation foundations | `frontend/3.25-embeddings-fundamentals` | `[ ]` |
| **3.26** | Generating Embeddings via API | ⚙️ Shared | Batch API embedding generation | `frontend/3.26-generating-embeddings-api` | `[ ]` |
| **3.27** | Embedding Similarity & Distance Metrics | 🎨 Frontend | Visual similarity match percentage badges (`components/citation_card.py`) | `frontend/3.27-embedding-similarity-distance` | `[ ]` |
| **3.28** | Batch Embedding & Rate/Cost Management | 🎨 Frontend | Multi-step progress animation in upload drawer (`components/upload_panel.py`) | `frontend/3.28-batch-embedding-rate-cost` | `[ ]` |
| **3.29** | Embedding Quality Checks & Sanity Tests | ⚙️ Shared | Retrieval sanity checks & assertions | `frontend/3.29-embedding-quality-checks` | `[ ]` |
| **3.30** | Vector Database Setup & Collection Design | ⚙️ Shared | Vector database setup & collection schema | `frontend/3.30-vector-db-setup-collection` | `[ ]` |
| **3.31** | Indexing Embeddings & Metadata Storage | 🎨 Frontend | Clause index stats & filter counters (`components/clause_search.py`) | `frontend/3.31-indexing-embeddings-metadata` | `[ ]` |
| **3.32** | Similarity Search & Top-K Retrieval | 🎨 Frontend | Top-K retrieval visualization (`components/query_box.py`) | `frontend/3.32-similarity-search-top-k` | `[ ]` |
| **3.33** | Metadata Filtering & Hybrid Search | 🎨 Frontend | Live clause search drawer with keyword + metadata filters (`components/clause_search.py`) | `frontend/3.33-metadata-filtering-hybrid-search` | `[ ]` |
| **3.34** | Retrieval Relevance Tuning | ⚙️ Shared | Precision tuning & threshold adjustment | `frontend/3.34-retrieval-relevance-tuning` | `[ ]` |
| **3.35** | Chunk Re-Ranking for Precision | 🎨 Frontend | Re-ranked citation cards arranged by confidence score | `frontend/3.35-chunk-re-ranking-precision` | `[ ]` |
| **3.36** | Retrieval Evaluation & Recall Testing | ⚙️ Shared | Query evaluation test suite | `frontend/3.36-retrieval-eval-recall-testing` | `[ ]` |
| **3.37** | RAG Pipeline Architecture & Flow Design | 🎨 Frontend | Deterministic Provenance Lineage Tree visualization (`components/provenance_chain.py`) | `frontend/3.37-rag-pipeline-architecture-flow` | `[ ]` |
| **3.38** | Context Injection & Prompt Augmentation | 🎨 Frontend | Grounded prompt assembly & contextual badges (`components/answer_card.py`) | `frontend/3.38-context-injection-augmentation` | `[ ]` |
| **3.39** | Grounded Answer Generation | 🎨 Frontend | Grounded answer display with verified specification seals (`views/research_view.py`) | `frontend/3.39-grounded-answer-generation` | `[ ]` |
| **3.40** | Source Citation & Attribution | 🎨 Frontend | Physical document excerpt sheets with highlighted clauses (`components/evidence_card.py`) | `frontend/3.40-source-citation-attribution` | `[ ]` |
| **3.41** | Hallucination Guardrails & Refusal Handling | 🎨 Frontend | Confidence thresholds & graceful fallback notices | `frontend/3.41-hallucination-guardrails` | `[ ]` |
| **3.42** | Conversational RAG & Follow-Up Context | 🎨 Frontend | Interactive question suggestions & session tracking (`components/query_box.py`) | `frontend/3.42-conversational-rag-followup` | `[ ]` |
| **3.43** | RAG Evaluation & Answer Quality Scoring | 🎨 Frontend | Provisional Reconciler & Clause Delta Diff Viewer (`components/diff_viewer.py`) | `frontend/3.43-rag-evaluation-answer-quality` | `[ ]` |
| **3.44** | Backend API for the RAG Service | 🎨 Frontend | Clean service layer interface (`services/base.py`, `services/rag_service.py`) | `frontend/3.44-backend-api-rag-service` | `[ ]` |
| **3.45** | Document Upload & Indexing Endpoint | 🎨 Frontend | Multi-step interactive document ingestion panel (`components/upload_panel.py`) | `frontend/3.45-doc-upload-indexing-endpoint` | `[ ]` |
| **3.46** | Chat Interface & Query UI | 🎨 Frontend | Research & Instant Answer page complete UI (`views/research_view.py`) | `frontend/3.46-chat-interface-query-ui` | `[ ]` |
| **3.47** | Streaming Responses & Citation Display | 🎨 Frontend | Visual Evidence & Excerpt Sheets canvas (`views/evidence_view.py`) | `frontend/3.47-streaming-responses-citations` | `[ ]` |
| **3.48** | Caching, Logging & Usage Monitoring | 🎨 Frontend | Audit dossier download & inquiry tracking (`services/evidence_service.py`) | `frontend/3.48-caching-logging-monitoring` | `[ ]` |
| **3.49** | Deployment, Documentation & Delivery | 🎨 Frontend | Comprehensive README, installation steps, and UI guide (`README.md`) | `frontend/3.49-deployment-docs-delivery` | `[ ]` |
| **3.50** | Sprint 2 RAG Application - Final Submission | 🎨 Frontend | Complete integrated FOLIO platform (`app.py`, `views/`, `components/`) | `frontend/3.50-sprint2-final-submission` | `[ ]` |

---

## 🛡️ Git Workflow Rules

1. **Never push directly to `main`**: All work is submitted via isolated feature branches (`frontend/3.x-...`).
2. **One PR per Day / Milestone**: Keep PRs atomic, focused, and mapped directly to the milestone topic.
3. **Always review the One-Click URL**: The helper script generates a prefilled GitHub URL with PR title and description ready to submit.
4. **Track History**: `pr_history.json` automatically saves your submission timestamps and commit hashes.

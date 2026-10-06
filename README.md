# FOLIO — Grant Intelligence Platform

An institutional, editorial intelligence platform designed for foundation officers, institutional grantmakers, and nonprofit program staff to query complex grant guidelines, donor agreements, and impact reports with 100% deterministic provenance and zero-extrapolation citations.

---

## Visual & Product Design System

Folio embodies the **Quiet Editorial** design aesthetic:
- **Tone:** Measured, institutional, transparent, and quietly confident.
- **Typography:** Juxtaposition between authoritative literary serif (`Newsreader`) and crisp humanist sans (`Plus Jakarta Sans`).
- **Color Palette:** Layered ivory paper canvas (`#FDFBF7` / `#FBF9F4`), soft cream document sheets (`#F7F4EE`), deep mineral charcoal ink (`#1C1D1B`), botanical forest green (`#1E382B`), and archival terracotta accents (`#D96B43` / `#A0401C`).
- **Tactile Paper Tiers:** Physical sheet layering with hairline borders (`#E4DFD3`, `#DDD7CA`) and deckle accents rather than synthetic glassmorphism or neon gradients.

---

## Core Pages & Features

### 1. Research / Instant Answer (`Research`)
- **Query Input & Suggestions:** Fast query bar with interactive suggestion chips (`Reporting deadlines`, `Indirect costs`, `Annual report due`, `Reallocation limits`, `Financial audit / GAAP`).
- **Answer State Block:**
  - Verified query metadata recap (`Asked: "..." · 2 sources verified`) with `PORTAL VERIFIED SPECIFICATION` badge.
  - Editorial headline and concise grounded prose.
  - **Visual Communication Grid:** 3 expressive metric blocks (e.g. `30 DAYS` deadline, `YEAR END` annual report, `10% CAP` indirect cost variance).
  - **Sources Mini-Sheets:** Paper-like cited agreements with clause badges and direct inspect actions.
  - **Primary CTA:** "View evidence →" deep linking into the Provenance view.

### 2. Visual Evidence & Provenance (`Evidence`)
- **Verified Provenance Audit:** Header with unique inquiry tracking (`REF #EV-2025-419`).
- **Authority & Citation Branch (Lineage Tree):** 100% deterministic lineage mapping from synthesized answer statement down through parent regulatory frameworks and binding grantee instruments.
- **Original Physical Text Excerpts:** Authentic printed typography paper sheets with colored deckle accent bars, SHA-256 integrity verification, section headers, and highlighted `<mark>` clauses.
- **Provisional Reconciler & Conflict Check:** Cross-instrument side-by-side metric comparison (e.g. Active 2025 vs Historical 2023) and collapsible structural clause delta check diff drawer.
- **Downloadable Audit Dossier:** Export verified provenance audit reports.

### 3. Documents / Digital Paper Archive (`Documents`)
- **Fast Clause Search & Excerpts Drawer:** Live clause scanner highlighting matching keywords (e.g. `indirect costs`) with direct "Open in sheet →" navigation.
- **Archival Shelf Dossier Cards:** Asymmetrical grid displaying spine bookmark bands, status seals (`Active`, `Fully Executed`, `Approved`, `Active Amendment`), key indexed clauses, obligation matrices, milestone ledgers, and executive scopes.
- **Full Document Dossier Reader:** Clean reading experience displaying full unadulterated charter text, effective cycle, page count, and SHA-256 checksums.
- **Drag-and-Drop Archival Dropzone:** Multi-step upload simulation (`Uploading...` → `Extracting text (OCR)...` → `Creating semantic chunks...` → `Generating hashes...` → `Indexed successfully`) with immediate archive integration.

---

## Project Structure

```
Sprint 2/
├── .streamlit/
│   └── config.toml               # Streamlit server & theme configuration
├── app.py                        # Main application entrypoint & page router
├── config/
│   └── settings.py               # Global settings, feature flags, and API URLs
├── styles/
│   └── theme.css                 # Quiet Editorial CSS tokens & component overrides
├── data/
│   ├── mock_documents.py         # 8+ rich grant guidelines, agreements, and reports
│   ├── mock_queries.py           # 8+ realistic queries with metrics and citations
│   └── mock_evidence.py          # Lineage trees, excerpt sheets, and diff records
├── services/
│   ├── base.py                   # Service abstract base interfaces
│   ├── rag_service.py            # RAG question answering & suggestion engine
│   ├── document_service.py       # Archive management, clause search & upload
│   └── evidence_service.py       # Provenance retrieval & audit export
├── utils/
│   ├── constants.py              # Navigation tabs and classification types
│   ├── formatting.py             # Text highlighters, currency & page formatters
│   └── state.py                  # Streamlit session state manager
├── components/
│   ├── header.py                 # Sticky top navigation bar & workspace pill
│   ├── query_box.py              # Search bar and suggested question chips
│   ├── answer_card.py            # Grounded answer block, metrics & source cards
│   ├── citation_card.py          # Paper-like mini sheet citation card
│   ├── provenance_chain.py       # Deterministic lineage tree diagram
│   ├── evidence_card.py          # Physical document excerpt sheet with deckle accent
│   ├── document_card.py          # Archival shelf dossier card with spine bookmark
│   ├── clause_search.py          # Live clause search matching drawer
│   ├── diff_viewer.py            # Provisional reconciler & diff comparison drawer
│   ├── upload_panel.py           # Multi-step upload & indexing workflow
│   └── document_viewer.py        # Full document dossier reading canvas
├── views/
│   ├── research_view.py          # Page 1: Research / Instant Answer
│   ├── evidence_view.py          # Page 2: Visual Evidence & Provenance
│   └── documents_view.py         # Page 3: Documents / Digital Archive
├── requirements.txt              # Project dependencies
├── .env.example                  # Environment configuration template
└── README.md                     # Documentation & demo guide
```

---

## Installation & Running Locally

### 1. Prerequisites
- Python 3.10+
- pip
- A valid OpenRouter API key

### 2. Set up your environment
Create a `.env` file in the project root with one of these keys:

```env
OPENROUTER_API_KEY=your_key_here
```

The backend also accepts:

```env
Open_router_API_KEY=your_key_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the backend API
```bash
python Back_end/app.py
```

The backend will run at:
```text
http://localhost:8000
```

Available routes:
- `GET /` — service check
- `GET /health` — health endpoint
- `POST /ask` — submit a question and receive an answer from OpenRouter

### 5. Start the Streamlit app
```bash
streamlit run app.py
```

The frontend will open at:
```text
http://localhost:8501
```

---

## OpenRouter Backend API

The backend file is located at [Back_end/app.py](Back_end/app.py). It exposes a simple chat endpoint that reads the API key from `.env` and sends the request to OpenRouter.

### Request example
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the reporting deadlines?",
    "model": "openai/gpt-4o-mini",
    "system_prompt": "You are a helpful grant assistant."
  }'
```

### Response example
```json
{
  "answer": "The reporting deadline is typically 30 days after the funding cycle closes.",
  "model": "openai/gpt-4o-mini"
}
```

---

## Complete Demo Flow Walkthrough

1. **Launch Folio:** Open `http://localhost:8501`. Notice the Quiet Editorial typography, warm ivory paper canvas, and top navbar.
2. **Start the API:** Run the backend command above to make the chat route available.
3. **Execute a Query:** In the `Research` page, click on the suggestion chip `"Reporting deadlines"` (or type `"What are the reporting requirements?"`).
4. **Inspect Grounded Answer:** View the synthesized answer with `PORTAL VERIFIED SPECIFICATION` seal, 3 metric blocks (`30 DAYS`, `YEAR END`, `10% CAP`), and 2 mini citation sheets.
5. **Follow Provenance:** Click `"View evidence →"`. The app navigates to `Evidence`, rendering the **Authority & Citation Branch Lineage Tree** and physical document paper sheets with highlighted clauses.
6. **Inspect Cross-Instrument Diff:** Click `"⚙ Side-by-side Diff"` in the Provisional Reconciler to view structural clause deltas between the 2023 baseline and 2025 active rule.
7. **Export Audit Dossier:** Click `"Export Audit Dossier (.PDF)"` to download the verified audit trail.
8. **Browse Digital Archive:** Click `"Open Document Archive →"` (or `"Documents"` in top nav) to view the archival shelf of executed agreements and guidelines.
9. **Test Fast Clause Search:** In the search bar, type `indirect costs`. The instant matching drawer opens showing highlighted clauses from both Grant Guidelines and Donor Agreements.
10. **Inspect Document Dossier:** Click `"Inspect →"` on *Grant Guidelines* to read the full document dossier and verify metadata.
11. **Test Document Upload:** Click `"+ Add documents"` and upload a sample grant agreement file to watch the multi-step indexing simulation in real time.

---

## Notes

- This project now includes a working local chatbot backend powered by OpenRouter.
- The backend reads the API key from `.env`, so you do not need to hardcode secrets in code.
- If you want the app to serve real answers from your own grant data, the next step is to connect the `/ask` route to your retrieval or indexing pipeline.

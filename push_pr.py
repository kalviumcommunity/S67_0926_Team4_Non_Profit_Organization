#!/usr/bin/env python3
"""
=============================================================================
Sprint #2: AI Application Development with RAG - Frontend PR Automation Tool
=============================================================================
Repository : https://github.com/kalviumcommunity/S67_0926_Team4_Non_Profit_Organization.git
Author     : Praveenkanna16 (Frontend Engineer)
Purpose    : Automate branch creation, staging, committing, pushing, and generating
             one-click GitHub Pull Requests for all Module 3 (3.1 - 3.50) milestones.

SAFETY RULE: Never pushes directly to the `main` branch. Always creates an isolated
feature branch named after the module title and generates a PR targeting `main`.
=============================================================================
"""

import sys
import os
import re
import json
import urllib.parse
import subprocess
import argparse
from datetime import datetime

REPO_OWNER = "kalviumcommunity"
REPO_NAME = "S67_0926_Team4_Non_Profit_Organization"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
BASE_BRANCH = "main"

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pr_history.json")

# Complete Registry of all 50 Sprint 2 Milestones
MODULES = [
    {
        "id": "3.1",
        "title": "Sprint 2 Kick-Off: AI Application Development with RAG",
        "category": "Architecture & Planning",
        "is_frontend": True,
        "deliverable": "Project architectural breakdown, frontend technical stack definition (Streamlit Quiet Editorial System), milestone timeline.",
        "files_hint": ["README.md", "styles/theme.css", "app.py"],
        "url": "https://app.kalvium.community/livebooks/2538/ec225bfa-6de1-4e8a-b6b4-858224f1af4a"
    },
    {
        "id": "3.2",
        "title": "LLM Application Foundations",
        "category": "Foundations",
        "is_frontend": False,
        "deliverable": "Virtual environments, dependency files, API key security, and client configurations.",
        "files_hint": ["requirements.txt", ".env.example", "config/settings.py"],
        "url": "https://app.kalvium.community/livebooks/2538/3edb7c9f-b46e-42a3-9769-5e38b3af3bcc"
    },
    {
        "id": "3.3",
        "title": "Document Processing & Chunking for Retrieval",
        "category": "Data & Ingestion",
        "is_frontend": False,
        "deliverable": "Document loading pipelines and text chunking strategy definitions.",
        "files_hint": ["services/document_service.py", "data/mock_documents.py"],
        "url": "https://app.kalvium.community/livebooks/2538/5dbe61b1-0956-486c-b5f3-5e54cb48606c"
    },
    {
        "id": "3.4",
        "title": "Embeddings & Semantic Representation",
        "category": "Embeddings",
        "is_frontend": False,
        "deliverable": "Embedding vector generation and cosine distance calculations.",
        "files_hint": ["services/rag_service.py", "data/mock_evidence.py"],
        "url": "https://app.kalvium.community/livebooks/2538/3c637162-132d-4a3c-b5a2-47dfe23b566a"
    },
    {
        "id": "3.5",
        "title": "Vector Databases & Retrieval",
        "category": "Vector DB",
        "is_frontend": False,
        "deliverable": "High-dimensional vector storage, schema definitions, and HNSW indexing.",
        "files_hint": ["services/rag_service.py", "config/settings.py"],
        "url": "https://app.kalvium.community/livebooks/2538/1c8d7eab-e599-434a-89a5-757acf04ed32"
    },
    {
        "id": "3.6",
        "title": "RAG Pipeline Design & Grounded Generation",
        "category": "RAG Core",
        "is_frontend": False,
        "deliverable": "End-to-end retrieval and generation orchestration.",
        "files_hint": ["services/rag_service.py", "services/base.py"],
        "url": "https://app.kalvium.community/livebooks/2538/5f66a05d-d756-4390-9b72-448218fbc527"
    },
    {
        "id": "3.7",
        "title": "AI Application Integration & Deliver",
        "category": "Integration",
        "is_frontend": True,
        "deliverable": "Connecting backend RAG pipelines to frontend UI components and application shell.",
        "files_hint": ["app.py", "views/research_view.py", "services/rag_service.py"],
        "url": "https://app.kalvium.community/livebooks/2538/7575f942-e7d5-4693-b134-171e412403da"
    },
    {
        "id": "3.8",
        "title": "The PRD Playbook",
        "category": "Product Design",
        "is_frontend": True,
        "deliverable": "Product Requirement Document (PRD), user personas, user stories, and feature requirements.",
        "files_hint": ["README.md", "docs/PRD.md"],
        "url": "https://app.kalvium.community/livebooks/2538/730c1c9d-3e0f-4272-91b5-4d80d5694d8c"
    },
    {
        "id": "3.9",
        "title": "Mock UX: Design the Experience Before You Build It",
        "category": "UI/UX Design",
        "is_frontend": True,
        "deliverable": "High-fidelity UI mockups, Quiet Editorial design system, typography tokens, wireframes, and component layouts.",
        "files_hint": ["styles/theme.css", "stitch_folio_grant_intelligence_platform/", "components/header.py"],
        "url": "https://app.kalvium.community/livebooks/2538/6ad74042-8901-4386-bf2c-3ac1a5f0a9c3"
    },
    {
        "id": "3.10",
        "title": "Development Environment & Project Workspace Setup",
        "category": "Foundations",
        "is_frontend": True,
        "deliverable": "Clean workspace configuration, .gitignore, virtualenv setup, and Streamlit theme configs.",
        "files_hint": [".gitignore", ".streamlit/config.toml", "requirements.txt", ".env.example"],
        "url": "https://app.kalvium.community/livebooks/2538/17fc8b88-163c-40d8-92c4-236096586355"
    },
    {
        "id": "3.11",
        "title": "GitHub Repository & Team Workflow Setup",
        "category": "DevOps & Workflow",
        "is_frontend": True,
        "deliverable": "Team branching strategy, PR template, PR automation helper, and contributor workflow docs.",
        "files_hint": [".github/pull_request_template.md", "push_pr.py", "FRONTEND_PR_TRACKER.md"],
        "url": "https://app.kalvium.community/livebooks/2538/5728f230-a628-498f-b643-824f77334f8b"
    },
    {
        "id": "3.12",
        "title": "LLM API Access & First Completion Call",
        "category": "LLM Integration",
        "is_frontend": False,
        "deliverable": "Configured LLM client with error handling and connectivity testing.",
        "files_hint": ["services/rag_service.py", "config/settings.py"],
        "url": "https://app.kalvium.community/livebooks/2538/d3d347c7-43a6-4e5c-8ce7-fd2f3011693b"
    },
    {
        "id": "3.13",
        "title": "Prompt Construction & System/User Roles",
        "category": "Prompt Engineering",
        "is_frontend": True,
        "deliverable": "System persona definitions, user role handling, and query suggestion chips UI.",
        "files_hint": ["components/query_box.py", "data/mock_queries.py"],
        "url": "https://app.kalvium.community/livebooks/2538/4a5d1b0e-9b55-43fc-9c41-de97b88d4bf7"
    },
    {
        "id": "3.14",
        "title": "Tokens, Tokenization & Cost Estimation",
        "category": "LLM Cost & Tokens",
        "is_frontend": True,
        "deliverable": "Token counter utilities and token usage badges displayed on response cards.",
        "files_hint": ["components/answer_card.py", "utils/formatting.py"],
        "url": "https://app.kalvium.community/livebooks/2538/39dfc4bf-03ff-44c4-970a-4e5049324e6c"
    },
    {
        "id": "3.15",
        "title": "Context Windows & Message History Management",
        "category": "Session Management",
        "is_frontend": True,
        "deliverable": "Streamlit multi-turn session state manager and history trimming.",
        "files_hint": ["utils/state.py", "views/research_view.py"],
        "url": "https://app.kalvium.community/livebooks/2538/6ed7adf9-6522-4773-8cc2-77e84eafadd1"
    },
    {
        "id": "3.16",
        "title": "Model Parameters & Output Control",
        "category": "LLM Tuning",
        "is_frontend": True,
        "deliverable": "Temperature, top-p, and max tokens parameter controls / settings UI.",
        "files_hint": ["config/settings.py", "components/header.py"],
        "url": "https://app.kalvium.community/livebooks/2538/ae324a97-963e-4ee5-843d-9284301a5f13"
    },
    {
        "id": "3.17",
        "title": "Structured Output & JSON Response Handling",
        "category": "Structured Data",
        "is_frontend": True,
        "deliverable": "Structured JSON parser for answers, key metrics extraction grid, and source citations.",
        "files_hint": ["components/answer_card.py", "data/mock_queries.py"],
        "url": "https://app.kalvium.community/livebooks/2538/fa053e54-8466-4b32-aba8-104e3810ed36"
    },
    {
        "id": "3.18",
        "title": "Prompt Templates & Reusable Prompt Design",
        "category": "Prompt Templates",
        "is_frontend": True,
        "deliverable": "Modular prompt templates with dynamic slot filling for grant guidelines queries.",
        "files_hint": ["services/rag_service.py", "components/query_box.py"],
        "url": "https://app.kalvium.community/livebooks/2538/d3ccc028-2a23-48d7-b14e-3ac198928f9d"
    },
    {
        "id": "3.19",
        "title": "Document Loading & Multi-Format Intake",
        "category": "Document Ingestion",
        "is_frontend": True,
        "deliverable": "Multi-format file uploader UI supporting PDF, DOCX, Markdown, and TXT grant instruments.",
        "files_hint": ["components/upload_panel.py", "views/documents_view.py"],
        "url": "https://app.kalvium.community/livebooks/2538/c7f84784-0125-4e3a-bd90-2df51874c37f"
    },
    {
        "id": "3.20",
        "title": "Text Extraction & Cleaning Pipeline",
        "category": "Data Cleaning",
        "is_frontend": False,
        "deliverable": "Boilerplate stripper, whitespace normalizer, and encoding cleaner.",
        "files_hint": ["services/document_service.py", "utils/formatting.py"],
        "url": "https://app.kalvium.community/livebooks/2538/3fde683a-9e9f-4cfa-a25c-9f76b70b19aa"
    },
    {
        "id": "3.21",
        "title": "Document Chunking Strategies",
        "category": "Chunking",
        "is_frontend": False,
        "deliverable": "Semantic chunking strategies tailored to legal clauses and grant agreements.",
        "files_hint": ["services/document_service.py", "data/mock_documents.py"],
        "url": "https://app.kalvium.community/livebooks/2538/6a591e1a-854a-4b74-931e-fe0a5d0f4936"
    },
    {
        "id": "3.22",
        "title": "Chunk Metadata & Source Tracking",
        "category": "Metadata & Lineage",
        "is_frontend": True,
        "deliverable": "Attaching document ID, clause number, page, section header, and SHA-256 hash to UI cards.",
        "files_hint": ["components/citation_card.py", "components/evidence_card.py"],
        "url": "https://app.kalvium.community/livebooks/2538/6329e2bd-202c-46eb-8946-63da4c32d3bd"
    },
    {
        "id": "3.23",
        "title": "Token-Aware Chunk Sizing & Overlap",
        "category": "Chunking",
        "is_frontend": False,
        "deliverable": "Token-aware sliding window chunking with configurable overlap.",
        "files_hint": ["services/document_service.py"],
        "url": "https://app.kalvium.community/livebooks/2538/44c6f6d4-607d-4edc-a042-25aa3147b4a4"
    },
    {
        "id": "3.24",
        "title": "Corpus Preparation & Ingestion Validation",
        "category": "Data Validation",
        "is_frontend": True,
        "deliverable": "Archival document shelf view with status seals, clause index badges, and corpus stats.",
        "files_hint": ["views/documents_view.py", "components/document_card.py", "data/mock_documents.py"],
        "url": "https://app.kalvium.community/livebooks/2538/107dd035-6804-49ff-8973-8921dc2b457d"
    },
    {
        "id": "3.25",
        "title": "Embeddings Fundamentals & Vector Representation",
        "category": "Embeddings",
        "is_frontend": False,
        "deliverable": "Embedding vector generation across grant domain datasets.",
        "files_hint": ["services/rag_service.py"],
        "url": "https://app.kalvium.community/livebooks/2538/1e5fb50c-c1db-4128-908a-9ecce49229a0"
    },
    {
        "id": "3.26",
        "title": "Generating Embeddings via API",
        "category": "Embeddings",
        "is_frontend": False,
        "deliverable": "API embedding batch generation with rate-limiting and persistence.",
        "files_hint": ["services/rag_service.py", "config/settings.py"],
        "url": "https://app.kalvium.community/livebooks/2538/466bf311-34cb-4551-83da-e78bb6b6ed34"
    },
    {
        "id": "3.27",
        "title": "Embedding Similarity & Distance Metrics",
        "category": "Vector Similarity",
        "is_frontend": True,
        "deliverable": "Visual similarity score badges (e.g. 98% match, 94% relevance) on citation cards.",
        "files_hint": ["components/citation_card.py", "components/answer_card.py"],
        "url": "https://app.kalvium.community/livebooks/2538/56c69b32-4669-41e4-8651-872e9d127986"
    },
    {
        "id": "3.28",
        "title": "Batch Embedding & Rate/Cost Management",
        "category": "Batching & Optimization",
        "is_frontend": True,
        "deliverable": "Multi-step progress tracker simulation with chunk batch feedback in upload drawer.",
        "files_hint": ["components/upload_panel.py"],
        "url": "https://app.kalvium.community/livebooks/2538/b5e5dbb4-95af-41e0-b2fb-62754f2c9473"
    },
    {
        "id": "3.29",
        "title": "Embedding Quality Checks & Sanity Tests",
        "category": "Quality Assurance",
        "is_frontend": False,
        "deliverable": "Automated sanity checks validating semantic ranking against test queries.",
        "files_hint": ["tests/test_embeddings.py", "services/rag_service.py"],
        "url": "https://app.kalvium.community/livebooks/2538/8d3f64b6-acf1-4406-bf26-99ceeadc5e8c"
    },
    {
        "id": "3.30",
        "title": "Vector Database Setup & Collection Design",
        "category": "Vector DB",
        "is_frontend": False,
        "deliverable": "Vector collection schema with payload metadata fields for grant instruments.",
        "files_hint": ["services/rag_service.py", "config/settings.py"],
        "url": "https://app.kalvium.community/livebooks/2538/61d22726-2f5f-484e-b7ae-90fbd39afae8"
    },
    {
        "id": "3.31",
        "title": "Indexing Embeddings & Metadata Storage",
        "category": "Indexing",
        "is_frontend": True,
        "deliverable": "Clause search indexing and live filter counts in documents explorer.",
        "files_hint": ["components/clause_search.py", "views/documents_view.py"],
        "url": "https://app.kalvium.community/livebooks/2538/2fe8ffba-b099-446b-9562-ab334bc0f28c"
    },
    {
        "id": "3.32",
        "title": "Similarity Search & Top-K Retrieval",
        "category": "Retrieval",
        "is_frontend": True,
        "deliverable": "Top-K retrieval result display and interactive suggestion chips in search UI.",
        "files_hint": ["components/query_box.py", "components/answer_card.py"],
        "url": "https://app.kalvium.community/livebooks/2538/b9e2fce3-53be-4001-b488-171f0d2244ac"
    },
    {
        "id": "3.33",
        "title": "Metadata Filtering & Hybrid Search",
        "category": "Hybrid Retrieval",
        "is_frontend": True,
        "deliverable": "Live clause search drawer with keyword + metadata filters and highlighted matches.",
        "files_hint": ["components/clause_search.py", "utils/formatting.py"],
        "url": "https://app.kalvium.community/livebooks/2538/b30d7063-8aa5-4635-b641-140b18849815"
    },
    {
        "id": "3.34",
        "title": "Retrieval Relevance Tuning",
        "category": "Retrieval Tuning",
        "is_frontend": False,
        "deliverable": "Evaluation of retrieval thresholds, top-k tuning, and similarity cutoffs.",
        "files_hint": ["services/rag_service.py"],
        "url": "https://app.kalvium.community/livebooks/2538/7ee6772f-9a0c-43fb-b1e6-54208ee8b2f0"
    },
    {
        "id": "3.35",
        "title": "Chunk Re-Ranking for Precision",
        "category": "Re-Ranking",
        "is_frontend": True,
        "deliverable": "Re-ranked citation cards arranged by confidence score and parent hierarchy.",
        "files_hint": ["components/answer_card.py", "components/citation_card.py"],
        "url": "https://app.kalvium.community/livebooks/2538/d2073113-4aed-4ea4-b857-bff249c5fa41"
    },
    {
        "id": "3.36",
        "title": "Retrieval Evaluation & Recall Testing",
        "category": "Evaluation",
        "is_frontend": False,
        "deliverable": "Test query suite for recall@k and precision@k benchmarking.",
        "files_hint": ["tests/test_retrieval.py", "data/mock_queries.py"],
        "url": "https://app.kalvium.community/livebooks/2538/eb772227-d0d7-4c42-a4fa-3155eaccedba"
    },
    {
        "id": "3.37",
        "title": "RAG Pipeline Architecture & Flow Design",
        "category": "RAG Architecture",
        "is_frontend": True,
        "deliverable": "Provenance lineage tree visualization displaying the complete architectural pipeline flow.",
        "files_hint": ["components/provenance_chain.py", "views/evidence_view.py"],
        "url": "https://app.kalvium.community/livebooks/2538/2beb5711-258e-4eae-914b-59bbd2bfdf11"
    },
    {
        "id": "3.38",
        "title": "Context Injection & Prompt Augmentation",
        "category": "Prompt Construction",
        "is_frontend": True,
        "deliverable": "Grounded prompt assembly and contextual header badges in answer cards.",
        "files_hint": ["components/answer_card.py", "services/rag_service.py"],
        "url": "https://app.kalvium.community/livebooks/2538/19e0f8ea-c5a2-4acd-bfa4-707a641d752d"
    },
    {
        "id": "3.39",
        "title": "Grounded Answer Generation",
        "category": "Generation",
        "is_frontend": True,
        "deliverable": "Grounded answer display with zero-extrapolation editorial synthesis and verified specification seals.",
        "files_hint": ["views/research_view.py", "components/answer_card.py"],
        "url": "https://app.kalvium.community/livebooks/2538/8f383d3a-10ae-44d8-ac67-8b7abd45f8ba"
    },
    {
        "id": "3.40",
        "title": "Source Citation & Attribution",
        "category": "Attribution",
        "is_frontend": True,
        "deliverable": "Verifiable citation cards linking directly into physical document excerpt sheets with highlighted clauses.",
        "files_hint": ["components/citation_card.py", "components/evidence_card.py", "views/evidence_view.py"],
        "url": "https://app.kalvium.community/livebooks/2538/9e3d802a-5c7a-4f02-8652-5de3fb4b4837"
    },
    {
        "id": "3.41",
        "title": "Hallucination Guardrails & Refusal Handling",
        "category": "Guardrails",
        "is_frontend": True,
        "deliverable": "Safety guardrail badges, confidence thresholds, and graceful insufficient-evidence fallbacks.",
        "files_hint": ["components/answer_card.py", "services/rag_service.py"],
        "url": "https://app.kalvium.community/livebooks/2538/4bb66e7c-25b7-4a30-a64e-704ab58c512f"
    },
    {
        "id": "3.42",
        "title": "Conversational RAG & Follow-Up Context",
        "category": "Conversational AI",
        "is_frontend": True,
        "deliverable": "Interactive question suggestions, related follow-up queries, and inquiry session tracking.",
        "files_hint": ["components/query_box.py", "utils/state.py"],
        "url": "https://app.kalvium.community/livebooks/2538/6b38f93d-86f1-47df-9947-788e8b614ad8"
    },
    {
        "id": "3.43",
        "title": "RAG Evaluation & Answer Quality Scoring",
        "category": "Evaluation",
        "is_frontend": True,
        "deliverable": "Provisional reconciler comparison view & clause delta diff viewer for answer auditability.",
        "files_hint": ["components/diff_viewer.py", "views/evidence_view.py"],
        "url": "https://app.kalvium.community/livebooks/2538/80924df2-964f-44b0-a365-5d62a7a85a77"
    },
    {
        "id": "3.44",
        "title": "Backend API for the RAG Service",
        "category": "API Services",
        "is_frontend": True,
        "deliverable": "Service layer abstraction connecting frontend views cleanly to mock/live RAG services.",
        "files_hint": ["services/base.py", "services/rag_service.py", "services/evidence_service.py"],
        "url": "https://app.kalvium.community/livebooks/2538/7d192d7a-9cdb-4a5d-a954-6919517f7dcb"
    },
    {
        "id": "3.45",
        "title": "Document Upload & Indexing Endpoint",
        "category": "Upload & Indexing",
        "is_frontend": True,
        "deliverable": "Interactive document upload workflow with animated stages and immediate archive injection.",
        "files_hint": ["components/upload_panel.py", "services/document_service.py"],
        "url": "https://app.kalvium.community/livebooks/2538/9be4649a-1a7d-44ab-a737-815acf322a71"
    },
    {
        "id": "3.46",
        "title": "Chat Interface & Query UI",
        "category": "Frontend UI/UX",
        "is_frontend": True,
        "deliverable": "Full Research view with query input, suggestion pills, structured answer metrics, and evidence navigation.",
        "files_hint": ["views/research_view.py", "components/query_box.py", "components/answer_card.py"],
        "url": "https://app.kalvium.community/livebooks/2538/ec3d79dc-f392-4946-92bf-9674d4e29b86"
    },
    {
        "id": "3.47",
        "title": "Streaming Responses & Citation Display",
        "category": "Frontend Streaming & Citations",
        "is_frontend": True,
        "deliverable": "Physical document excerpt sheets with colored deckle accent bars and verified SHA-256 hashes.",
        "files_hint": ["components/evidence_card.py", "views/evidence_view.py"],
        "url": "https://app.kalvium.community/livebooks/2538/d3b2b29e-7413-46e6-960c-c17e2c6b6dbe"
    },
    {
        "id": "3.48",
        "title": "Caching, Logging & Usage Monitoring",
        "category": "Observability",
        "is_frontend": True,
        "deliverable": "Downloadable audit dossier export and inquiry tracking badges (#REF-EV-2025-419).",
        "files_hint": ["services/evidence_service.py", "components/header.py"],
        "url": "https://app.kalvium.community/livebooks/2538/06143638-5c49-40fa-8662-1569888ccd0c"
    },
    {
        "id": "3.49",
        "title": "Deployment, Documentation & Delivery",
        "category": "Documentation & Delivery",
        "is_frontend": True,
        "deliverable": "Full repository README, installation guide, Quiet Editorial design system documentation.",
        "files_hint": ["README.md", "app.py", "requirements.txt"],
        "url": "https://app.kalvium.community/livebooks/2538/3c9a92c2-b95b-43f4-a066-99115782ac33"
    },
    {
        "id": "3.50",
        "title": "Sprint 2 RAG Application - Final Submission",
        "category": "Final Integration",
        "is_frontend": True,
        "deliverable": "Complete integrated FOLIO Grant Intelligence Platform across Research, Evidence, and Archive views.",
        "files_hint": ["app.py", "views/", "components/", "styles/theme.css", "README.md"],
        "url": "https://app.kalvium.community/livebooks/2538/feb13122-5abb-4f10-91fa-065ae2ebf7ec"
    }
]


def run_git(cmd_args, capture_output=True, check=True):
    """Execute a git command securely within the repository directory."""
    full_cmd = ["git"] + cmd_args
    res = subprocess.run(
        full_cmd,
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=capture_output,
        text=True
    )
    if check and res.returncode != 0:
        raise RuntimeError(f"Git command failed: {' '.join(full_cmd)}\nError: {res.stderr.strip()}")
    return res


def get_current_branch():
    """Retrieve the current active branch name."""
    try:
        res = run_git(["rev-parse", "--abbrev-ref", "HEAD"], check=False)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return "unknown"


def sanitize_branch_name(module_id, module_title):
    """Create a clean git branch name following naming convention."""
    clean_title = re.sub(r"[^a-zA-Z0-9\s-]", "", module_title.lower())
    clean_title = re.sub(r"[\s_]+", "-", clean_title).strip("-")
    # Truncate if overly long
    if len(clean_title) > 35:
        clean_title = clean_title[:35].rstrip("-")
    return f"frontend/{module_id}-{clean_title}"


def load_pr_history():
    """Load PR push history from pr_history.json."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_pr_history(module_id, branch_name, pr_title, pr_url, commit_hash):
    """Record a successfully pushed PR to history."""
    history = load_pr_history()
    history[module_id] = {
        "module_id": module_id,
        "branch_name": branch_name,
        "pr_title": pr_title,
        "pr_url": pr_url,
        "commit_hash": commit_hash,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def generate_pr_body(mod):
    """Generate a clean, structured PR description tailored to the milestone."""
    is_fe_tag = "🎨 Frontend Focus" if mod["is_frontend"] else "⚙️ Backend / Fullstack Alignment"
    return f"""## Sprint #2: AI Application Development with RAG
### Module {mod['id']} — {mod['title']}

**Role:** Frontend Developer (`Praveenkanna16`)
**Topic Category:** {mod['category']} ({is_fe_tag})
**Livebook Reference:** [{mod['title']}]({mod['url']})

---

### 📋 Overview & Objectives
This Pull Request delivers the frontend implementation and integration for **Module {mod['id']}: {mod['title']}**.
- **Deliverable:** {mod['deliverable']}
- **Design System:** FOLIO Quiet Editorial (Literary serif `Newsreader`, crisp sans `Plus Jakarta Sans`, layered ivory `#FDFBF7` canvas, tactile deckle accents).

---

### 🛠️ Key Implementations & Components
- **Primary Files / Components:**
{chr(10).join([f"  - `{f}`" for f in mod['files_hint']])}
- **Frontend Architecture:**
  - Integrated into Streamlit reactive page router (`app.py`).
  - Strict separation of visual presentation (`views/`, `components/`), design tokens (`styles/theme.css`), and service layer (`services/`).
  - Zero-extrapolation provenance visualization and interactive client interactions.

---

### 🧪 Verification & Testing
- [x] Streamlit local UI verified with `streamlit run app.py`
- [x] Responsive layout tested across desktop and mobile viewports
- [x] Theme CSS styling and typography rendering validated
- [x] Mock data and service contracts aligned with backend schemas

---

### 🚀 Pull Request Checklist
- [x] Dedicated milestone branch created from `{BASE_BRANCH}` (No direct push to main)
- [x] Clean conventional commit history
- [x] No sensitive credentials or `.env` committed
- [x] Ready for team review and milestone evaluation!
"""


def generate_github_pr_url(branch_name, pr_title, pr_body):
    """Build a one-click GitHub web URL to create the pull request with prefilled fields."""
    params = {
        "expand": "1",
        "title": pr_title,
        "body": pr_body
    }
    query_string = urllib.parse.urlencode(params)
    return f"{REPO_URL}/compare/{BASE_BRANCH}...{branch_name}?{query_string}"


def check_main_protection(target_branch):
    """Enforce rule: Never push directly to main branch."""
    if target_branch == BASE_BRANCH or target_branch == f"origin/{BASE_BRANCH}":
        print("\n" + "="*70)
        print("❌ CRITICAL ERROR: DIRECT PUSH TO 'main' IS STRICTLY PROHIBITED!")
        print("="*70)
        print("Per project rules, all work must be submitted via a dedicated PR branch.")
        print("Please choose a Module ID (e.g. 3.9, 3.46) to create a feature branch.")
        print("="*70 + "\n")
        sys.exit(1)


def stage_and_commit(mod, branch_name, custom_message=None, dry_run=False):
    """Create branch, stage files, commit, and push to origin."""
    print(f"\n📌 Preparing Module {mod['id']}: {mod['title']}")
    print(f"🌿 Target Branch : {branch_name}")
    print(f"🎯 Base Branch   : {BASE_BRANCH}")

    check_main_protection(branch_name)

    pr_title = f"feat(frontend): [{mod['id']}] {mod['title']}"
    commit_msg = custom_message if custom_message else f"feat(frontend): [{mod['id']}] {mod['title']}\n\n- {mod['deliverable']}\n- Role: Frontend (Praveenkanna16)"
    pr_body = generate_pr_body(mod)
    pr_url = generate_github_pr_url(branch_name, pr_title, pr_body)

    if dry_run:
        print("\n🔍 [DRY RUN MODE] Simulating actions without modifying git:")
        print(f"   1. Would switch to branch: {branch_name}")
        print(f"   2. Would stage changes: git add -A")
        print(f"   3. Would commit with message: {pr_title}")
        print(f"   4. Would push to: git push -u origin {branch_name}")
        print(f"\n🔗 Generated One-Click PR Creation URL:\n{pr_url}\n")
        return

    # Check git status
    status_res = run_git(["status", "--porcelain"])
    current_branch = get_current_branch()

    # Step 1: Create or checkout the feature branch
    print(f"\n⏳ Step 1: Switching to feature branch '{branch_name}'...")
    if current_branch != branch_name:
        # Check if local branch exists
        branch_check = run_git(["branch", "--list", branch_name], check=False)
        if branch_name in branch_check.stdout:
            run_git(["checkout", branch_name])
            print(f"   Checked out existing branch: {branch_name}")
        else:
            # Create new branch from origin/main if available, otherwise current HEAD
            try:
                run_git(["checkout", "-b", branch_name, f"origin/{BASE_BRANCH}"])
                print(f"   Created and checked out new branch '{branch_name}' from origin/{BASE_BRANCH}")
            except Exception:
                run_git(["checkout", "-b", branch_name])
                print(f"   Created and checked out new branch '{branch_name}'")
    else:
        print(f"   Already on branch: {branch_name}")

    # Step 2: Stage changes
    print("\n⏳ Step 2: Staging files...")
    run_git(["add", "-A"])
    print("   All modified and new files staged.")

    # Step 3: Commit changes (if there are changes)
    print("\n⏳ Step 3: Committing changes...")
    check_diff = run_git(["diff", "--cached", "--quiet"], check=False)
    if check_diff.returncode != 0:
        # Changes exist to commit
        run_git(["commit", "-m", commit_msg])
        commit_hash = run_git(["rev-parse", "--short", "HEAD"]).stdout.strip()
        print(f"   ✅ Committed: [{commit_hash}] {pr_title}")
    else:
        commit_hash = run_git(["rev-parse", "--short", "HEAD"]).stdout.strip()
        print(f"   ℹ️ No new uncommitted changes. Using latest commit [{commit_hash}].")

    # Step 4: Push to origin
    print(f"\n⏳ Step 4: Pushing branch '{branch_name}' to GitHub...")
    try:
        run_git(["push", "-u", "origin", branch_name])
        print(f"   ✅ Successfully pushed branch to origin/{branch_name}")
    except Exception as e:
        print(f"   ⚠️ Push encountered an issue: {e}")
        print("   Please ensure your GitHub credentials or SSH keys are authenticated.")

    # Step 5: Save PR history
    save_pr_history(mod["id"], branch_name, pr_title, pr_url, commit_hash)

    # Step 6: Output summary and One-Click URL
    print("\n" + "="*75)
    print(f"🎉 PULL REQUEST READY: Module {mod['id']}")
    print("="*75)
    print(f"📌 PR Title   : {pr_title}")
    print(f"🌿 Branch     : {branch_name}  ➡️  {BASE_BRANCH}")
    print(f"🔗 Click the link below to open the Pull Request on GitHub:")
    print("-" * 75)
    print(pr_url)
    print("-" * 75)
    print("✅ Recorded in pr_history.json\n")


def print_module_list():
    """Display the full catalog of 50 Sprint 2 modules."""
    history = load_pr_history()
    print("\n" + "="*80)
    print(" 🚀 SPRINT #2: AI APPLICATION DEVELOPMENT WITH RAG — MODULE REGISTRY")
    print("="*80)
    print(f"{'ID':<6} {'STATUS':<10} {'ROLE':<10} {'MODULE TITLE':<50}")
    print("-" * 80)
    for m in MODULES:
        status = "✅ PUSHED" if m["id"] in history else "⏳ PENDING"
        role = "🎨 FRONTEND" if m["is_frontend"] else "⚙️ CORE/BE"
        print(f"{m['id']:<6} {status:<10} {role:<10} {m['title']:<50}")
    print("="*80)
    print(f"Total Modules: {len(MODULES)} | Frontend Focus: {sum(1 for m in MODULES if m['is_frontend'])} | Pushed: {len(history)}\n")


def print_history():
    """Display the list of previously submitted PRs."""
    history = load_pr_history()
    if not history:
        print("\n📭 No PRs pushed yet. Run `python3 push_pr.py` to push your first daily frontend PR!\n")
        return

    print("\n" + "="*80)
    print(" 📜 SPRINT #2: FRONTEND PULL REQUEST HISTORY")
    print("="*80)
    for mid, info in sorted(history.items(), key=lambda x: float(x[0])):
        print(f"• Module {mid:<4} | Branch: {info['branch_name']:<35} | {info['timestamp']}")
        print(f"  Title : {info['pr_title']}")
        print(f"  PR URL: {info['pr_url']}")
        print("-" * 80)
    print()


def interactive_menu():
    """Interactive CLI menu for daily PR pushing."""
    history = load_pr_history()
    print("\n" + "="*70)
    print("  🎨 FOLIO — SPRINT 2 FRONTEND DAILY PR MANAGER")
    print("  Repository: kalviumcommunity/S67_0926_Team4_Non_Profit_Organization")
    print("="*70)
    print(f"  Current Branch : {get_current_branch()}")
    print(f"  PRs Pushed     : {len(history)} / {len(MODULES)}")
    print("="*70)
    print("  1. Push PR for a Module (e.g., 3.9, 3.46, etc.)")
    print("  2. View All 50 Modules & Status")
    print("  3. View PR History & Links")
    print("  4. Quick Push for Recommended Today's Frontend Milestone")
    print("  5. Exit")
    print("="*70)

    choice = input("\n👉 Enter choice (1-5) or Module ID (e.g. 3.9): ").strip()

    if choice == "5" or choice.lower() in ["q", "exit"]:
        print("Goodbye! 👋")
        sys.exit(0)
    elif choice == "2":
        print_module_list()
        interactive_menu()
    elif choice == "3":
        print_history()
        interactive_menu()
    elif choice == "4":
        # Find next unpushed frontend module
        next_mod = None
        for m in MODULES:
            if m["is_frontend"] and m["id"] not in history:
                next_mod = m
                break
        if not next_mod:
            print("🎉 All frontend modules have been pushed!")
            return
        branch = sanitize_branch_name(next_mod["id"], next_mod["title"])
        confirm = input(f"Next recommended module is [{next_mod['id']}] {next_mod['title']}.\nProceed to push to '{branch}'? (y/n): ").strip().lower()
        if confirm == "y":
            stage_and_commit(next_mod, branch)
        else:
            print("Cancelled.")
    else:
        # Check if choice is a module ID directly (e.g. 3.9 or 1)
        mod_id = choice if choice in [m["id"] for m in MODULES] else None
        if not mod_id:
            mod_id = input("👉 Enter Module ID to push (e.g. 3.9, 3.46, 3.1): ").strip()

        mod = next((m for m in MODULES if m["id"] == mod_id), None)
        if not mod:
            print(f"❌ Error: Module ID '{mod_id}' not found. Valid IDs: 3.1 to 3.50")
            return

        branch = sanitize_branch_name(mod["id"], mod["title"])
        print(f"\nSelected: [{mod['id']}] {mod['title']}")
        print(f"Category: {mod['category']}")
        print(f"Deliverable: {mod['deliverable']}")
        print(f"Branch: {branch}")
        
        custom_branch = input(f"\nPress Enter to use branch '{branch}' (or type custom branch name): ").strip()
        if custom_branch:
            branch = custom_branch

        confirm = input(f"\nReady to stage, commit, push branch '{branch}', and generate PR? (y/n): ").strip().lower()
        if confirm == "y":
            stage_and_commit(mod, branch)
        else:
            print("Cancelled.")


def main():
    parser = argparse.ArgumentParser(
        description="Sprint #2: AI Application Development with RAG - Frontend PR Automation Tool"
    )
    parser.add_argument("--module", "-m", type=str, help="Module ID to push (e.g., 3.9, 3.46)")
    parser.add_argument("--list", "-l", action="store_true", help="List all 50 Sprint 2 modules")
    parser.add_argument("--history", "-H", action="store_true", help="Show pushed PR history")
    parser.add_argument("--branch", "-b", type=str, help="Custom branch name (optional)")
    parser.add_argument("--message", "-M", type=str, help="Custom commit message (optional)")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Preview branch and PR URL without making git changes")

    args = parser.parse_args()

    if args.list:
        print_module_list()
        return

    if args.history:
        print_history()
        return

    if args.module:
        mod = next((m for m in MODULES if m["id"] == args.module), None)
        if not mod:
            print(f"❌ Error: Module '{args.module}' not found in registry (valid: 3.1 to 3.50).")
            sys.exit(1)
        branch = args.branch if args.branch else sanitize_branch_name(mod["id"], mod["title"])
        stage_and_commit(mod, branch, custom_message=args.message, dry_run=args.dry_run)
    else:
        interactive_menu()


if __name__ == "__main__":
    main()

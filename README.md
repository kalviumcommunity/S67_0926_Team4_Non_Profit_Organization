### S67_0926_Team4_Non_Profit_Organization

# FOLIO — Nonprofit Grant Intelligence & Funder Query Assistant

> An AI-powered RAG application that helps nonprofit teams quickly find, understand, and verify information across grant guidelines, donor agreements, impact reports, and other organizational documents.

---

## 📌 Overview

Nonprofit organizations often manage large collections of grant guidelines, donor agreements, impact reports, and funding documents. Relevant information can be scattered across multiple documents, making it difficult for program staff to quickly answer funder-related questions.

**FOLIO** provides a natural-language AI assistant that retrieves relevant information from organizational documents and generates grounded answers with source citations.

---

## 🎯 Problem Statement

A nonprofit organization holds grant guidelines, donor agreements, and impact reports, but program staff cannot quickly answer funder questions because the relevant clauses are scattered across many documents.

### Key Challenges

- Information is distributed across multiple documents.
- Documents can be long and difficult to search manually.
- Relevant information may use different terminology.
- Staff need answers that can be traced back to the original source.
- AI-generated answers must be grounded in available evidence.

---

## 💡 Solution

FOLIO uses **Retrieval-Augmented Generation (RAG)** to connect an LLM with the organization's document knowledge base.

The system:

1. Ingests organizational documents.
2. Extracts and cleans the text.
3. Splits documents into searchable chunks.
4. Generates embeddings.
5. Stores document information and embeddings.
6. Retrieves relevant evidence for user questions.
7. Provides the evidence to the LLM as context.
8. Generates a grounded answer.
9. Provides source citations for verification.
10. Can refuse to answer when sufficient evidence is unavailable.

---

## ✨ Key Features

### 🔎 Intelligent Document Search

Users can ask questions in natural language instead of manually searching through documents.

### 🤖 Agentic RAG

An orchestration layer can select appropriate retrieval tools such as vector search, keyword search, metadata filtering, and structured queries.

### 🧠 Semantic Search

Document chunks and user questions are converted into embeddings to retrieve semantically relevant information.

### 📚 Source Citations & Provenance

Answers are connected to their original documents, pages, sections, and retrieved evidence.

### 🔍 Evidence Verification

Users can trace an answer back to the original document and inspect the supporting evidence.

### 💬 Conversational RAG

Users can ask follow-up questions while maintaining relevant conversation context.

### 🧠 Memory

Mem0 can store and retrieve relevant reusable conversational context without sending the entire conversation history to the LLM.

### ⚡ Caching

Caching can reduce repeated computation and improve response performance.

### 🛡️ Grounded Answers

The system can check whether sufficient evidence is available before returning an answer.

---

## 🏗️ How It Works

### Document Ingestion

```text
Documents
    ↓
Upload
    ↓
Text Extraction
    ↓
Cleaning
    ↓
Chunking
    ↓
Metadata
    ↓
Embeddings
    ↓
Qdrant
```

### Question Answering

```text
User
  ↓
Web App
  ↓
User Question
  ↓
Backend API
  ↓
Cache Check
  ↓
RAG Orchestrator
  ↓
Retrieval
  ↓
Relevant Evidence
  ↓
Context Assembly
  ↓
LLM
  ↓
Grounding & Citation
  ↓
Answer
```

---

## 🗄️ Data Layer

| Component | Purpose |
|---|---|
| PostgreSQL | Structured document and application metadata |
| Qdrant | Vector storage and semantic retrieval |
| S3 / MinIO | Original document storage |
| Mem0 | Relevant conversational memory |
| Redis / Cache | Performance optimization |

---

## 🛠️ Tech Stack

### Frontend
- Next.js
- React
- TypeScript

### Backend
- Python
- FastAPI

### AI / RAG
- Large Language Model API
- Embedding Model / API
- Retrieval-Augmented Generation
- Agent / Tool Orchestration

### Data & Storage
- PostgreSQL
- Qdrant
- S3 / MinIO
- Redis
- Mem0

---

## 📁 Project Structure

```text
FOLIO/
├── frontend/
├── backend/
├── data/
├── evaluation/
├── tests/
├── docs/
├── .env.example
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 👥 Team Responsibilities

### Database & Retrieval
- PostgreSQL
- Document and chunk metadata
- S3 / MinIO
- Qdrant
- Embeddings
- Vector search
- Retrieval integration

### RAG & LLM
- RAG orchestration
- Prompt construction
- LLM integration
- Grounding
- Citations
- Hallucination guardrails

### Full Stack / Application
- Frontend
- Backend APIs
- Chat interface
- Document upload
- Evidence interface
- Integration
- Deployment

---

## 🚧 Project Status

**In Development**

FOLIO is currently being developed as an AI-powered nonprofit document intelligence and Retrieval-Augmented Generation application.

---

## 🔮 Future Scope

- Advanced hybrid search
- Improved re-ranking
- Multi-document reasoning
- Better citation highlighting
- Document comparison
- Streaming responses
- Improved RAG evaluation
- Usage analytics
- Multi-tenant support

---

## 🎓 Academic Context

FOLIO is developed as part of an academic project focused on:

- Large Language Model applications
- Retrieval-Augmented Generation
- Document processing
- Embeddings
- Vector databases
- Agentic AI
- Full-stack application development
- AI evaluation and deployment

# S67_0926_Team4_Non_Profit_Organization

# FOLIO — Nonprofit Grant Intelligence & Funder Query Assistant

> An AI-powered RAG application that helps nonprofit teams quickly find, understand, and verify information across grant guidelines, donor agreements, impact reports, policy documents, and organizational data.

---

## 📌 Overview

Nonprofit organizations manage large collections of grant guidelines, donor agreements, impact reports, policy documents, transaction records, and other organizational information.

Relevant information can be scattered across multiple documents and data sources, making it difficult for staff to quickly find the information they need.

**FOLIO** uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from the organization's knowledge base and provide grounded answers with source citations.

The system is designed to reduce the time spent manually searching through documents while maintaining traceability between answers and their original sources.

---

## 🎯 Problem Statement

A nonprofit organization holds grant guidelines, donor agreements, and impact reports, but program staff cannot quickly answer funder questions because the relevant clauses are scattered across many documents.

### Key Challenges

- Information is distributed across multiple documents and data sources.
- Documents can be long and difficult to search manually.
- Relevant information may use different terminology.
- Staff need answers that can be traced back to the original source.
- Organizational data must be validated before processing.
- AI-generated answers must be grounded in available evidence.
- Updated documents need to be detected and reflected in the knowledge base.

---

## 💡 Solution

FOLIO uses **Retrieval-Augmented Generation (RAG)** to connect an LLM with the organization's document and data knowledge base.

The system:

1. Ingests organizational documents and structured data.
2. Validates incoming data against defined schemas.
3. Extracts and cleans document text.
4. Detects duplicate documents and records.
5. Splits documents into meaningful chunks.
6. Generates vector embeddings for document chunks.
7. Stores embeddings in Pinecone.
8. Stores structured metadata and records in SQL.
9. Retrieves the most relevant information for user questions.
10. Applies metadata filters such as document type, date, version, and access level.
11. Provides retrieved evidence to the LLM as context.
12. Generates a grounded answer based on the retrieved information.
13. Provides source citations for verification.
14. Returns a clear "no information found" response when the available evidence does not support an answer.

---

## ✨ Key Features

### 🔎 Natural Language Information Retrieval

Users can ask questions in natural language instead of manually searching through multiple organizational documents.

### 🧠 Semantic Search

Document chunks and user queries are represented using vector embeddings, allowing the system to retrieve semantically relevant information.

### 📚 Source Citations & Provenance

Answers include source information such as:

- Document name
- Section or page
- Version
- Date

This allows users to trace answers back to the original information.

### 🔍 Metadata-Based Retrieval

Retrieval can be filtered using document metadata such as:

- Document type
- Date
- Version
- Access level

### 💬 Conversational Question Answering

The system supports natural-language interaction so users can ask questions and follow-up questions about organizational information.

### 🛡️ Grounded Answers

The system is designed to generate answers only from retrieved evidence and return a **"no information found"** response when sufficient supporting information is unavailable.

### 📄 Document & Data Ingestion

The system supports organizational documents and structured data including:

- Grant guidelines
- Donor agreements
- Impact reports
- Policy documents
- Transaction and donation records
- Backend pipeline metrics
- Deployment history
- Team ownership data

---

## 🏗️ How It Works

### Document & Data Ingestion

```text
Documents / Structured Data
            ↓
       Data Ingestion
            ↓
      Schema Validation
            ↓
   Text Extraction & Cleaning
            ↓
      Duplicate Detection
            ↓
          Chunking
            ↓
       Metadata Creation
            ↓
       Embedding Generation
            ↓
      ┌──────────────────┐
      │                  │
      ▼                  ▼
     SQL             Pinecone
      │                  │
      └────────┬─────────┘
               ↓
        Knowledge Base
```

Question Answering
```
User
  ↓
Streamlit Application
  ↓
Natural-Language Question
  ↓
Query Processing
  ↓
Pinecone Retrieval
  ↓
Metadata Filtering
  ↓
Relevant Evidence
  ↓
Context Construction
  ↓
LLM / RAG
  ↓
Grounding Check
  ↓
Answer + Source Citations
```

### 🗄️ Data Layer

Component	Purpose
SQL	Structured document metadata, transaction records, and processing logs
Pinecone	Vector embeddings, semantic search, and Top-K retrieval
File-based document storage	Input documents used for ingestion and processing

The PRD specifies SQL as the structured data layer and Pinecone as the vector database.

### 📊 Data Sources

FOLIO is designed to work with multiple organizational data sources.

Data Source	Example Information
Documents	Grant guidelines, donor agreements, impact reports, policies
Transactions	Donations and transaction records
Backend Metrics	CPU utilization, memory, storage, requests handled
Deployment History	Deployment ID, service, version, deployment time
Team Ownership	Service, team, cost center

All incoming data is expected to pass schema validation and preprocessing before being used by the system.

### 🛠️ Tech Stack

- Core Development
- Python
- NumPy
- Scikit-learn
- AI / RAG
- Large Language Model
- Embedding Model / API
- Retrieval-Augmented Generation
- Vector Embeddings

Data & Retrieval
- Pinecone — Vector database and semantic retrieval
- SQL — Structured data and metadata storage
- Document Processing
- Py2Pdf — PDF document processing

Application
- Streamlit — User interface and application layer

### 🔄 RAG Pipeline

FOLIO follows a Retrieval-Augmented Generation architecture:

User Question
      ↓
Query Representation
      ↓
Vector Retrieval
      ↓
Top-K Relevant Chunks
      ↓
Metadata Filtering
      ↓
Retrieved Evidence
      ↓
Context Assembly
      ↓
LLM
      ↓
Grounded Answer
      ↓
Source Citation

The LLM receives retrieved organizational information as context so that responses can be grounded in the available knowledge base.

📁 Project Structure

```text
FOLIO/
├── src/
│   ├── ingestion/
│   ├── processing/
│   ├── embeddings/
│   ├── retrieval/
│   ├── database/
│   └── rag/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── tests/
├── docs/
├── app/
├── requirements.txt
├── .env.example
└── README.md
```

### 👥 Team Responsibilities


#### Data Engineering & Retrieval

- Data schema design and validation
- Data cleaning and preprocessing
- Document metadata management
- Transaction and organizational data processing
- Document chunking
- Checksum-based duplicate detection
- Document version/change detection
- Embedding generation
- Pinecone vector indexing
- Metadata-based retrieval
- SQL data storage
- Processing and pipeline logs
- Data quality validation
- Knowledge-base refresh and maintenance

#### RAG & AI

- RAG pipeline design
- Query processing
- Context construction
- Prompt construction
- LLM integration
- Grounded answer generation
- Source citation and attribution
- Hallucination and refusal handling
- Sensitive-information guardrails
- RAG evaluation and answer quality

#### Application & Integration

- Streamlit application
- Chat interface
- Document management interface
- Retrieval integration
- Metadata and date-range filters
- Citation and source presentation
- Monitoring interface
- Application integration and delivery

#### 📈 Evaluation Targets

The project defines the following target metrics:

- Metric	Target
- Answer Accuracy	≥ 90%
- Retrieval Relevance — Recall@5	≥ 85%
- Citation Coverage	100%
- Pinecone Query Latency	< 1 second (p95)
- End-to-End Response Time	< 10 seconds (p95)
- Pipeline Test Coverage	≥ 80%
- Data Schema Validation	100%
- Vector Index Completeness	100%

The system also targets reliable handling of sensitive-information requests and data-quality issues.

### 🔐 Data Validation & Reliability

FOLIO is designed to validate data before it enters the knowledge base.

The ingestion pipeline includes:

- Schema validation
- Missing-field handling
- Duplicate detection
- Checksum-based document change detection
- Malformed record logging
- Document version tracking
- Processing logs
- Data quality checks

Malformed or unreadable records should be isolated and logged rather than causing the entire ingestion pipeline to fail.

### 🛡️ Security & Privacy

The project is designed to handle organizational information responsibly.

Development and evaluation use synthetic or anonymized data where appropriate.

Sensitive configuration such as API keys should be stored through environment variables and should not be committed to the repository.

The system is also designed to identify and flag sensitive-information requests according to the PRD's guardrail requirements.

### 🚧 Project Status

In Development

FOLIO is being developed as an AI-powered nonprofit information retrieval system using Retrieval-Augmented Generation, semantic search, structured data storage, and source-based answer generation.

### 🎓 Academic Context

FOLIO is developed as part of an academic project focused on:

- Large Language Model Applications
- Retrieval-Augmented Generation
- Document Processing
- Text Chunking
- Embeddings
- Vector Databases
- Semantic Search
- Data Engineering
- Structured Data Management
- AI Evaluation
- Streamlit Application Development


### 📌 Project Goals

FOLIO aims to provide nonprofit teams with:

- Faster access to organizational information
- Reliable retrieval from multiple documents
- Grounded AI-generated answers
- Source traceability and verification
- Structured organizational data management
- A reusable foundation for future AI-powered information systems

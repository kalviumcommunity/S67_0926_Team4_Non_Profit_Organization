"""
FOLIO Platform - Pinecone Vector Database & Semantic Embedding Utilities.
Provides robust indexing, upserting, and vector similarity search.
"""

import os
from typing import List, Dict, Any, Optional, Tuple
from pinecone import Pinecone, ServerlessSpec
import streamlit as st

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "folio-grants")
DEFAULT_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "folio-doc")
EMBEDDING_DIMENSION = 384  # 'all-MiniLM-L6-v2' dimension


class LocalFallbackEmbeddingModel:
    """Lightweight deterministic fallback embedding generator when heavy weights are unavailable."""
    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def encode(self, texts):
        import hashlib
        import numpy as np
        
        is_single = isinstance(texts, str)
        text_list = [texts] if is_single else texts
        embeddings = []
        for t in text_list:
            # Deterministic pseudo-embedding based on sha256 hash
            seed = int(hashlib.md5(t.encode("utf-8")).hexdigest(), 16) % (2**32)
            rng = np.random.RandomState(seed)
            vec = rng.randn(self.dimension)
            vec = vec / (np.linalg.norm(vec) + 1e-9)
            embeddings.append(vec.tolist())
        return embeddings[0] if is_single else embeddings


@st.cache_resource(show_spinner="Initializing Pinecone & semantic embeddings...")
def get_pinecone_and_embedding_model(api_key: Optional[str] = None):
    """
    Initializes Pinecone client and the sentence-transformers embedding model.
    Cached across Streamlit runs to prevent duplicate weight loading.
    """
    # 1. Resolve API key
    pinecone_api_key = api_key
    if not pinecone_api_key:
        try:
            pinecone_api_key = st.secrets.get("PINECONE_API_KEY")
        except Exception:
            pass
    if not pinecone_api_key:
        pinecone_api_key = os.getenv("PINECONE_API_KEY")

    if not pinecone_api_key:
        raise ValueError("PINECONE_API_KEY is not configured in .env or secrets.toml.")

    pc = Pinecone(api_key=pinecone_api_key)

    # 2. Resolve embedding model
    embedding_model = None
    if SentenceTransformer is not None:
        try:
            embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            st.warning(f"Could not load SentenceTransformer ('all-MiniLM-L6-v2'): {e}. Using deterministic fallback.")
            embedding_model = LocalFallbackEmbeddingModel(dimension=EMBEDDING_DIMENSION)
    else:
        embedding_model = LocalFallbackEmbeddingModel(dimension=EMBEDDING_DIMENSION)

    return pc, embedding_model


def initialize_pinecone_index(pc: Pinecone, index_name: str = INDEX_NAME, dimension: int = EMBEDDING_DIMENSION):
    """
    Checks for the Pinecone index and creates a serverless index if it doesn't exist.
    """
    try:
        existing_indexes = [idx.name for idx in pc.list_indexes()]
        if index_name not in existing_indexes:
            st.info(f"Creating new Pinecone index: '{index_name}' ({dimension}-dim, cosine). This may take ~30 seconds...")
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        return pc.Index(index_name)
    except Exception as e:
        st.error(f"Error initializing Pinecone index '{index_name}': {e}")
        try:
            return pc.Index(index_name)
        except Exception:
            return None


def upsert_chunks_to_pinecone(
    index,
    chunks: List[str],
    namespace: str = DEFAULT_NAMESPACE,
    doc_id: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
    embedding_model = None
) -> bool:
    """
    Embeds and upserts text chunks into the specified Pinecone namespace.
    """
    if not index or not chunks:
        return False

    if embedding_model is None:
        try:
            _, embedding_model = get_pinecone_and_embedding_model()
        except Exception as e:
            st.error(f"Cannot acquire embedding model: {e}")
            return False

    vectors_to_upsert = []
    base_meta = extra_metadata or {}
    
    for i, chunk in enumerate(chunks):
        try:
            raw_emb = embedding_model.encode(chunk)
            embedding = raw_emb.tolist() if hasattr(raw_emb, "tolist") else raw_emb
            
            chunk_id = f"{doc_id or 'chunk'}_{i}"
            meta = {
                "text": chunk,
                "chunk_index": i,
                "total_chunks": len(chunks),
                **base_meta
            }
            vectors_to_upsert.append({
                "id": chunk_id,
                "values": embedding,
                "metadata": meta
            })
        except Exception as e:
            st.warning(f"Error embedding chunk {i}: {e}")

    try:
        # Upsert in batches of 50
        batch_size = 50
        for b_start in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[b_start:b_start + batch_size]
            index.upsert(vectors=batch, namespace=namespace or DEFAULT_NAMESPACE)
        return True
    except Exception as e:
        st.error(f"Failed to upsert data to Pinecone: {e}")
        return False


def query_pinecone(
    index,
    question: str,
    top_k: int = 4,
    namespace: str = DEFAULT_NAMESPACE,
    embedding_model = None
) -> str:
    """
    Queries Pinecone to get relevant text chunks for a question.
    Returns concatenated context string.
    """
    if not index or not question.strip():
        return ""

    if embedding_model is None:
        try:
            _, embedding_model = get_pinecone_and_embedding_model()
        except Exception as e:
            st.error(f"Cannot acquire embedding model: {e}")
            return ""

    try:
        raw_emb = embedding_model.encode(question)
        query_embedding = raw_emb.tolist() if hasattr(raw_emb, "tolist") else raw_emb

        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace or DEFAULT_NAMESPACE
        )

        matches = results.get("matches", []) if isinstance(results, dict) else getattr(results, "matches", [])
        extracted_texts = []
        for match in matches:
            meta = match.get("metadata", {}) if isinstance(match, dict) else getattr(match, "metadata", {})
            if meta and "text" in meta:
                score = match.get("score") if isinstance(match, dict) else getattr(match, "score", 0)
                extracted_texts.append(f"[Relevance: {round(score, 3) if score else 'N/A'}]\n{meta['text']}")

        return "\n\n---\n\n".join(extracted_texts)
    except Exception as e:
        st.warning(f"Pinecone query warning: {e}")
        return ""


def query_pinecone_structured(
    index,
    question: str,
    top_k: int = 4,
    namespace: str = DEFAULT_NAMESPACE,
    embedding_model = None
) -> List[Dict[str, Any]]:
    """
    Queries Pinecone and returns structured match list with scores, texts, and source metadata.
    """
    if not index or not question.strip():
        return []

    if embedding_model is None:
        try:
            _, embedding_model = get_pinecone_and_embedding_model()
        except Exception:
            return []

    try:
        raw_emb = embedding_model.encode(question)
        query_embedding = raw_emb.tolist() if hasattr(raw_emb, "tolist") else raw_emb

        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace or DEFAULT_NAMESPACE
        )

        matches = results.get("matches", []) if isinstance(results, dict) else getattr(results, "matches", [])
        items = []
        for match in matches:
            meta = match.get("metadata", {}) if isinstance(match, dict) else getattr(match, "metadata", {})
            score = match.get("score", 0) if isinstance(match, dict) else getattr(match, "score", 0)
            mid = match.get("id", "") if isinstance(match, dict) else getattr(match, "id", "")
            items.append({
                "id": mid,
                "score": float(score) if score else 0.0,
                "text": meta.get("text", "") if meta else "",
                "metadata": meta or {}
            })
        return items
    except Exception as e:
        st.warning(f"Pinecone structured query error: {e}")
        return []

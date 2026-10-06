"""FOLIO embedding and Pinecone indexing package."""
from .embed_and_index import EmbeddingError, embed_chunks, index_chunks
__all__ = ["EmbeddingError", "embed_chunks", "index_chunks"]

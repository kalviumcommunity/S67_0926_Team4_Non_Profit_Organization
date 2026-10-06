"""Unit tests for FOLIO AI and Multimedia RAG Modules."""

import io
from PIL import Image
from modules.openrouter_utils import (
    PERSONA_PROMPTS,
    FORMAT_PROMPTS,
    get_openrouter_response,
    resolve_openrouter_api_key,
    DEFAULT_OPENROUTER_MODEL
)
from modules.gemini_utils import get_gemini_response
from modules.pinecone_utils import LocalFallbackEmbeddingModel
from modules.utils import encode_image_to_base64, process_image
from services.rag_service import rag_service
from services.document_service import document_service


def test_persona_and_format_prompts():
    """Verify standard personas and formats are defined."""
    assert "Default" in PERSONA_PROMPTS
    assert "Expert Analyst" in PERSONA_PROMPTS
    assert "Creative Brainstormer" in PERSONA_PROMPTS
    assert "ELI5 (Explain Like I'm 5)" in PERSONA_PROMPTS

    assert "Default" in FORMAT_PROMPTS
    assert "Bullet Points" in FORMAT_PROMPTS
    assert "JSON" in FORMAT_PROMPTS
    assert "Short Paragraph" in FORMAT_PROMPTS


def test_openrouter_response_without_key():
    """Test that missing API key returns a clear instructional message without crashing."""
    res = get_openrouter_response("Hello", api_key="")
    assert "OpenRouter API Key Required" in res or "API Key" in res


def test_gemini_alias():
    """Test that get_gemini_response functions properly as alias."""
    res = get_gemini_response("What is the reporting rule?")
    assert isinstance(res, str)


def test_fallback_embedding_model():
    """Test the deterministic 384-dimensional embedding generator."""
    model = LocalFallbackEmbeddingModel(dimension=384)
    vec = model.encode("Helios Foundation reporting guidelines")
    assert len(vec) == 384
    assert isinstance(vec[0], float)


def test_image_base64_encoding():
    """Test PIL image to base64 data URI conversion."""
    img = Image.new("RGB", (32, 32), color="red")
    b64 = encode_image_to_base64(img)
    assert b64.startswith("data:image/jpeg;base64,")


def test_rag_service_query():
    """Test RAG service synthesis and telemetry generation."""
    res = rag_service.ask_question(
        query="What are the reporting requirements?",
        persona="Expert Analyst",
        output_format="Bullet Points"
    )
    assert res["status"] == "success"
    data = res["data"]
    assert "question" in data
    assert "pipeline_telemetry" in data
    assert len(data["sources"]) > 0


def test_document_service_upload():
    """Test document upload and hashing."""
    sample_txt = b"Section 1. Helios Foundation quarterly grant reporting directives."
    doc = document_service.upload_document(sample_txt, "test_agreement.txt")
    assert doc["id"].startswith("DOC-UP-")
    assert doc["sha256"] is not None
    assert len(doc["sha256"]) == 64

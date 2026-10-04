from src.preprocessing.chunk_documents import (
    chunk_document,
    split_into_sections,
    split_with_overlap,
)


def document(text):
    return {
        "document_id": "doc123",
        "source_file": "example.pdf",
        "pages": [{"page_number": 1, "text": text}],
    }


def test_sections_are_detected():
    sections = split_into_sections(
        "Eligibility Criteria\n"
        "Registered animal welfare organizations may apply.\n"
        "Funding Conditions\n"
        "Funds must be used for approved activities."
    )

    assert [item["section"] for item in sections] == [
        "Eligibility Criteria",
        "Funding Conditions",
    ]


def test_short_section_remains_one_chunk():
    chunks = chunk_document(
        document(
            "Eligibility Criteria\n"
            "Registered animal welfare organizations may apply."
        ),
        chunk_size=50,
        overlap=5,
    )

    assert len(chunks) == 1
    assert chunks[0]["section"] == "Eligibility Criteria"
    assert chunks[0]["page_number"] == 1
    assert chunks[0]["document_id"] == "doc123"


def test_long_section_uses_overlap():
    text = "Eligibility Criteria\n" + " ".join(
        f"word{i}" for i in range(120)
    )

    chunks = chunk_document(document(text), chunk_size=50, overlap=10)

    assert len(chunks) == 3

    first = chunks[0]["text"].split()
    second = chunks[1]["text"].split()

    assert first[-10:] == second[:10]


def test_metadata_is_preserved_for_each_chunk():
    chunks = chunk_document(
        document(
            "Funding Conditions\n"
            "The funds may be used for approved animal welfare activities."
        ),
        chunk_size=20,
        overlap=5,
    )

    assert chunks
    assert all(chunk["document_id"] == "doc123" for chunk in chunks)
    assert all(chunk["page_number"] == 1 for chunk in chunks)
    assert all(chunk["section"] == "Funding Conditions" for chunk in chunks)
    assert all(chunk["chunk_id"] for chunk in chunks)


def test_empty_page_creates_no_chunks():
    assert chunk_document(document("")) == []


def test_invalid_chunk_settings_raise_error():
    try:
        split_with_overlap("some text", chunk_size=10, overlap=10)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid overlap")

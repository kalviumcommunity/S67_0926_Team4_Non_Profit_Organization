"""Context formatting for FOLIO RAG responses."""

def build_context(results: list[dict]) -> tuple[str, list[dict]]:
    """Build grounded context and source metadata from retrieval results."""
    if not isinstance(results, list):
        raise ValueError("results must be a list")

    context_parts = []
    sources = []

    for index, result in enumerate(results, start=1):
        text = (result.get("text") or "").strip()
        if not text:
            continue

        source_file = result.get("source_file") or "Unknown source"
        page = result.get("page_number")
        section = result.get("section") or "Unknown section"

        location = f"{source_file}"
        if page is not None:
            location += f", page {page}"

        context_parts.append(
            f"[Source {index}] {location}\n"
            f"Section: {section}\n"
            f"{text}"
        )

        sources.append({
            "source_file": result.get("source_file"),
            "page_number": page,
            "section": result.get("section"),
            "document_id": result.get("document_id"),
            "chunk_id": result.get("chunk_id"),
            "score": result.get("score"),
        })

    return "\n\n".join(context_parts), sources

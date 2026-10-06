"""Section-aware document chunking for FOLIO.

This module consumes the processed JSON documents produced by the PDF
ingestion pipeline and creates retrieval-ready chunks.

The implementation follows the PRD requirement for section-aware chunking:
- preserve document/page/source metadata
- keep meaningful sections together where possible
- split oversized sections into smaller overlapping chunks
- write deterministic JSON output for the downstream embedding stage

Chunk size and overlap are expressed as configurable word counts for this
stage. Token-aware sizing is intentionally not implemented here because the
embedding model/tokenizer is a downstream concern.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_CHUNK_SIZE = 500
DEFAULT_OVERLAP = 50

# Heading patterns are intentionally conservative. They support common
# numbered headings and title-style headings in grant/animal-welfare PDFs.
NUMBERED_HEADING_RE = re.compile(
    r"^\s*(?:section\s+)?\d+(?:\.\d+)*[.)]?\s+[A-Za-z][A-Za-z0-9/&(),:'\- ]{1,100}\s*$",
    re.IGNORECASE,
)


def normalize_text(text: str) -> str:
    """Normalize whitespace without destroying line boundaries."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = []
    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def is_heading(line: str) -> bool:
    """Identify likely standalone section headings."""
    line = line.strip()

    if not line or len(line) > 100:
        return False

    if NUMBERED_HEADING_RE.match(line):
        return True

    if line.endswith((".", "?", "!")):
        return False

    words = line.split()
    if not 1 <= len(words) <= 10:
        return False

    # All-caps headings are common in reports.
    if any(ch.isalpha() for ch in line) and line.upper() == line:
        return True

    # Title-case headings are useful when they contain at least two words.
    if len(words) >= 2 and all(
        (not word[0].isalpha()) or word[0].isupper()
        for word in words
    ):
        return True

    return False


def split_into_sections(text: str) -> list[dict[str, str]]:
    """Split page text into named sections."""
    text = normalize_text(text)
    if not text:
        return []

    sections: list[dict[str, str]] = []
    current_heading = "Document"
    current_lines: list[str] = []

    for line in text.split("\n"):
        if is_heading(line):
            if current_lines:
                body = "\n".join(current_lines).strip()
                if body:
                    sections.append(
                        {"section": current_heading, "text": body}
                    )
                current_lines = []
            current_heading = line
        else:
            current_lines.append(line)

    body = "\n".join(current_lines).strip()
    if body:
        sections.append({"section": current_heading, "text": body})

    return sections


def split_with_overlap(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[str]:
    """Split text into overlapping word windows."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    words = text.split()
    if not words:
        return []

    step = chunk_size - overlap
    chunks: list[str] = []

    for start in range(0, len(words), step):
        current = words[start : start + chunk_size]
        if not current:
            break
        chunks.append(" ".join(current))
        if start + chunk_size >= len(words):
            break

    return chunks


def _document_pages(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Return page records from the ingestion output."""
    pages = document.get("pages")
    if not isinstance(pages, list):
        raise ValueError("Processed document must contain a 'pages' list")
    return pages


def chunk_document(
    document: dict[str, Any],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[dict[str, Any]]:
    """Create section-aware chunks from one processed document."""
    document_id = str(document.get("document_id", "")).strip()
    if not document_id:
        raise ValueError("Processed document is missing document_id")

    source_file = document.get("source_filename")

    chunks: list[dict[str, Any]] = []

    for page in _document_pages(document):
        page_number = page.get("page_number")
        page_text = page.get("text", "")

        if not isinstance(page_text, str) or not page_text.strip():
            continue

        sections = split_into_sections(page_text)

        for section in sections:
            section_name = section["section"]
            section_text = section["text"]

            for section_chunk_index, chunk_text in enumerate(
                split_with_overlap(section_text, chunk_size, overlap),
                start=1,
            ):
                chunks.append(
                    {
                        "document_id": document_id,
                        "chunk_id": (
                            f"{document_id}_chunk_{len(chunks) + 1:04d}"
                        ),
                        "page_number": page_number,
                        "section": section_name,
                        "section_chunk_index": section_chunk_index,
                        "text": chunk_text,
                        "source_file": source_file,
                    }
                )

    return chunks


def write_chunks(
    input_path: Path,
    output_dir: Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> Path:
    """Chunk one processed document and atomically write its JSON output."""
    with input_path.open("r", encoding="utf-8") as file:
        document = json.load(file)

    chunks = chunk_document(document, chunk_size, overlap)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{input_path.stem}_chunks.json"
    temp_path = output_path.with_suffix(".tmp")

    payload = {
        "document_id": document["document_id"],
        "source_file": document.get("source_file"),
        "chunk_count": len(chunks),
        "chunks": chunks,
    }

    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")

    temp_path.replace(output_path)
    return output_path


def process_directory(
    input_dir: Path,
    output_dir: Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> dict[str, int]:
    """Process all JSON documents in a directory."""
    processed = 0
    failed = 0

    for input_path in sorted(input_dir.glob("*.json")):
        try:
            write_chunks(input_path, output_dir, chunk_size, overlap)
            processed += 1
        except (OSError, ValueError, json.JSONDecodeError, KeyError):
            failed += 1

    return {"processed": processed, "failed": failed}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create section-aware FOLIO document chunks."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/processed/documents"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed/chunks"),
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help="Maximum words per chunk.",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=DEFAULT_OVERLAP,
        help="Overlapping words between adjacent chunks.",
    )
    args = parser.parse_args()

    result = process_directory(
        args.input_dir,
        args.output_dir,
        args.chunk_size,
        args.overlap,
    )
    print(f"processed: {result['processed']}")
    print(f"failed: {result['failed']}")


if __name__ == "__main__":
    main()

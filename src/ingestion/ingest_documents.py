"""Safe, deterministic PDF text extraction for the FOLIO data pipeline."""
from __future__ import annotations
import argparse, hashlib, json, logging, os, re, tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from pypdf import PdfReader
from pypdf.errors import PdfReadError

LOGGER = logging.getLogger(__name__)
PDF_MAGIC = b"%PDF-"
DEFAULT_MAX_BYTES = 50 * 1024 * 1024
DEFAULT_MAX_PAGES = 2000

class IngestionError(ValueError):
    """Raised when a PDF cannot be safely ingested."""

def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def _safe_stem(filename: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(filename).stem).strip("._-")
    return stem[:100] or "document"

def _atomic_write_json(destination: Path, payload: dict[str, Any]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=destination.parent,
            prefix=f".{destination.name}.", suffix=".tmp", delete=False
        ) as stream:
            temp_name = stream.name
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, destination)
    except Exception:
        if temp_name:
            try: os.unlink(temp_name)
            except FileNotFoundError: pass
        raise

def ingest_pdf(pdf_path: str | Path, output_dir: str | Path, *,
               max_bytes: int = DEFAULT_MAX_BYTES, max_pages: int = DEFAULT_MAX_PAGES,
               overwrite: bool = False) -> dict[str, Any]:
    """Extract a PDF to page-preserving JSON; raw input is never modified."""
    source, output = Path(pdf_path), Path(output_dir)
    if not source.is_file():
        raise IngestionError(f"PDF does not exist or is not a file: {source}")
    if source.suffix.lower() != ".pdf":
        raise IngestionError("Only .pdf files are supported")
    if max_bytes <= 0 or max_pages <= 0:
        raise ValueError("max_bytes and max_pages must be positive")
    size = source.stat().st_size
    if size == 0: raise IngestionError("PDF is empty")
    if size > max_bytes: raise IngestionError(f"PDF exceeds maximum size of {max_bytes} bytes")
    with source.open("rb") as stream:
        if stream.read(len(PDF_MAGIC)) != PDF_MAGIC:
            raise IngestionError("File does not have a valid PDF signature")
    checksum = _sha256(source)
    destination = output / f"{_safe_stem(source.name)}_{checksum[:12]}.json"
    if destination.exists() and not overwrite:
        try:
            existing = json.loads(destination.read_text(encoding="utf-8"))
            if existing.get("sha256") == checksum:
                return {"status":"skipped_duplicate","source":str(source),
                        "output":str(destination),"sha256":checksum,
                        "pages":existing.get("page_count",0)}
        except (OSError, json.JSONDecodeError):
            pass
    try:
        reader = PdfReader(str(source), strict=False)
        if reader.is_encrypted:
            try: unlocked = reader.decrypt("")
            except Exception as exc: raise IngestionError("Encrypted PDFs are not supported") from exc
            if not unlocked: raise IngestionError("Encrypted PDFs are not supported")
        count = len(reader.pages)
        if count == 0: raise IngestionError("PDF contains no pages")
        if count > max_pages: raise IngestionError(f"PDF exceeds maximum page count of {max_pages}")
        pages = []
        for number, page in enumerate(reader.pages, start=1):
            try: extracted = page.extract_text() or ""
            except Exception as exc: raise IngestionError(f"Text extraction failed on page {number}") from exc
            pages.append({"page_number":number,"text":extracted.strip()})
    except IngestionError: raise
    except (PdfReadError, OSError, ValueError, TypeError) as exc:
        raise IngestionError(f"Unable to read PDF: {exc}") from exc
    except Exception as exc:
        raise IngestionError(f"Unexpected PDF processing error: {exc}") from exc
    if not any(page["text"] for page in pages):
        raise IngestionError("No extractable text found; scanned PDFs may require OCR")
    metadata = reader.metadata
    payload = {
        "schema_version":1, "document_id":f"sha256:{checksum}",
        "source_filename":source.name, "document_type":"pdf", "sha256":checksum,
        "file_size_bytes":size, "page_count":count,
        "ingested_at":datetime.now(timezone.utc).isoformat(),
        "pdf_metadata":{key:getattr(metadata, key, None) if metadata else None
                        for key in ("title","author","subject","creator")},
        "extraction":{"engine":"pypdf","status":"completed","ocr_applied":False},
        "pages":pages,
    }
    _atomic_write_json(destination,payload)
    return {"status":"processed","source":str(source),"output":str(destination),
            "sha256":checksum,"pages":count}

def ingest_pdf_directory(input_dir: str | Path, output_dir: str | Path, *,
                         max_bytes: int = DEFAULT_MAX_BYTES, max_pages: int = DEFAULT_MAX_PAGES,
                         overwrite: bool = False) -> dict[str, Any]:
    """Process top-level PDFs independently and return a per-file summary."""
    source_dir=Path(input_dir)
    if not source_dir.is_dir(): raise IngestionError(f"Input directory does not exist: {source_dir}")
    results=[]
    for source in sorted(source_dir.iterdir(),key=lambda p:p.name.lower()):
        if not source.is_file() or source.suffix.lower() != ".pdf": continue
        try:
            results.append(ingest_pdf(source,output_dir,max_bytes=max_bytes,
                                      max_pages=max_pages,overwrite=overwrite))
        except IngestionError as exc:
            LOGGER.warning("Failed to ingest %s: %s",source.name,exc)
            results.append({"status":"failed","source":str(source),"error":str(exc)})
    return {"total":len(results),
            "processed":sum(r["status"]=="processed" for r in results),
            "duplicates":sum(r["status"]=="skipped_duplicate" for r in results),
            "failed":sum(r["status"]=="failed" for r in results),"results":results}

def main(argv: Iterable[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",default="data/raw/documents",help="PDF file or directory")
    parser.add_argument("--output",default="data/processed/documents",help="JSON output directory")
    parser.add_argument("--max-bytes",type=int,default=DEFAULT_MAX_BYTES)
    parser.add_argument("--max-pages",type=int,default=DEFAULT_MAX_PAGES)
    parser.add_argument("--overwrite",action="store_true",help="Reprocess matching output")
    args=parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO,format="%(levelname)s: %(message)s")
    try:
        source=Path(args.input)
        if source.is_dir():
            result=ingest_pdf_directory(source,args.output,max_bytes=args.max_bytes,
                max_pages=args.max_pages,overwrite=args.overwrite)
            print(json.dumps(result,indent=2))
            return 1 if result["failed"] else 0
        print(json.dumps(ingest_pdf(source,args.output,max_bytes=args.max_bytes,
            max_pages=args.max_pages,overwrite=args.overwrite),indent=2))
        return 0
    except (IngestionError,OSError,ValueError) as exc:
        LOGGER.error("%s",exc); return 1

if __name__=="__main__": raise SystemExit(main())

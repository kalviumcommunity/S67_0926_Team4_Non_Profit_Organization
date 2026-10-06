import json
import pytest
from src.ingestion import ingest_documents as module
from src.ingestion.ingest_documents import IngestionError, ingest_pdf, ingest_pdf_directory

class FakePage:
    def __init__(self,text): self.text=text
    def extract_text(self): return self.text
class FakeReader:
    def __init__(self,path,strict=False):
        self.is_encrypted=False
        self.pages=[FakePage(" Grant deadline: 30 November 2026 "),FakePage("Maximum grant: INR 15 lakh")]
        self.metadata=None
    def __len__(self): return len(self.pages)

def pdf(path):
    path.write_bytes(b"%PDF-1.7\nfake fixture")
    return path

def test_extracts_page_text_and_metadata(tmp_path,monkeypatch):
    monkeypatch.setattr(module,"PdfReader",FakeReader)
    source=pdf(tmp_path/"grant.pdf")
    result=ingest_pdf(source,tmp_path/"processed")
    assert result["status"]=="processed"
    data=json.loads((tmp_path/"processed"/(source.stem+"_"+result["sha256"][:12]+".json")).read_text())
    assert data["pages"]==[{"page_number":1,"text":"Grant deadline: 30 November 2026"},{"page_number":2,"text":"Maximum grant: INR 15 lakh"}]
    assert data["document_id"]=="sha256:"+result["sha256"]
    assert source.read_bytes().startswith(b"%PDF-")

def test_identical_input_is_idempotent(tmp_path,monkeypatch):
    monkeypatch.setattr(module,"PdfReader",FakeReader)
    source=pdf(tmp_path/"same.pdf")
    first=ingest_pdf(source,tmp_path/"out")
    second=ingest_pdf(source,tmp_path/"out")
    assert first["status"]=="processed"
    assert second["status"]=="skipped_duplicate"

def test_rejects_missing_wrong_extension_empty_and_bad_signature(tmp_path):
    with pytest.raises(IngestionError): ingest_pdf(tmp_path/"missing.pdf",tmp_path/"out")
    wrong=tmp_path/"wrong.txt"; wrong.write_text("x")
    with pytest.raises(IngestionError,match="Only .pdf"): ingest_pdf(wrong,tmp_path/"out")
    empty=tmp_path/"empty.pdf"; empty.write_bytes(b"")
    with pytest.raises(IngestionError,match="empty"): ingest_pdf(empty,tmp_path/"out")
    bad=tmp_path/"bad.pdf"; bad.write_bytes(b"not pdf")
    with pytest.raises(IngestionError,match="signature"): ingest_pdf(bad,tmp_path/"out")

def test_rejects_oversize_and_invalid_limits(tmp_path):
    source=pdf(tmp_path/"a.pdf")
    with pytest.raises(IngestionError,match="maximum size"): ingest_pdf(source,tmp_path/"out",max_bytes=2)
    with pytest.raises(ValueError,match="positive"): ingest_pdf(source,tmp_path/"out",max_pages=0)

def test_rejects_empty_or_scanned_text(tmp_path,monkeypatch):
    class BlankReader(FakeReader):
        def __init__(self,path,strict=False):
            super().__init__(path,strict); self.pages=[FakePage(" "),FakePage(None)]
    monkeypatch.setattr(module,"PdfReader",BlankReader)
    with pytest.raises(IngestionError,match="No extractable text"):
        ingest_pdf(pdf(tmp_path/"scan.pdf"),tmp_path/"out")

def test_directory_reports_individual_failures(tmp_path,monkeypatch):
    def reader(path, strict=False):
        if str(path).endswith("bad.pdf"):
            raise ValueError("malformed fixture")
        return FakeReader(path, strict)
    monkeypatch.setattr(module,"PdfReader",reader)
    source=tmp_path/"raw"; source.mkdir()
    pdf(source/"good.pdf"); (source/"bad.pdf").write_bytes(b"%PDF-invalid")
    (source/"ignore.txt").write_text("ignored")
    result=ingest_pdf_directory(source,tmp_path/"processed")
    assert result["total"]==2 and result["processed"]==1 and result["failed"]==1

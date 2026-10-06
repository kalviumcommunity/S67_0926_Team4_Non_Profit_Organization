from pathlib import Path
import pytest
from src.database.database import DatabaseError, init_db, add_document, get_document, update_document_status, log_ingestion, get_ingestion_logs

def doc(): return {'document_id':'sha256:test','source_filename':'test.pdf','document_type':'pdf','sha256':'abc','file_size_bytes':2048,'page_count':3,'version':'1','status':'ingested'}
def test_init(tmp_path):
    db=tmp_path/'folio.db'; init_db(db)
    import sqlite3
    with sqlite3.connect(db) as c: names={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {'documents','ingestion_logs'} <= names
def test_add_get(tmp_path):
    db=tmp_path/'folio.db'; add_document(doc(),db); r=get_document('sha256:test',db); assert r['source_filename']=='test.pdf' and r['page_count']==3
def test_duplicate(tmp_path):
    db=tmp_path/'folio.db'; add_document(doc(),db)
    with pytest.raises(DatabaseError): add_document(doc(),db)
def test_status(tmp_path):
    db=tmp_path/'folio.db'; add_document(doc(),db); update_document_status('sha256:test','completed',db); assert get_document('sha256:test',db)['status']=='completed'
def test_log(tmp_path):
    db=tmp_path/'folio.db'; add_document(doc(),db); lid=log_ingestion('sha256:test','embedding','completed',db_path=db); logs=get_ingestion_logs('sha256:test',db); assert lid==1 and logs[0]['stage']=='embedding'
def test_missing_document_log(tmp_path):
    with pytest.raises(DatabaseError): log_ingestion('missing','embedding','failed',db_path=tmp_path/'folio.db')

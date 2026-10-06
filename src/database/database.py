from __future__ import annotations
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
DEFAULT_DB_PATH='data/folio.db'
class DatabaseError(RuntimeError): pass
def _utc_now(): return datetime.now(timezone.utc).isoformat()
def _connect(db_path):
    path=Path(db_path); path.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(path); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
def init_db(db_path=DEFAULT_DB_PATH):
    try:
        with _connect(db_path) as c:
            c.executescript('''CREATE TABLE IF NOT EXISTS documents (document_id TEXT PRIMARY KEY, source_filename TEXT NOT NULL, document_type TEXT NOT NULL, sha256 TEXT NOT NULL UNIQUE, file_size_bytes INTEGER, page_count INTEGER, version TEXT, ingested_at TEXT NOT NULL, status TEXT NOT NULL); CREATE TABLE IF NOT EXISTS ingestion_logs (log_id INTEGER PRIMARY KEY AUTOINCREMENT, document_id TEXT NOT NULL, stage TEXT NOT NULL, status TEXT NOT NULL, started_at TEXT NOT NULL, completed_at TEXT, error_message TEXT, FOREIGN KEY(document_id) REFERENCES documents(document_id) ON DELETE CASCADE); CREATE INDEX IF NOT EXISTS idx_ingestion_logs_document ON ingestion_logs(document_id); CREATE INDEX IF NOT EXISTS idx_ingestion_logs_status ON ingestion_logs(status);''')
    except sqlite3.Error as e: raise DatabaseError(f'Database initialization failed: {e}') from e
def add_document(document:dict[str,Any],db_path=DEFAULT_DB_PATH):
    required=('document_id','source_filename','document_type','sha256'); missing=[k for k in required if not document.get(k)]
    if missing: raise DatabaseError(f"Missing required document fields: {', '.join(missing)}")
    try:
        init_db(db_path)
        with _connect(db_path) as c: c.execute('INSERT INTO documents VALUES (?,?,?,?,?,?,?,?,?)',(document['document_id'],document['source_filename'],document['document_type'],document['sha256'],document.get('file_size_bytes'),document.get('page_count'),document.get('version'),document.get('ingested_at') or _utc_now(),document.get('status','ingested')))
    except sqlite3.IntegrityError as e: raise DatabaseError(f'Document already exists or violates a database constraint: {e}') from e
    except sqlite3.Error as e: raise DatabaseError(f'Could not add document: {e}') from e
def get_document(document_id,db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    with _connect(db_path) as c: row=c.execute('SELECT * FROM documents WHERE document_id=?',(document_id,)).fetchone()
    return dict(row) if row else None
def update_document_status(document_id,status,db_path=DEFAULT_DB_PATH):
    if not status.strip(): raise ValueError('status must not be empty')
    init_db(db_path)
    with _connect(db_path) as c:
        cur=c.execute('UPDATE documents SET status=? WHERE document_id=?',(status,document_id))
        if cur.rowcount==0: raise DatabaseError(f'Document not found: {document_id}')
def log_ingestion(document_id,stage,status,started_at=None,completed_at=None,error_message=None,db_path=DEFAULT_DB_PATH):
    if not stage.strip(): raise ValueError('stage must not be empty')
    if not status.strip(): raise ValueError('status must not be empty')
    try:
        init_db(db_path)
        with _connect(db_path) as c:
            cur=c.execute('INSERT INTO ingestion_logs (document_id,stage,status,started_at,completed_at,error_message) VALUES (?,?,?,?,?,?)',(document_id,stage,status,started_at or _utc_now(),completed_at,error_message)); return int(cur.lastrowid)
    except sqlite3.IntegrityError as e: raise DatabaseError(f'Could not create ingestion log: {e}') from e
def get_ingestion_logs(document_id,db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    with _connect(db_path) as c: rows=c.execute('SELECT * FROM ingestion_logs WHERE document_id=? ORDER BY log_id ASC',(document_id,)).fetchall()
    return [dict(r) for r in rows]

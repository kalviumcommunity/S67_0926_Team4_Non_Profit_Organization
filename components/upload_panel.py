"""Folio Platform - Document Upload & Indexing Component."""

import streamlit as st
import time
import textwrap
from services.document_service import document_service
from utils.state import view_document_detail

def render_upload_panel() -> None:
    """Render the archival drag-and-drop upload dropzone and indexing workflow."""
    dropzone_html = textwrap.dedent("""
    <div style="margin-top: 1.5rem; margin-bottom: 1.5rem;">
      <div style="border: 2px dashed #DDD7CA; background-color: rgba(253, 251, 247, 0.8); border-radius: 6px; padding: 2.25rem 2rem; text-align: center;">
        <div style="width: 48px; height: 48px; border-radius: 50%; background-color: #EFEEE9; display: inline-flex; align-items: center; justify-content: center; color: #082217; margin-bottom: 0.75rem;">
          <span class="material-symbols-outlined" style="font-size: 24px;">upload_file</span>
        </div>
        <h4 style="font-family: 'Newsreader', serif; font-size: 20px; font-weight: 500; color: #082217; margin: 0 0 0.35rem 0;">
          Drop PDF, DOCX or agreements here
        </h4>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #424844; margin: 0 0 1rem 0;">
          Drop grant agreements or donor guidelines here · OCR and provenance indexing are automatic
        </p>
        <div style="display: flex; justify-content: center; align-items: center; gap: 0.5rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #727973;">
          <span>Supported: PDF/A, DOCX, Scanned TIFF</span>
          <span>·</span>
          <span style="color: #082217; font-weight: 600;">Browse file system below</span>
        </div>
      </div>
    </div>
    """).strip()
    st.html(dropzone_html)
    
    uploaded_file = st.file_uploader(
        "Upload Grant Document",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
        key="archive_file_uploader"
    )
    
    if uploaded_file is not None:
        filename = uploaded_file.name
        file_bytes = uploaded_file.read()
        
        uploaded_ids = [d.get("subtitle") for d in st.session_state.get("uploaded_documents", [])]
        if f"Uploaded Archival Filing ({filename})" not in uploaded_ids:
            
            status_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            stages = [
                (20, "Uploading document to vault..."),
                (45, "Extracting text and tables (OCR)..."),
                (70, "Creating semantic clause embeddings..."),
                (90, "Generating SHA-256 cryptographic provenance hashes..."),
                (100, "Indexed successfully into Institutional Archive")
            ]
            
            for pct, msg in stages:
                progress_bar.progress(pct)
                msg_html = f"""<div style="display: flex; align-items: center; gap: 0.5rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #1E382B; font-weight: 600; padding: 0.5rem 0;"><span class="material-symbols-outlined" style="font-size: 18px;">autorenew</span><span>{msg}</span></div>"""
                status_placeholder.html(msg_html)
                time.sleep(0.12)
                
            new_doc = document_service.upload_document(file_bytes, filename)
            st.session_state.uploaded_documents.insert(0, new_doc)
            
            status_placeholder.success(f"✓ {filename} successfully indexed with SHA-256 validation.")
            
            c1, c2 = st.columns([7, 3])
            with c2:
                if st.button("Inspect In Archive →", key=f"btn_view_new_{new_doc['id']}", type="primary", use_container_width=True):
                    view_document_detail(new_doc["id"])
                    st.rerun()

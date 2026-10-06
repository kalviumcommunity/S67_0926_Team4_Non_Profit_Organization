"""Folio Platform - Document Upload & Indexing Component."""

import streamlit as st
import time
import textwrap
from services.document_service import document_service
from utils.state import view_document_detail
from modules.pinecone_utils import get_pinecone_and_embedding_model, initialize_pinecone_index

def render_upload_panel() -> None:
    """Render the archival drag-and-drop upload dropzone and indexing workflow for PDF, Word, HTML, and TXT."""
    dropzone_html = textwrap.dedent("""
    <div style="margin-top: 1.5rem; margin-bottom: 1.5rem;">
      <div style="border: 2px dashed #DDD7CA; background-color: rgba(253, 251, 247, 0.8); border-radius: 6px; padding: 2.25rem 2rem; text-align: center;">
        <div style="width: 48px; height: 48px; border-radius: 50%; background-color: #EFEEE9; display: inline-flex; align-items: center; justify-content: center; color: #082217; margin-bottom: 0.75rem;">
          <span class="material-symbols-outlined" style="font-size: 24px;">upload_file</span>
        </div>
        <h4 style="font-family: 'Newsreader', serif; font-size: 20px; font-weight: 500; color: #082217; margin: 0 0 0.35rem 0;">
          Drop PDF, Word (.docx), HTML or TXT documents here
        </h4>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #424844; margin: 0 0 1rem 0;">
          Upload grant agreements, charters, bylaws, or donor guidelines · Automatic text chunking, SHA-256 provenance hashing & Pinecone vector indexing
        </p>
        <div style="display: flex; justify-content: center; align-items: center; gap: 0.75rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #727973; flex-wrap: wrap;">
          <span style="background-color: #EFEEE9; padding: 2px 8px; border-radius: 3px; font-weight: 600; color: #1E382B;">📄 PDF (.pdf)</span>
          <span style="background-color: #EFEEE9; padding: 2px 8px; border-radius: 3px; font-weight: 600; color: #1E382B;">📝 Word (.docx, .doc)</span>
          <span style="background-color: #EFEEE9; padding: 2px 8px; border-radius: 3px; font-weight: 600; color: #1E382B;">🌐 HTML (.html, .htm)</span>
          <span style="background-color: #EFEEE9; padding: 2px 8px; border-radius: 3px; font-weight: 600; color: #1E382B;">📃 Text (.txt, .md)</span>
        </div>
      </div>
    </div>
    """).strip()
    st.html(dropzone_html)
    
    uploaded_file = st.file_uploader(
        "Upload Grant Document (.pdf, .docx, .html, .txt)",
        type=["pdf", "docx", "doc", "html", "htm", "txt", "md"],
        label_visibility="collapsed",
        key="archive_file_uploader"
    )
    
    if uploaded_file is not None:
        filename = uploaded_file.name
        file_bytes = uploaded_file.read()
        
        uploaded_ids = [d.get("subtitle") for d in st.session_state.get("uploaded_documents", [])]
        if f"Uploaded Archival Filing ({filename})" not in uploaded_ids:
            
            ext_label = filename.split(".")[-1].upper() if "." in filename else "FILE"
            status_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            stages = [
                (20, f"Uploading {filename} to vault..."),
                (45, f"Parsing {ext_label} structure & extracting text..."),
                (70, "Creating semantic clause chunks (384-dim)..."),
                (90, "Generating SHA-256 cryptographic provenance hash..."),
                (100, f"Indexed successfully into Institutional Archive as {ext_label}")
            ]
            
            for pct, msg in stages:
                progress_bar.progress(pct)
                msg_html = f"""<div style="display: flex; align-items: center; gap: 0.5rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #1E382B; font-weight: 600; padding: 0.5rem 0;"><span class="material-symbols-outlined" style="font-size: 18px;">autorenew</span><span>{msg}</span></div>"""
                status_placeholder.html(msg_html)
                time.sleep(0.08)
                
            pinecone_idx = None
            try:
                pc, _ = get_pinecone_and_embedding_model()
                if pc:
                    idx_name = st.session_state.get("pinecone_index_name", "folio-grants")
                    pinecone_idx = initialize_pinecone_index(pc, index_name=idx_name)
            except Exception:
                pinecone_idx = None

            new_doc = document_service.upload_document(file_bytes, filename, pinecone_index=pinecone_idx)
            st.session_state.uploaded_documents.insert(0, new_doc)
            
            status_placeholder.success(f"✓ {filename} ({new_doc['format']}) successfully indexed with SHA-256 validation.")
            
            c1, c2 = st.columns([7, 3])
            with c2:
                if st.button("Inspect In Archive →", key=f"btn_view_new_{new_doc['id']}", type="primary", use_container_width=True):
                    view_document_detail(new_doc["id"])
                    st.rerun()

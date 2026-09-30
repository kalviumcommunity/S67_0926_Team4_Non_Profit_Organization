"""Folio Platform - Documents & Digital Paper Archive View."""

import streamlit as st
import textwrap
from services.document_service import document_service
from components.document_card import render_document_card
from components.clause_search import render_clause_search
from components.upload_panel import render_upload_panel
from components.document_viewer import render_document_reader
from utils.constants import DOCUMENT_CATEGORIES, DOC_TYPE_ALL

def render_documents_view() -> None:
    """Render Page 3: Documents / Digital Archive matching Stitch editorial design."""
    view_mode = st.session_state.get("document_view_mode", "shelf")
    selected_doc_id = st.session_state.get("selected_document_id")
    uploaded_docs = st.session_state.get("uploaded_documents", [])
    
    # Reader Mode Modal / Sheet
    if view_mode == "reader" and selected_doc_id:
        doc = document_service.get_document_by_id(selected_doc_id, extra_documents=uploaded_docs)
        if doc:
            render_document_reader(doc)
            return
            
    # Shelf Mode
    active_category = st.session_state.get("document_filter_type", DOC_TYPE_ALL)
    search_query = st.session_state.get("document_search_query", "")
    show_upload = st.session_state.get("show_upload_modal", False)
    
    # Retrieve matching documents & clauses
    docs = document_service.get_documents(category=active_category, search_query=search_query, extra_documents=uploaded_docs)
    matching_clauses = document_service.search_clauses(search_query, extra_documents=uploaded_docs) if search_query else []
    
    # 1. Header & Actions Area
    col_title, col_btns = st.columns([7.0, 3.5], gap="large")
    with col_title:
        title_html = textwrap.dedent(f"""
        <div>
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;">
            <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973;">Institutional Archive</span>
            <span style="color: #C2C8C2;">/</span>
            <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; color: #082217; letter-spacing: 0.05em;">Active Repository</span>
          </div>
          <h1 class="folio-headline-lg" style="margin: 0 0 0.35rem 0;">Your documents</h1>
          <p class="folio-body-md" style="color: #424844; margin: 0;">{len(docs)} active agreements and guidelines indexed for Helios Foundation.</p>
        </div>
        """).strip()
        st.html(title_html)
        
    with col_btns:
        st.html('<div style="padding-top: 1.25rem;"></div>')
        c_index_btn, c_add_btn = st.columns([1.1, 1.4], gap="small")
        with c_index_btn:
            if st.button("Index view", key="btn_index_view", type="secondary", use_container_width=True):
                pass
        with c_add_btn:
            upload_btn_label = "✕ Close" if show_upload else "+ Add documents"
            if st.button(upload_btn_label, key="btn_toggle_upload_panel", type="primary" if not show_upload else "secondary", use_container_width=True):
                st.session_state.show_upload_modal = not show_upload
                st.rerun()
                
    st.html('<div style="border-bottom: 1px solid #E4DFD3; margin-top: 1.25rem; margin-bottom: 1.75rem;"></div>')

    # Conditional Upload Dropzone Panel
    if show_upload:
        render_upload_panel()

    # 2. Fast Clause Search & Instant Excerpts Drawer
    render_clause_search(matching_clauses, search_query)

    # 3. Archival Shelf Header
    shelf_hdr_html = textwrap.dedent("""
    <div style="margin-top: 2.5rem; margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: baseline;">
      <div>
        <h2 class="folio-headline-sm" style="margin: 0;">Archival Shelf</h2>
        <p class="folio-body-sm" style="color: #424844; margin: 0.25rem 0 0 0;">Structured sheets with verified legal seals and clause indices.</p>
      </div>
      <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; color: #727973; text-transform: uppercase; letter-spacing: 0.08em;">Storage Tier: Primary Paper</span>
    </div>
    """).strip()
    st.html(shelf_hdr_html)
    
    # 4. 4-Column Archival Shelf Grid
    if docs:
        cols_per_row = 4
        for r_start in range(0, len(docs), cols_per_row):
            row_docs = docs[r_start:r_start + cols_per_row]
            grid_cols = st.columns(cols_per_row, gap="medium")
            for d_idx, doc in enumerate(row_docs):
                with grid_cols[d_idx]:
                    render_document_card(doc, key_suffix=f"shelf_{r_start + d_idx}")
    else:
        empty_html = textwrap.dedent("""
        <div style="background-color: #F7F4EE; border: 1px solid #E4DFD3; border-radius: 6px; padding: 3rem; text-align: center; margin-top: 1rem;">
          <h3 class="folio-headline-sm" style="margin-bottom: 0.5rem;">No documents match your search</h3>
          <p class="folio-body-md" style="color: #63625D;">Clear the search filter or add a new grant agreement above.</p>
        </div>
        """).strip()
        st.html(empty_html)

    # 5. Drag-and-Drop Archival Dropzone (At bottom)
    if not show_upload:
        dropzone_html = textwrap.dedent("""
        <div style="margin-top: 3.5rem; border: 2px dashed #C2C8C2; background-color: rgba(255, 255, 255, 0.6); border-radius: 6px; padding: 2.5rem 2rem; text-align: center; transition: all 0.2s ease;">
          <div style="max-width: 520px; margin: 0 auto; display: flex; flex-direction: column; align-items: center;">
            <div style="width: 48px; height: 48px; border-radius: 50%; background-color: #EFEEE9; display: flex; align-items: center; justify-content: center; color: #082217; margin-bottom: 0.75rem;">
              <span class="material-symbols-outlined" style="font-size: 24px;">upload_file</span>
            </div>
            <h4 style="font-family: 'Newsreader', serif; font-size: 20px; font-weight: 500; color: #082217; margin: 0 0 0.35rem 0;">
              Drop PDF, DOCX or agreements here
            </h4>
            <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #424844; margin: 0;">
              Drop grant agreements or donor guidelines here · OCR and provenance indexing are automatic
            </p>
            <div style="margin-top: 1rem; display: flex; align-items: center; gap: 0.5rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #727973;">
              <span>Supported: PDF/A, DOCX, Scanned TIFF</span>
              <span>·</span>
              <span style="color: #082217; font-weight: 600; text-decoration: underline; cursor: pointer;">Browse file system</span>
            </div>
          </div>
        </div>
        """).strip()
        st.html(dropzone_html)

    # 6. Archival Integrity Footer Note
    footer_html = textwrap.dedent("""
    <footer style="margin-top: 3.5rem; padding-top: 1.5rem; border-top: 1px solid #E4DFD3; display: flex; justify-content: space-between; align-items: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #727973; flex-wrap: wrap; gap: 1rem;">
      <div style="display: flex; align-items: center; gap: 0.5rem;">
        <span class="material-symbols-outlined" style="font-size: 16px;">lock</span>
        <span>FOLIO Institutional Vault · Cryptographic hashing active on all 6 Helios agreements</span>
      </div>
      <div style="display: flex; align-items: center; gap: 1.5rem;">
        <span style="cursor: pointer;">Export Citation Ledger</span>
        <span>·</span>
        <span style="cursor: pointer;">Audit Trail</span>
        <span>·</span>
        <span style="cursor: pointer;">Repository Settings</span>
      </div>
    </footer>
    """).strip()
    st.html(footer_html)

"""Folio Platform - Full Document Dossier Reader Component."""

import streamlit as st
import textwrap
from typing import Dict, Any

import html

def render_document_reader(doc: Dict[str, Any]) -> None:
    """Render a clean editorial document-reading experience."""
    if not doc:
        st.warning("Document not found in archive.")
        return
        
    title = doc.get("title", "GRANT DOCUMENT")
    subtitle = doc.get("subtitle", "")
    category = doc.get("category", "Grant Guidelines")
    org = doc.get("organization", "Helios Foundation")
    year = doc.get("year", "2026")
    pages = doc.get("pages", 32)
    fmt = doc.get("format", "PDF/A")
    status = doc.get("status", "Active")
    ref_code = doc.get("ref_code", "REF #HG-25-A")
    sha256 = doc.get("sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    full_text = doc.get("full_text", "No text available.")
    escaped_text = html.escape(full_text)
    
    # Back button bar
    col_back, _, col_act = st.columns([3.0, 5.0, 4.0])
    with col_back:
        if st.button("← Back to Archive", key="btn_back_to_shelf", type="secondary", use_container_width=True):
            st.session_state.document_view_mode = "shelf"
            st.session_state.selected_document_id = None
            st.rerun()
            
    with col_act:
        st.download_button(
            label="Download Archival Copy (.PDF)",
            data=full_text,
            file_name=f"{doc.get('id', 'doc')}_archive.txt",
            mime="text/plain",
            key="btn_download_doc_text",
            use_container_width=True
        )

    # Document Header Dossier
    header_html = f"""<div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 2rem 2.25rem; margin-top: 1.5rem; margin-bottom: 2rem; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.05);"><div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid #E4DFD3; padding-bottom: 1.25rem; margin-bottom: 1.5rem;"><div><span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #1E382B; display: block; margin-bottom: 0.25rem;">Institutional Dossier / {category}</span><h1 style="font-family: 'Newsreader', serif; font-size: 28px; font-weight: 500; color: #082217; margin: 0;">{title}</h1><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; color: #424844; margin: 0.25rem 0 0 0;">{subtitle} · {org}</p></div><div style="text-align: right;"><span style="background-color: #E8EFEA; color: #1E382B; border-radius: 4px; padding: 0.25rem 0.65rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; font-weight: 600;">{status}</span><div style="font-family: ui-monospace, monospace; font-size: 11px; color: #727973; margin-top: 0.5rem;">{ref_code}</div></div></div><div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; background-color: #F5F4EF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.15rem; margin-bottom: 1.5rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px;"><div><span style="color: #727973; display: block; font-size: 11px;">Effective Cycle</span><strong style="color: #1B1C19;">{year}</strong></div><div><span style="color: #727973; display: block; font-size: 11px;">Page Count</span><strong style="color: #1B1C19;">{pages} pages</strong></div><div><span style="color: #727973; display: block; font-size: 11px;">Archival Format</span><strong style="color: #1B1C19;">{fmt}</strong></div><div><span style="color: #727973; display: block; font-size: 11px;">SHA-256 Checksum</span><strong style="font-family: ui-monospace, monospace; font-size: 10px; color: #1E382B;">{sha256[:16]}...</strong></div></div><div style="background-color: #FBF9F4; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.75rem; font-family: 'Newsreader', serif; font-size: 15px; line-height: 1.75; color: #1B1C19; white-space: pre-wrap;">{escaped_text}</div></div>"""
    
    st.html(header_html)

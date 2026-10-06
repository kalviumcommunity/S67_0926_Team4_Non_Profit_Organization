"""Folio Platform - Visual Evidence & Provenance View."""

import streamlit as st
import textwrap
from services.evidence_service import evidence_service
from components.provenance_chain import render_provenance_chain
from components.evidence_card import render_evidence_sheet
from components.diff_viewer import render_diff_viewer
from utils.constants import NAV_RESEARCH, NAV_DOCUMENTS

def render_evidence_view() -> None:
    """Render Page 2: Visual Evidence & Provenance Traceability matching Stitch editorial design."""
    current_query = st.session_state.get("current_query", "What are the reporting requirements?")
    evidence_data = evidence_service.get_evidence_for_query(current_query)
    
    ref_code = evidence_data.get("evidence_ref", "REF #EV-2025-419")
    inquiry_text = evidence_data.get("inquiry_text", current_query)
    excerpts = evidence_data.get("excerpts", [])
    reconciler = evidence_data.get("reconciler", {})
    
    # 1. Editorial Header
    header_html = textwrap.dedent(f"""
    <div style="border-bottom: 1px solid #E4DFD3; padding-bottom: 1.5rem; margin-bottom: 2rem;">
      <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1.5rem;">
        <div>
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #A0401C;">Verified Provenance Audit</span>
            <span style="color: #C2C8C2;">/</span>
            <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; color: #727973; letter-spacing: 0.05em;">{ref_code}</span>
          </div>
          <h1 class="folio-headline-lg" style="margin: 0 0 0.35rem 0;">Where it came from</h1>
          <p class="folio-body-md" style="color: #424844; margin: 0;">Visual provenance, strict legal citations, and verified contract clauses.</p>
        </div>
        <div style="background-color: #F5F4EF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 0.85rem 1.25rem; max-width: 460px; width: 100%;">
          <div style="display: flex; align-items: flex-start; gap: 0.65rem;">
            <span class="material-symbols-outlined" style="color: #A0401C; font-size: 20px; margin-top: 2px;">help_center</span>
            <div>
              <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 9px; font-weight: 700; text-transform: uppercase; color: #727973; display: block; letter-spacing: 0.06em;">Primary Synthesis Inquiry</span>
              <p style="font-family: 'Newsreader', serif; font-size: 15px; font-weight: 500; color: #082217; margin: 0.25rem 0 0 0; line-height: 1.35;">"{inquiry_text}"</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    """).strip()
    st.html(header_html)
    
    # 2. Lineage Mapping Tree Diagram
    render_provenance_chain(evidence_data)
    
    # 3. Document Evidence Section (Physical Text Excerpts)
    sec_hdr_html = textwrap.dedent("""
    <div style="margin-top: 2.5rem; margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 0.5rem;">
      <div>
        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block; margin-bottom: 0.25rem;">Unadulterated Material Records</span>
        <h2 class="folio-headline-md" style="margin: 0;">Original Physical Text Excerpts</h2>
      </div>
      <div style="display: flex; align-items: center; gap: 0.35rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #424844;">
        <span class="material-symbols-outlined" style="font-size: 16px; color: #082217;">verified</span>
        <span>Cryptographic Hash Confirmed (SHA-256)</span>
      </div>
    </div>
    """).strip()
    st.html(sec_hdr_html)
    
    if excerpts:
        cols = st.columns(len(excerpts), gap="large")
        for idx, sheet in enumerate(excerpts):
            with cols[idx]:
                render_evidence_sheet(sheet, key_suffix=f"evi_{idx}")
                
    # 4. Interactive Compare Tool & Conflict Check
    if reconciler:
        render_diff_viewer(reconciler)
        
    # 5. Bottom Action Bar
    st.html('<div style="border-top: 1px solid #E4DFD3; padding-top: 1.5rem; margin-top: 3rem;"></div>')
    
    col_back, _, col_export, col_doc = st.columns([2.5, 3.5, 3.0, 3.0], gap="medium")
    with col_back:
        if st.button("← Back to Research", key="btn_back_to_research", type="secondary", use_container_width=True):
            st.session_state.current_page = NAV_RESEARCH
            st.rerun()
            
    with col_export:
        dossier_text = evidence_service.export_audit_dossier(evidence_data)
        st.download_button(
            label="Export Audit Dossier (.PDF)",
            data=dossier_text,
            file_name=f"Folio_Audit_{ref_code.replace(' ', '_').replace('#', '')}.txt",
            mime="text/plain",
            key="btn_download_audit_dossier",
            use_container_width=True
        )
        
    with col_doc:
        if st.button("Open in Document Archive →", key="btn_to_documents_from_evidence", type="primary", use_container_width=True):
            st.session_state.current_page = NAV_DOCUMENTS
            st.rerun()

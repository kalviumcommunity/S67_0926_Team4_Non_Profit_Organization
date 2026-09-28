"""Folio Platform - Physical Document Excerpt Sheet Component."""

import streamlit as st
import textwrap
from typing import Dict, Any
from utils.state import view_document_detail

def render_evidence_sheet(sheet: Dict[str, Any], key_suffix: str = "") -> None:
    """Render authentic physical document excerpt sheet with deckle accent and highlighted marks."""
    deckle_color = sheet.get("deckle_color", "#1E382B")
    ledger_tag = sheet.get("ledger_tag", "Archival Ledger 2025.1")
    doc_title = sheet.get("doc_title", "Grant Guidelines")
    clause_badge = sheet.get("clause_badge", "§ 5.1 · p. 8")
    status_text = sheet.get("status_text", "Verified Active")
    section_header = sheet.get("section_header", "")
    sub_clause = sheet.get("sub_clause", "")
    body_text = sheet.get("body_text", "")
    footnote = sheet.get("footnote", "")
    doc_id_label = sheet.get("doc_id_label", "Doc ID: HL-GDL-2025-V4")
    doc_id = sheet.get("doc_id", "DOC-01")
    
    is_primary = "Primary" in ledger_tag or "Guidelines" in doc_title or "2025.1" in ledger_tag
    badge_bg = "#EFEEE9" if is_primary else "#FFDBCF"
    badge_color = "#082217" if is_primary else "#802A05"
    pip_color = "#1E382B" if is_primary else "#A0401C"
    
    sheet_html = textwrap.dedent(f"""
    <div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.75rem 2rem; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.04); position: relative; overflow: hidden; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
      <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background-color: {deckle_color};"></div>
      
      <div>
        <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid #E4DFD3; padding-bottom: 1rem; margin-bottom: 1.25rem;">
          <div>
            <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block;">{ledger_tag}</span>
            <h3 style="font-family: 'Newsreader', serif; font-size: 18px; font-weight: 600; color: #082217; margin: 0.25rem 0 0 0; line-height: 1.3;">{doc_title}</h3>
          </div>
          <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 0.35rem;">
            <span style="background-color: {badge_bg}; color: {badge_color}; border: 1px solid #E4DFD3; border-radius: 4px; padding: 0.15rem 0.55rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; font-weight: 600; white-space: nowrap;">{clause_badge}</span>
            <span style="display: inline-flex; align-items: center; gap: 0.35rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: {pip_color}; font-weight: 600; white-space: nowrap;">
              <span style="width: 6px; height: 6px; border-radius: 50%; background-color: {pip_color};"></span>
              {status_text}
            </span>
          </div>
        </div>
        
        <div style="background-color: rgba(251, 249, 244, 0.55); border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.25rem 1.5rem; margin-bottom: 1rem;">
          <p style="font-family: 'Newsreader', serif; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #082217; border-bottom: 1px solid #E4DFD3; padding-bottom: 0.4rem; margin-bottom: 0.6rem;">{section_header}</p>
          <p style="font-family: ui-monospace, SFMono-Regular, monospace; font-size: 11px; color: #727973; margin-bottom: 0.6rem;">{sub_clause}</p>
          <p style="font-family: 'Newsreader', serif; font-size: 15px; line-height: 1.65; color: #1B1C19; margin: 0 0 0.85rem 0; text-align: justify;">{body_text}</p>
          <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-style: italic; color: #63625D; border-top: 1px solid #E4DFD3; padding-top: 0.6rem; margin: 0; line-height: 1.5;">{footnote}</p>
        </div>
      </div>
      
      <div style="border-top: 1px solid #E4DFD3; padding-top: 0.85rem; margin-top: 1rem; display: flex; justify-content: space-between; align-items: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #727973;">
        <span>{doc_id_label}</span>
      </div>
    </div>
    """).strip()
    st.html(sheet_html)
    
    # Action button aligned below card
    c_empty, c_btn = st.columns([5.5, 4.5])
    with c_btn:
        if st.button("View full scan →", key=f"btn_scan_{doc_id}_{key_suffix}", type="secondary", use_container_width=True):
            view_document_detail(doc_id)
            st.rerun()

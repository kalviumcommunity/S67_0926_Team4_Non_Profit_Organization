"""Folio Platform - Citation Mini-Sheet Card Component."""

import streamlit as st
from typing import Dict, Any
from utils.state import view_evidence_for_query

def render_citation_card(source: Dict[str, Any], key_suffix: str = "") -> None:
    """Render a paper-like mini sheet citation card matching Stitch design."""
    title = source.get("document_title", "GRANT GUIDELINES")
    citation_ref = source.get("citation_ref", "§ 5.1 · p. 8")
    excerpt = source.get("excerpt", "")
    border_color = source.get("border_color", "var(--folio-primary)")
    evidence_id = source.get("evidence_id", "EV-01")
    
    html_card = f"""<div class="citation-sheet" style="border-left: 3px solid {border_color}; margin-bottom: 0.75rem;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;"><span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #082217;">{title}</span><span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #727973;">{citation_ref}</span></div><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #424844; font-style: italic; line-height: 1.5; margin: 0;">{excerpt}</p></div>"""
    st.html(html_card)
    
    col1, col2 = st.columns([5, 5])
    with col2:
        if st.button(f"Inspect Evidence →", key=f"btn_cite_{evidence_id}_{key_suffix}", type="secondary", use_container_width=True):
            view_evidence_for_query(evidence_id=evidence_id)
            st.rerun()

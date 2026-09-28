"""Folio Platform - Fast Clause Search & Live Excerpt Drawer Component."""

import streamlit as st
import textwrap
from typing import List, Dict, Any
from utils.formatting import highlight_search_terms
from utils.state import view_document_detail

def render_clause_search(matching_clauses: List[Dict[str, Any]], active_search_query: str) -> None:
    """Render the clause search input and instant matching excerpts drawer matching Stitch."""
    
    with st.container(border=True):
        col_icon, col_input, col_clear = st.columns([0.35, 10.2, 1.45], gap="small")
        
        with col_icon:
            st.html("""<div style="display: flex; align-items: center; justify-content: center; height: 100%; padding-top: 0.45rem;"><span class="material-symbols-outlined" style="color: #727973; font-size: 20px;">search</span></div>""")
            
        with col_input:
            search_val = st.text_input(
                "Clause Search",
                value=active_search_query,
                placeholder="Search documents or clauses (e.g., 'indirect costs', 'reporting window')...",
                label_visibility="collapsed",
                key="input_clause_search"
            )
        with col_clear:
            st.html('<div class="folio-chip-item">')
            if st.button("Esc to clear", key="btn_clear_clause_search", type="secondary", use_container_width=True):
                st.session_state.document_search_query = ""
                st.rerun()
            st.html('</div>')
            
    if search_val != active_search_query:
        st.session_state.document_search_query = search_val
        st.rerun()

    # In-Document Excerpts Matching Drawer
    if active_search_query and active_search_query.strip() and matching_clauses:
        q_clean = active_search_query.strip()
        
        cards_html = "".join([
            f"""<div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.15rem 1.25rem; box-shadow: 0 1px 3px rgba(44, 45, 42, 0.03); display: flex; flex-direction: column; justify-content: space-between;"><div><div style="display: flex; justify-content: space-between; align-items: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; margin-bottom: 0.65rem;"><span style="font-weight: 700; color: #082217; font-size: 12px;">{cl.get('doc_title')}</span><span style="color: #727973; font-size: 10px; font-weight: 600;">{cl.get('meta')}</span></div><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #1B1C19; font-style: italic; line-height: 1.6; margin: 0 0 0.75rem 0;">“{highlight_search_terms(cl.get('text', ''), q_clean, 'ink-highlight-primary')}”</p></div><div style="border-top: 1px solid #EFEEE9; padding-top: 0.65rem; display: flex; justify-content: space-between; align-items: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #727973;"><span>{cl.get('parent_name')}</span><span style="color: #A0401C; font-weight: 600; cursor: pointer;">Open in sheet →</span></div></div>"""
            for cl in matching_clauses
        ])
            
        drawer_html = f"""<div style="background-color: #F5F4EF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 1.5rem; margin-top: 1rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(44, 45, 42, 0.02);"><div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E4DFD3; padding-bottom: 0.85rem; margin-bottom: 1.25rem;"><div style="display: flex; align-items: center; gap: 0.5rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; font-weight: 600; color: #1B1C19;"><span class="material-symbols-outlined" style="font-size: 18px; color: #A0401C;">find_in_page</span><span>Found {len(matching_clauses)} matching clauses for <span style="color: #A0401C;">“{q_clean}”</span>:</span></div><span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; color: #727973; text-transform: uppercase; letter-spacing: 0.05em;">Provenance verified</span></div><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.25rem;">{cards_html}</div></div>"""
        st.html(drawer_html)

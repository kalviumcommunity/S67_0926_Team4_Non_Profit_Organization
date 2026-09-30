"""Folio Platform - Top Editorial Masthead & Navigation Bar Component."""

import streamlit as st
import textwrap
from utils.constants import NAV_RESEARCH, NAV_EVIDENCE, NAV_DOCUMENTS, NAV_ABOUT

def render_top_navbar() -> None:
    """Render the sticky shared top navigation bar matching the Stitch editorial design."""
    current_page = st.session_state.get("current_page", NAV_RESEARCH)
    
    st.html('<div class="folio-header-container">')
    
    col_nav, col_tools = st.columns([6.0, 6.0], gap="medium")
    
    with col_nav:
        c_brand, c_r, c_e, c_d, c_a = st.columns([1.2, 1.1, 1.1, 1.3, 1.2], gap="small")
        
        with c_brand:
            st.html('<div style="padding-top: 0.2rem; cursor: pointer;"><span class="folio-brand-wordmark">FOLIO</span></div>')
            
        with c_r:
            is_active = current_page == NAV_RESEARCH
            if st.button("Research", key="top_nav_research", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state.current_page = NAV_RESEARCH
                st.session_state.document_view_mode = "shelf"
                st.rerun()
            
        with c_e:
            is_active = current_page == NAV_EVIDENCE
            if st.button("Evidence", key="top_nav_evidence", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state.current_page = NAV_EVIDENCE
                st.session_state.document_view_mode = "shelf"
                st.rerun()
            
        with c_d:
            is_active = current_page == NAV_DOCUMENTS
            if st.button("Documents", key="top_nav_documents", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state.current_page = NAV_DOCUMENTS
                st.session_state.document_view_mode = "shelf"
                st.rerun()

        with c_a:
            is_active = current_page == NAV_ABOUT
            if st.button("About Us", key="top_nav_about", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state.current_page = NAV_ABOUT
                st.session_state.document_view_mode = "shelf"
                st.rerun()
            
    with col_tools:
        tools_html = """<div style="display: flex; justify-content: flex-end; align-items: center; gap: 0.85rem; height: 100%; padding-top: 0.15rem;"><div class="folio-workspace-badge"><span class="folio-workspace-dot"></span><span style="font-weight: 600; color: #1B1C19;">Helios Foundation 2025–26 Grants</span><span style="color: #63625D; font-size: 11px; margin-left: 2px;">· 4 agreements active</span></div><div class="folio-search-trigger" style="cursor: default;"><span class="material-symbols-outlined" style="font-size: 15px; color: #63625D;">search</span><span>⌘K Search</span></div><div style="color: #082217; display: flex; align-items: center; cursor: pointer; padding: 2px;"><span class="material-symbols-outlined" style="font-size: 24px; color: #082217;">account_circle</span></div></div>"""
        st.html(tools_html)
        
    st.html('</div>')

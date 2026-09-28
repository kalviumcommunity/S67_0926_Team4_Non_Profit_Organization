"""Folio Platform - Research & Instant Answer View."""

import streamlit as st
import time
import textwrap
from components.query_box import render_query_box
from components.answer_card import render_answer_card
from services.rag_service import rag_service

def render_research_view() -> None:
    """Render Page 1: Research / Instant Answer."""
    render_query_box()
    
    current_query = st.session_state.get("current_query", "What are the reporting requirements?")
    is_loading = st.session_state.get("is_loading_query", False)
    
    # Handle Loading State
    if is_loading:
        loading_html = textwrap.dedent("""
        <div style="background-color: #F7F4EE; border: 1px solid #E4DFD3; border-radius: 6px; padding: 2.5rem; margin-top: 1rem; margin-bottom: 2rem; text-align: center;">
          <div style="display: inline-flex; align-items: center; gap: 0.75rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; color: #1E382B; font-weight: 600;">
            <span class="material-symbols-outlined" style="font-size: 22px;">hourglass_top</span>
            <span>Synthesizing grounded answer against active institutional charters...</span>
          </div>
          <div style="width: 240px; height: 3px; background-color: #EFEEE9; border-radius: 2px; margin: 1rem auto 0 auto; overflow: hidden;">
            <div style="background-color: #1E382B; height: 100%; width: 65%;"></div>
          </div>
        </div>
        """).strip()
        st.html(loading_html)
        time.sleep(0.3)
        st.session_state.is_loading_query = False
        st.rerun()

    # Execute RAG Query
    res = rag_service.ask_question(current_query)
    
    if res.get("status") == "success":
        render_answer_card(res.get("data", {}))
    elif res.get("status") == "no_results":
        render_answer_card(res.get("data", {}))
    elif res.get("status") == "empty":
        empty_html = textwrap.dedent("""
        <div style="background-color: #F7F4EE; border: 1px solid #E4DFD3; border-radius: 6px; padding: 3rem; margin-top: 1rem; text-align: center;">
          <h3 class="folio-headline-sm" style="margin-bottom: 0.5rem;">No question asked yet</h3>
          <p class="folio-body-md" style="color: #63625D;">Type an inquiry above or select one of the suggested query chips to inspect institutional grant rules.</p>
        </div>
        """).strip()
        st.html(empty_html)

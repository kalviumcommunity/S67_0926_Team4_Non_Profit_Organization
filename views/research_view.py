"""Folio Platform - Research & Instant Answer View."""

import streamlit as st
import time
import textwrap
from components.query_box import render_query_box
from components.answer_card import render_answer_card
from services.rag_service import rag_service
from modules.pinecone_utils import get_pinecone_and_embedding_model, initialize_pinecone_index

def render_research_view() -> None:
    """Render Page 1: Research / Instant Answer."""
    render_query_box()
    
    current_query = st.session_state.get("current_query", "What are the reporting requirements?")
    is_loading = st.session_state.get("is_loading_query", False)
    
    # Handle Loading State
    if is_loading:
        persona = st.session_state.get("selected_persona", "Default")
        output_format = st.session_state.get("selected_format", "Default")
        model = st.session_state.get("selected_model", "google/gemini-2.5-flash")
        
        loading_html = textwrap.dedent(f"""
        <div style="background-color: #F7F4EE; border: 1px solid #E4DFD3; border-radius: 6px; padding: 2.5rem; margin-top: 1rem; margin-bottom: 2rem; text-align: center;">
          <div style="display: inline-flex; align-items: center; gap: 0.75rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; color: #1E382B; font-weight: 600;">
            <span class="material-symbols-outlined" style="font-size: 22px;">hourglass_top</span>
            <span>Synthesizing answer as <em>{persona}</em> in <em>{output_format}</em> format ({model.split('/')[-1]})...</span>
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

    # Attempt to retrieve Pinecone index if configured
    pinecone_idx = None
    try:
        pc, _ = get_pinecone_and_embedding_model()
        if pc:
            idx_name = st.session_state.get("pinecone_index_name", "folio-grants")
            pinecone_idx = initialize_pinecone_index(pc, index_name=idx_name)
    except Exception:
        pinecone_idx = None

    # Execute RAG Query with AI Persona, Format, Model, and Multimedia Context
    persona = st.session_state.get("selected_persona", "Default")
    output_format = st.session_state.get("selected_format", "Default")
    model = st.session_state.get("selected_model", "google/gemini-2.5-flash")
    multimedia_ctx = st.session_state.get("multimedia_context", [])

    res = rag_service.ask_question(
        query=current_query,
        persona=persona,
        output_format=output_format,
        model=model,
        multimedia_context=multimedia_ctx,
        pinecone_index=pinecone_idx
    )
    
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

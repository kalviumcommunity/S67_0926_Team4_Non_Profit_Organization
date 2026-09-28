"""Folio Platform - Query Input & Suggestion Chips Component."""

import streamlit as st
from utils.state import set_query

def render_query_box() -> None:
    """Render the primary question input bar and suggested query chips matching Stitch."""
    st.html("""<h1 class="folio-headline-lg" style="margin-bottom: 1.5rem;">Ask your grants.</h1>""")
    
    current_val = st.session_state.get("current_query", "What are the reporting requirements?")
    
    # 1. Search Box Shell Container
    with st.container(border=True):
        col_icon, col_input, col_btn = st.columns([0.4, 10.8, 0.8], gap="small")
        
        with col_icon:
            st.html("""<div style="display: flex; align-items: center; justify-content: center; height: 100%; padding-top: 0.5rem;"><span class="material-symbols-outlined" style="color: #727973; font-size: 22px;">search</span></div>""")
            
        with col_input:
            user_query = st.text_input(
                "Query Input",
                value=current_val,
                placeholder="What are the reporting requirements?",
                label_visibility="collapsed",
                key="query_text_input_widget"
            )
            
        with col_btn:
            search_clicked = st.button("↑", key="btn_execute_query", type="primary", use_container_width=True, help="Execute Query")
        
    if search_clicked or (user_query and user_query != st.session_state.get("current_query")):
        if user_query.strip():
            set_query(user_query.strip(), auto_execute=True)
            st.rerun()

    # 2. Suggested Chips Row (Ample sizing to prevent word breaks)
    c_lbl, c1, c2, c3, c4, _ = st.columns([1.1, 2.0, 1.6, 1.8, 1.6, 3.9], gap="small")
    
    with c_lbl:
        st.html("""<div style="padding-top: 0.45rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; color: #727973; text-transform: uppercase; white-space: nowrap;">SUGGESTED</div>""")
        
    with c1:
        st.html('<div class="folio-chip-item">')
        if st.button("Reporting deadlines", key="chip_1", use_container_width=True):
            set_query("What are the reporting requirements?", auto_execute=True)
            st.rerun()
        st.html('</div>')
        
    with c2:
        st.html('<div class="folio-chip-item">')
        if st.button("Indirect costs", key="chip_2", use_container_width=True):
            set_query("What are the indirect costs rules?", auto_execute=True)
            st.rerun()
        st.html('</div>')
        
    with c3:
        st.html('<div class="folio-chip-item">')
        if st.button("Eligible expenses", key="chip_3", use_container_width=True):
            set_query("What are the eligible expenses?", auto_execute=True)
            st.rerun()
        st.html('</div>')
        
    with c4:
        st.html('<div class="folio-chip-item">')
        if st.button("Funding rules", key="chip_4", use_container_width=True):
            set_query("What are the budget reallocation limits?", auto_execute=True)
            st.rerun()
        st.html('</div>')

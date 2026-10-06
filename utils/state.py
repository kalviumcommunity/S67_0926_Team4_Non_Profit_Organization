"""Folio Platform - Session State Management."""

import os
import streamlit as st
from typing import Optional, Dict, Any, List
from utils.constants import NAV_RESEARCH, DOC_TYPE_ALL

def init_session_state() -> None:
    """Initialize all required session state variables with default values."""
    defaults = {
        "current_page": NAV_RESEARCH,
        "current_query": "What are the reporting requirements?",
        "query_input_text": "What are the reporting requirements?",
        "query_history": [
            "What are the reporting requirements?",
            "What are the indirect costs rules?",
            "When is the annual impact report due?"
        ],
        "query_result": None,
        "selected_document_id": None,
        "selected_evidence_id": "EV-01",
        "document_filter_type": DOC_TYPE_ALL,
        "document_search_query": "",
        "uploaded_documents": [],
        "show_upload_modal": False,
        "show_diff_drawer": False,
        "show_settings_drawer": False,
        "is_loading_query": False,
        "query_error": None,
        "document_view_mode": "shelf", # "shelf" or "reader"
        
        # AI Controls (Persona, Format, Model)
        "selected_persona": "Default",
        "selected_format": "Default",
        "selected_model": "google/gemini-2.5-flash",
        
        # OpenRouter & Pinecone Configuration
        "openrouter_api_key": os.getenv("OPENROUTER_API_KEY", ""),
        "pinecone_api_key": os.getenv("PINECONE_API_KEY", ""),
        "pinecone_index_name": os.getenv("PINECONE_INDEX_NAME", "folio-grants"),
        
        # Multimedia Context Ingestion (PDF / Image / Video)
        "doc_type": None,
        "doc_content": None,
        "multimedia_context": [],
        "multimedia_preview_name": None
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def set_page(page_name: str) -> None:
    """Navigate to a specific page."""
    st.session_state.current_page = page_name

def set_query(query_text: str, auto_execute: bool = True) -> None:
    """Set the active query and optionally trigger execution."""
    st.session_state.current_query = query_text
    st.session_state.query_input_text = query_text
    if auto_execute:
        st.session_state.is_loading_query = True
        if query_text not in st.session_state.query_history:
            st.session_state.query_history.insert(0, query_text)

def view_document_detail(document_id: str) -> None:
    """Open document reader mode for a specific document."""
    st.session_state.selected_document_id = document_id
    st.session_state.document_view_mode = "reader"
    st.session_state.current_page = "Documents"

def view_evidence_for_query(query_text: Optional[str] = None, evidence_id: Optional[str] = None) -> None:
    """Navigate to Evidence page with specific query or evidence focus."""
    if query_text:
        st.session_state.current_query = query_text
    if evidence_id:
        st.session_state.selected_evidence_id = evidence_id
    st.session_state.current_page = "Evidence"

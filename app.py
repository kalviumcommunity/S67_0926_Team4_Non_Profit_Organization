"""
FOLIO — Grant Intelligence Platform
Production Streamlit Frontend Application
"""

import os
import streamlit as st

# 1. Page Configuration (Must be first Streamlit call)
st.set_page_config(
    page_title="FOLIO — Grant Intelligence Platform",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inject Custom Quiet Editorial CSS Stylesheet
def inject_custom_styles() -> None:
    """Read and inject theme.css into the Streamlit app DOM."""
    css_path = os.path.join(os.path.dirname(__file__), "styles", "theme.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

inject_custom_styles()

# 3. Initialize Session State
from utils.state import init_session_state
from utils.constants import NAV_RESEARCH, NAV_EVIDENCE, NAV_DOCUMENTS, NAV_ABOUT

init_session_state()

# 4. Render Shared Top Navigation Header
from components.header import render_top_navbar

render_top_navbar()

# 5. Route to Active Page Canvas
from views.research_view import render_research_view
from views.evidence_view import render_evidence_view
from views.documents_view import render_documents_view
from views.about_view import render_about_view

current_page = st.session_state.get("current_page", NAV_RESEARCH)

if current_page == NAV_RESEARCH:
    render_research_view()
elif current_page == NAV_EVIDENCE:
    render_evidence_view()
elif current_page == NAV_DOCUMENTS:
    render_documents_view()
elif current_page == NAV_ABOUT:
    render_about_view()
else:
    st.error(f"Unknown page: {current_page}")

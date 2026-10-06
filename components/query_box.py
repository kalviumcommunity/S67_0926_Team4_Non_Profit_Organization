"""Folio Platform - Query Input, AI Controls & Suggestion Chips Component."""

import streamlit as st
from PIL import Image
from utils.state import set_query
from modules.openrouter_utils import PERSONA_PROMPTS, FORMAT_PROMPTS, POPULAR_MODELS, resolve_openrouter_api_key
from modules.utils import process_document_by_type, process_video, process_image

def render_query_box() -> None:
    """Render the primary question input bar, AI personas/formats controls, and suggested chips."""
    
    col_hdr, col_cfg = st.columns([8.5, 3.5])
    with col_hdr:
        st.html("""<h1 class="folio-headline-lg" style="margin-bottom: 0.5rem;">Ask your grants.</h1>""")
        st.html("""<p class="folio-body-sm" style="color: #63625D; margin-bottom: 1.25rem;">Query institutional guidelines, donor charters, or attach PDF, Word (.docx), HTML, TXT or media records with zero-extrapolation verified synthesis.</p>""")
    with col_cfg:
        has_key = bool(resolve_openrouter_api_key())
        status_color = "#1E382B" if has_key else "#A0401C"
        status_bg = "#E8EFEA" if has_key else "#FDF2EC"
        status_label = "OpenRouter Active" if has_key else "OpenRouter Key Needed"
        
        st.html(f"""
        <div style="display: flex; justify-content: flex-end; align-items: center; padding-top: 0.5rem;">
          <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; font-weight: 700; color: {status_color}; background-color: {status_bg}; border: 1px solid {status_color}33; padding: 4px 10px; border-radius: 4px; display: inline-flex; align-items: center; gap: 0.4rem;">
            <span style="width: 7px; height: 7px; border-radius: 50%; background-color: {status_color};"></span>
            {status_label}
          </span>
        </div>
        """)
        
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

    # 2. Advanced AI Controls & Document/Media Attachment Expander
    with st.expander("⚙️ AI Persona, Format & Document/Media Attachment", expanded=False):
        c_persona, c_format, c_model = st.columns(3, gap="medium")
        
        with c_persona:
            selected_persona = st.selectbox(
                "Agent Persona:",
                options=list(PERSONA_PROMPTS.keys()),
                index=list(PERSONA_PROMPTS.keys()).index(st.session_state.get("selected_persona", "Default")),
                key="sel_persona_widget"
            )
            st.session_state.selected_persona = selected_persona
            
        with c_format:
            selected_format = st.selectbox(
                "Output Format:",
                options=list(FORMAT_PROMPTS.keys()),
                index=list(FORMAT_PROMPTS.keys()).index(st.session_state.get("selected_format", "Default")),
                key="sel_format_widget"
            )
            st.session_state.selected_format = selected_format
            
        with c_model:
            selected_model = st.selectbox(
                "OpenRouter Model:",
                options=POPULAR_MODELS,
                index=POPULAR_MODELS.index(st.session_state.get("selected_model", "google/gemini-2.5-flash")) if st.session_state.get("selected_model") in POPULAR_MODELS else 0,
                key="sel_model_widget"
            )
            st.session_state.selected_model = selected_model

        # OpenRouter Key Quick Input (if not set in env)
        if not resolve_openrouter_api_key():
            st.markdown("---")
            key_col, save_col = st.columns([9, 3])
            with key_col:
                new_key = st.text_input(
                    "Set OpenRouter API Key (sk-or-v1-...)",
                    type="password",
                    value=st.session_state.get("openrouter_api_key", ""),
                    placeholder="Enter sk-or-v1-... key for live LLM synthesis",
                    key="or_key_input"
                )
            with save_col:
                st.html("<div style='padding-top: 1.75rem;'></div>")
                if st.button("Save API Key", key="btn_save_or_key", type="primary", use_container_width=True):
                    if new_key.strip():
                        st.session_state.openrouter_api_key = new_key.strip()
                        st.success("OpenRouter API key configured for session.")
                        st.rerun()

        # Document & Media Attachment Dropzone (PDF, Word, HTML, TXT, Image, Video)
        st.markdown("---")
        st.caption("📎 Attach Document or Media Inquiry Evidence (.pdf, .docx, .html, .txt, image, video)")
        uploaded_media = st.file_uploader(
            "Upload Document/Media for Context",
            type=["pdf", "docx", "doc", "html", "htm", "txt", "md", "png", "jpg", "jpeg", "mp4", "mov"],
            label_visibility="collapsed",
            key="media_context_uploader"
        )
        
        if uploaded_media is not None:
            if st.button(f"Process {uploaded_media.name} as Inquiry Context", key="btn_process_media_ctx"):
                with st.spinner(f"Processing {uploaded_media.name}..."):
                    mime = getattr(uploaded_media, "type", "")
                    fn = uploaded_media.name.lower()
                    
                    if fn.endswith((".pdf", ".docx", ".doc", ".html", ".htm", ".txt", ".md")):
                        chunks, _ = process_document_by_type(uploaded_media, uploaded_media.name)
                        if chunks:
                            st.session_state.multimedia_context = chunks
                            st.session_state.doc_type = fn.split(".")[-1].upper()
                            st.session_state.multimedia_preview_name = uploaded_media.name
                            st.success(f"{st.session_state.doc_type} processed: {len(chunks)} context chunks attached to inquiry.")
                    elif "image" in mime or fn.endswith((".png", ".jpg", ".jpeg")):
                        img = process_image(uploaded_media)
                        if img:
                            st.session_state.multimedia_context = [img]
                            st.session_state.doc_type = "image"
                            st.session_state.multimedia_preview_name = uploaded_media.name
                            st.image(img, caption="Attached Evidence Image", width=300)
                            st.success("Image attached to inquiry context.")
                    elif "video" in mime or fn.endswith((".mp4", ".mov")):
                        frames = process_video(uploaded_media)
                        if frames:
                            st.session_state.multimedia_context = frames
                            st.session_state.doc_type = "video"
                            st.session_state.multimedia_preview_name = uploaded_media.name
                            st.success(f"Video sampled: {len(frames)} key frames attached.")

    # Show active media context indicator if attached
    if st.session_state.get("multimedia_preview_name"):
        c_att1, c_att2 = st.columns([10, 2])
        with c_att1:
            st.info(f"📎 Attached Context: **{st.session_state.multimedia_preview_name}** ({st.session_state.get('doc_type', 'doc').upper()})")
        with c_att2:
            if st.button("Clear Context", key="btn_clear_ctx"):
                st.session_state.multimedia_context = []
                st.session_state.doc_type = None
                st.session_state.multimedia_preview_name = None
                st.rerun()

    # Trigger search on submit
    if search_clicked or (user_query and user_query != st.session_state.get("current_query")):
        if user_query.strip():
            set_query(user_query.strip(), auto_execute=True)
            st.rerun()

    # 3. Suggested Chips Row
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

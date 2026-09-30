"""Folio Platform - Grounded Answer Card Component."""

import streamlit as st
import textwrap
from typing import Dict, Any
from utils.state import view_evidence_for_query

def render_answer_card(rag_data: Dict[str, Any]) -> None:
    """Render the primary answer block matching Stitch editorial design."""
    if not rag_data:
        return
        
    question = rag_data.get("question", "")
    verified_count = rag_data.get("verified_count", "2 sources verified")
    spec_badge = rag_data.get("spec_badge", "PORTAL VERIFIED SPECIFICATION")
    headline = rag_data.get("editorial_headline", "REPORTING REQUIREMENTS")
    answer_lead = rag_data.get("answer_lead", "")
    answer_body = rag_data.get("answer_body", "")
    metrics = rag_data.get("metrics", [])
    sources = rag_data.get("sources", [])
    
    # Build 3-column Equal-Height Metrics HTML
    metrics_list = []
    for m in metrics:
        pill_type = m.get("pill_type", "green")
        pill_bg = "#CBEAD7" if pill_type == "green" else "#FFDBCF"
        pill_text_color = "#052015" if pill_type == "green" else "#722200"
        numeral_color = "#082217" if m.get("numeral_color") == "primary" else "#A0401C"
        icon_name = m.get("pill_icon", "calendar_today")
        
        m_item = f"""<div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.25rem 1.4rem; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.04); display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 175px;"><div><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.65rem;"><span style="display: inline-flex; align-items: center; gap: 0.25rem; background-color: {pill_bg}; color: {pill_text_color}; border-radius: 3px; padding: 0.15rem 0.5rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; white-space: nowrap;"><span class="material-symbols-outlined" style="font-size: 13px;">{icon_name}</span>{m.get('pill_text', 'Deadline')}</span><span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; color: #727973; letter-spacing: 0.06em; text-transform: uppercase;">{m.get('sub_pill', '')}</span></div><div style="font-family: 'Newsreader', serif; font-size: 42px; font-weight: 400; line-height: 1.1; letter-spacing: -0.02em; color: {numeral_color}; margin: 0.35rem 0 0.5rem 0;">{m.get('numeral', '')}</div></div><div style="border-top: 1px solid #EFEEE9; padding-top: 0.75rem; margin-top: 0.5rem;"><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 600; color: #1B1C19; margin: 0;">{m.get('title', '')}</p><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #424844; margin: 0.2rem 0 0 0;">{m.get('subtext', '')}</p></div></div>"""
        metrics_list.append(m_item)
    metrics_html = "".join(metrics_list)

    # Build Citation Sources HTML
    sources_list = []
    for idx, s in enumerate(sources):
        border_col = "#1E382B" if idx == 0 else "#A0401C"
        doc_title = s.get('document_title', s.get('doc_title', 'GRANT GUIDELINES 2025'))
        citation_ref = s.get('citation_ref', f"{s.get('section', '§ 5.1')} · p. {s.get('page_number', '8')}")
        excerpt_text = s.get('excerpt', s.get('quote_excerpt', ''))
        
        s_item = f"""<div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.25rem 1.4rem; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.04); display: flex; flex-direction: column; justify-content: space-between;"><div><div style="display: flex; justify-content: space-between; align-items: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; color: #727973; margin-bottom: 0.65rem;"><span style="text-transform: uppercase; color: #082217; font-weight: 700; letter-spacing: 0.08em;">{doc_title}</span><span style="color: #63625D; font-weight: 500;">{citation_ref}</span></div><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; font-style: italic; line-height: 1.6; color: #424844; border-left: 2px solid {border_col}; padding-left: 0.85rem; margin: 0.35rem 0 0 0;">{excerpt_text}</p></div></div>"""
        sources_list.append(s_item)
    sources_html = "".join(sources_list)

    full_card_html = textwrap.dedent(f"""
    <div style="background-color: #F7F4EE; border: 1px solid #E4DFD3; border-radius: 8px; padding: 2rem 2.5rem; margin-top: 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(44, 45, 42, 0.02);">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E4DFD3; padding-bottom: 1.25rem; margin-bottom: 1.75rem; flex-wrap: wrap; gap: 0.75rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #424844;">
          <span style="color: #1B1C19; font-weight: 600;">Asked:</span>
          <span style="color: #1B1C19;">“{question}”</span>
          <span style="color: #C2C8C2;">·</span>
          <span style="display: inline-flex; align-items: center; gap: 0.35rem; color: #082217; font-weight: 600;">
            <span class="material-symbols-outlined" style="font-size: 16px; color: #082217;">verified</span>
            {verified_count}
          </span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span style="font-family: ui-monospace, monospace; font-size: 10px; background-color: #E8EFEA; color: #1E382B; border: 1px solid #C2D9CB; padding: 2px 7px; border-radius: 3px; font-weight: 600;">⚡ 1,180 ms · 5 RAG Steps</span>
          <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; color: #727973; text-transform: uppercase;">{spec_badge}</span>
        </div>
      </div>
      
      <h2 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #A0401C; margin: 0 0 0.85rem 0;">
        {headline}
      </h2>
      
      <div style="max-width: 960px; margin-bottom: 2rem;">
        <p style="font-family: 'Newsreader', serif; font-size: 20px; font-weight: 500; line-height: 1.5; color: #1B1C19; margin: 0 0 0.85rem 0;">
          {answer_lead}
        </p>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 400; line-height: 1.65; color: #424844; margin: 0;">
          {answer_body}
        </p>
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; margin-bottom: 2.25rem;">
        {metrics_html}
      </div>
      
      <div style="border-top: 1px solid #E4DFD3; padding-top: 1.75rem; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <h3 style="font-family: 'Newsreader', serif; font-size: 20px; font-weight: 500; color: #082217; margin: 0;">Sources</h3>
            <span style="background-color: #EFEEE9; border: 1px solid #E4DFD3; border-radius: 4px; padding: 0.2rem 0.65rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; color: #424844; text-transform: uppercase; letter-spacing: 0.05em;">
              {len(sources)} primary agreements cited
            </span>
          </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.25rem;">
          {sources_html}
        </div>
      </div>
    </div>
    """).strip()
    
    st.html(full_card_html)
    
    # RAG Pipeline Execution Flow Inspector
    telemetry = rag_data.get("pipeline_telemetry", {})
    if telemetry and telemetry.get("pipeline_stages"):
        with st.expander("⚡ Inspect RAG Pipeline Execution Flow (Latency: 1,180 ms)", expanded=False):
            stages = telemetry.get("pipeline_stages", [])
            stage_cards = []
            for s in stages:
                s_num = s.get("stage_num", 1)
                s_name = s.get("name", "")
                s_det = s.get("details", "")
                s_lat = s.get("latency_ms", 0)
                card = f"""<div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 0.85rem 1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;"><div><span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; color: #1E382B; text-transform: uppercase; background-color: #E8EFEA; padding: 2px 6px; border-radius: 2px; margin-right: 0.5rem;">STEP {s_num}</span><strong style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #1B1C19;">{s_name}</strong><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #63625D; margin: 0.2rem 0 0 0;">{s_det}</p></div><span style="font-family: ui-monospace, monospace; font-size: 11px; font-weight: 600; color: #082217; background-color: #EFEEE9; padding: 3px 8px; border-radius: 3px; white-space: nowrap;">{s_lat} ms</span></div>"""
                stage_cards.append(card)
            st.html("".join(stage_cards))
    
    # CTA Action Row (View evidence)
    col_msg, col_cta = st.columns([7.2, 2.8], gap="medium")
    with col_msg:
        st.html('<div style="padding-top: 0.65rem; font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 13px; color: #424844;">Full cross-referenced dossier compiled from original executed charters.</div>')
    with col_cta:
        if st.button("View evidence →", key="btn_cta_view_evidence", type="primary", use_container_width=True):
            view_evidence_for_query(query_text=question)
            st.rerun()
            
    # Context Footer Sub-note
    footer_text = """<footer style="text-align: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #727973; margin-top: 3.5rem; letter-spacing: 0.02em;">FOLIO Editorial Grants Intelligence · Institutional Archive Helios 2025–2026</footer>"""
    st.html(footer_text)

"""Folio Platform - Archival Shelf Document Dossier Card Component."""

import streamlit as st
import textwrap
from typing import Dict, Any
from utils.state import view_document_detail

def render_document_card(doc: Dict[str, Any], key_suffix: str = "") -> None:
    """Render an archival shelf document dossier card matching the Stitch editorial design."""
    doc_id = doc.get("id", "DOC-01")
    dossier_num = doc.get("dossier_num", "01")
    title = doc.get("title", "GRANT GUIDELINES")
    subtitle = doc.get("subtitle", "")
    year = doc.get("year", "2026")
    pages = doc.get("pages", 32)
    fmt = doc.get("format", "PDF/A")
    status = doc.get("status", "Active")
    ref_code = doc.get("ref_code", "REF #HG-25-A")
    seal = doc.get("seal", "")
    spine_color = doc.get("spine_color", "#1E382B")
    key_clauses = doc.get("key_clauses", [])
    obligation_matrix = doc.get("obligation_matrix")
    milestone_ledger = doc.get("milestone_ledger")
    executive_scope = doc.get("executive_scope")
    
    is_executed = status in ["Fully Executed", "Approved"]
    is_amendment = status == "Active Amendment"
    
    if is_amendment:
        badge_style = "background-color: #F9EBE6; color: #C85A32; font-weight: 600;"
        type_label = "Addendum"
    elif is_executed and "Agreement" in title:
        badge_style = "background-color: #E8EFEA; color: #1E382B; font-weight: 600;"
        type_label = "Contract"
    elif is_executed and "Report" in title:
        badge_style = "background-color: #E8EFEA; color: #1E382B; font-weight: 600;"
        type_label = "Report"
    elif is_executed and "Fellowship" in title or "COMPACT" in title:
        badge_style = "background-color: #E8EFEA; color: #1E382B; font-weight: 600;"
        type_label = "Compact"
    else:
        badge_style = "background-color: #EFEEE9; color: #424844; border: 1px solid #E4DFD3; font-weight: 600;"
        type_label = "Dossier"
        
    clauses_html = ""
    if key_clauses:
        items_html = "".join([
            f'<div style="display: flex; align-items: center; gap: 0.4rem;"><span style="width: 4px; height: 4px; border-radius: 50%; background-color: #A0401C; flex-shrink: 0;"></span><span style="{"font-weight: 600; color: #082217;" if cl.get("highlight") else ""}">{cl.get("section", "")} {cl.get("title", "")}</span></div>'
            for cl in key_clauses[:3]
        ])
        clauses_html = f'<div style="margin-top: 0.85rem; flex: 1;"><span style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block; margin-bottom: 0.5rem;">Key Clauses Indexed</span><div style="display: flex; flex-direction: column; gap: 0.35rem; font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 12px; color: #424844;">{items_html}</div></div>'
    elif obligation_matrix:
        clauses_html = f'<div style="margin-top: 0.85rem; flex: 1;"><span style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block; margin-bottom: 0.4rem;">Obligation Matrix</span><div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; padding: 0.65rem; border-radius: 4px;"><div style="font-family: \'Newsreader\', serif; font-size: 22px; font-weight: 600; color: #082217;">{obligation_matrix.get("amount")}</div><div style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 10px; color: #727973; margin-top: 2px;">{obligation_matrix.get("term")}</div></div><p style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 11px; font-style: italic; color: #424844; margin-top: 0.45rem; line-height: 1.4;">{obligation_matrix.get("note")}</p></div>'
    elif milestone_ledger:
        clauses_html = f'<div style="margin-top: 0.85rem; flex: 1;"><span style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block; margin-bottom: 0.4rem;">Milestone Ledger</span><div style="display: flex; justify-content: space-between; align-items: center; font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 12px; color: #1B1C19; margin-bottom: 0.25rem;"><span>{milestone_ledger.get("completed")}</span><span class="material-symbols-outlined" style="font-size: 16px; color: #1E382B;">check_circle</span></div><div style="display: flex; justify-content: space-between; align-items: center; font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 12px; color: #63625D; margin-bottom: 0.45rem;"><span>{milestone_ledger.get("pending")}</span><span class="material-symbols-outlined" style="font-size: 16px; color: #727973;">schedule</span></div><div style="width: 100%; background-color: #EFEEE9; height: 4px; border-radius: 2px; overflow: hidden;"><div style="background-color: #1E382B; height: 100%; width: {milestone_ledger.get("progress")}%;"></div></div></div>'
    elif executive_scope:
        clauses_html = f'<div style="margin-top: 0.85rem; flex: 1;"><span style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block; margin-bottom: 0.35rem;">Executive Scope</span><p style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 11px; color: #1B1C19; line-height: 1.45; margin: 0 0 0.45rem 0;">{executive_scope}</p><div style="padding: 0.35rem 0.5rem; background-color: #EFEEE9; border: 1px dashed #E4DFD3; border-radius: 3px; display: flex; align-items: center; gap: 0.35rem;"><span class="material-symbols-outlined" style="font-size: 16px; color: #A0401C;">verified</span><span style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #424844;">Verified Legal Ratification</span></div></div>'

    bottom_stamp = seal if seal else ref_code

    card_html = f"""<div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.04); overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; height: 390px; position: relative;"><div style="height: 6px; background-color: {spine_color}; width: 100%;"></div><div style="padding: 1.25rem 1.35rem; display: flex; flex-direction: column; flex: 1; justify-content: space-between;"><div><div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.65rem;"><span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #1E382B;">{type_label} / {dossier_num}</span><span style="border-radius: 4px; padding: 0.15rem 0.45rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; {badge_style}">{status}</span></div><div style="border-bottom: 1px solid #E4DFD3; padding-bottom: 0.65rem; margin-bottom: 0.65rem;"><h3 style="font-family: 'Newsreader', serif; font-size: 17px; font-weight: 600; color: #082217; margin: 0; line-height: 1.3;">{title}</h3><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #424844; margin: 0.25rem 0 0 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{subtitle}</p></div><div style="display: flex; align-items: center; gap: 0.45rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; color: #727973; border-bottom: 1px solid #E4DFD3; padding-bottom: 0.65rem;"><span>{year}</span><span>·</span><span>{pages} pages</span><span>·</span><span>{fmt}</span></div>{clauses_html}</div><div style="margin-top: 0.75rem; border-top: 1px solid #E4DFD3; padding-top: 0.5rem; display: flex; justify-content: space-between; align-items: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px;"><span style="font-family: ui-monospace, monospace; color: #727973; letter-spacing: 0.04em;">{bottom_stamp}</span></div></div></div>"""
    
    st.html(card_html)
    
    # Inspect button aligned with card
    c_sp, c_ins = st.columns([4, 6])
    with c_ins:
        if st.button("Inspect →", key=f"btn_inspect_{doc_id}_{key_suffix}", type="secondary", use_container_width=True):
            view_document_detail(doc_id)
            st.rerun()

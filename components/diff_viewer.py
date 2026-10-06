"""Folio Platform - Cross-Instrument Diff & Reconciliation Component."""

import streamlit as st
import textwrap
from typing import Dict, Any

def render_diff_viewer(reconciler_data: Dict[str, Any]) -> None:
    """Render the provisional reconciler, side-by-side comparison metrics, and diff drawer."""
    if not reconciler_data:
        return
        
    status_text = reconciler_data.get("status_text", "Conflict check: No direct contradiction found (1 variance note)")
    active_col = reconciler_data.get("active_column", {})
    hist_col = reconciler_data.get("historical_column", {})
    diff_drawer = reconciler_data.get("diff_drawer", {})
    show_diff = st.session_state.get("show_diff_drawer", True)
    
    # Active Metrics HTML
    active_list = []
    for m in active_col.get("metrics", []):
        m_html = f"""<div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.25rem 1.4rem; margin-bottom: 1rem; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.04);"><span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; text-transform: uppercase; color: #727973; display: block; letter-spacing: 0.06em;">{m.get('label')}</span><div style="display: flex; justify-content: space-between; align-items: baseline; margin: 0.5rem 0 0.25rem 0;"><div class="folio-metric-numeral" style="color: #082217; font-size: 42px;">{m.get('numeral')}</div><span class="metric-pill-green">{m.get('pill')}</span></div><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #424844; margin: 0.5rem 0 0 0; line-height: 1.5;">{m.get('description')}</p></div>"""
        active_list.append(m_html)
    active_cards_html = "".join(active_list)

    # Historical Metrics HTML
    hist_list = []
    for m in hist_col.get("metrics", []):
        is_strike = 'line-through' in m.get('numeral_style', '') or 'Superseded' in m.get('pill', '')
        num_style = "color: #727973; text-decoration: line-through; opacity: 0.7;" if is_strike else "color: #A0401C;"
        h_html = f"""<div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.25rem 1.4rem; margin-bottom: 1rem; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.04);"><span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; text-transform: uppercase; color: #727973; display: block; letter-spacing: 0.06em;">{m.get('label')}</span><div style="display: flex; justify-content: space-between; align-items: baseline; margin: 0.5rem 0 0.25rem 0;"><div class="folio-metric-numeral" style="{num_style} font-size: 42px;">{m.get('numeral')}</div><span class="metric-pill-terracotta">{m.get('pill')}</span></div><p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #424844; margin: 0.5rem 0 0 0; line-height: 1.5;">{m.get('description')}</p></div>"""
        hist_list.append(h_html)
    hist_cards_html = "".join(hist_list)

    # Diff Drawer HTML
    if show_diff and diff_drawer:
        diff_items = []
        for itm in diff_drawer.get("items", []):
            itype = itm.get("type")
            prefix = itm.get("prefix", "")
            text = itm.get("text", "")
            if itype == "minus":
                diff_items.append(f'<div style="color: #BA1A1A; margin-bottom: 0.45rem;"><strong>{prefix}</strong> {text}</div>')
            elif itype == "plus":
                diff_items.append(f'<div style="color: #1E382B; margin-bottom: 0.45rem;"><strong>{prefix}</strong> {text}</div>')
            else:
                diff_items.append(f'<div style="color: #727973; font-style: italic; margin-top: 0.25rem;"><strong>{prefix}</strong> {text}</div>')
        diff_items_html = "".join(diff_items)

        diff_box_html = f"""<div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.15rem 1.4rem; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 12px; line-height: 1.65; margin-top: 1.25rem; box-shadow: 0 1px 3px rgba(44, 45, 42, 0.02);"><div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E4DFD3; padding-bottom: 0.65rem; margin-bottom: 0.85rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #727973;"><span>{diff_drawer.get('header', 'STRUCTURAL CLAUSE DELTA CHECK')}</span><span style="color: #1E382B; font-weight: 600;">{diff_drawer.get('classification', 'Variance Classification: Minor / Reconciled')}</span></div>{diff_items_html}</div>"""
    else:
        diff_box_html = ""

    container_html = textwrap.dedent(f"""
    <div style="background-color: #F5F4EF; border: 1px solid #E4DFD3; border-radius: 8px; padding: 2rem 2.25rem; margin-top: 2.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(44, 45, 42, 0.02);">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E4DFD3; padding-bottom: 1rem; margin-bottom: 1.75rem; flex-wrap: wrap; gap: 0.75rem;">
        <div>
          <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block; margin-bottom: 0.25rem;">Cross-Instrument Verification</span>
          <h2 style="font-family: 'Newsreader', serif; font-size: 20px; font-weight: 500; color: #082217; margin: 0;">Provisional Reconciler & Conflict Check</h2>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
          <div style="display: inline-flex; align-items: center; gap: 0.35rem; background-color: #EFEEE9; border: 1px solid #E4DFD3; border-radius: 4px; padding: 0.35rem 0.75rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #424844;">
            <span class="material-symbols-outlined" style="font-size: 16px; color: #A0401C;">info</span>
            <span>{status_text}</span>
          </div>
        </div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.75rem;">
        <div>
          <div style="margin-bottom: 1rem; border-bottom: 1px solid #E4DFD3; padding-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 700; color: #082217; letter-spacing: 0.04em;">{active_col.get('title', 'GRANT GUIDELINES (Active)')}</span>
            <span style="font-family: ui-monospace, monospace; font-size: 11px; color: #727973;">{active_col.get('meta', 'Current Cycle')}</span>
          </div>
          {active_cards_html}
        </div>
        <div>
          <div style="margin-bottom: 1rem; border-bottom: 1px solid #E4DFD3; padding-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 700; color: #A0401C; letter-spacing: 0.04em;">{hist_col.get('title', 'DONOR AGREEMENT / HISTORICAL')}</span>
            <span style="font-family: ui-monospace, monospace; font-size: 11px; color: #A0401C;">{hist_col.get('meta', 'Historical Precedent')}</span>
          </div>
          {hist_cards_html}
        </div>
      </div>
      
      {diff_box_html}
    </div>
    """).strip()
    
    st.html(container_html)
    
    # Toggle Diff Drawer Button
    c_space, c_toggle = st.columns([7.8, 2.2])
    with c_toggle:
        diff_label = "Hide Diff Drawer" if show_diff else "Side-by-side Diff"
        if st.button(f"⚙ {diff_label}", key="btn_toggle_diff_drawer", type="secondary", use_container_width=True):
            st.session_state.show_diff_drawer = not show_diff
            st.rerun()

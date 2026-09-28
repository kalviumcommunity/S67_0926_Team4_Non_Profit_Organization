"""Folio Platform - Visual Lineage & Provenance Tree Component."""

import streamlit as st
import textwrap
from typing import Dict, Any

def render_provenance_chain(evidence_data: Dict[str, Any]) -> None:
    """Render the 100% deterministic lineage tree diagram matching Stitch editorial design."""
    if not evidence_data:
        return
        
    root = evidence_data.get("lineage_root", {})
    branch_a = evidence_data.get("branch_a", {})
    branch_b = evidence_data.get("branch_b", {})
    
    tree_html = textwrap.dedent(f"""
    <div style="background-color: #F5F4EF; border: 1px solid #E4DFD3; border-radius: 8px; padding: 2rem; margin-bottom: 2.5rem; box-shadow: 0 1px 3px rgba(44, 45, 42, 0.02);">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E4DFD3; padding-bottom: 1rem; margin-bottom: 2rem; flex-wrap: wrap; gap: 0.75rem;">
        <div>
          <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block; margin-bottom: 0.25rem;">Lineage Mapping</span>
          <h2 style="font-family: 'Newsreader', serif; font-size: 20px; font-weight: 500; color: #082217; margin: 0;">Authority & Citation Branch</h2>
        </div>
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: #EFEEE9; border: 1px solid #E4DFD3; border-radius: 4px; padding: 0.35rem 0.75rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 600; color: #082217;">
          <span style="width: 6px; height: 6px; border-radius: 50%; background-color: #1E382B;"></span>
          <span>100% Deterministic Lineage</span>
        </div>
      </div>
      
      <div style="display: flex; flex-direction: column; align-items: center; max-width: 760px; margin: 0 auto; padding: 0.5rem 0;">
        <div style="background-color: #FFFFFF; border: 2px solid #1E382B; border-radius: 4px; padding: 1.25rem 2rem; width: 100%; max-width: 540px; text-align: center; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.05);">
          <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #A0401C; display: block; margin-bottom: 0.35rem;">
            {root.get('title', 'Synthesized Answer Statement')}
          </span>
          <p style="font-family: 'Newsreader', serif; font-size: 20px; font-weight: 600; color: #082217; margin: 0 0 0.4rem 0;">
            {root.get('statement', 'Quarterly within 30 days · Annual at year-end')}
          </p>
          <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; font-weight: 600; color: #727973; letter-spacing: 0.04em;">
            {root.get('meta', '2 Authoritative Records · Zero Extrapolations')}
          </div>
        </div>
        
        <div style="width: 1px; height: 32px; background-color: #C2C8C2;"></div>
        
        <div style="position: relative; width: 100%; max-width: 520px; height: 1px; background-color: #C2C8C2;">
          <div style="position: absolute; left: 20%; top: 0; width: 1px; height: 24px; background-color: #C2C8C2; display: flex; flex-direction: column; align-items: center;">
            <div style="margin-top: 24px; width: 8px; height: 8px; border-radius: 50%; background-color: #1E382B;"></div>
          </div>
          <div style="position: absolute; right: 20%; top: 0; width: 1px; height: 24px; background-color: #C2C8C2; display: flex; flex-direction: column; align-items: center;">
            <div style="margin-top: 24px; width: 8px; height: 8px; border-radius: 50%; background-color: #A0401C;"></div>
          </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; width: 100%; max-width: 680px; margin-top: 2.5rem;">
          <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.15rem 1.5rem; width: 100%; text-align: center; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.04);">
              <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block;">
                {branch_a.get('category', 'Primary Regulatory Framework')}
              </span>
              <p style="font-family: 'Newsreader', serif; font-size: 17px; font-weight: 600; color: #082217; margin: 0.35rem 0 0.15rem 0;">
                {branch_a.get('doc_name', 'GRANT GUIDELINES')}
              </p>
              <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #727973; margin: 0;">
                {branch_a.get('doc_sub', 'Helios Operational Directives 2025–26')}
              </p>
            </div>
            <div style="width: 1px; height: 16px; background-color: #C2C8C2;"></div>
            <div style="width: 6px; height: 6px; border-radius: 1px; background-color: #1E382B;"></div>
            <div style="width: 1px; height: 12px; background-color: #C2C8C2;"></div>
            <div style="background-color: #FBF9F4; border: 1px solid #E4DFD3; border-radius: 4px; padding: 0.25rem 0.75rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 600; color: #082217;">
              {branch_a.get('clause_tag', '§ 5.1 · Page 8')}
            </div>
          </div>
          
          <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 4px; padding: 1.15rem 1.5rem; width: 100%; text-align: center; box-shadow: 0 2px 8px -2px rgba(44, 45, 42, 0.04);">
              <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #727973; display: block;">
                {branch_b.get('category', 'Binding Grantee Instrument')}
              </span>
              <p style="font-family: 'Newsreader', serif; font-size: 17px; font-weight: 600; color: #082217; margin: 0.35rem 0 0.15rem 0;">
                {branch_b.get('doc_name', 'DONOR AGREEMENT')}
              </p>
              <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; color: #727973; margin: 0;">
                {branch_b.get('doc_sub', 'Bilateral Compact #H-882 (Nov 2024)')}
              </p>
            </div>
            <div style="width: 1px; height: 16px; background-color: #C2C8C2;"></div>
            <div style="width: 6px; height: 6px; border-radius: 1px; background-color: #A0401C;"></div>
            <div style="width: 1px; height: 12px; background-color: #C2C8C2;"></div>
            <div style="background-color: #FBF9F4; border: 1px solid #E4DFD3; border-radius: 4px; padding: 0.25rem 0.75rem; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 600; color: #A0401C;">
              {branch_b.get('clause_tag', '§ 7.2 · Page 14')}
            </div>
          </div>
        </div>
      </div>
    </div>
    """).strip()
    st.html(tree_html)

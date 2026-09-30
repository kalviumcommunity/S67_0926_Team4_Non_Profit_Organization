"""Folio Platform - About the Project & Non-Profit Organization View."""

import streamlit as st
import textwrap
from utils.constants import NAV_RESEARCH, NAV_EVIDENCE, NAV_DOCUMENTS

def render_about_view() -> None:
    """Render the About page focused entirely on the project, non-profit organization mission, and platform impact."""
    
    # 1. Editorial Masthead & Hero
    hero_html = textwrap.dedent("""
    <div style="background: linear-gradient(180deg, #FBF9F4 0%, #F5F1E8 100%); border: 1px solid #E4DFD3; border-radius: 8px; padding: 2.5rem 2.5rem 2.2rem 2.5rem; margin-top: 0.5rem; margin-bottom: 2rem; position: relative; overflow: hidden; box-shadow: 0 4px 16px -4px rgba(28, 29, 27, 0.05);">
      <div style="position: absolute; top: 0; left: 0; bottom: 0; width: 5px; background-color: #1E382B;"></div>
      
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #1E382B; background-color: #E8EFEA; padding: 4px 10px; border-radius: 4px; border: 1px solid #C2D9CB;">
          NON-PROFIT GRANT INTELLIGENCE & STEWARDSHIP
        </span>
        <span style="font-family: 'Newsreader', Georgia, serif; font-style: italic; font-size: 14px; color: #63625D;">
          Institutional Document Intelligence
        </span>
      </div>

      <h1 style="font-family: 'Newsreader', Georgia, serif; font-size: 32px; font-weight: 600; color: #1B1C19; margin: 0 0 0.85rem 0; line-height: 1.25;">
        Empowering Non-Profit Stewardship Through Grounded Document Intelligence
      </h1>
      
      <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; color: #424844; line-height: 1.65; max-width: 960px; margin: 0;">
        <strong>FOLIO</strong> is an institutional document intelligence platform built specifically for non-profit organizations, philanthropic foundations, and grantmakers. The platform bridges the gap between complex legal grant instruments and mission execution, providing instant, verifiable answers to critical compliance, allowable cost, and reporting questions.
      </p>
    </div>
    """).strip()
    st.html(hero_html)

    # 2. The Non-Profit Challenge & Our Purpose
    st.html('<h2 style="font-family: \'Newsreader\', Georgia, serif; font-size: 22px; font-weight: 600; color: #1B1C19; margin: 0 0 1rem 0;">Our Purpose & Non-Profit Mission</h2>')
    
    col_p1, col_p2 = st.columns(2, gap="medium")
    
    with col_p1:
        p1_html = textwrap.dedent("""
        <div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 1.6rem; height: 100%; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
          <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;">
            <div style="width: 36px; height: 36px; border-radius: 6px; background-color: #E8EFEA; color: #1E382B; display: flex; align-items: center; justify-content: center;">
              <span class="material-symbols-outlined" style="font-size: 20px;">balance</span>
            </div>
            <h3 style="font-family: 'Newsreader', Georgia, serif; font-size: 18px; font-weight: 600; color: #1B1C19; margin: 0;">The Non-Profit Compliance Challenge</h3>
          </div>
          <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13.5px; color: #555A56; line-height: 1.6; margin: 0;">
            Non-profit organizations manage multi-year grants governed by strict donor covenants, indirect cost caps, matching fund mandates, and quarterly milestones. Navigating hundreds of pages of legal text takes valuable time away from community impact and creates compliance vulnerabilities during annual audits.
          </p>
        </div>
        """).strip()
        st.html(p1_html)

    with col_p2:
        p2_html = textwrap.dedent("""
        <div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 1.6rem; height: 100%; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
          <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;">
            <div style="width: 36px; height: 36px; border-radius: 6px; background-color: #F9EBE6; color: #D96B43; display: flex; align-items: center; justify-content: center;">
              <span class="material-symbols-outlined" style="font-size: 20px;">volunteer_activism</span>
            </div>
            <h3 style="font-family: 'Newsreader', Georgia, serif; font-size: 18px; font-weight: 600; color: #1B1C19; margin: 0;">Our Institutional Commitment</h3>
          </div>
          <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13.5px; color: #555A56; line-height: 1.6; margin: 0;">
            FOLIO empowers program directors, financial stewards, and board members with immediate, zero-hallucination clarity on what is allowable, required, or restricted. Every answer is grounded directly in legally binding agreements, ensuring non-profits protect donor trust and pass every financial audit.
          </p>
        </div>
        """).strip()
        st.html(p2_html)

    st.html('<div style="height: 1.5rem;"></div>')

    # 3. Core Capabilities Grid
    st.html('<h2 style="font-family: \'Newsreader\', Georgia, serif; font-size: 22px; font-weight: 600; color: #1B1C19; margin: 0 0 1rem 0;">What the Project Delivers</h2>')
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        cap1_html = textwrap.dedent("""
        <div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 1.5rem; height: 100%; box-shadow: 0 2px 6px rgba(0,0,0,0.03); display: flex; flex-direction: column;">
          <div style="width: 38px; height: 38px; border-radius: 6px; background-color: #E8EFEA; color: #1E382B; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <span class="material-symbols-outlined" style="font-size: 22px;">verified</span>
          </div>
          <h3 style="font-family: 'Newsreader', Georgia, serif; font-size: 17.5px; font-weight: 600; color: #1B1C19; margin: 0 0 0.5rem 0;">Grounded Grant Synthesis</h3>
          <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #63625D; line-height: 1.55; margin: 0;">
            Delivers executive summaries, allowable overhead rate calculations, and deadline schedules synthesized strictly from active donor agreements with zero AI speculation.
          </p>
        </div>
        """).strip()
        st.html(cap1_html)

    with col2:
        cap2_html = textwrap.dedent("""
        <div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 1.5rem; height: 100%; box-shadow: 0 2px 6px rgba(0,0,0,0.03); display: flex; flex-direction: column;">
          <div style="width: 38px; height: 38px; border-radius: 6px; background-color: #F9EBE6; color: #D96B43; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <span class="material-symbols-outlined" style="font-size: 22px;">inventory_2</span>
          </div>
          <h3 style="font-family: 'Newsreader', Georgia, serif; font-size: 17.5px; font-weight: 600; color: #1B1C19; margin: 0 0 0.5rem 0;">Physical Excerpt Sheets</h3>
          <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #63625D; line-height: 1.55; margin: 0;">
            Presents highlighted primary source clauses alongside generated responses, allowing grant officers to visually cross-examine source text before making fiduciary decisions.
          </p>
        </div>
        """).strip()
        st.html(cap2_html)

    with col3:
        cap3_html = textwrap.dedent("""
        <div style="background-color: #FFFFFF; border: 1px solid #E4DFD3; border-radius: 6px; padding: 1.5rem; height: 100%; box-shadow: 0 2px 6px rgba(0,0,0,0.03); display: flex; flex-direction: column;">
          <div style="width: 38px; height: 38px; border-radius: 6px; background-color: #EFECE4; color: #1B1C19; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <span class="material-symbols-outlined" style="font-size: 22px;">description</span>
          </div>
          <h3 style="font-family: 'Newsreader', Georgia, serif; font-size: 17.5px; font-weight: 600; color: #1B1C19; margin: 0 0 0.5rem 0;">Audit-Ready Export Dossiers</h3>
          <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #63625D; line-height: 1.55; margin: 0;">
            Generates standardized, timestamped audit dossiers with reference tracking codes that can be downloaded and attached directly to annual financial and tax filings.
          </p>
        </div>
        """).strip()
        st.html(cap3_html)

    st.html('<div style="height: 1.5rem;"></div>')

    # 4. Non-Profit Stakeholders & Organizational Impact
    st.html('<h2 style="font-family: \'Newsreader\', Georgia, serif; font-size: 22px; font-weight: 600; color: #1B1C19; margin: 0 0 1rem 0;">Who Benefits from FOLIO</h2>')
    
    col_s1, col_s2, col_s3 = st.columns(3, gap="medium")
    
    with col_s1:
        s1_html = textwrap.dedent("""
        <div style="background-color: #FBF9F4; border: 1px solid #E4DFD3; border-radius: 6px; padding: 1.4rem; height: 100%;">
          <div style="font-weight: 700; color: #1E382B; font-size: 14px; margin-bottom: 0.4rem; font-family: 'Plus Jakarta Sans', sans-serif;">
            🏛️ Philanthropic Foundations
          </div>
          <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #555A56; line-height: 1.55; margin: 0;">
            Monitor portfolio-wide compliance and ensure grant disbursements align with donor intents and foundation bylaws.
          </p>
        </div>
        """).strip()
        st.html(s1_html)

    with col_s2:
        s2_html = textwrap.dedent("""
        <div style="background-color: #FBF9F4; border: 1px solid #E4DFD3; border-radius: 6px; padding: 1.4rem; height: 100%;">
          <div style="font-weight: 700; color: #1E382B; font-size: 14px; margin-bottom: 0.4rem; font-family: 'Plus Jakarta Sans', sans-serif;">
            🌱 Non-Profit Program Directors
          </div>
          <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #555A56; line-height: 1.55; margin: 0;">
            Quickly check spending eligibility, budget reallocation thresholds, and milestone reporting schedules without legal bottlenecks.
          </p>
        </div>
        """).strip()
        st.html(s2_html)

    with col_s3:
        s3_html = textwrap.dedent("""
        <div style="background-color: #FBF9F4; border: 1px solid #E4DFD3; border-radius: 6px; padding: 1.4rem; height: 100%;">
          <div style="font-weight: 700; color: #1E382B; font-size: 14px; margin-bottom: 0.4rem; font-family: 'Plus Jakarta Sans', sans-serif;">
            📋 Compliance & Audit Officers
          </div>
          <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #555A56; line-height: 1.55; margin: 0;">
            Instantly verify evidence trails, clause fidelity, and historical documentation for annual Single Audits and donor reviews.
          </p>
        </div>
        """).strip()
        st.html(s3_html)

    st.html('<div style="height: 1.5rem;"></div>')

    # 5. Quick Navigation Launcher Bar
    st.html('<h3 style="font-family: \'Newsreader\', Georgia, serif; font-size: 19px; font-weight: 600; color: #1B1C19; margin: 0 0 0.75rem 0;">Explore FOLIO Platform Modules</h3>')
    
    col_b1, col_b2, col_b3 = st.columns(3, gap="small")
    
    with col_b1:
        if st.button("🔍 Launch Research & Query Engine", key="about_goto_research", use_container_width=True, type="primary"):
            st.session_state.current_page = NAV_RESEARCH
            st.rerun()

    with col_b2:
        if st.button("📑 Inspect Evidence & Excerpt Sheets", key="about_goto_evidence", use_container_width=True):
            st.session_state.current_page = NAV_EVIDENCE
            st.rerun()

    with col_b3:
        if st.button("🗄️ Browse Document Archival Shelf", key="about_goto_documents", use_container_width=True):
            st.session_state.current_page = NAV_DOCUMENTS
            st.session_state.document_view_mode = "shelf"
            st.rerun()

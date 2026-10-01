"""Folio Platform - Application Views Package."""

from views.research_view import render_research_view
from views.evidence_view import render_evidence_view
from views.documents_view import render_documents_view
from views.about_view import render_about_view

__all__ = [
    "render_research_view",
    "render_evidence_view",
    "render_documents_view",
    "render_about_view",
]

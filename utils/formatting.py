"""Folio Platform - Formatting, Text Processing & Highlighting Utilities."""

import re
import html

def highlight_search_terms(text: str, search_term: str, highlight_class: str = "ink-highlight-primary") -> str:
    """Safely highlight search terms in text with HTML mark tags."""
    if not text or not search_term or len(search_term.strip()) == 0:
        return html.escape(text) if text else ""
    
    escaped_text = html.escape(text)
    escaped_term = re.escape(html.escape(search_term.strip()))
    
    pattern = re.compile(f"({escaped_term})", re.IGNORECASE)
    replacement = f'<mark class="{highlight_class}">\\1</mark>'
    
    return pattern.sub(replacement, escaped_text)

def format_currency(amount: float) -> str:
    """Format currency values cleanly (e.g., $1,250,000)."""
    return f"${amount:,.0f}"

def format_page_range(start_page: int, end_page: int = None) -> str:
    """Format page indicators (e.g. p. 8 or pp. 8–10)."""
    if end_page and end_page != start_page:
        return f"pp. {start_page}–{end_page}"
    return f"p. {start_page}"

def sanitize_snippet(snippet: str, max_length: int = 240) -> str:
    """Truncate text cleanly with ellipsis."""
    if not snippet:
        return ""
    if len(snippet) <= max_length:
        return snippet
    return snippet[:max_length].rstrip() + "..."

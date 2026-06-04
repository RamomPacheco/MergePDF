"""Inline SVG icon strings for the UI."""

APP_LOGO_SVG = """
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="2" width="18" height="20" rx="2" fill="none" stroke="#4f8ef7" stroke-width="1.5"/>
  <path d="M7 8h10M7 12h10M7 16h6" stroke="#4f8ef7" stroke-width="1.5" stroke-linecap="round"/>
</svg>
"""

CHECK_SVG = """
<svg viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 9l4 4 8-8" fill="none" stroke="#22c55e" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

UPLOAD_SVG = """
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 16V4M8 8l4-4 4 4" fill="none" stroke="#6b7280" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M4 20h16" fill="none" stroke="#6b7280" stroke-width="1.5" stroke-linecap="round"/>
</svg>
"""

ICON_MERGE = """
<svg viewBox="0 0 18 18"><path d="M2 5h6v8H2zm8 0h6v8h-6z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
"""
ICON_SPLIT = """
<svg viewBox="0 0 18 18"><path d="M9 2v14M4 6l5-4 5 4M4 12l5 4 5-4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
"""
ICON_ROTATE = """
<svg viewBox="0 0 18 18"><path d="M14 9a5 5 0 10-5 5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M14 5v4h-4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
"""
ICON_WATERMARK = """
<svg viewBox="0 0 18 18"><path d="M3 14c2-4 4-6 6-6s4 2 6 6" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="9" cy="7" r="2" fill="currentColor" opacity="0.5"/></svg>
"""
ICON_EXTRACT = """
<svg viewBox="0 0 18 18"><path d="M4 4h10v10H4z" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M6 8h6M6 11h4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
"""
ICON_TABLE = """
<svg viewBox="0 0 18 18"><rect x="3" y="4" width="12" height="10" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M3 8h12M9 4v10" stroke="currentColor" stroke-width="1.2"/></svg>
"""
ICON_LOCK = """
<svg viewBox="0 0 18 18"><rect x="4" y="8" width="10" height="8" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M6 8V6a3 3 0 116 0v2" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
"""
ICON_EDIT = """
<svg viewBox="0 0 18 18"><path d="M4 14l2-6 6-2 2 2-6 2-6 2z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>
"""
ICON_DOCX = """
<svg viewBox="0 0 18 18"><path d="M4 3h7l4 4v8H4z" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M11 3v4h4M6 10h6M6 13h4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
"""

SIDEBAR_ICONS = [
    ICON_MERGE,
    ICON_SPLIT,
    ICON_ROTATE,
    ICON_WATERMARK,
    ICON_EXTRACT,
    ICON_TABLE,
    ICON_LOCK,
    ICON_EDIT,
    ICON_DOCX,
]

SIDEBAR_LABELS = [
    "Mesclar PDFs",
    "Dividir PDF",
    "Rotacionar",
    "Watermark",
    "Extrair Texto",
    "Extrair Tabelas",
    "Proteger PDF",
    "Editar Texto (Direto)",
    "Editar via DOCX",
]

"""Centralized QSS theme for PDF Toolkit."""

from __future__ import annotations

from PySide6.QtGui import QFont, QFontDatabase

COLORS = {
    "bg": "#0f0f0f",
    "surface": "#1a1a1a",
    "border": "#2a2a2a",
    "accent": "#4f8ef7",
    "accent2": "#a78bfa",
    "text": "#f0f0f0",
    "text_muted": "#6b7280",
    "success": "#22c55e",
    "error": "#ef4444",
    "warning": "#f59e0b",
}


def resolve_mono_font() -> str:
    """Return JetBrains Mono if available, else Consolas."""
    db = QFontDatabase()
    families = set(db.families())
    if "JetBrains Mono" in families:
        return "JetBrains Mono"
    if "Consolas" in families:
        return "Consolas"
    return "Courier New"


def build_stylesheet() -> str:
    """Build the application-wide QSS stylesheet."""
    mono = resolve_mono_font()
    c = COLORS
    return f"""
    QWidget {{
        background-color: {c["bg"]};
        color: {c["text"]};
        font-family: "Segoe UI";
        font-size: 10pt;
    }}

    #header {{
        background-color: {c["surface"]};
        border-bottom: 2px solid qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {c["accent"]}, stop:0.5 {c["accent2"]}, stop:1 {c["accent"]}
        );
    }}

    #appTitle {{
        font-size: 14pt;
        font-weight: bold;
        color: {c["text"]};
    }}

    #appVersion {{
        color: {c["text_muted"]};
        font-size: 9pt;
    }}

    #winBtnMin, #winBtnMax, #winBtnClose {{
        border-radius: 7px;
        min-width: 14px;
        max-width: 14px;
        min-height: 14px;
        max-height: 14px;
        border: none;
    }}
    #winBtnMin {{ background-color: #f59e0b; }}
    #winBtnMax {{ background-color: #22c55e; }}
    #winBtnClose {{ background-color: #ef4444; }}

    #sidebar {{
        background-color: {c["surface"]};
        border-right: 1px solid {c["border"]};
    }}

    #sidebarItem {{
        text-align: left;
        padding: 10px 14px;
        border: none;
        border-left: 3px solid transparent;
        border-radius: 0;
        background-color: transparent;
        color: {c["text_muted"]};
    }}
    #sidebarItem:hover {{
        background-color: #ffffff08;
    }}
    #sidebarItem:checked {{
        background-color: #4f8ef720;
        border-left: 3px solid {c["accent"]};
        color: {c["text"]};
    }}

    #contentArea {{
        background-color: {c["bg"]};
    }}

    #panelTitle {{
        font-size: 16pt;
        font-weight: bold;
        color: {c["text"]};
    }}

    #panelDesc {{
        color: {c["text_muted"]};
        font-size: 10pt;
    }}

    #dropZone {{
        background-color: {c["surface"]};
        border: 2px dashed {c["border"]};
        border-radius: 12px;
        min-height: 120px;
    }}
    #dropZone[hover="true"] {{
        border-color: {c["accent"]};
        background-color: #4f8ef710;
    }}
    #dropZone[filled="true"] {{
        border-color: {c["success"]};
        border-style: solid;
    }}

    #dropHint {{
        color: {c["text_muted"]};
    }}

    #fileNameLabel {{
        font-family: "{mono}";
        color: {c["text"]};
    }}

    #monoLabel {{
        font-family: "{mono}";
        color: {c["text_muted"]};
        font-size: 9pt;
    }}

    QLineEdit, QSpinBox, QComboBox {{
        background-color: {c["surface"]};
        border: 1px solid {c["border"]};
        border-radius: 6px;
        padding: 8px 10px;
        color: {c["text"]};
        min-height: 20px;
    }}
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border-color: {c["accent"]};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {c["surface"]};
        border: 1px solid {c["border"]};
        selection-background-color: #4f8ef730;
    }}

    #primaryButton {{
        background-color: {c["accent"]};
        color: white;
        border: none;
        border-radius: 8px;
        min-height: 44px;
        font-weight: bold;
        font-size: 11pt;
    }}
    #primaryButton:hover {{
        background-color: #6ba3f9;
    }}
    #primaryButton:disabled {{
        background-color: {c["border"]};
        color: {c["text_muted"]};
    }}

    #logArea {{
        background-color: {c["surface"]};
        border: 1px solid {c["border"]};
        border-radius: 8px;
        font-family: "{mono}";
        font-size: 9pt;
        color: {c["text_muted"]};
        padding: 8px;
    }}

    #footer {{
        background-color: {c["surface"]};
        border-top: 1px solid {c["border"]};
        min-height: 36px;
        max-height: 36px;
    }}

    #footerStatus {{
        color: {c["text_muted"]};
        font-size: 9pt;
    }}

    #footerSession {{
        color: {c["text_muted"]};
        font-size: 9pt;
    }}

    #statusDotReady {{
        background-color: {c["success"]};
        border-radius: 6px;
        min-width: 12px;
        max-width: 12px;
        min-height: 12px;
        max-height: 12px;
    }}
    #statusDotPartial {{
        background-color: {c["warning"]};
        border-radius: 6px;
        min-width: 12px;
        max-width: 12px;
        min-height: 12px;
        max-height: 12px;
    }}
    #statusDotMissing {{
        background-color: {c["error"]};
        border-radius: 6px;
        min-width: 12px;
        max-width: 12px;
        min-height: 12px;
        max-height: 12px;
    }}

    #chipOk {{
        background-color: #22c55e20;
        color: {c["success"]};
        border: 1px solid #22c55e40;
        border-radius: 10px;
        padding: 2px 8px;
        font-size: 8pt;
        font-family: "{mono}";
    }}
    #chipError {{
        background-color: #ef444420;
        color: {c["error"]};
        border: 1px solid #ef444440;
        border-radius: 10px;
        padding: 2px 8px;
        font-size: 8pt;
        font-family: "{mono}";
    }}

    #toastSuccess {{
        background-color: #22c55e15;
        border: 1px solid {c["success"]};
        border-radius: 8px;
        padding: 12px 16px;
        color: {c["text"]};
    }}
    #toastError {{
        background-color: #ef444415;
        border: 1px solid {c["error"]};
        border-radius: 8px;
        padding: 12px 16px;
        color: {c["text"]};
    }}

    #splash {{
        background-color: {c["bg"]};
    }}
    #splashTitle {{
        font-size: 18pt;
        font-weight: bold;
        color: {c["text"]};
    }}

    QProgressBar {{
        background-color: {c["surface"]};
        border: none;
        border-radius: 2px;
        max-height: 4px;
    }}
    QProgressBar::chunk {{
        background-color: {c["accent"]};
        border-radius: 2px;
    }}

    QRadioButton {{
        color: {c["text"]};
        spacing: 6px;
    }}
    QRadioButton::indicator {{
        width: 14px;
        height: 14px;
        border-radius: 7px;
        border: 1px solid {c["border"]};
        background: {c["surface"]};
    }}
    QRadioButton::indicator:checked {{
        background: {c["accent"]};
        border-color: {c["accent"]};
    }}

    QScrollBar:vertical {{
        background: {c["surface"]};
        width: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {c["border"]};
        border-radius: 4px;
        min-height: 24px;
    }}
    """


def apply_app_font(app) -> None:
    """Set default application font."""
    app.setFont(QFont("Segoe UI", 10))

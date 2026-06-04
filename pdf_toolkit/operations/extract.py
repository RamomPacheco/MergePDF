"""Extract text and tables from PDF files."""

from __future__ import annotations

from pathlib import Path

import pdfplumber


def extract_text(input_file: str) -> str:
    """Extract all text from the PDF preserving page order."""
    try:
        src = Path(input_file)
        if not src.is_file():
            raise FileNotFoundError(f"File not found: {src}")

        parts: list[str] = []
        with pdfplumber.open(str(src)) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                parts.append(text)
        return "\n".join(parts)
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to extract text: {exc}") from exc


def extract_tables(input_file: str) -> list:
    """Extract tables from all pages of the PDF."""
    try:
        src = Path(input_file)
        if not src.is_file():
            raise FileNotFoundError(f"File not found: {src}")

        tables: list = []
        with pdfplumber.open(str(src)) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables() or []
                tables.extend(page_tables)
        return tables
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to extract tables: {exc}") from exc

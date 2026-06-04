"""Direct PDF text editing via PyMuPDF."""

from __future__ import annotations

import warnings
from pathlib import Path

import fitz


def has_selectable_text(input_file: str) -> bool:
    """Return True if the PDF contains extractable (non-empty) text."""
    try:
        src = Path(input_file)
        if not src.is_file():
            raise FileNotFoundError(f"File not found: {src}")

        doc = fitz.open(str(src))
        try:
            for page in doc:
                if page.get_text().strip():
                    return True
            return False
        finally:
            doc.close()
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to inspect PDF text: {exc}") from exc


def _embedded_font_names(doc: fitz.Document) -> set[str]:
    names: set[str] = set()
    for page_index in range(doc.page_count):
        fonts = doc.get_page_fonts(page_index)
        for entry in fonts:
            if len(entry) > 3 and entry[3]:
                names.add(entry[3])
    return names


def _resolve_fontname(doc: fitz.Document, span_font: str) -> str:
    embedded = _embedded_font_names(doc)
    if span_font in embedded:
        return span_font
    warnings.warn(
        f"Font '{span_font}' is not embedded; using fallback 'helv'.",
        UserWarning,
        stacklevel=2,
    )
    return "helv"


def edit_text(
    input_file: str,
    output_file: str,
    old_text: str,
    new_text: str,
) -> int:
    """Replace old_text with new_text by covering spans and rewriting."""
    try:
        if not old_text:
            raise ValueError("old_text cannot be empty")

        if not has_selectable_text(input_file):
            raise ValueError(
                "PDF escaneado detectado. Use OCR antes de editar."
            )

        src = Path(input_file)
        out = Path(output_file)
        out.parent.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(str(src))
        replacements = 0
        try:
            for page in doc:
                blocks = page.get_text("dict").get("blocks", [])
                for block in blocks:
                    if block.get("type") != 0:
                        continue
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            span_text = span.get("text", "")
                            if old_text not in span_text:
                                continue

                            bbox = fitz.Rect(span["bbox"])
                            page.draw_rect(
                                bbox,
                                color=(1, 1, 1),
                                fill=(1, 1, 1),
                            )

                            updated = span_text.replace(old_text, new_text)
                            fontname = _resolve_fontname(
                                doc,
                                span.get("font", "helv"),
                            )
                            fontsize = span.get("size", 11)
                            origin = span.get("origin", (bbox.x0, bbox.y1))

                            page.insert_text(
                                origin,
                                updated,
                                fontname=fontname,
                                fontsize=fontsize,
                            )
                            replacements += 1

            doc.save(str(out))
        finally:
            doc.close()

        return replacements
    except (ValueError, FileNotFoundError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to edit PDF text: {exc}") from exc

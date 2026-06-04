"""Apply a watermark PDF over every page."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def add_watermark(
    input_file: str,
    watermark_file: str,
    output_file: str,
) -> None:
    """Overlay a watermark PDF on all pages of the input document."""
    try:
        src = Path(input_file)
        mark = Path(watermark_file)
        if not src.is_file():
            raise FileNotFoundError(f"File not found: {src}")
        if not mark.is_file():
            raise FileNotFoundError(f"Watermark not found: {mark}")

        reader = PdfReader(str(src))
        watermark_reader = PdfReader(str(mark))
        watermark_page = watermark_reader.pages[0]

        writer = PdfWriter()
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)

        out = Path(output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("wb") as fp:
            writer.write(fp)
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to add watermark: {exc}") from exc

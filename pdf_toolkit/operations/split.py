"""Split a PDF into one file per page."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def split_pdf(input_file: str, output_dir: str) -> None:
    """Save each page of the input PDF as a separate file."""
    try:
        src = Path(input_file)
        if not src.is_file():
            raise FileNotFoundError(f"File not found: {src}")

        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        reader = PdfReader(str(src))
        stem = src.stem

        for index, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            page_path = out_dir / f"{stem}_page_{index + 1:03d}.pdf"
            with page_path.open("wb") as fp:
                writer.write(fp)
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to split PDF: {exc}") from exc

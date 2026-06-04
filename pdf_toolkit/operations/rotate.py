"""Rotate pages in a PDF."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter

VALID_DEGREES = (90, 180, 270)


def rotate_pdf(
    input_file: str,
    output_file: str,
    degrees: int,
    pages: list[int] | None = None,
) -> None:
    """Rotate specific pages or all pages by the given degrees."""
    try:
        if degrees not in VALID_DEGREES:
            raise ValueError("Degrees must be 90, 180, or 270")

        src = Path(input_file)
        if not src.is_file():
            raise FileNotFoundError(f"File not found: {src}")

        reader = PdfReader(str(src))
        writer = PdfWriter()
        writer.append(reader)

        page_count = len(writer.pages)
        if pages is None:
            target_pages = list(range(page_count))
        else:
            target_pages = pages

        for page_index in target_pages:
            if page_index < 0 or page_index >= page_count:
                raise ValueError(
                    f"Page index {page_index} is out of range (0-{page_count - 1})"
                )
            writer.pages[page_index].rotate(degrees)

        out = Path(output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("wb") as fp:
            writer.write(fp)
    except (ValueError, FileNotFoundError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to rotate PDF: {exc}") from exc

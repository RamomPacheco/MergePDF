"""Merge multiple PDF files into one."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def merge_pdfs(input_files: list[str], output_file: str) -> None:
    """Merge a list of PDFs into a single output file."""
    try:
        if not input_files:
            raise ValueError("No input files provided")

        paths = [Path(f) for f in input_files]
        for path in paths:
            if not path.is_file():
                raise FileNotFoundError(f"File not found: {path}")

        writer = PdfWriter()
        for path in paths:
            reader = PdfReader(str(path))
            writer.append(reader)

        out = Path(output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("wb") as fp:
            writer.write(fp)
    except (ValueError, FileNotFoundError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to merge PDFs: {exc}") from exc

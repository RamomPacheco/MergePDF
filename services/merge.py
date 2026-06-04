from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pdf_oxide import Pdf, PdfDocument


def merge_pdfs(files: Iterable[str], output_file: str) -> int:
    paths = [str(Path(f)) for f in files]
    if not paths:
        raise ValueError("No files to merge")

    out = Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)

    if len(paths) == 1:
        doc = PdfDocument(paths[0])
        doc.save(str(out))
        return doc.page_count()

    merged = Pdf.merge(paths)
    merged.save(str(out))
    return PdfDocument(str(out)).page_count()

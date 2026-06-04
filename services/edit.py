from __future__ import annotations

from pathlib import Path

from pdf_oxide import PdfDocument


def open_document(path: str) -> PdfDocument:
    return PdfDocument(path)


def save_document(doc: PdfDocument, path: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))


def rotate_all_pages(doc: PdfDocument, degrees: int) -> None:
    doc.rotate_all_pages(degrees)


def rotate_page(doc: PdfDocument, page_index: int, degrees: int) -> None:
    doc.rotate_page(page_index, degrees)


def delete_page(doc: PdfDocument, page_index: int) -> None:
    doc.delete_page(page_index)


def move_page(doc: PdfDocument, from_index: int, to_index: int) -> None:
    doc.move_page(from_index, to_index)


def extract_page_range(
    doc: PdfDocument,
    start_page: int,
    end_page: int,
    output_file: str,
) -> None:
    if start_page < 0 or end_page < start_page:
        raise ValueError("Invalid page range")
    pages = list(range(start_page, end_page + 1))
    if end_page >= doc.page_count():
        raise ValueError("Page range exceeds document length")
    doc.extract_pages(pages, output_file)


def replace_text(doc: PdfDocument, needle: str, replacement: str) -> int:
    if not needle:
        raise ValueError("Search text cannot be empty")

    replacements = 0
    for page_index in range(doc.page_count()):
        page = doc.page(page_index)
        modified = False
        for text in page.find_text_containing(needle):
            if needle not in text.value:
                continue
            page.set_text(text.id, text.value.replace(needle, replacement))
            replacements += 1
            modified = True
        if modified:
            doc.save_page(page)
    return replacements


def set_metadata(
    doc: PdfDocument,
    *,
    title: str | None = None,
    author: str | None = None,
) -> None:
    if title is not None:
        doc.set_title(title)
    if author is not None:
        doc.set_author(author)

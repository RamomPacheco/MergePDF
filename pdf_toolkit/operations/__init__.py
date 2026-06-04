"""PDF operation modules."""

from operations.edit_text import edit_text, has_selectable_text
from operations.extract import extract_tables, extract_text
from operations.merge import merge_pdfs
from operations.protect import decrypt_pdf, encrypt_pdf
from operations.rotate import rotate_pdf
from operations.split import split_pdf
from operations.watermark import add_watermark

__all__ = [
    "add_watermark",
    "decrypt_pdf",
    "edit_text",
    "encrypt_pdf",
    "extract_tables",
    "extract_text",
    "has_selectable_text",
    "merge_pdfs",
    "rotate_pdf",
    "split_pdf",
]

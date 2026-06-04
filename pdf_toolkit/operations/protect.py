"""Encrypt and decrypt PDF files."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def encrypt_pdf(input_file: str, output_file: str, password: str) -> None:
    """Encrypt a PDF with the given password."""
    try:
        if not password:
            raise ValueError("Password cannot be empty")

        src = Path(input_file)
        if not src.is_file():
            raise FileNotFoundError(f"File not found: {src}")

        reader = PdfReader(str(src))
        writer = PdfWriter()
        writer.append(reader)
        writer.encrypt(password)

        out = Path(output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("wb") as fp:
            writer.write(fp)
    except (ValueError, FileNotFoundError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to encrypt PDF: {exc}") from exc


def decrypt_pdf(input_file: str, output_file: str, password: str) -> None:
    """Decrypt a password-protected PDF."""
    try:
        if not password:
            raise ValueError("Password cannot be empty")

        src = Path(input_file)
        if not src.is_file():
            raise FileNotFoundError(f"File not found: {src}")

        reader = PdfReader(str(src))
        if reader.is_encrypted:
            result = reader.decrypt(password)
            if result == 0:
                raise ValueError("Invalid password")

        writer = PdfWriter()
        writer.append(reader)

        out = Path(output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("wb") as fp:
            writer.write(fp)
    except (ValueError, FileNotFoundError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to decrypt PDF: {exc}") from exc

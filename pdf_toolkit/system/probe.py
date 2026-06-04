"""Environment probing for Word engine and PDF libraries."""

from __future__ import annotations

import importlib
import shutil
import sys
from dataclasses import dataclass, field
from enum import Enum
from importlib import metadata


class WordEngineStatus(Enum):
    """DOCX conversion engine availability."""

    READY = "ready"
    PARTIAL = "partial"
    MISSING = "missing"


@dataclass
class ProbeResult:
    """Result of system environment probing."""

    word_status: WordEngineStatus
    word_message: str
    has_python_docx: bool
    has_libreoffice: bool
    has_word: bool
    libraries: dict[str, tuple[bool, str]] = field(default_factory=dict)


def _check_python_docx() -> bool:
    try:
        importlib.import_module("docx")
        return True
    except ImportError:
        return False


def _check_libreoffice() -> bool:
    return bool(shutil.which("soffice") or shutil.which("libreoffice"))


def _check_microsoft_word() -> bool:
    if sys.platform == "win32":
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\WINWORD.EXE",
            )
            winreg.QueryValue(key, None)
            winreg.CloseKey(key)
            return True
        except OSError:
            pass
        try:
            import win32com.client  # noqa: F401

            return True
        except ImportError:
            pass
    return bool(shutil.which("winword"))


def _check_library(module_name: str, dist_name: str | None = None) -> tuple[bool, str]:
    dist = dist_name or module_name
    try:
        importlib.import_module(module_name)
        try:
            version = metadata.version(dist)
        except metadata.PackageNotFoundError:
            version = "installed"
        return True, version
    except ImportError:
        return False, "missing"


def run_probe() -> ProbeResult:
    """Probe Word engine and PDF libraries."""
    has_docx = _check_python_docx()
    has_lo = _check_libreoffice()
    has_word = _check_microsoft_word()
    has_converter = has_lo or has_word

    if has_docx and has_converter:
        status = WordEngineStatus.READY
        if has_word:
            message = "Motor Word detectado"
        else:
            message = "Motor LibreOffice detectado"
    elif has_docx:
        status = WordEngineStatus.PARTIAL
        message = "Motor Word parcial (python-docx OK, conversor ausente)"
    else:
        status = WordEngineStatus.MISSING
        message = "Motor Word não encontrado"

    libraries = {
        "pypdf": _check_library("pypdf"),
        "pdfplumber": _check_library("pdfplumber"),
        "pymupdf": _check_library("fitz", "pymupdf"),
        "pdf2docx": _check_library("pdf2docx"),
    }

    return ProbeResult(
        word_status=status,
        word_message=message,
        has_python_docx=has_docx,
        has_libreoffice=has_lo,
        has_word=has_word,
        libraries=libraries,
    )

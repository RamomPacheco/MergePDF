"""Background workers for non-blocking UI operations."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QThread, Signal

from system.probe import ProbeResult, run_probe


class SystemProbeThread(QThread):
    """Run system probing off the main thread."""

    finished_probe = Signal(object)

    def run(self) -> None:
        result = run_probe()
        self.finished_probe.emit(result)


class PdfWorkerThread(QThread):
    """Execute a PDF operation in a background thread."""

    started_op = Signal()
    progress = Signal(int)
    finished_ok = Signal(object)
    failed = Signal(str)

    def __init__(
        self,
        func: Callable[..., Any],
        kwargs: dict[str, Any] | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._func = func
        self._kwargs = kwargs or {}

    def run(self) -> None:
        self.started_op.emit()
        try:
            result = self._func(**self._kwargs)
            self.finished_ok.emit(result)
        except Exception as exc:
            message = str(exc).strip() or repr(exc)
            cause = exc.__cause__
            if cause is not None:
                cause_msg = str(cause).strip()
                if cause_msg:
                    message = f"{message} ({cause_msg})"
            self.failed.emit(message)

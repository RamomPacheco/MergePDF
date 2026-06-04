"""Application footer with engine and library status."""

from __future__ import annotations

from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from system.probe import ProbeResult, WordEngineStatus
from ui.widgets.status_chip import StatusChip


class Footer(QWidget):
    """Footer bar with Word engine status, session count, and library chips."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("footer")
        self._session_count = 0
        self._pulse_anim: QPropertyAnimation | None = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 6, 16, 6)

        left = QHBoxLayout()
        self._status_dot = QLabel()
        self._status_dot.setFixedSize(12, 12)
        self._status_dot.setObjectName("statusDotMissing")
        self._status_label = QLabel("Verificando motor...")
        self._status_label.setObjectName("footerStatus")
        left.addWidget(self._status_dot)
        left.addWidget(self._status_label)
        layout.addLayout(left, 2)

        self._session_label = QLabel("0 operações realizadas nesta sessão")
        self._session_label.setObjectName("footerSession")
        self._session_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._session_label, 3)

        chips_layout = QHBoxLayout()
        chips_layout.setSpacing(6)
        self._chips = {
            "pypdf": StatusChip("pypdf"),
            "pdfplumber": StatusChip("pdfplumber"),
            "pymupdf": StatusChip("pymupdf"),
            "pdf2docx": StatusChip("pdf2docx"),
        }
        for chip in self._chips.values():
            chips_layout.addWidget(chip)
        layout.addLayout(chips_layout, 2)

    def update_probe(self, result: ProbeResult) -> None:
        """Update footer from probe results."""
        if result.word_status == WordEngineStatus.READY:
            self._status_dot.setObjectName("statusDotReady")
            self._start_pulse()
        elif result.word_status == WordEngineStatus.PARTIAL:
            self._status_dot.setObjectName("statusDotPartial")
            self._stop_pulse()
        else:
            self._status_dot.setObjectName("statusDotMissing")
            self._stop_pulse()
        self._status_dot.style().unpolish(self._status_dot)
        self._status_dot.style().polish(self._status_dot)
        self._status_label.setText(result.word_message)

        for name, chip in self._chips.items():
            ok, version = result.libraries.get(name, (False, "missing"))
            chip.set_status(ok, version)

    def _start_pulse(self) -> None:
        if self._pulse_anim is not None:
            return
        self._pulse_anim = QPropertyAnimation(self._status_dot, b"windowOpacity")
        self._pulse_anim.setDuration(900)
        self._pulse_anim.setStartValue(1.0)
        self._pulse_anim.setEndValue(0.4)
        self._pulse_anim.setLoopCount(-1)
        self._pulse_anim.start()

    def _stop_pulse(self) -> None:
        if self._pulse_anim is not None:
            self._pulse_anim.stop()
            self._pulse_anim = None
        self._status_dot.setWindowOpacity(1.0)

    def increment_session(self) -> None:
        """Increment completed operations counter."""
        self._session_count += 1
        label = "operação" if self._session_count == 1 else "operações"
        self._session_label.setText(
            f"{self._session_count} {label} realizadas nesta sessão"
        )

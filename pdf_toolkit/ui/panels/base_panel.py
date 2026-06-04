"""Base panel with drop zone, log area, and worker integration."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.drop_zone import DropZone
from ui.workers import PdfWorkerThread


class LoadingSpinner(QWidget):
    """Simple rotating arc spinner."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(18, 18)
        self._angle = 0
        from PySide6.QtCore import QTimer

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.setInterval(50)

    def start(self) -> None:
        self._timer.start()
        self.show()

    def stop(self) -> None:
        self._timer.stop()
        self.hide()

    def _tick(self) -> None:
        self._angle = (self._angle + 30) % 360
        self.update()

    def paintEvent(self, event) -> None:
        from PySide6.QtGui import QColor, QPainter, QPen

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#ffffff"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawArc(2, 2, 14, 14, self._angle * 16, 120 * 16)
        painter.end()


class BasePanel(QWidget):
    """Base operation panel with shared UI elements."""

    def __init__(
        self,
        title: str,
        description: str,
        button_text: str,
        parent: QWidget | None = None,
        *,
        multiple_files: bool = False,
        drop_extensions: tuple[str, ...] = (".pdf",),
        show_drop_zone: bool = True,
    ) -> None:
        super().__init__(parent)
        self._button_text = button_text
        self._worker: PdfWorkerThread | None = None
        self._on_success_callback: Callable[[], None] | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 16)
        layout.setSpacing(12)

        self._title = QLabel(title)
        self._title.setObjectName("panelTitle")
        layout.addWidget(self._title)

        self._desc = QLabel(description)
        self._desc.setObjectName("panelDesc")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        self.drop_zone: DropZone | None = None
        if show_drop_zone:
            self.drop_zone = DropZone(
                self,
                multiple=multiple_files,
                extensions=drop_extensions,
            )
            layout.addWidget(self.drop_zone)

        self.config_layout = QVBoxLayout()
        self.config_layout.setSpacing(8)
        layout.addLayout(self.config_layout)

        layout.addStretch(1)

        btn_row = QHBoxLayout()
        self._spinner = LoadingSpinner(self)
        self._spinner.hide()
        self.primary_button = QPushButton(button_text)
        self.primary_button.setObjectName("primaryButton")
        self.primary_button.setCursor(Qt.PointingHandCursor)
        self.primary_button.clicked.connect(self._on_run_clicked)
        btn_row.addWidget(self._spinner)
        btn_row.addWidget(self.primary_button, 1)
        layout.addLayout(btn_row)

        self.log_area = QTextEdit()
        self.log_area.setObjectName("logArea")
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(100)
        layout.addWidget(self.log_area)

    def set_on_success(self, callback: Callable[[], None]) -> None:
        """Register callback after successful operation."""
        self._on_success_callback = callback

    def log_info(self, message: str) -> None:
        """Append an info log line."""
        self.log_area.append(f'<span style="color:#4f8ef7">[INFO]</span> {message}')

    def log_ok(self, message: str) -> None:
        """Append a success log line."""
        self.log_area.append(f'<span style="color:#22c55e">[OK]</span> {message}')

    def log_error(self, message: str) -> None:
        """Append an error log line."""
        self.log_area.append(f'<span style="color:#ef4444">[ERRO]</span> {message}')

    def set_loading(self, loading: bool) -> None:
        """Toggle loading state on the primary button."""
        self.primary_button.setDisabled(loading)
        if loading:
            self.primary_button.setText("Processando...")
            self._spinner.start()
        else:
            self.primary_button.setText(self._button_text)
            self._spinner.stop()

    def run_worker(self, func: Callable[..., Any], **kwargs: Any) -> None:
        """Run an operation in a background thread."""
        if self._worker is not None and self._worker.isRunning():
            self.log_error("Operação em andamento.")
            return

        self.set_loading(True)
        self.log_info("Iniciando operação...")

        self._worker = PdfWorkerThread(func, kwargs, self)
        self._worker.finished_ok.connect(self._on_worker_success)
        self._worker.failed.connect(self._on_worker_failed)
        self._worker.start()

    def _on_worker_success(self, result: object) -> None:
        self.set_loading(False)
        self._handle_success(result)

    def _on_worker_failed(self, message: str) -> None:
        self.set_loading(False)
        self.log_error(message)
        window = self.window()
        if hasattr(window, "show_error_toast"):
            window.show_error_toast(message)

    def _handle_success(self, result: object) -> None:
        """Override in subclasses for custom success handling."""
        self.log_ok("Operação concluída.")
        window = self.window()
        if hasattr(window, "show_success_toast"):
            window.show_success_toast()
        if hasattr(window, "increment_session"):
            window.increment_session()
        if self._on_success_callback:
            self._on_success_callback()

    def _on_run_clicked(self) -> None:
        """Override in subclasses."""
        pass

    def _require_paths(self, multiple: bool = False) -> list[str] | str | None:
        if self.drop_zone is None:
            return [] if multiple else None
        paths = self.drop_zone.paths()
        if not paths:
            self.log_error("Selecione um arquivo PDF.")
            return None
        return paths if multiple else paths[0]

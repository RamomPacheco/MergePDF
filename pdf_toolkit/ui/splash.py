"""Splash screen shown on startup."""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from ui.styles.icons import APP_LOGO_SVG


class SplashScreen(QWidget):
    """Frameless splash screen with logo and progress bar."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("splash")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen)
        self.setFixedSize(400, 260)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        logo = QSvgWidget(self)
        logo.load(APP_LOGO_SVG.encode())
        logo.setFixedSize(64, 64)
        layout.addWidget(logo, alignment=Qt.AlignCenter)

        title = QLabel("PDF Toolkit")
        title.setObjectName("splashTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self._progress = QProgressBar()
        self._progress.setRange(0, 0)
        self._progress.setFixedWidth(200)
        layout.addWidget(self._progress, alignment=Qt.AlignCenter)

        self._on_finish = None

    def show_for(
        self,
        duration_ms: int,
        on_finish,
    ) -> None:
        """Show splash and call on_finish after duration."""
        self._on_finish = on_finish
        self.show()
        QTimer.singleShot(duration_ms, self._finish)

    def _finish(self) -> None:
        self.close()
        if self._on_finish:
            self._on_finish()

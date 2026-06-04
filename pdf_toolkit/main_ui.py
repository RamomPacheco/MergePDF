"""Desktop UI entry point for PDF Toolkit."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.splash import SplashScreen
from ui.styles.theme import apply_app_font, build_stylesheet


def main() -> None:
    """Launch the PDF Toolkit desktop application."""
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Toolkit")
    app.setApplicationVersion("1.0.0")
    apply_app_font(app)
    app.setStyleSheet(build_stylesheet())

    window = MainWindow()

    def show_main() -> None:
        window.show()

    splash = SplashScreen()
    splash.show_for(1500, show_main)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

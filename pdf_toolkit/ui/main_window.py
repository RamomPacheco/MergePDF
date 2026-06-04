"""Main application window."""

from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.footer import Footer
from ui.panels.edit_direct_panel import EditDirectPanel
from ui.panels.edit_docx_panel import EditDocxPanel
from ui.panels.extract_panel import ExtractTablesPanel, ExtractTextPanel
from ui.panels.merge_panel import MergePanel
from ui.panels.protect_panel import ProtectPanel
from ui.panels.rotate_panel import RotatePanel
from ui.panels.split_panel import SplitPanel
from ui.panels.watermark_panel import WatermarkPanel
from ui.sidebar import Sidebar
from ui.styles.icons import APP_LOGO_SVG
from ui.widgets.toast import Toast
from ui.workers import SystemProbeThread


class HeaderBar(QWidget):
    """Draggable header with window controls."""

    def __init__(self, parent_window: QMainWindow) -> None:
        super().__init__()
        self.setObjectName("header")
        self.setFixedHeight(60)
        self._window = parent_window
        self._drag_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)

        logo = QSvgWidget(self)
        logo.load(APP_LOGO_SVG.encode())
        logo.setFixedSize(24, 24)
        layout.addWidget(logo)

        title = QLabel("PDF Toolkit")
        title.setObjectName("appTitle")
        layout.addWidget(title)
        layout.addStretch()

        version = QLabel("v1.0.0")
        version.setObjectName("appVersion")
        layout.addWidget(version)
        layout.addSpacing(16)

        btn_min = QPushButton()
        btn_min.setObjectName("winBtnMin")
        btn_min.setCursor(Qt.PointingHandCursor)
        btn_min.clicked.connect(parent_window.showMinimized)
        layout.addWidget(btn_min)

        btn_max = QPushButton()
        btn_max.setObjectName("winBtnMax")
        btn_max.setCursor(Qt.PointingHandCursor)
        btn_max.clicked.connect(lambda: None)
        layout.addWidget(btn_max)

        btn_close = QPushButton()
        btn_close.setObjectName("winBtnClose")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(parent_window.close)
        layout.addWidget(btn_close)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint()
                - self._window.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self._window.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None
        super().mouseReleaseEvent(event)


class MainWindow(QMainWindow):
    """Frameless main window hosting sidebar, panels, and footer."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PDF Toolkit")
        self.setFixedSize(1100, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._header = HeaderBar(self)
        root.addWidget(self._header)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self._sidebar = Sidebar()
        self._sidebar.operationSelected.connect(self._switch_panel)
        body.addWidget(self._sidebar)

        content_wrapper = QWidget()
        content_wrapper.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()
        self._opacity = QGraphicsOpacityEffect(self._stack)
        self._stack.setGraphicsEffect(self._opacity)
        self._opacity.setOpacity(1.0)

        self._panels = [
            MergePanel(),
            SplitPanel(),
            RotatePanel(),
            WatermarkPanel(),
            ExtractTextPanel(),
            ExtractTablesPanel(),
            ProtectPanel(),
            EditDirectPanel(),
            EditDocxPanel(),
        ]
        for panel in self._panels:
            self._stack.addWidget(panel)

        content_layout.addWidget(self._stack)
        body.addWidget(content_wrapper, 1)
        root.addLayout(body)

        self._footer = Footer()
        root.addWidget(self._footer)

        self._toast = Toast(self)
        self._current_index = 0

        self._probe_thread = SystemProbeThread(self)
        self._probe_thread.finished_probe.connect(self._footer.update_probe)
        self._probe_thread.start()

    def _switch_panel(self, index: int) -> None:
        if index == self._current_index:
            return
        self._fade_to(index)

    def _fade_to(self, index: int) -> None:
        anim_out = QPropertyAnimation(self._opacity, b"opacity")
        anim_out.setDuration(100)
        anim_out.setStartValue(1.0)
        anim_out.setEndValue(0.0)
        anim_out.setEasingCurve(QEasingCurve.InQuad)

        def on_faded_out() -> None:
            self._stack.setCurrentIndex(index)
            self._current_index = index
            self._sidebar.set_active(index)
            anim_in = QPropertyAnimation(self._opacity, b"opacity")
            anim_in.setDuration(100)
            anim_in.setStartValue(0.0)
            anim_in.setEndValue(1.0)
            anim_in.setEasingCurve(QEasingCurve.OutQuad)
            anim_in.start()
            self._fade_in_anim = anim_in

        anim_out.finished.connect(on_faded_out)
        anim_out.start()
        self._fade_out_anim = anim_out

    def show_success_toast(self, text: str = "Operação concluída") -> None:
        """Show success toast notification."""
        self._toast.show_success(text)

    def show_error_toast(self, text: str) -> None:
        """Show error toast notification."""
        self._toast.show_error(text)

    def increment_session(self) -> None:
        """Increment session operation counter in footer."""
        self._footer.increment_session()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self._toast.isVisible():
            self._toast._reposition()

    def closeEvent(self, event) -> None:
        if self._probe_thread.isRunning():
            self._probe_thread.quit()
            self._probe_thread.wait(2000)
        super().closeEvent(event)

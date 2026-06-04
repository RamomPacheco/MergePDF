"""Animated toast notifications."""

from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QTimer, Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class Toast(QWidget):
    """Slide-in toast notification widget."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(Qt.SubWindow)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._label = QLabel(self)
        self._label.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._label)
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._animate_out)
        self._anim: QPropertyAnimation | None = None
        self.hide()

    def _show_toast(self, text: str, object_name: str) -> None:
        self._label.setText(text)
        self.setObjectName(object_name)
        self.style().unpolish(self)
        self.style().polish(self)
        self.adjustSize()
        self._reposition()
        self.show()
        self.raise_()
        start_x = self.x() + 80
        self._animate_in(start_x, self.x())
        self._hide_timer.start(3000)

    def show_success(self, text: str = "Operação concluída") -> None:
        """Show a success toast."""
        self._show_toast(text, "toastSuccess")

    def show_error(self, text: str) -> None:
        """Show an error toast."""
        self._show_toast(text, "toastError")

    def _reposition(self) -> None:
        parent = self.parentWidget()
        if parent is None:
            return
        margin = 20
        x = parent.width() - self.width() - margin
        y = parent.height() - self.height() - margin - 50
        self.setGeometry(x, y, self.width(), self.height())

    def _animate_in(self, start_x: int, end_x: int) -> None:
        if self._anim is not None:
            self._anim.stop()
        self._anim = QPropertyAnimation(self, b"pos")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.setStartValue(QPoint(start_x, self.y()))
        self._anim.setEndValue(QPoint(end_x, self.y()))
        self._anim.start()

    def _animate_out(self) -> None:
        if self._anim is not None:
            self._anim.stop()
        end_x = self.x() + 80
        self._anim = QPropertyAnimation(self, b"pos")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.InCubic)
        self._anim.setStartValue(self.pos())
        self._anim.setEndValue(QPoint(end_x, self.y()))
        self._anim.finished.connect(self.hide)
        self._anim.start()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self.isVisible():
            self._reposition()

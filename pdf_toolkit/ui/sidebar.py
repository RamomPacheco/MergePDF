"""Sidebar navigation widget."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QButtonGroup, QPushButton, QVBoxLayout, QWidget

from ui.styles.icons import SIDEBAR_ICONS, SIDEBAR_LABELS


def _svg_icon(svg_data: str, size: int = 18) -> QIcon:
    renderer = QSvgRenderer(svg_data.encode())
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    from PySide6.QtGui import QPainter

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


class Sidebar(QWidget):
    """Left sidebar with operation navigation."""

    operationSelected = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 12)
        layout.setSpacing(2)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._buttons: list[QPushButton] = []

        for index, (icon_svg, label) in enumerate(
            zip(SIDEBAR_ICONS, SIDEBAR_LABELS, strict=True)
        ):
            btn = QPushButton(f"  {label}")
            btn.setObjectName("sidebarItem")
            btn.setCheckable(True)
            btn.setIcon(_svg_icon(icon_svg))
            btn.setIconSize(QSize(18, 18))
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=index: self._on_click(i))
            self._group.addButton(btn, index)
            self._buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()
        if self._buttons:
            self._buttons[0].setChecked(True)

    def _on_click(self, index: int) -> None:
        self.operationSelected.emit(index)

    def set_active(self, index: int) -> None:
        """Set the active sidebar item."""
        if 0 <= index < len(self._buttons):
            self._buttons[index].setChecked(True)

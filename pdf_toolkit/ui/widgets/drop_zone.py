"""Drag-and-drop file zone widget."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ui.styles.icons import CHECK_SVG, UPLOAD_SVG


class DropZone(QWidget):
    """Reusable drag-and-drop zone for PDF files."""

    filesSelected = Signal(list)

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        multiple: bool = False,
        extensions: tuple[str, ...] = (".pdf",),
    ) -> None:
        super().__init__(parent)
        self._multiple = multiple
        self._extensions = tuple(ext.lower() for ext in extensions)
        self._paths: list[str] = []
        self.setObjectName("dropZone")
        self.setAcceptDrops(True)
        self.setProperty("hover", False)
        self.setProperty("filled", False)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self._icon = QSvgWidget(self)
        self._icon.load(UPLOAD_SVG.encode())
        self._icon.setFixedSize(32, 32)
        layout.addWidget(self._icon, alignment=Qt.AlignCenter)

        self._hint = QLabel("Arraste arquivos PDF aqui ou clique para selecionar")
        self._hint.setObjectName("dropHint")
        self._hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._hint)

        self._file_row = QWidget(self)
        file_layout = QHBoxLayout(self._file_row)
        file_layout.setContentsMargins(0, 0, 0, 0)
        self._check = QSvgWidget(self._file_row)
        self._check.load(CHECK_SVG.encode())
        self._check.setFixedSize(18, 18)
        self._file_label = QLabel(self._file_row)
        self._file_label.setObjectName("fileNameLabel")
        file_layout.addWidget(self._check)
        file_layout.addWidget(self._file_label)
        self._file_row.hide()
        layout.addWidget(self._file_row, alignment=Qt.AlignCenter)

    def paths(self) -> list[str]:
        """Return currently selected file paths."""
        return list(self._paths)

    def first_path(self) -> str | None:
        """Return the first selected path or None."""
        return self._paths[0] if self._paths else None

    def clear(self) -> None:
        """Clear selected files."""
        self._set_paths([])

    def _set_paths(self, paths: list[str]) -> None:
        self._paths = paths
        filled = bool(paths)
        self.setProperty("filled", filled)
        self._hint.setVisible(not filled)
        self._icon.setVisible(not filled)
        self._file_row.setVisible(filled)
        if filled:
            if len(paths) == 1:
                self._file_label.setText(Path(paths[0]).name)
            else:
                self._file_label.setText(f"{len(paths)} arquivos selecionados")
        self.style().unpolish(self)
        self.style().polish(self)
        self.filesSelected.emit(list(paths))

    def _is_valid(self, path: str) -> bool:
        return Path(path).suffix.lower() in self._extensions

    def _collect_urls(self, urls) -> list[str]:
        paths: list[str] = []
        for url in urls:
            if not url.isLocalFile():
                continue
            path = url.toLocalFile()
            if self._is_valid(path):
                paths.append(path)
        return paths

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            paths = self._collect_urls(event.mimeData().urls())
            if paths:
                self.setProperty("hover", True)
                self.style().unpolish(self)
                self.style().polish(self)
                event.acceptProposedAction()
                return
        event.ignore()

    def dragLeaveEvent(self, event) -> None:
        self.setProperty("hover", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        self.setProperty("hover", False)
        self.style().unpolish(self)
        self.style().polish(self)
        paths = self._collect_urls(event.mimeData().urls())
        if not paths:
            event.ignore()
            return
        if self._multiple:
            merged = list(dict.fromkeys(self._paths + paths))
            self._set_paths(merged)
        else:
            self._set_paths([paths[0]])
        event.acceptProposedAction()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._open_dialog()
        super().mousePressEvent(event)

    def _open_dialog(self) -> None:
        filters = " ".join(f"*{ext}" for ext in self._extensions)
        if self._multiple:
            paths, _ = QFileDialog.getOpenFileNames(
                self,
                "Selecionar arquivos",
                "",
                f"Arquivos ({filters})",
            )
            if paths:
                valid = [p for p in paths if self._is_valid(p)]
                self._set_paths(valid)
        else:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Selecionar arquivo",
                "",
                f"Arquivos ({filters})",
            )
            if path and self._is_valid(path):
                self._set_paths([path])

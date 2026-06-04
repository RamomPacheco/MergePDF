"""Rotate PDF panel."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from operations.rotate import rotate_pdf
from ui.panels.base_panel import BasePanel


class RotatePanel(BasePanel):
    """Panel for rotating PDF pages."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Rotacionar",
            "Gire páginas específicas ou todo o documento.",
            "Rotacionar",
            parent,
        )
        deg_row = QHBoxLayout()
        deg_row.addWidget(QLabel("Graus:"))
        self.degrees_combo = QComboBox()
        self.degrees_combo.addItems(["90", "180", "270"])
        deg_row.addWidget(self.degrees_combo)
        deg_row.addStretch()
        self.config_layout.addLayout(deg_row)

        page_row = QHBoxLayout()
        page_row.addWidget(QLabel("Páginas (1,2,3 ou vazio = todas):"))
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Ex: 1,3,5")
        page_row.addWidget(self.pages_input, 1)
        self.config_layout.addLayout(page_row)

        out_row = QHBoxLayout()
        out_row.addWidget(QLabel("Arquivo de saída:"))
        self.output_input = QLineEdit("rotated.pdf")
        out_row.addWidget(self.output_input, 1)
        browse = QPushButton("...")
        browse.setFixedWidth(36)
        browse.clicked.connect(self._browse_output)
        out_row.addWidget(browse)
        self.config_layout.addLayout(out_row)

    def _browse_output(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Salvar PDF", self.output_input.text(), "PDF (*.pdf)"
        )
        if path:
            if not path.lower().endswith(".pdf"):
                path += ".pdf"
            self.output_input.setText(path)

    def _parse_pages(self) -> list[int] | None:
        raw = self.pages_input.text().strip()
        if not raw:
            return None
        pages: list[int] = []
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            num = int(part)
            if num < 1:
                raise ValueError("Números de página devem ser >= 1")
            pages.append(num - 1)
        return pages

    def _on_run_clicked(self) -> None:
        input_file = self._require_paths()
        if not input_file:
            return
        output = self.output_input.text().strip()
        if not output:
            self.log_error("Informe o arquivo de saída.")
            return
        try:
            pages = self._parse_pages()
        except ValueError as exc:
            self.log_error(str(exc))
            return
        degrees = int(self.degrees_combo.currentText())
        self.run_worker(
            rotate_pdf,
            input_file=str(input_file),
            output_file=output,
            degrees=degrees,
            pages=pages,
        )

    def _handle_success(self, result: object) -> None:
        self.log_ok(f"PDF salvo em: {self.output_input.text().strip()}")
        super()._handle_success(result)

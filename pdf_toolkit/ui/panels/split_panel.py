"""Split PDF panel."""

from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton

from operations.split import split_pdf
from ui.panels.base_panel import BasePanel


class SplitPanel(BasePanel):
    """Panel for splitting a PDF into single-page files."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Dividir PDF",
            "Separe cada página do PDF em um arquivo individual.",
            "Dividir PDF",
            parent,
        )
        row = QHBoxLayout()
        row.addWidget(QLabel("Pasta de saída:"))
        self.output_dir = QLineEdit()
        self.output_dir.setPlaceholderText("Selecione a pasta de destino")
        row.addWidget(self.output_dir, 1)
        browse = QPushButton("...")
        browse.setFixedWidth(36)
        browse.clicked.connect(self._browse_dir)
        row.addWidget(browse)
        self.config_layout.addLayout(row)

    def _browse_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Pasta de saída")
        if path:
            self.output_dir.setText(path)

    def _on_run_clicked(self) -> None:
        input_file = self._require_paths()
        if not input_file:
            return
        output_dir = self.output_dir.text().strip()
        if not output_dir:
            self.log_error("Selecione a pasta de saída.")
            return
        self.run_worker(
            split_pdf,
            input_file=str(input_file),
            output_dir=output_dir,
        )

    def _handle_success(self, result: object) -> None:
        self.log_ok(f"Páginas salvas em: {self.output_dir.text().strip()}")
        super()._handle_success(result)

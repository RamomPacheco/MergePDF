"""Merge PDFs panel."""

from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton

from operations.merge import merge_pdfs
from ui.panels.base_panel import BasePanel


class MergePanel(BasePanel):
    """Panel for merging multiple PDF files."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Mesclar PDFs",
            "Combine vários arquivos PDF em um único documento.",
            "Mesclar PDFs",
            parent,
            multiple_files=True,
        )
        row = QHBoxLayout()
        row.addWidget(QLabel("Arquivo de saída:"))
        self.output_input = QLineEdit("merged_output.pdf")
        self.output_input.setObjectName("monoInput")
        row.addWidget(self.output_input, 1)
        browse = QPushButton("...")
        browse.setFixedWidth(36)
        browse.setCursor(browse.cursor())
        browse.clicked.connect(self._browse_output)
        row.addWidget(browse)
        self.config_layout.addLayout(row)

    def _browse_output(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar PDF",
            self.output_input.text(),
            "PDF (*.pdf)",
        )
        if path:
            if not path.lower().endswith(".pdf"):
                path += ".pdf"
            self.output_input.setText(path)

    def _on_run_clicked(self) -> None:
        paths = self._require_paths(multiple=True)
        if not paths:
            return
        output = self.output_input.text().strip()
        if not output:
            self.log_error("Informe o arquivo de saída.")
            return
        self.run_worker(merge_pdfs, input_files=list(paths), output_file=output)

    def _handle_success(self, result: object) -> None:
        self.log_ok(f"PDF salvo em: {self.output_input.text().strip()}")
        super()._handle_success(result)

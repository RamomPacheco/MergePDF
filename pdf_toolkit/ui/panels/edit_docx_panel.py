"""DOCX bridge rich text edit panel."""

from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton

from docx_bridge.pdf_to_docx import edit_via_docx
from ui.panels.base_panel import BasePanel


class EditDocxPanel(BasePanel):
    """Panel for editing PDF via DOCX conversion."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Editar via DOCX",
            "Edição rica: PDF → DOCX → substituição → PDF (requer Word).",
            "Editar via DOCX",
            parent,
        )
        self.config_layout.addWidget(QLabel("Texto a substituir:"))
        self.old_input = QLineEdit()
        self.config_layout.addWidget(self.old_input)
        self.config_layout.addWidget(QLabel("Novo texto:"))
        self.new_input = QLineEdit()
        self.config_layout.addWidget(self.new_input)

        out_row = QHBoxLayout()
        out_row.addWidget(QLabel("Arquivo de saída (.pdf):"))
        self.output_input = QLineEdit("edited_rich.pdf")
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

    def _on_run_clicked(self) -> None:
        input_file = self._require_paths()
        if not input_file:
            return
        old_text = self.old_input.text()
        new_text = self.new_input.text()
        output = self.output_input.text().strip()
        if not old_text:
            self.log_error("Informe o texto a substituir.")
            return
        if not output:
            self.log_error("Informe o arquivo de saída.")
            return
        self.run_worker(
            edit_via_docx,
            input_pdf=str(input_file),
            output_pdf=output,
            old_text=old_text,
            new_text=new_text,
        )

    def _handle_success(self, result: object) -> None:
        out = self.output_input.text().strip()
        if not out.lower().endswith(".pdf"):
            out += ".pdf"
        self.log_ok(f"PDF salvo em: {out}")
        super()._handle_success(result)

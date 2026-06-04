"""Watermark panel."""

from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton

from operations.watermark import add_watermark
from ui.panels.base_panel import BasePanel
from ui.widgets.drop_zone import DropZone


class WatermarkPanel(BasePanel):
    """Panel for applying a watermark PDF."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Watermark",
            "Aplique um PDF de marca d'água sobre todas as páginas.",
            "Aplicar Watermark",
            parent,
            show_drop_zone=False,
        )
        self.doc_zone = DropZone(self, multiple=False)
        self.doc_zone._hint.setText("Arraste o PDF principal ou clique para selecionar")
        self.config_layout.addWidget(QLabel("PDF principal:"))
        self.config_layout.addWidget(self.doc_zone)

        self.wm_zone = DropZone(self, multiple=False)
        self.wm_zone._hint.setText("Arraste o PDF watermark ou clique para selecionar")
        self.config_layout.addWidget(QLabel("PDF watermark:"))
        self.config_layout.addWidget(self.wm_zone)

        out_row = QHBoxLayout()
        out_row.addWidget(QLabel("Arquivo de saída:"))
        self.output_input = QLineEdit("watermarked.pdf")
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
        doc = self.doc_zone.first_path()
        wm = self.wm_zone.first_path()
        if not doc:
            self.log_error("Selecione o PDF principal.")
            return
        if not wm:
            self.log_error("Selecione o PDF watermark.")
            return
        output = self.output_input.text().strip()
        if not output:
            self.log_error("Informe o arquivo de saída.")
            return
        self.run_worker(
            add_watermark,
            input_file=doc,
            watermark_file=wm,
            output_file=output,
        )

    def _handle_success(self, result: object) -> None:
        self.log_ok(f"PDF salvo em: {self.output_input.text().strip()}")
        super()._handle_success(result)

"""Encrypt and decrypt PDF panel."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QButtonGroup,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

from operations.protect import decrypt_pdf, encrypt_pdf
from ui.panels.base_panel import BasePanel


class ProtectPanel(BasePanel):
    """Panel for encrypting or decrypting PDFs."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Proteger PDF",
            "Adicione ou remova proteção por senha no documento.",
            "Aplicar",
            parent,
        )
        mode_layout = QVBoxLayout()
        self._mode_group = QButtonGroup(self)
        self.encrypt_radio = QRadioButton("Proteger com senha")
        self.decrypt_radio = QRadioButton("Remover senha")
        self.encrypt_radio.setChecked(True)
        self._mode_group.addButton(self.encrypt_radio)
        self._mode_group.addButton(self.decrypt_radio)
        mode_layout.addWidget(self.encrypt_radio)
        mode_layout.addWidget(self.decrypt_radio)
        self.config_layout.addLayout(mode_layout)

        pass_row = QHBoxLayout()
        pass_row.addWidget(QLabel("Senha:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        pass_row.addWidget(self.password_input, 1)
        self.config_layout.addLayout(pass_row)

        out_row = QHBoxLayout()
        out_row.addWidget(QLabel("Arquivo de saída:"))
        self.output_input = QLineEdit("protected.pdf")
        out_row.addWidget(self.output_input, 1)
        browse = QPushButton("...")
        browse.setFixedWidth(36)
        browse.clicked.connect(self._browse_output)
        out_row.addWidget(browse)
        self.config_layout.addLayout(out_row)

        self.encrypt_radio.toggled.connect(self._update_button)
        self._update_button()

    def _update_button(self) -> None:
        if self.encrypt_radio.isChecked():
            self._button_text = "Proteger PDF"
        else:
            self._button_text = "Remover senha"
        self.primary_button.setText(self._button_text)

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
        output = self.output_input.text().strip()
        password = self.password_input.text()
        if not output:
            self.log_error("Informe o arquivo de saída.")
            return
        if not password:
            self.log_error("Informe a senha.")
            return
        if self.encrypt_radio.isChecked():
            self.run_worker(
                encrypt_pdf,
                input_file=str(input_file),
                output_file=output,
                password=password,
            )
        else:
            self.run_worker(
                decrypt_pdf,
                input_file=str(input_file),
                output_file=output,
                password=password,
            )

    def _handle_success(self, result: object) -> None:
        self.log_ok(f"PDF salvo em: {self.output_input.text().strip()}")
        super()._handle_success(result)

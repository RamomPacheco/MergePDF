from __future__ import annotations

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.merge import merge_pdfs
from utils.fs import open_folder


class MergeTab(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.pdf_list = QListWidget()
        self.pdf_list.setAcceptDrops(True)
        self.pdf_list.dragEnterEvent = self._drag_enter
        self.pdf_list.dropEvent = self._drop
        layout.addWidget(self.pdf_list)

        row = QHBoxLayout()
        select_button = QPushButton("Selecionar PDFs")
        select_button.clicked.connect(self._select_pdfs)
        row.addWidget(select_button)

        remove_button = QPushButton("Remover")
        remove_button.clicked.connect(self._remove_selected)
        row.addWidget(remove_button)

        up_button = QPushButton("Subir")
        up_button.clicked.connect(lambda: self._move_item(-1))
        row.addWidget(up_button)

        down_button = QPushButton("Descer")
        down_button.clicked.connect(lambda: self._move_item(1))
        row.addWidget(down_button)
        layout.addLayout(row)

        layout.addWidget(QLabel("Nome do arquivo de saída:"))
        self.filename_input = QLineEdit("pdf_unificado")
        layout.addWidget(self.filename_input)

        merge_button = QPushButton("Juntar PDFs")
        merge_button.clicked.connect(self._merge_pdfs)
        layout.addWidget(merge_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

    def _drag_enter(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def _drop(self, event: QDropEvent) -> None:
        if not event.mimeData().hasUrls():
            event.ignore()
            return
        event.setDropAction(Qt.CopyAction)
        event.accept()
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(".pdf"):
                self.pdf_list.addItem(file_path)

    def _select_pdfs(self) -> None:
        pdf_files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar arquivos PDF",
            "",
            "Arquivos PDF (*.pdf)",
        )
        if pdf_files:
            self.pdf_list.clear()
            self.pdf_list.addItems(pdf_files)

    def _remove_selected(self) -> None:
        for item in self.pdf_list.selectedItems():
            row = self.pdf_list.row(item)
            self.pdf_list.takeItem(row)

    def _move_item(self, delta: int) -> None:
        row = self.pdf_list.currentRow()
        if row < 0:
            return
        new_row = row + delta
        if new_row < 0 or new_row >= self.pdf_list.count():
            return
        item = self.pdf_list.takeItem(row)
        self.pdf_list.insertItem(new_row, item)
        self.pdf_list.setCurrentRow(new_row)

    def _merge_pdfs(self) -> None:
        files_to_merge = [
            self.pdf_list.item(i).text() for i in range(self.pdf_list.count())
        ]
        if not files_to_merge:
            QMessageBox.critical(self, "Erro", "Nenhum arquivo PDF selecionado.")
            return

        save_dir = QFileDialog.getExistingDirectory(self, "Salvar PDF unificado")
        if not save_dir:
            return

        output_filename = self.filename_input.text().strip() or "pdf_unificado"
        output_file = os.path.join(save_dir, f"{output_filename}.pdf")

        self.progress_bar.setValue(0)
        try:
            total = len(files_to_merge)
            for i, _ in enumerate(files_to_merge, start=1):
                self.progress_bar.setValue(int((i - 1) / total * 100))
                QApplication.processEvents()

            page_count = merge_pdfs(files_to_merge, output_file)
            self.progress_bar.setValue(100)

            reply = QMessageBox.question(
                self,
                "Concluído",
                f"PDF unificado com {page_count} página(s). Deseja continuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                try:
                    open_folder(os.path.dirname(output_file))
                except Exception:
                    pass
                QApplication.quit()
            else:
                self.progress_bar.setValue(0)
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Erro ao unir os PDFs: {exc}")

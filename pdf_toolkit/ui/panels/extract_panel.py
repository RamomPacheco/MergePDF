"""Text and table extraction panel."""

from __future__ import annotations

from operations.extract import extract_tables, extract_text
from ui.panels.base_panel import BasePanel


class ExtractTextPanel(BasePanel):
    """Panel for extracting text from a PDF."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Extrair Texto",
            "Extraia todo o texto selecionável do documento.",
            "Extrair Texto",
            parent,
        )

    def _on_run_clicked(self) -> None:
        input_file = self._require_paths()
        if not input_file:
            return
        self.run_worker(extract_text, input_file=str(input_file))

    def _handle_success(self, result: object) -> None:
        text = str(result) if result else ""
        preview = text[:2000] + ("..." if len(text) > 2000 else "")
        self.log_ok(f"{len(text)} caracteres extraídos.")
        self.log_info(preview or "(vazio)")
        super()._handle_success(result)


class ExtractTablesPanel(BasePanel):
    """Panel for extracting tables from a PDF."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Extrair Tabelas",
            "Detecte e extraia tabelas preservando a estrutura.",
            "Extrair Tabelas",
            parent,
        )

    def _on_run_clicked(self) -> None:
        input_file = self._require_paths()
        if not input_file:
            return
        self.run_worker(extract_tables, input_file=str(input_file))

    def _handle_success(self, result: object) -> None:
        tables = result if isinstance(result, list) else []
        self.log_ok(f"{len(tables)} tabela(s) encontrada(s).")
        for index, table in enumerate(tables[:5], start=1):
            self.log_info(f"Tabela {index}: {len(table)} linhas")
        if len(tables) > 5:
            self.log_info(f"... e mais {len(tables) - 5} tabela(s)")
        super()._handle_success(result)

"""Library status pill badge."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel


class StatusChip(QLabel):
    """Small pill showing library availability."""

    def __init__(self, name: str, parent=None) -> None:
        super().__init__(name, parent)
        self._name = name
        self.setObjectName("chipError")

    def set_status(self, ok: bool, version: str) -> None:
        """Update chip appearance and tooltip."""
        self.setObjectName("chipOk" if ok else "chipError")
        self.style().unpolish(self)
        self.style().polish(self)
        status = version if ok else "missing"
        self.setToolTip(f"{self._name}: {status}")

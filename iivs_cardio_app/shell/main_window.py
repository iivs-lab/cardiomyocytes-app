from __future__ import annotations

__all__ = ("MainWindow",)

from typing import Final

from PySide6.QtWidgets import QMainWindow, QWidget

WINDOW_TITLE: Final[str] = "Cardiomyocytes App"
DEFAULT_SIZE: Final[tuple[int, int]] = (1280, 800)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*DEFAULT_SIZE)

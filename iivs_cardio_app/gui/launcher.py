from __future__ import annotations

__all__ = ("LauncherWindow",)

from typing import Final

from PySide6.QtWidgets import QMainWindow, QWidget

from iivs_cardio_app.gui.menu_bar import MenuBar

WINDOW_TITLE: Final[str] = "Cardiomyocytes App"
DEFAULT_SIZE: Final[tuple[int, int]] = (1280, 800)


class LauncherWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*DEFAULT_SIZE)
        self.setMenuBar(MenuBar(self))

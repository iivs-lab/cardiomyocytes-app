from __future__ import annotations

__all__ = ("load_app_icon", "main")

import sys
from importlib.resources import as_file, files

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from iivs_cardio_app.gui.launcher import LauncherWindow


def load_app_icon() -> QIcon:
    with as_file(files(__package__) / "assets" / "icon.ico") as path:
        return QIcon(str(path))


def main() -> int:
    app = QApplication(sys.argv)
    app.setWindowIcon(load_app_icon())
    window = LauncherWindow()
    window.show()
    return app.exec()

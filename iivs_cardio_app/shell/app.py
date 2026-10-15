from __future__ import annotations

__all__ = ("main",)

import sys

from PySide6.QtWidgets import QApplication

from iivs_cardio_app.shell.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

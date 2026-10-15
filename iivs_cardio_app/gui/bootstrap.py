from __future__ import annotations

__all__ = ("main",)

import sys

from PySide6.QtWidgets import QApplication

from iivs_cardio_app.gui.launcher import LauncherWindow


def main() -> int:
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    return app.exec()

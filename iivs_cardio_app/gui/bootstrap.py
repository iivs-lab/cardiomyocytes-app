from __future__ import annotations

__all__ = ("main",)

import sys

from PySide6.QtWidgets import QApplication

from iivs_cardio_app.gui.app_manager import AppManager


def main() -> int:
    app = QApplication(sys.argv)
    manager = AppManager()
    app.setWindowIcon(manager.assets.icon)
    manager.show_launcher()
    return app.exec()

from __future__ import annotations

__all__ = ("main",)

import sys
from typing import Final

from PySide6.QtWidgets import QApplication

from iivs_cardio_app.shell.main_window import MainWindow

APPLICATION_NAME: Final[str] = "cardiomyocytes-app"
ORGANIZATION_NAME: Final[str] = "iivs-lab"


def main() -> int:
    """Run the application until its last window closes and return the exit code."""
    app = QApplication(sys.argv)
    app.setApplicationName(APPLICATION_NAME)
    app.setOrganizationName(ORGANIZATION_NAME)

    window = MainWindow()
    window.show()
    return app.exec()

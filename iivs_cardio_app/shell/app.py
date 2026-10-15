from __future__ import annotations

__all__ = ("main",)

import sys
from typing import Final

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from iivs_cardio_app.shell.appearance import apply_color_scheme, load_color_scheme
from iivs_cardio_app.shell.main_window import MainWindow

APPLICATION_NAME: Final[str] = "cardiomyocytes-app"
ORGANIZATION_NAME: Final[str] = "iivs-lab"


def main() -> int:
    """Run the application until its last window closes and return the exit code."""
    app = QApplication(sys.argv)
    app.setApplicationName(APPLICATION_NAME)
    app.setOrganizationName(ORGANIZATION_NAME)

    # Apply the saved scheme before the window shows, so it does not flash the other.
    settings = QSettings()
    apply_color_scheme(app.styleHints(), load_color_scheme(settings))

    window = MainWindow(settings)
    window.show()
    return app.exec()

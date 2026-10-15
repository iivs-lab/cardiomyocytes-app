from __future__ import annotations

__all__ = ("MainWindow",)

from typing import TYPE_CHECKING, Final

from PySide6.QtGui import QAction, QActionGroup, QGuiApplication
from PySide6.QtWidgets import QMainWindow, QWidget

from iivs_cardio_app.shell.appearance import (
    COLOR_SCHEMES,
    apply_color_scheme,
    load_color_scheme,
    save_color_scheme,
)

if TYPE_CHECKING:
    from PySide6.QtCore import QSettings

    from iivs_cardio_app.shell.appearance import ColorScheme

WINDOW_TITLE: Final[str] = "Cardiomyocytes App"
DEFAULT_SIZE: Final[tuple[int, int]] = (1280, 800)
COLOR_SCHEME_LABELS: Final[dict[ColorScheme, str]] = {
    "system": "&System",
    "light": "&Light",
    "dark": "&Dark",
}


class MainWindow(QMainWindow):
    """The application's top-level window, which will host the sub-apps.

    Args:
        settings: Where the window reads and saves the user's choices, such as the
            color scheme.
        parent: The parent widget, if any.
    """

    def __init__(self, settings: QSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._settings = settings
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*DEFAULT_SIZE)
        self._create_view_menu()

    def _create_view_menu(self) -> None:
        theme_menu = self.menuBar().addMenu("&View").addMenu("&Theme")
        theme_group = QActionGroup(self)
        current = load_color_scheme(self._settings)

        for scheme in COLOR_SCHEMES:
            action = QAction(COLOR_SCHEME_LABELS[scheme], theme_group)
            action.setCheckable(True)
            action.setChecked(scheme == current)
            action.triggered.connect(
                lambda _checked=False, scheme=scheme: self._set_color_scheme(scheme),
            )
            theme_menu.addAction(action)

    def _set_color_scheme(self, scheme: ColorScheme) -> None:
        apply_color_scheme(QGuiApplication.styleHints(), scheme)
        save_color_scheme(self._settings, scheme)

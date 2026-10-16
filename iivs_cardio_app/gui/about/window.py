from __future__ import annotations

__all__ = ("AboutWindow",)

from typing import TYPE_CHECKING, Final

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from iivs_cardio_app.gui.about.about_tab import AboutTab
from iivs_cardio_app.gui.about.licenses_tab import LicensesTab

if TYPE_CHECKING:
    from iivs_cardio_app.gui.app_manager import AppInfo

DEFAULT_SIZE: Final[tuple[int, int]] = (640, 560)
MINIMUM_SIZE: Final[tuple[int, int]] = (480, 400)


class AboutWindow(QDialog):
    """The window that tells about the application and the licenses it ships.

    It is not modal, and closing it never quits the application.

    Args:
        info: The facts it shows about the application.
        parent: The parent widget, if any; the application opens it without one.
    """

    def __init__(self, info: AppInfo, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._info = info
        self.setWindowTitle(f"About {info.name}")
        self.resize(*DEFAULT_SIZE)
        self.setMinimumSize(*MINIMUM_SIZE)
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, on=False)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        tabs = QTabWidget(parent=self)
        tabs.addTab(AboutTab(self._info, parent=tabs), "&About")
        tabs.addTab(LicensesTab(parent=tabs), "&Licenses")
        self._button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close,
            parent=self,
        )

        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        layout.addWidget(self._button_box)

    def _connect_signals(self) -> None:
        self._button_box.rejected.connect(self.close)

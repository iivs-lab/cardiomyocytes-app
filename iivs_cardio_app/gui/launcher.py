from __future__ import annotations

__all__ = ("LauncherWindow",)

from typing import TYPE_CHECKING, Final, override

from PySide6.QtWidgets import QMainWindow, QWidget

from iivs_cardio_app.gui.menu_bar import MenuBar

if TYPE_CHECKING:
    from PySide6.QtGui import QCloseEvent

    from iivs_cardio_app.gui.app_manager import AppManager

DEFAULT_SIZE: Final[tuple[int, int]] = (1280, 800)
MINIMUM_SIZE: Final[tuple[int, int]] = (960, 600)


class LauncherWindow(QMainWindow):
    """The window the application opens with, from which the sub-apps start.

    Closing it quits the application: it first closes every other window through
    `AppManager.close_windows()`, and stays open if one of them refuses.

    Args:
        manager: The process's `AppManager`, which its menus act on.
        parent: The parent widget, if any; the application opens it without one.
    """

    def __init__(self, manager: AppManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._manager = manager
        self.setWindowTitle(manager.assets.info.name)
        self.resize(*DEFAULT_SIZE)
        self.setMinimumSize(*MINIMUM_SIZE)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setMenuBar(MenuBar(self._manager, parent=self))

    @override
    def closeEvent(self, event: QCloseEvent) -> None:
        # The launcher is the last window `AppManager.quit()` closes, so this also
        # answers a quit; Qt quits once the launcher, its last window, has closed.
        if self._manager.close_windows(keep=self):
            event.accept()
        else:
            event.ignore()

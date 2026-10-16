from __future__ import annotations

__all__ = ("AppAssets", "AppInfo", "AppManager")

import tomllib
from dataclasses import dataclass
from functools import partial
from importlib.resources import as_file, files
from typing import TYPE_CHECKING

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from iivs_cardio_app.gui.about import AboutWindow
from iivs_cardio_app.gui.launcher import LauncherWindow

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtWidgets import QWidget


@dataclass(frozen=True, slots=True)
class AppInfo:
    """The facts about the application that its windows show.

    Args:
        name: The name shown to users, such as in window titles.
        version: The application version.
        description: A one-line description.
        copyright: The copyright line of the application's license.
        license: The SPDX expression of the application's license.
        homepage: The project's web page.
    """

    name: str
    version: str
    description: str
    copyright: str
    license: str
    homepage: str

    @classmethod
    def load(cls) -> AppInfo:
        """Read the facts from `gui/assets/app.toml`."""
        text = (files(__package__) / "assets" / "app.toml").read_text(encoding="utf-8")
        return cls(**tomllib.loads(text))


@dataclass(frozen=True, slots=True)
class AppAssets:
    """The data files the whole application shares, read from `gui/assets/`.

    Args:
        info: The facts the windows show about the application.
        icon: The application icon, in every size its ICO file holds.
    """

    info: AppInfo
    icon: QIcon

    @classmethod
    def load(cls) -> AppAssets:
        """Read every shared asset; call it once a `QApplication` exists."""
        with as_file(files(__package__) / "assets" / "icon.ico") as path:
            icon = QIcon(str(path))
        return cls(info=AppInfo.load(), icon=icon)


class AppManager:
    """The owner of the application's shared assets and of its windows in one process.

    It loads the assets when created. Each window kind exists at most once per
    manager: the first request creates the window, and a later one brings it to the
    front, restoring it if it is minimized. Closing a window only hides it, so it
    comes back as it was left. The bootstrap creates one manager per process, after
    the `QApplication`, and passes it down to the windows that open others; nothing
    reaches it through a global.
    """

    __slots__ = ("_assets", "_windows")

    def __init__(self) -> None:
        self._assets = AppAssets.load()
        self._windows: dict[type[QWidget], QWidget] = {}

    @property
    def assets(self) -> AppAssets:
        """The data files the whole application shares."""
        return self._assets

    @staticmethod
    def _bring_to_front(window: QWidget) -> None:
        if window.isMinimized():
            window.showNormal()
        else:
            window.show()
        window.raise_()
        window.activateWindow()

    def _show[W: QWidget](self, kind: type[W], create: Callable[[], W]) -> W:
        window = self._windows.get(kind)
        if not isinstance(window, kind):
            window = create()
            self._windows[kind] = window
        self._bring_to_front(window)
        return window

    def show_launcher(self) -> LauncherWindow:
        return self._show(LauncherWindow, partial(LauncherWindow, self))

    def show_about(self) -> AboutWindow:
        return self._show(AboutWindow, partial(AboutWindow, self._assets.info))

    def close_windows(self, *, keep: QWidget | None = None) -> bool:
        """Close every open window but `keep`, the newest first.

        Each window decides in its `closeEvent` whether it may close. One that
        refuses, such as a window whose user keeps unsaved work, stops the round:
        the windows closed before it stay hidden, and the rest stay open.

        Returns:
            Whether every window but `keep` is closed.
        """
        for window in reversed(self._windows.values()):
            if window is not keep and window.isVisible() and not window.close():
                return False
        return True

    def quit(self) -> bool:
        """Close every open window, as `close_windows()` does, then quit.

        Returns:
            Whether the application quits; it does not when a window refuses.
        """
        if not self.close_windows():
            return False
        QApplication.quit()
        return True

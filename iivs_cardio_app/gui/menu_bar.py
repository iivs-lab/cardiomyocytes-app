from __future__ import annotations

__all__ = ("MenuBar",)

from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenuBar, QWidget

if TYPE_CHECKING:
    from PySide6.QtWidgets import QMenu


@dataclass(frozen=True, slots=True)
class ItemSpec:
    text: str
    shortcut: QKeySequence.StandardKey | str | None = None
    role: QAction.MenuRole = QAction.MenuRole.NoRole


@dataclass(frozen=True, slots=True)
class Separator:
    pass


SEPARATOR: Final[Separator] = Separator()


@dataclass(frozen=True, slots=True)
class MenuSpec:
    title: str
    entries: tuple[ItemSpec | Separator, ...]


FILE_MENU: Final[MenuSpec] = MenuSpec(
    "&File",
    (
        ItemSpec("&Preferences…", "Ctrl+,", QAction.MenuRole.PreferencesRole),
        SEPARATOR,
        ItemSpec("&Close Window", QKeySequence.StandardKey.Close),
        ItemSpec("&Quit", "Ctrl+Q", QAction.MenuRole.QuitRole),
    ),
)


WINDOW_MENU: Final[MenuSpec] = MenuSpec(
    "&Window",
    (ItemSpec("&Launcher"),),
)


HELP_MENU: Final[MenuSpec] = MenuSpec(
    "&Help",
    (
        ItemSpec("&About Cardiomyocytes App", role=QAction.MenuRole.AboutRole),
        SEPARATOR,
        ItemSpec("&Report an Issue"),
    ),
)


class MenuBar(QMenuBar):
    """The menus every window of the application shows, the launcher and each sub-app.

    Each window gets its own instance, since a Qt widget belongs to one window. The
    shared menus are the `MenuSpec` constants of this module; a sub-app's own menus
    join them in its window and are not declared here. Shortcuts of the shared menus
    hold in every window, so a sub-app must not reuse them. An item with a menu role
    moves into the application menu on macOS, where each role takes one item.

    Args:
        parent: The window that shows the menu bar.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        for spec in (FILE_MENU, WINDOW_MENU, HELP_MENU):
            self._add_menu(spec)

    def _add_menu(self, spec: MenuSpec) -> QMenu:
        menu = self.addMenu(spec.title)
        for entry in spec.entries:
            if isinstance(entry, Separator):
                menu.addSeparator()
            else:
                menu.addAction(self._create_action(entry, menu))
        return menu

    @staticmethod
    def _create_action(spec: ItemSpec, parent: QMenu) -> QAction:
        action = QAction(spec.text, parent)
        if isinstance(spec.shortcut, QKeySequence.StandardKey):
            action.setShortcuts(spec.shortcut)
        elif spec.shortcut is not None:
            action.setShortcut(QKeySequence(spec.shortcut))
        action.setMenuRole(spec.role)
        action.setEnabled(False)
        return action

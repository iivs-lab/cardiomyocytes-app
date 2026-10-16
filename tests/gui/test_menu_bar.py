from __future__ import annotations

import pytest
from PySide6.QtGui import QAction, QKeySequence

from iivs_cardio_app.gui.menu_bar import MenuBar


class FakeManager:
    """An `AppManager` stand-in that records what the menu items asked of it."""

    def __init__(self):
        self.calls = []

    def show_about(self):
        self.calls.append("show_about")

    def quit(self):
        self.calls.append("quit")


@pytest.fixture()
def manager():
    return FakeManager()


@pytest.fixture()
def menu_bar(qtbot, manager):
    menu_bar = MenuBar(manager)
    qtbot.addWidget(menu_bar)
    return menu_bar


def _items(menu_bar):
    """Map each menu title to its items' texts, with `"-"` for a separator."""
    return {
        menu_action.text(): [
            "-" if action.isSeparator() else action.text()
            for action in menu_action.menu().actions()
        ]
        for menu_action in menu_bar.actions()
    }


def _action(menu_bar, text):
    return next(
        action for action in menu_bar.findChildren(QAction) if action.text() == text
    )


def test_menu_bar_holds_the_shared_menus_in_order(menu_bar):
    assert _items(menu_bar) == {
        "&File": ["&Preferences…", "-", "&Close Window", "&Quit"],
        "&Window": ["&Launcher"],
        "&Help": [
            "&About Cardiomyocytes App",
            "-",
            "&Report an Issue",
        ],
    }


def test_only_items_with_a_feature_are_enabled(menu_bar):
    items = []
    for menu_action in menu_bar.actions():
        items.extend(menu_action.menu().actions())
    enabled = [
        action.text()
        for action in items
        if action.isEnabled() and not action.isSeparator()
    ]

    assert enabled == ["&Quit", "&About Cardiomyocytes App"]


def test_about_item_asks_the_manager_for_the_about_window(menu_bar, manager):
    _action(menu_bar, "&About Cardiomyocytes App").trigger()

    assert manager.calls == ["show_about"]


@pytest.mark.parametrize(
    ("text", "role"),
    (
        ("&Preferences…", QAction.MenuRole.PreferencesRole),
        ("&Quit", QAction.MenuRole.QuitRole),
        ("&About Cardiomyocytes App", QAction.MenuRole.AboutRole),
        ("&Close Window", QAction.MenuRole.NoRole),
        ("&Report an Issue", QAction.MenuRole.NoRole),
    ),
)
def test_only_preferences_quit_and_about_move_to_the_macos_app_menu(
    menu_bar, text, role
):
    assert _action(menu_bar, text).menuRole() == role


@pytest.mark.parametrize(
    ("text", "shortcut"),
    (
        ("&Preferences…", "Ctrl+,"),
        ("&Close Window", "Ctrl+W"),
        ("&Quit", "Ctrl+Q"),
    ),
)
def test_items_carry_their_shortcuts(menu_bar, text, shortcut):
    shortcuts = [
        sequence.toString() for sequence in _action(menu_bar, text).shortcuts()
    ]

    assert QKeySequence(shortcut).toString() in shortcuts


def test_quit_item_asks_the_manager_to_quit(menu_bar, manager):
    _action(menu_bar, "&Quit").trigger()

    assert manager.calls == ["quit"]

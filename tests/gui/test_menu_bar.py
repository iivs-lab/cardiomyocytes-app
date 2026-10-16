from __future__ import annotations

import pytest
from PySide6.QtGui import QAction, QKeySequence

from iivs_cardio_app.gui.menu_bar import MenuBar


@pytest.fixture()
def menu_bar(qtbot):
    menu_bar = MenuBar()
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


def test_every_item_is_disabled_until_its_feature_exists(menu_bar):
    items = []
    for menu_action in menu_bar.actions():
        items.extend(menu_action.menu().actions())
    items = [action for action in items if not action.isSeparator()]

    assert items
    assert not any(action.isEnabled() for action in items)


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

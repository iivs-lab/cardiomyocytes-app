from __future__ import annotations

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPlainTextEdit, QTreeWidget

from iivs_cardio_app.gui.about.licenses import Component
from iivs_cardio_app.gui.about.licenses_tab import LicensesTab


@pytest.fixture()
def tab(qtbot):
    tab = LicensesTab()
    qtbot.addWidget(tab)
    return tab


def _rows(item):
    """Map each child of `item` to its three columns and its own children."""
    return [
        (
            tuple(item.child(row).text(column) for column in range(3)),
            _rows(item.child(row)),
        )
        for row in range(item.childCount())
    ]


def _expected(components):
    return [
        (
            (component.name, component.version, component.license),
            _expected(component.bundled),
        )
        for component in components
    ]


def _item(tab, name):
    tree = tab.findChild(QTreeWidget)
    flags = Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchRecursive
    return tree, tree.findItems(name, flags)[0]


def test_tab_nests_bundled_components_under_their_host(tab):
    tree = tab.findChild(QTreeWidget)

    assert _rows(tree.invisibleRootItem()) == _expected(Component.load_all())


def test_tab_shows_bundled_components_expanded(tab):
    _tree, python = _item(tab, "Python")

    assert python.isExpanded()


def test_tab_starts_with_the_first_license_shown(tab):
    text = tab.findChild(QPlainTextEdit).toPlainText()

    assert text == Component.load_all()[0].read_license_text()


def test_selecting_a_component_shows_its_note_before_its_license(tab):
    tree, qt = _item(tab, "Qt")

    tree.setCurrentItem(qt)
    text = tab.findChild(QPlainTextEdit).toPlainText()

    assert text.startswith("Includes Qt for Python")
    assert "GNU LESSER GENERAL PUBLIC LICENSE" in text


def test_selecting_a_bundled_component_shows_its_license(tab):
    tree, libffi = _item(tab, "libffi")
    (expected,) = [c for c in Component.load_all()[0].bundled if c.name == "libffi"]

    tree.setCurrentItem(libffi)

    assert tab.findChild(QPlainTextEdit).toPlainText() == expected.read_license_text()

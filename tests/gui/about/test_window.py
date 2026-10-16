from __future__ import annotations

import pytest
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QDialogButtonBox, QTabWidget

from iivs_cardio_app.gui.about import AboutWindow
from iivs_cardio_app.gui.about.about_tab import AboutTab
from iivs_cardio_app.gui.about.licenses_tab import LicensesTab


@pytest.fixture()
def window(qtbot, manager):
    window = AboutWindow(manager.assets.info)
    qtbot.addWidget(window)
    return window


def test_holds_the_about_tab_before_the_licenses_tab(window):
    tabs = window.findChild(QTabWidget)
    pages = [
        (tabs.tabText(index), type(tabs.widget(index))) for index in range(tabs.count())
    ]

    assert window.windowTitle() == "About Cardiomyocytes App"
    assert pages == [("&About", AboutTab), ("&Licenses", LicensesTab)]


def test_opens_at_its_default_size_and_shrinks_only_to_its_minimum(window):
    assert window.size() == QSize(640, 560)
    assert window.minimumSize() == QSize(480, 400)


def test_closing_it_never_quits_the_application(window):
    assert not window.testAttribute(Qt.WidgetAttribute.WA_QuitOnClose)


def test_close_button_closes_it(qtbot, window):
    window.show()
    qtbot.waitExposed(window)

    window.findChild(QDialogButtonBox).button(
        QDialogButtonBox.StandardButton.Close,
    ).click()

    assert not window.isVisible()

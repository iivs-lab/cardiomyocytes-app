from __future__ import annotations

import pytest
from PySide6.QtCore import QSize

from iivs_cardio_app.gui.launcher import LauncherWindow
from iivs_cardio_app.gui.menu_bar import MenuBar


@pytest.fixture()
def window(qtbot, manager):
    window = LauncherWindow(manager)
    qtbot.addWidget(window)
    return window


def test_launcher_opens_with_the_application_title(qtbot, window):
    window.show()
    qtbot.waitExposed(window)

    assert window.isVisible()
    assert window.windowTitle() == "Cardiomyocytes App"


def test_launcher_opens_at_its_default_size_and_shrinks_only_to_its_minimum(window):
    assert window.size() == QSize(1280, 800)
    assert window.minimumSize() == QSize(960, 600)


def test_launcher_shows_the_shared_menu_bar(window):
    assert isinstance(window.menuBar(), MenuBar)
    assert window.menuBar().parent() is window

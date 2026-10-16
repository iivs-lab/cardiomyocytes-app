from __future__ import annotations

from iivs_cardio_app.gui.launcher import LauncherWindow
from iivs_cardio_app.gui.menu_bar import MenuBar


def test_launcher_opens_with_the_application_title(qtbot):
    window = LauncherWindow()
    qtbot.addWidget(window)

    window.show()
    qtbot.waitExposed(window)

    assert window.isVisible()
    assert window.windowTitle() == "Cardiomyocytes App"


def test_launcher_shows_the_shared_menu_bar(qtbot):
    window = LauncherWindow()
    qtbot.addWidget(window)

    assert isinstance(window.menuBar(), MenuBar)
    assert window.menuBar().parent() is window

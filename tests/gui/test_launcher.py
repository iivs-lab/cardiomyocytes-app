from __future__ import annotations

from iivs_cardio_app.gui.launcher import LauncherWindow


def test_launcher_opens_with_the_application_title(qtbot):
    window = LauncherWindow()
    qtbot.addWidget(window)

    window.show()
    qtbot.waitExposed(window)

    assert window.isVisible()
    assert window.windowTitle() == "Cardiomyocytes App"
